export interface AIMessage {
  id?: string;
  conversation_id?: string;
  role: 'USER' | 'AI' | 'SYSTEM';
  message: string;
  created_at?: string;
}

export interface AIConversation {
  id: string;
  user_id: string;
  dataset_id: string | null;
  title: string;
  status: 'ACTIVE' | 'ARCHIVED';
  pinned: boolean;
  created_at: string;
  updated_at: string;
  messages: AIMessage[];
}

export interface AIInsight {
  id: string;
  dataset_id: string;
  category: string;
  insight: string;
  confidence: number;
  importance: 'HIGH' | 'MEDIUM' | 'LOW';
  source: string | null;
  generated_at: string;
}

export interface AIRecommendation {
  id: string;
  dataset_id: string;
  priority: 'HIGH' | 'MEDIUM' | 'LOW';
  recommendation: string;
  business_impact: string | null;
  confidence: number;
  status: 'NEW' | 'ACCEPTED' | 'REJECTED' | 'IMPLEMENTED';
  created_at: string;
}

export interface ChatRequest {
  message: string;
  dataset_id?: string;
  conversation_id?: string;
  stream?: boolean;
}
