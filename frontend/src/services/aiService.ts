import { api } from './api';
import { AIConversation, ChatRequest } from '../types/ai';

export const aiService = {
  getConversations: async (): Promise<AIConversation[]> => {
    const response = await api.get('/ai/conversations');
    return response.data;
  },

  getConversation: async (id: string): Promise<AIConversation> => {
    const response = await api.get(`/ai/conversations/${id}`);
    return response.data;
  },

  deleteConversation: async (id: string): Promise<void> => {
    await api.delete(`/ai/conversations/${id}`);
  },

  chatStream: async (
    request: ChatRequest, 
    onChunk: (chunk: string) => void,
    signal?: AbortSignal
  ): Promise<void> => {
    const token = localStorage.getItem('token');
    
    // We use native fetch for streaming since axios doesn't support streams in the browser easily
    const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
    
    try {
      const response = await fetch(`${baseURL}/ai/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ ...request, stream: true }),
        signal
      });

      if (!response.ok) {
        throw new Error(`Chat API error: ${response.statusText}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder('utf-8');

      if (!reader) return;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value, { stream: true });
        if (chunk) {
          onChunk(chunk);
        }
      }
    } catch (error: any) {
      if (error.name === 'AbortError') {
        console.log('Chat request cancelled');
      } else {
        throw error;
      }
    }
  },
  
  explainMetric: async (datasetId: string, target: string, context?: any) => {
    const response = await api.post('/ai/explain', { dataset_id: datasetId, target, context });
    return response.data.explanation;
  }
};
