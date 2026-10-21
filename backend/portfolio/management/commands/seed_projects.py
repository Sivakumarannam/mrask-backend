from django.core.management.base import BaseCommand

from portfolio.models import Project

PROJECTS = [
    {
        'slug': 'rag-chatbot',
        'title': 'RAG Chatbot',
        'tagline': 'Chat with your PDF documents using a local LLM',
        'role': 'Solo project',
        'summary': (
            'A Retrieval-Augmented Generation chatbot that answers questions from uploaded '
            'PDF documents. It runs locally with Ollama, so no cloud LLM is needed.'
        ),
        'highlights': [
            'Upload PDFs and extract their text',
            'Split text into chunks and generate embeddings',
            'Store vectors in FAISS and retrieve the most relevant context',
            'Generate grounded answers with Qwen2.5 through Ollama',
            'Simple Streamlit chat interface',
        ],
        'stack': ['Python', 'LangChain', 'FAISS', 'Ollama', 'Qwen2.5', 'Streamlit'],
        'steps': [
            'Upload a PDF',
            'Extract the text',
            'Split into chunks',
            'Create embeddings',
            'Store vectors in FAISS',
            'Retrieve relevant chunks',
            'Qwen2.5 writes the answer',
        ],
        'github_url': 'https://github.com/Sivakumarannam/rag-chatbot-langchain-ollama',
        'demo_url': '',
        'demo_kind': 'rag',
        'order': 1,
    },
    {
        'slug': 'weather-app',
        'title': 'Weather App',
        'tagline': 'Live weather information from a weather API',
        'role': 'Solo project',
        'summary': (
            'A weather application that fetches live weather data from a weather API. '
            "The live demo on its page runs through this portfolio's own Django API."
        ),
        'highlights': [
            'Fetches current weather and a 5-day forecast for any city',
            'Python / Django API cleans the data into simple JSON',
            'Works on web, Android and iOS from one codebase',
        ],
        'stack': ['Python', 'Django', 'REST API', 'Open-Meteo', 'React Native'],
        'steps': [
            'You enter a city',
            'Django API receives the request',
            'Geocoding finds the coordinates',
            'Weather API returns the forecast',
            'API cleans it into simple JSON',
            'The app shows the result',
        ],
        'github_url': 'https://github.com/Sivakumarannam/weather_API_Backup',
        'demo_url': '',
        'demo_kind': 'weather',
        'order': 2,
    },
]


class Command(BaseCommand):
    help = 'Create or update the portfolio projects.'

    def handle(self, *args, **options):
        for data in PROJECTS:
            slug = data['slug']
            _, created = Project.objects.update_or_create(slug=slug, defaults=data)
            self.stdout.write(f"{'Created' if created else 'Updated'}: {slug}")
