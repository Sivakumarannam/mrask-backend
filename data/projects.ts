// Fallback project data. When the Django API is running, projects are loaded from
// PostgreSQL instead (see lib/api.ts). Keep this list in sync with the seed command.

export type Project = {
  id: string;
  title: string;
  tagline: string;
  role: string;
  summary: string;
  highlights: string[];
  stack: string[];
  steps: string[];
  github: string;
  demoUrl?: string;
  demoKind?: 'weather' | 'rag' | '';
};

export const projects: Project[] = [
  {
    id: 'rag-chatbot',
    title: 'RAG Chatbot',
    tagline: 'Chat with your PDF documents using a local LLM',
    role: 'Solo project',
    summary:
      'A Retrieval-Augmented Generation chatbot that answers questions from uploaded PDF documents. It runs locally with Ollama, so no cloud LLM is needed.',
    highlights: [
      'Upload PDFs and extract their text',
      'Split text into chunks and generate embeddings',
      'Store vectors in FAISS and retrieve the most relevant context',
      'Generate grounded answers with Qwen2.5 through Ollama',
      'Simple Streamlit chat interface',
    ],
    stack: ['Python', 'LangChain', 'FAISS', 'Ollama', 'Qwen2.5', 'Streamlit'],
    steps: [
      'Upload a PDF',
      'Extract the text',
      'Split into chunks',
      'Create embeddings',
      'Store vectors in FAISS',
      'Retrieve relevant chunks',
      'Qwen2.5 writes the answer',
    ],
    github: 'https://github.com/Sivakumarannam/rag-chatbot-langchain-ollama',
    demoKind: 'rag',
  },
  {
    id: 'weather-app',
    title: 'Weather App',
    tagline: 'Live weather information from a weather API',
    role: 'Solo project',
    summary:
      'A weather application that fetches live weather data from a weather API. The live demo on its page runs through this portfolio\'s own Django API.',
    highlights: [
      'Fetches current weather and a 5-day forecast for any city',
      'Python / Django API cleans the data into simple JSON',
      'Works on web, Android and iOS from one codebase',
    ],
    stack: ['Python', 'Django', 'REST API', 'Open-Meteo', 'React Native'],
    steps: [
      'You enter a city',
      'Django API receives the request',
      'Geocoding finds the coordinates',
      'Weather API returns the forecast',
      'API cleans it into simple JSON',
      'The app shows the result',
    ],
    github: 'https://github.com/Sivakumarannam/weather_API_Backup',
    demoKind: 'weather',
  },
];
