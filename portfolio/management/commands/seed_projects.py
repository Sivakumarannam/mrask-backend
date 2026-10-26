from django.core.management.base import BaseCommand

from portfolio.models import Project

PROJECTS = [
    {
        'slug': 'sevone-automation',
        'title': 'SevOne NMS, NOC/SOC & Service Assurance Automation',
        'tagline': 'Enterprise NOC/SOC telemetry, security anomaly mitigation & operational automation',
        'role': 'Associate Software Engineer (MasterCom / Client: Tata Communications Ltd)',
        'summary': (
            'End-to-end automation of monitoring, reporting, and operational security tasks across telecom NOC & SOC environments '
            'on SevOne NMS, PMS, and DISHA (Assure1) for Tata Communications Ltd. Built Python and Perl automations that reduced manual '
            'operational effort by 35%, deployed DDoS mitigation runbooks, correlated 5,000+ SNMP & NetFlow streams, and maintained '
            'strict ServiceNow SLAs.'
        ),
        'highlights': [
            'Automated NOC/SOC device discovery, backups, log cleanup, and security telemetry collection via Python, Perl & Shell scripts (cut effort by ~35%)',
            'Correlated 5,000+ SNMP metrics and NetFlow flows on SevOne & Assure1 dashboards, reducing incident detection time from 45 to 20 minutes',
            'Engineered automated Python SSH runbooks mitigating volumetric traffic spikes and routing anomalies in under 4 seconds',
            'Led database migration from MySQL to PostgreSQL with join rewrites via Python/Perl and DBeaver, optimizing query execution by 2.5 seconds',
            'Engineered Python RESTful APIs with caching and performance optimization, reducing database strain by 30%',
            'Delivered L2/L3 support on Assure1 & Spotlight for real-time monitoring, security anomaly troubleshooting, and RCA under strict SLAs in ServiceNow',
        ],
        'stack': ['Python', 'Perl', 'Bash', 'Django REST Framework', 'MySQL', 'PostgreSQL', 'SevOne NMS', 'DISHA (Assure1)', 'NOC/SOC', 'SNMP', 'NetFlow', 'Linux', 'ServiceNow'],
        'steps': [
            'Ingest SNMP & NetFlow telemetry across global PoPs',
            'Correlate 5,000+ metrics & volumetric security anomalies in SevOne/Assure1',
            'Trigger threshold alerts & SOC incident events',
            'Automated Python/Perl scripts execute discovery, diagnostic checks & cleanup',
            'Python REST API serves live NOC/SOC analytics dashboards',
            'Sync tickets & SLA tracking via ServiceNow with RCA logs',
        ],
        'github_url': '',
        'demo_url': '',
        'demo_kind': '',
        'order': 1,
    },
    {
        'slug': 'telecom-db-migration',
        'title': 'MySQL → PostgreSQL Telecom Database Migration',
        'tagline': 'High-throughput database migration, join optimization & Python API caching',
        'role': 'Associate Software Engineer (MasterCom / Client: Tata Communications Ltd)',
        'summary': (
            'Engineered and executed mission-critical database migration from legacy MySQL to PostgreSQL for Tata Communications telecom infrastructure. '
            'Rewrote complex joins using Python and Perl hashes, optimized query execution times by 2.5 seconds, and designed Python RESTful APIs '
            'with caching that cut database strain by 30%.'
        ),
        'highlights': [
            'Successfully migrated large-scale relational schemas from MySQL to PostgreSQL with zero downtime or data loss',
            'Optimized multi-table join logic and query structures, cutting average query execution time by 2.5s',
            'Engineered Python RESTful APIs with caching and parameter validation, reducing database load by 30%',
            'Authored automated Python and Perl validation scripts verifying data integrity across all migrated tables',
        ],
        'stack': ['Python', 'Perl', 'PostgreSQL', 'MySQL', 'SQL', 'DBeaver', 'Linux'],
        'steps': [
            'Schema analysis & data type mapping',
            'Python/Perl automated extraction scripts',
            'PostgreSQL schema creation & indexing',
            'Complex join rewrites & benchmark testing',
            'API caching layer implementation',
            'Cutover validation & SLA signoff',
        ],
        'github_url': '',
        'demo_url': '',
        'demo_kind': '',
        'order': 2,
    },
    {
        'slug': 'rag-chatbot',
        'title': 'RAG Document Intelligence Studio',
        'tagline': 'Chat with custom PDF/Text documents using local LLMs & FAISS vector search',
        'role': 'Generative AI & LLM Project',
        'summary': (
            'An end-to-end Retrieval-Augmented Generation (RAG) system built with LangChain, local Ollama LLMs '
            '(Qwen2.5/Llama3), Sentence-Transformers, and FAISS vector indexing. Enables multi-turn context-aware '
            'Q&A on custom knowledge bases with streaming SSE tokens and grounded source citations.'
        ),
        'highlights': [
            'Ingests PDF and text documents, splits text into overlapping semantic chunks, and creates 384-dimensional dense embeddings',
            'Performs real-time sub-millisecond vector similarity search using FAISS (IndexFlatIP / Cosine Similarity)',
            'Streams LLM tokens in real-time to web and mobile clients via Server-Sent Events (SSE)',
            'Displays grounded citations highlighting exact source paragraphs to prevent hallucinations',
            'Self-hosted on-premise pipeline running with local Ollama, eliminating third-party cloud API costs',
        ],
        'stack': ['Python', 'LangChain', 'FAISS', 'Ollama', 'Qwen2.5', 'Sentence-Transformers', 'PyPDF', 'Django', 'React Native'],
        'steps': [
            'Upload PDF or text document',
            'Extract text via PyPDF reader',
            'Split into overlapping semantic chunks',
            'Generate embeddings with Sentence-Transformers',
            'Index vectors into FAISS store',
            'Cosine similarity retrieves top citations',
            'LLM streams grounded answer via SSE',
        ],
        'github_url': 'https://github.com/Sivakumarannam/rag-chatbot-langchain-ollama',
        'demo_url': '',
        'demo_kind': 'rag',
        'order': 3,
    },
    {
        'slug': 'weather-app',
        'title': 'Real-Time Weather Microservice',
        'tagline': 'Geocoding resolver & meteorological forecast microservice',
        'role': 'Full-Stack Microservice',
        'summary': (
            'A resilient weather microservice powered by Django REST Framework on Render and a cross-platform Expo client. '
            'Resolves geographic coordinates via Open-Meteo geocoding, aggregates 5-day forecasts, implements scoped rate limiting, '
            'and caches responses for high availability.'
        ),
        'highlights': [
            'Fetches current weather, apparent temperature, humidity, wind speed, and 5-day daily forecast for any global city',
            'Django REST Framework backend normalizes weather WMO codes into intuitive emojis and human-readable descriptions',
            'Includes scoped throttling (30 req/min) to prevent abuse and protect downstream APIs',
            'Seamless cross-platform UI built with custom glassmorphism design tokens running on Web, Android, and iOS',
        ],
        'stack': ['Python', 'Django', 'Django REST Framework', 'REST API', 'Open-Meteo', 'React Native', 'Expo'],
        'steps': [
            'User queries city name',
            'Django API checks cache & rate limits',
            'Geocoding API resolves latitude & longitude',
            'Open-Meteo retrieves hourly & daily forecast',
            'Backend formats and serializes response JSON',
            'Client renders interactive 5-day forecast card',
        ],
        'github_url': 'https://github.com/Sivakumarannam/weather_API_Backup',
        'demo_url': '',
        'demo_kind': 'weather',
        'order': 4,
    },
    {
        'slug': 'gitops-platform',
        'title': 'GitOps Continuous Deployment Platform',
        'tagline': 'Automated declarative delivery using GitHub Actions & Kubernetes',
        'role': 'Cloud & DevOps Capstone',
        'summary': (
            'An end-to-end GitOps deployment pipeline utilizing GitHub Actions, Docker containerization, and Kubernetes manifests '
            'for declarative continuous delivery. Automates pipeline execution, container image builds, SonarQube code scanning, '
            'and environment promotion.'
        ),
        'highlights': [
            'Configured automated CI/CD workflows using GitHub Actions and Jenkins with Slack notifications',
            'Integrated SonarQube for static code quality analysis and Nexus for artifact management',
            'Managed Kubernetes deployments, services, ConfigMaps, Secrets, and resource limits',
            'Implemented Infrastructure as Code (IaC) patterns using Terraform for repeatable cloud provisioning',
        ],
        'stack': ['Docker', 'Kubernetes', 'GitHub Actions', 'Jenkins', 'Terraform', 'AWS', 'SonarQube', 'Linux'],
        'steps': [
            'Code push triggers GitHub Actions workflow',
            'Linting & unit tests run in parallel runner',
            'SonarQube validates code quality & security',
            'Docker container image built and tagged',
            'Pushed to container registry',
            'Kubernetes applies declarative manifest updates',
        ],
        'github_url': '',
        'demo_url': '',
        'demo_kind': '',
        'order': 5,
    },
]


class Command(BaseCommand):
    help = 'Create or update the portfolio projects.'

    def handle(self, *args, **options):
        for data in PROJECTS:
            slug = data['slug']
            _, created = Project.objects.update_or_create(slug=slug, defaults=data)
            self.stdout.write(f"{'Created' if created else 'Updated'}: {slug}")
