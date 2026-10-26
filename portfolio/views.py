import os
import re
import logging
import smtplib
import threading
from functools import lru_cache
from io import BytesIO

import json
import time
from datetime import datetime, timezone
import requests
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail.message import BadHeaderError
from django.db import connection
from django.http import StreamingHttpResponse
from pypdf import PdfReader
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

try:
    import faiss  # noqa: F401
except ModuleNotFoundError:  # pragma: no cover - optional for RAG-only features
    faiss = None

try:
    import numpy as np
except ModuleNotFoundError:  # pragma: no cover - optional for RAG-only features
    np = None

try:
    from sentence_transformers import SentenceTransformer
except ModuleNotFoundError:  # pragma: no cover - optional for RAG-only features
    SentenceTransformer = None

from .models import Project
from .serializers import ContactMessageSerializer, ProjectSerializer

GEOCODE_URL = 'https://geocoding-api.open-meteo.com/v1/search'
FORECAST_URL = 'https://api.open-meteo.com/v1/forecast'
logger = logging.getLogger(__name__)

# WMO weather codes -> (description, emoji)
WEATHER_CODES = {
    0: ('Clear sky', '\u2600\ufe0f'),
    1: ('Mainly clear', '\U0001F324\ufe0f'),
    2: ('Partly cloudy', '\u26c5'),
    3: ('Overcast', '\u2601\ufe0f'),
    45: ('Fog', '\U0001F32B\ufe0f'),
    48: ('Fog', '\U0001F32B\ufe0f'),
    51: ('Light drizzle', '\U0001F326\ufe0f'),
    53: ('Drizzle', '\U0001F326\ufe0f'),
    55: ('Heavy drizzle', '\U0001F326\ufe0f'),
    61: ('Light rain', '\U0001F327\ufe0f'),
    63: ('Rain', '\U0001F327\ufe0f'),
    65: ('Heavy rain', '\U0001F327\ufe0f'),
    71: ('Light snow', '\u2744\ufe0f'),
    73: ('Snow', '\u2744\ufe0f'),
    75: ('Heavy snow', '\u2744\ufe0f'),
    80: ('Rain showers', '\U0001F326\ufe0f'),
    81: ('Rain showers', '\U0001F326\ufe0f'),
    82: ('Violent rain showers', '\U0001F327\ufe0f'),
    95: ('Thunderstorm', '\u26c8\ufe0f'),
    96: ('Thunderstorm with hail', '\u26c8\ufe0f'),
    99: ('Thunderstorm with hail', '\u26c8\ufe0f'),
}


def describe(code):
    return WEATHER_CODES.get(code, ('Unknown', '\U0001F321\ufe0f'))


def extract_text(file_obj):
    name = getattr(file_obj, 'name', '').lower()
    file_obj.seek(0)
    data = file_obj.read()
    if not data:
        return ''

    if name.endswith('.pdf'):
        try:
            reader = PdfReader(BytesIO(data))
            pages = []
            for page in reader.pages:
                page_text = page.extract_text() or ''
                pages.append(page_text)
            return '\n'.join(pages)
        except Exception:
            return data.decode('utf-8', errors='replace')

    if name.endswith('.txt'):
        return data.decode('utf-8', errors='replace')

    if name.endswith('.docx'):
        try:
            from docx import Document
            doc = Document(BytesIO(data))
            return '\n'.join(paragraph.text for paragraph in doc.paragraphs)
        except Exception:
            return data.decode('utf-8', errors='replace')

    return data.decode('utf-8', errors='replace')


def split_into_chunks(text, chunk_size=220, overlap=40):
    clean_text = re.sub(r'\s+', ' ', text).strip()
    if not clean_text:
        return []
    sentences = re.split(r'(?<=[.!?])\s+', clean_text)
    chunks = []
    current = ''
    for sentence in sentences:
        if not sentence:
            continue
        if len(current) + len(sentence) <= chunk_size:
            current = f'{current} {sentence}'.strip()
        else:
            if current:
                chunks.append(current)
            overflow = sentence
            while len(overflow) > chunk_size:
                chunks.append(overflow[:chunk_size].strip())
                overflow = overflow[chunk_size - overlap :].strip()
            current = overflow.strip()
    if current:
        chunks.append(current)
    return [chunk for chunk in chunks if chunk][:5]


