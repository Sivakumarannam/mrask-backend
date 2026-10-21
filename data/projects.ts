// Add a new project by adding one object to this list.

export type Project = {
  id: string;
  title: string;
  tagline: string;
  role: string;
  summary: string;
  highlights: string[];
  stack: string[];
  github: string;
  demo?: string;
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
    github: 'https://github.com/Sivakumarannam/rag-chatbot-langchain-ollama',
  },
  {
    // TODO: update the description, highlights and stack to match your weather app.
    id: 'weather-app',
    title: 'Weather App',
    tagline: 'Live weather information from a weather API',
    role: 'Solo project',
    summary: 'A weather application that fetches live weather data from a weather API.',
    highlights: ['Fetches current weather data from an API'],
    stack: ['Weather API'],
    github: 'https://github.com/Sivakumarannam/weather_API_Backup',
  },
];
