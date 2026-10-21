import { useMemo, useState } from 'react';
import { Pressable, Text, TextInput, View } from 'react-native';

import { Button, Chip } from '@/components/ui';
import { useTheme } from '@/constants/theme';
import { askRagQuestion } from '@/lib/api';

const sampleContext = `
Siva Kumar Annam is a full-stack developer focused on building web and mobile products.
He works with React Native, Expo, Django, PostgreSQL, Python, and AI tools like LangChain, FAISS, Ollama, and Qwen.
His portfolio includes a RAG chatbot that answers questions from uploaded PDF documents using local retrieval.
The project stores embeddings in FAISS and uses the model locally for grounded answers.
`;

const examplePrompts = [
  'Summarize this document and list the key points.',
  'What are the main features mentioned in this PDF?',
  'List the skills and responsibilities in this document.',
  'Give me a short 3-point summary of this file.',
];

export function RAGDemo() {
  const t = useTheme();
  const [question, setQuestion] = useState('Summarize this document and list the key points and features.');
  const [answer, setAnswer] = useState(
    'Upload a PDF and ask a real question about its content. The app will search the text, retrieve the most relevant passages, and answer from the document itself.'
  );
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadedFile, setUploadedFile] = useState('sample-document.pdf');
  const [contextUsed, setContextUsed] = useState<string[]>([
    'Siva Kumar Annam is a full-stack developer focused on building web and mobile products.',
    'He works with React Native, Expo, Django, PostgreSQL, Python, and AI tools like LangChain, FAISS, Ollama, and Qwen.',
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const matches = useMemo(
    () => ['Any PDF', 'Ask anything', 'Semantic retrieval', 'Grounded answer'],
    []
  );

  const pickDocument = () => {
    if (typeof document !== 'undefined') {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = '.pdf,.txt,.docx';
      input.onchange = (event: Event) => {
        const file = (event.target as HTMLInputElement).files?.[0];
        if (!file) {
          return;
        }
        setSelectedFile(file);
        setUploadedFile(file.name);
      };
      input.click();
      return;
    }

    setSelectedFile(null);
    setUploadedFile('sample-document.pdf');
  };

  const runDemo = async () => {
    const q = question.trim();

    if (!q) {
      setAnswer('Ask a question about the PDF document to see the RAG workflow in action.');
      return;
    }

    if (selectedFile) {
      setIsLoading(true);
      try {
        const data = await askRagQuestion(selectedFile, q);
        setAnswer(data.answer);
        setUploadedFile(data.file || selectedFile.name);
        setContextUsed(data.context_used ?? data.chunks_used ?? [sampleContext.trim()]);
      } catch (error) {
        setAnswer(
          error instanceof Error
            ? error.message
            : 'The document could not be processed right now. Please try again or use the demo document.'
        );
      } finally {
        setIsLoading(false);
      }
      return;
    }

    const qLower = q.toLowerCase();

    if (qLower.includes('pdf') || qLower.includes('document') || qLower.includes('upload')) {
      setAnswer('The app uploads a PDF, extracts text, splits it into chunks, and retrieves the most relevant content before generating a grounded answer.');
      return;
    }

    if (qLower.includes('how') || qLower.includes('work')) {
      setAnswer('The system reads the PDF, creates embeddings, stores them in FAISS, retrieves the most relevant chunks, and then uses a local language model to answer the question.');
      return;
    }

    if (qLower.includes('stack') || qLower.includes('technology') || qLower.includes('tool')) {
      setAnswer('This workflow uses Python, LangChain, FAISS, Ollama, and a local LLM such as Qwen.');
      return;
    }

    if (qLower.includes('who') || qLower.includes('siva') || qLower.includes('developer')) {
      setAnswer('This portfolio belongs to Siva Kumar Annam, a full-stack developer building web apps, mobile apps, and AI-powered projects.');
      return;
    }

    setAnswer('Based on the uploaded document, the app answers by retrieving the most relevant passages and combining them with local model reasoning.');
  };

  const handlePromptClick = (prompt: string) => {
    setQuestion(prompt);
  };

  return (
    <View>
      <Pressable
        style={{
          borderWidth: 1,
          borderColor: t.border,
          borderRadius: 14,
          backgroundColor: t.cardAlt,
          padding: 14,
          marginBottom: 12,
        }}
        onPress={pickDocument}>
        <Text style={{ color: t.muted, fontSize: 12, fontWeight: '700', letterSpacing: 0.4 }}>UPLOADED FILE</Text>
        <Text style={{ color: t.text, fontSize: 16, fontWeight: '700', marginTop: 6 }}>{uploadedFile}</Text>
      </Pressable>

      <TextInput
        value={question}
        onChangeText={setQuestion}
        placeholder="Ask a question about the PDF"
        placeholderTextColor={t.muted}
        style={{
          backgroundColor: t.cardAlt,
          color: t.text,
          borderColor: t.border,
          borderWidth: 1,
          borderRadius: 12,
          paddingHorizontal: 14,
          paddingVertical: 12,
          fontSize: 16,
          marginBottom: 12,
        }}
      />

      <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 14 }}>
        {matches.map((m) => (
          <Chip key={m} label={m} />
        ))}
      </View>

      <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 16 }}>
        {examplePrompts.map((prompt) => (
          <Chip key={prompt} label={prompt} onPress={() => handlePromptClick(prompt)} />
        ))}
      </View>

      <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginBottom: 16 }}>
        <Button label={isLoading ? 'Processing...' : 'Ask question'} onPress={runDemo} />
      </View>

      <View
        style={{
          backgroundColor: t.cardAlt,
          borderColor: t.border,
          borderWidth: 1,
          borderRadius: 18,
          padding: 18,
          shadowColor: '#149DDD',
          shadowOpacity: 0.08,
          shadowRadius: 18,
          shadowOffset: { width: 0, height: 10 },
        }}>
        <Text style={{ color: t.muted, fontSize: 12, fontWeight: '700', marginBottom: 10, letterSpacing: 0.5 }}>
          RAG ANSWER
        </Text>
        <Text style={{ color: t.text, fontSize: 18, fontWeight: '700', lineHeight: 28 }}>{answer}</Text>
      </View>

      <View style={{ marginTop: 18, backgroundColor: t.cardAlt, borderWidth: 1, borderColor: t.border, borderRadius: 14, padding: 14 }}>
        <Text style={{ color: t.muted, fontWeight: '700', marginBottom: 10 }}>Source excerpts</Text>
        {contextUsed.map((chunk, index) => (
          <View
            key={`${chunk.slice(0, 16)}-${index}`}
            style={{
              backgroundColor: index % 2 === 0 ? t.card : 'transparent',
              borderWidth: 1,
              borderColor: t.border,
              borderRadius: 10,
              padding: 10,
              marginBottom: 8,
            }}>
            <Text style={{ color: t.text, fontSize: 14, lineHeight: 22 }}>{chunk}</Text>
          </View>
        ))}
      </View>
    </View>
  );
}