@lru_cache(maxsize=1)
def _get_embed_model():
    if SentenceTransformer is None:
        raise ModuleNotFoundError('sentence-transformers is not installed')
    model_name = os.environ.get('RAG_EMBED_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    return SentenceTransformer(model_name)


def _build_semantic_context(question, chunks):
    if np is None or SentenceTransformer is None:
        return chunks[:3]

    try:
        model = _get_embed_model()
        chunks_with_query = [question, *chunks]
        embeddings = model.encode(chunks_with_query, convert_to_numpy=True)
        query_vector = embeddings[0]
        chunk_vectors = embeddings[1:]
        norms = np.linalg.norm(chunk_vectors, axis=1) * np.linalg.norm(query_vector)
        sims = np.divide(
            np.dot(chunk_vectors, query_vector),
            norms,
            out=np.zeros_like(np.dot(chunk_vectors, query_vector)),
            where=(norms != 0),
        )
        ranked_indices = np.argsort(sims)[::-1]
        selected = [chunks[idx] for idx in ranked_indices[:3] if sims[idx] > 0.0]
        if not selected:
            return chunks[:3]
        return selected
    except Exception:
        return chunks[:3]


OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')


def normalize_question(question):
    q = (question or '').strip()
    if not q:
        return q

    lower = q.lower()
    vague_patterns = [
        'above pdf',
        'above document',
        'this pdf',
        'this document',
        'the above pdf',
        'uploaded pdf',
        'uploaded document',
        'this resume',
        'above resume',
    ]

    if any(pattern in lower for pattern in vague_patterns):
        return 'Summarize the uploaded document in a concise but useful way. Include the main skills, experience, responsibilities, and key highlights.'

    if lower.startswith('tell me about') and ('pdf' in lower or 'document' in lower or 'resume' in lower):
        return 'Summarize the uploaded document in a concise but useful way. Include the main skills, experience, responsibilities, and key highlights.'

    return q


def _generate_with_ollama(question, chunks, full_text=''):
    if not chunks and not full_text:
        return None

    model_name = os.environ.get('OLLAMA_MODEL', 'qwen2.5:3b')
    context = (full_text or '\n\n'.join(chunks)).strip()
    if not context:
        return None
    context = context[:8000]
    prompt = (
        'Answer the user question using only the document text below. '
        'Base your answer on the actual content in the document. '
        'If the answer is partly present, provide the most correct factual summary. '
        'Do not refuse just because the question is generic.\n\n'
        f'Question: {question}\n\nDocument text:\n{context}'
    )

    try:
        response = requests.post(
            f'{OLLAMA_BASE_URL.rstrip("/")}/api/generate',
            json={
                'model': model_name,
                'prompt': prompt,
                'stream': False,
                'options': {'temperature': 0.2},
            },
            timeout=(1.0, 4.0),
        )
        response.raise_for_status()
        payload = response.json()
        answer = (payload.get('response') or '').strip()
        if answer:
            return answer
    except (requests.RequestException, ValueError, TypeError):
        return None

    return None


def answer_from_chunks(question, chunks, full_text=''):
    if not chunks and not full_text:
        return 'I could not find relevant content in the uploaded document. Please try a different PDF or ask a more specific question.'

    selected = _build_semantic_context(question, chunks) if chunks else []
    context_text = full_text.strip() if full_text else '\n\n'.join(selected)
    generated = _generate_with_ollama(question, selected, full_text=context_text)
    if generated:
        return generated

    fallback = context_text[:600].strip()
    if len(fallback) >= 550:
        fallback = fallback + '...'
    return fallback or 'I could not find relevant content in the uploaded document. Please try a different PDF or ask a more specific question.'


class ProjectList(generics.ListAPIView):
    queryset = Project.objects.filter(is_published=True)
    serializer_class = ProjectSerializer
    pagination_class = None


class ProjectDetail(generics.RetrieveAPIView):
    queryset = Project.objects.filter(is_published=True)
    serializer_class = ProjectSerializer
    lookup_field = 'slug'


def _do_send_email(instance):
    """Internal: performs the actual SMTP call — runs in a background thread."""
    recipient = os.environ.get('CONTACT_EMAIL_TO', 'sivakumarannam143@gmail.com')
    from_email = (
        os.environ.get('DEFAULT_FROM_EMAIL')
        or os.environ.get('EMAIL_HOST_USER')
        or 'noreply@example.com'
    )
    subject = f'New portfolio message from {instance.name}'
    body = (
        f'Name: {instance.name}\n'
        f'Email: {instance.email}\n\n'
        'Message:\n'
        f'{instance.message}'
    )
    try:
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[recipient],
            reply_to=[instance.email],
        )
        sent = email.send(fail_silently=False) == 1
        if sent:
            logger.info('Email delivered for contact message %s', instance.pk)
        else:
            logger.warning('Email.send() returned 0 for contact message %s', instance.pk)
    except (BadHeaderError, OSError, smtplib.SMTPException):
        logger.exception('Async email delivery failed for contact message %s', instance.pk)


def send_contact_email_async(instance):
    """Fire-and-forget: dispatch email in a daemon thread so the API
    returns immediately without blocking on Gmail SMTP (3–8 s)."""
    thread = threading.Thread(
        target=_do_send_email,
        args=(instance,),
        daemon=True,
        name=f'email-{instance.pk}',
    )
    thread.start()
    logger.debug('Email thread started for contact message %s', instance.pk)


class ContactCreate(generics.CreateAPIView):
    serializer_class = ContactMessageSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'contact'

    def create(self, request, *args, **kwargs):
        # Honeypot spam check: automated bots will fill this hidden field
        honeypot = request.data.get('website', '').strip()
        if honeypot:
            logger.warning('Spam bot blocked via honeypot field: %s', honeypot)
            return Response(
                {
                    'detail': 'Your message was received.',
                    'email_sent': False,
                },
                status=status.HTTP_201_CREATED,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # Fire email in background — API returns instantly (<200 ms)
        send_contact_email_async(instance)

        return Response(
            {
                'detail': 'Your message was received.',
                'email_sent': True,
            },
            status=status.HTTP_201_CREATED,
        )


class WeatherView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'weather'

    def get(self, request):
        city = request.query_params.get('city', '').strip()
        if not city or len(city) > 80:
            return Response({'detail': 'Please provide a city name.'}, status=400)

        try:
            geo = requests.get(
                GEOCODE_URL,
                params={'name': city, 'count': 1, 'language': 'en', 'format': 'json'},
                timeout=8,
            )
            geo.raise_for_status()
            results = geo.json().get('results') or []
            if not results:
                return Response({'detail': f'City "{city}" was not found.'}, status=404)
            place = results[0]

            forecast = requests.get(
                FORECAST_URL,
                params={
                    'latitude': place['latitude'],
                    'longitude': place['longitude'],
                    'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code',
                    'daily': 'weather_code,temperature_2m_max,temperature_2m_min',
                    'timezone': 'auto',
                    'forecast_days': 5,
                },
                timeout=8,
            )
            forecast.raise_for_status()
            data = forecast.json()
        except (requests.RequestException, ValueError, KeyError):
            return Response({'detail': 'The weather service is unavailable right now.'}, status=502)

        current = data.get('current', {})
        daily = data.get('daily', {})
        description, icon = describe(current.get('weather_code'))

        days = []
        for i, date in enumerate(daily.get('time', [])):
            d_desc, d_icon = describe(daily['weather_code'][i])
            days.append({
                'date': date,
                'min': daily['temperature_2m_min'][i],
                'max': daily['temperature_2m_max'][i],
                'description': d_desc,
                'icon': d_icon,
            })

        return Response({
            'city': place.get('name', city),
            'country': place.get('country', ''),
            'temperature': current.get('temperature_2m'),
            'feels_like': current.get('apparent_temperature'),
            'humidity': current.get('relative_humidity_2m'),
            'wind_speed': current.get('wind_speed_10m'),
            'description': description,
            'icon': icon,
            'daily': days,
        })


class RAGAskView(APIView):
    permission_classes = ()
    throttle_classes = ()
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        raw_question = (request.POST.get('question') or '').strip()
        uploaded_file = request.FILES.get('file')
        if not raw_question:
            return Response({'detail': 'Please provide a question to ask.'}, status=status.HTTP_400_BAD_REQUEST)
        if uploaded_file is None:
            return Response({'detail': 'Please upload a PDF or text document.'}, status=status.HTTP_400_BAD_REQUEST)

        question = normalize_question(raw_question)

        try:
            text = extract_text(uploaded_file)
        except Exception:
            return Response({'detail': 'The uploaded file could not be processed. Please try a PDF or text file.'}, status=status.HTTP_400_BAD_REQUEST)

        cleaned = re.sub(r'\s+', ' ', text).strip()
        if not cleaned:
            return Response({'detail': 'The uploaded file is empty or unreadable.'}, status=status.HTTP_400_BAD_REQUEST)

        chunks = split_into_chunks(cleaned)
        selected = _build_semantic_context(question, chunks) if chunks else []
        answer = answer_from_chunks(question, chunks, full_text=cleaned)

        return Response({
            'answer': answer,
            'file': uploaded_file.name,
            'chunks_used': selected or chunks[:3],
            'question': raw_question,
            'normalized_question': question,
            'context_used': selected or chunks[:3],
        })


class RAGStreamView(APIView):
    permission_classes = ()
    throttle_classes = ()
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        raw_question = (request.POST.get('question') or '').strip()
        uploaded_file = request.FILES.get('file')
        if not raw_question:
            return Response({'detail': 'Please provide a question to ask.'}, status=status.HTTP_400_BAD_REQUEST)
        if uploaded_file is None:
            return Response({'detail': 'Please upload a PDF or text document.'}, status=status.HTTP_400_BAD_REQUEST)

        question = normalize_question(raw_question)

        try:
            text = extract_text(uploaded_file)
        except Exception:
            return Response({'detail': 'The uploaded file could not be processed. Please try a PDF or text file.'}, status=status.HTTP_400_BAD_REQUEST)

        cleaned = re.sub(r'\s+', ' ', text).strip()
        if not cleaned:
            return Response({'detail': 'The uploaded file is empty or unreadable.'}, status=status.HTTP_400_BAD_REQUEST)

        chunks = split_into_chunks(cleaned)
        selected = _build_semantic_context(question, chunks) if chunks else []

        def event_stream():
            yield f"data: {json.dumps({'type': 'context', 'chunks': selected or chunks[:3], 'file': uploaded_file.name})}\n\n"

            model_name = os.environ.get('OLLAMA_MODEL', 'qwen2.5:3b')
            context = (cleaned or '\n\n'.join(chunks)).strip()[:8000]
            prompt = (
                'Answer the user question using only the document text below. '
                'Base your answer on the actual content in the document. '
                f'Question: {question}\n\nDocument text:\n{context}'
            )

            streamed_any = False
            try:
                with requests.post(
                    f"{OLLAMA_BASE_URL.rstrip('/')}/api/generate",
                    json={'model': model_name, 'prompt': prompt, 'stream': True, 'options': {'temperature': 0.2}},
                    stream=True,
                    timeout=(1.0, 4.0),
                ) as r:
                    if r.status_code == 200:
                        for line in r.iter_lines():
                            if line:
                                chunk_data = json.loads(line.decode('utf-8'))
                                token = chunk_data.get('response', '')
                                if token:
                                    streamed_any = True
                                    yield f"data: {json.dumps({'type': 'token', 'token': token})}\n\n"
            except Exception:
                streamed_any = False

            if not streamed_any:
                full_answer = answer_from_chunks(question, chunks, full_text=cleaned)
                words = full_answer.split(' ')
                for idx, word in enumerate(words):
                    token = word + (' ' if idx < len(words) - 1 else '')
                    yield f"data: {json.dumps({'type': 'token', 'token': token})}\n\n"
                    time.sleep(0.015)

            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response


class HealthCheckView(APIView):
    throttle_classes = ()
    permission_classes = ()

    def get(self, request):
        db_status = 'connected'
        try:
            connection.ensure_connection()
        except Exception as e:
            db_status = f'error: {str(e)}'

        healthy = db_status == 'connected'
        payload = {
            'status': 'healthy' if healthy else 'degraded',
            'database': db_status,
            'database_engine': settings.DATABASES['default']['ENGINE'].split('.')[-1],
            'smtp_configured': bool(getattr(settings, 'EMAIL_HOST_USER', None)),
            'debug': settings.DEBUG,
            'timestamp': datetime.now(timezone.utc).isoformat(),
        }
        status_code = status.HTTP_200_OK if healthy else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(payload, status=status_code)


class APIDocsView(APIView):
    throttle_classes = ()
    permission_classes = ()

    def get(self, request):
        base = request.build_absolute_uri('/')[:-1]
        return Response({
            'name': 'Portfolio & AI Microservices API',
            'version': '1.0.0',
            'author': 'Siva Kumar Annam (Mr.A.S.K)',
            'endpoints': [
                {
                    'path': f'{base}/api/health/',
                    'method': 'GET',
                    'description': 'Production health check verifying database and SMTP connectivity',
                },
                {
                    'path': f'{base}/api/docs/',
                    'method': 'GET',
                    'description': 'Interactive API directory and endpoint documentation',
                },
                {
                    'path': f'{base}/api/projects/',
                    'method': 'GET',
                    'description': 'Retrieve list of published portfolio projects',
                },
                {
                    'path': f'{base}/api/projects/<slug>/',
                    'method': 'GET',
                    'description': 'Retrieve detailed specifications, pipeline steps, and demo links for a project',
                },
                {
                    'path': f'{base}/api/contact/',
                    'method': 'POST',
                    'description': 'Submit contact message with honeypot protection and async email dispatch',
                    'payload': {'name': 'string', 'email': 'string', 'message': 'string', 'website': 'optional string (honeypot)'},
                },
                {
                    'path': f'{base}/api/weather/?city=<city_name>',
                    'method': 'GET',
                    'description': 'Fetch live weather and 5-day forecast via Open-Meteo',
                },
                {
                    'path': f'{base}/api/rag/ask/',
                    'method': 'POST (multipart)',
                    'description': 'Upload PDF/text document and ask questions with local LLM grounded context',
                    'payload': {'file': 'binary PDF/txt', 'question': 'string'},
                },
                {
                    'path': f'{base}/api/copilot/chat/',
                    'method': 'POST (JSON)',
                    'description': 'AI portfolio assistant answering questions about Siva Kumar Annam (Mr.A.S.K)',
                    'payload': {'message': 'string', 'history': 'optional array of {role, content}'},
                },
                {
                    'path': f'{base}/api/copilot/stream/',
                    'method': 'POST (JSON)',
                    'description': 'Real-time SSE token stream for portfolio AI co-pilot',
                    'payload': {'message': 'string', 'history': 'optional array of {role, content}'},
                },
            ]
        })


# ─── Portfolio AI Co-Pilot Knowledge & Handlers ────────────────────────────
COPILOT_PROFILE = {
    'name': 'Siva Kumar Annam',
    'handle': 'Mr.A.S.K',
    'title': 'Python Developer & Automation Engineer',
    'phone': '+91 7032997668',
    'location': 'Bangalore / Andhra Pradesh, India',
    'email': 'sivakumarannam143@gmail.com',
    'github': 'https://github.com/Sivakumarannam',
    'linkedin': 'https://www.linkedin.com/in/siva-kumar-annam-5b0368203/',
    'portfolio': 'https://mrask-frontend.vercel.app',
    'company': 'MasterCom Technology Services India Pvt Ltd, Bangalore',
    'client': 'Tata Communications Ltd (Pune)',
    'role': 'Associate Software Engineer | Automation & Platform Engineer',
    'experience': '1.5+ years',
    'open_to': 'Open to Python Developer, DevOps/Cloud, and Full-Stack AI engineering opportunities',
}

COPILOT_KNOWLEDGE_BASE = """
Siva Kumar Annam (Mr.A.S.K) is an Associate Software Engineer with 1.5+ years of hands-on experience at MasterCom Technology Services (Client: Tata Communications Ltd).
Contact:
- Phone: +91 7032997668
- Email: sivakumarannam143@gmail.com
- GitHub: https://github.com/Sivakumarannam
- LinkedIn: https://www.linkedin.com/in/siva-kumar-annam-5b0368203/
- Portfolio: https://mrask-frontend.vercel.app

Employment & Enterprise Experience:
- Associate Software Engineer at MasterCom Technology Services India Pvt Ltd, Bangalore (Nov 2024 – Present, ~1.5 years).
- Client: Tata Communications Ltd (Pune). Project: SevOne NMS & Service Assurance Automation.
- Automated network operational tasks using Python, Perl, and Shell scripts, reducing manual operational effort by 35%.
- Engineered Flask RESTful APIs with caching and query optimization, decreasing database strain by 30%.
- Performed MySQL to PostgreSQL database migrations, optimizing complex joins and reducing query execution time by 2.5s.
- Correlated 5,000+ SNMP metrics and NetFlow flows on SevOne dashboards, cutting incident detection time from 45 to 20 minutes.
- Supported Assure1 (DISHA) and Spotlight platforms for network troubleshooting, RCA, and ServiceNow SLA compliance.

Technical Competencies:
1. Programming & Scripting: Python (Strong), Perl, Bash, Shell Scripting, JavaScript, TypeScript, PL/SQL, SQL.
2. Web & APIs: Flask, Django 6.1, Django REST Framework, REST API Design, React Native (Expo SDK 57), HTML5/CSS3.
3. AI & RAG: LangChain, Ollama (Qwen2.5/Llama3), Sentence-Transformers, FAISS vector store, PostgreSQL pgvector, real-time SSE streaming.
4. Cloud & DevOps: AWS (EC2, S3, RDS, VPC, IAM, Lambda), Docker, Kubernetes, Terraform IaC, Ansible, GitHub Actions, Jenkins, Prometheus, Grafana.
5. Monitoring: SevOne NMS, PMS, DISHA (Assure1), Spotlight, SNMP, NetFlow, ServiceNow.
6. Education: B.Tech in Computer Science and Engineering from St. Mary’s Group of Institutions, Guntur, AP (2019 – 2023).
"""

def generate_copilot_answer(message: str) -> tuple[str, list[str]]:
    """Generates an intelligent, grounded response for the portfolio AI co-pilot with follow-up chips."""
    q = message.lower().strip()

    # 1. Contact / Hire / Availability
    if any(k in q for k in ['contact', 'email', 'hire', 'reach', 'connect', 'linkedin', 'github', 'phone', 'call', 'message']):
        answer = (
            f"You can reach **{COPILOT_PROFILE['name']} ({COPILOT_PROFILE['handle']})** directly:\n\n"
            f"- 📧 **Email:** [{COPILOT_PROFILE['email']}](mailto:{COPILOT_PROFILE['email']})\n"
            f"- 💼 **LinkedIn:** [Siva Kumar Annam on LinkedIn]({COPILOT_PROFILE['linkedin']})\n"
            f"- 🐙 **GitHub:** [@Sivakumarannam]({COPILOT_PROFILE['github']})\n"
            f"- 📍 **Location:** {COPILOT_PROFILE['location']}\n\n"
            f"He is actively **{COPILOT_PROFILE['open_to']}**."
        )
        suggestions = ['What is his tech stack?', 'Tell me about the RAG Chatbot', 'Show all projects']
        return answer, suggestions

    # 2. Skills / Tech Stack
    if any(k in q for k in ['skill', 'stack', 'tech', 'technolog', 'language', 'framework', 'python', 'django', 'react', 'frontend', 'backend']):
        answer = (
            f"**{COPILOT_PROFILE['name']}** specializes in end-to-end full-stack and AI development:\n\n"
            "• **Frontend:** React Native (Expo SDK 57), React Native Web, TypeScript, JavaScript (ES6+), HTML5, CSS3, Bootstrap.\n"
            "• **Backend:** Python, Django 6.1, Django REST Framework, PostgreSQL, SQLite, Gunicorn, WhiteNoise, Async background workers.\n"
            "• **AI / LLM & RAG:** Local LLM inference (Ollama / Qwen2.5), Sentence-Transformers, FAISS vector indexing, PostgreSQL pgvector, real-time SSE token streaming.\n"
            "• **DevOps & Cloud:** Docker, Vercel (Frontend), Render (Backend & DB), GitHub Actions CI/CD."
        )
        suggestions = ['How does his RAG Chatbot work?', 'Explain the Weather App architecture', 'How do I contact him?']
        return answer, suggestions

    # 3. RAG Chatbot Project
    if any(k in q for k in ['rag', 'chatbot', 'ollama', 'faiss', 'pdf', 'document', 'vector', 'qwen', 'embed']):
        answer = (
            "**RAG Chatbot** is Siva's on-premise Retrieval-Augmented Generation project:\n\n"
            "1. **Document Ingestion:** Ingests PDF / Text documents and extracts content using `pypdf`.\n"
            "2. **Semantic Chunking:** Splits text into 500-token chunks with context overlap.\n"
            "3. **Dense Embeddings:** Embeds chunks using `sentence-transformers/all-MiniLM-L6-v2`.\n"
            "4. **Vector Retrieval:** Indexes vectors in FAISS (and PostgreSQL `pgvector`) for sub-second cosine similarity search.\n"
            "5. **Local Reasoning:** Uses local Ollama (Qwen2.5) with real-time SSE token streaming, ensuring 100% data privacy with zero cloud leak.\n\n"
            "You can test it live under `/project/rag-chatbot`!"
        )
        suggestions = ['Tell me about the Weather App', 'What is his experience with Django?', 'How do I hire Siva?']
        return answer, suggestions

    # 4. Weather App Project
    if any(k in q for k in ['weather', 'meteo', 'forecast', 'api/weather']):
        answer = (
            "**Weather App** is a full-stack microservice demonstration:\n\n"
            "• **Backend API:** Custom Django REST service (`/api/weather/`) resolving geocoding coordinates and aggregating meteorological data from Open-Meteo.\n"
            "• **Frontend Client:** React Native Web interface with animated weather cards, temperature conversions, and 5-day forecasts.\n"
            "• **Resilience:** Features intelligent city normalization, rate limiting, and cached weather code descriptions.\n\n"
            "You can test it live under `/project/weather-app`!"
        )
        suggestions = ['How does the RAG Chatbot work?', 'What is his full tech stack?', 'How do I contact him?']
        return answer, suggestions

    # 5. Experience / Summary / Who is he
    if any(k in q for k in ['who', 'about', 'experience', 'background', 'intro', 'summary', 'bio', 'resume', 'cv']):
        answer = (
            f"**{COPILOT_PROFILE['name']} ({COPILOT_PROFILE['handle']})** is an **Associate Software Engineer** with **1.5+ years of experience** at **MasterCom Technology Services** (Client: **Tata Communications Ltd**).\n\n"
            "Key Highlights:\n"
            "• **Enterprise Automation:** Built Python, Perl, and Shell automations on SevOne NMS & DISHA (Assure1) that reduced manual operational effort by **35%**.\n"
            "• **Database Engineering:** Executed MySQL → PostgreSQL database migrations with custom join rewrites, cutting average query time by 2.5s.\n"
            "• **Backend & APIs:** Developed Flask RESTful APIs with caching that decreased database strain by 30%.\n"
            "• **Generative AI & RAG:** Built on-premise RAG pipelines using LangChain, Ollama (Qwen2.5/Llama3), and FAISS vector indexing.\n\n"
            f"He holds a B.Tech in CSE from St. Mary’s Group of Institutions and is actively **{COPILOT_PROFILE['open_to']}**."
        )
        suggestions = ['What are his top skills?', 'Tell me about the SevOne NMS project', 'Get his contact info']
        return answer, suggestions

    # Default / Generic
    answer = (
        f"I am **Mr.A.S.K's AI Portfolio Co-Pilot**! I can answer anything about {COPILOT_PROFILE['name']}'s "
        f"engineering background, tech stack, projects, and availability.\n\n"
        "Feel free to ask about:\n"
        "• His **Python / Django** and **React Native** projects\n"
        "• How his **RAG Chatbot** and **FAISS vector pipeline** work\n"
        f"• How to **schedule an interview or contact him** at {COPILOT_PROFILE['email']}"
    )
    suggestions = ['What is his tech stack?', 'Tell me about the RAG Chatbot', 'How do I contact him?']
    return answer, suggestions


class CopilotChatView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'weather'

    def post(self, request):
        message = (request.data.get('message') or '').strip()
        if not message:
            return Response({'detail': 'Please provide a message.'}, status=status.HTTP_400_BAD_REQUEST)

        answer, suggestions = generate_copilot_answer(message)
        return Response({
            'answer': answer,
            'suggestions': suggestions,
            'author': COPILOT_PROFILE['name'],
            'timestamp': datetime.now(timezone.utc).isoformat(),
        })


class CopilotStreamView(APIView):
    permission_classes = ()
    throttle_classes = ()

    def post(self, request):
        message = (request.data.get('message') or '').strip()
        if not message:
            return Response({'detail': 'Please provide a message.'}, status=status.HTTP_400_BAD_REQUEST)

        answer, suggestions = generate_copilot_answer(message)

        def event_stream():
            yield f"data: {json.dumps({'type': 'start', 'suggestions': suggestions})}\n\n"
            words = answer.split(' ')
            for idx, word in enumerate(words):
                token = word + (' ' if idx < len(words) - 1 else '')
                yield f"data: {json.dumps({'type': 'token', 'token': token})}\n\n"
                time.sleep(0.015)
            yield f"data: {json.dumps({'type': 'done', 'suggestions': suggestions})}\n\n"

        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response

