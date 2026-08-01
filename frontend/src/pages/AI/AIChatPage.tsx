import React, { useState, useEffect, useRef } from 'react';
import { aiService } from '../../services/aiService';
import { AIConversation, AIMessage, ChatRequest } from '../../types/ai';

const AIChatPage: React.FC = () => {
  const [conversations, setConversations] = useState<AIConversation[]>([]);
  const [activeConversation, setActiveConversation] = useState<AIConversation | null>(null);
  const [messages, setMessages] = useState<AIMessage[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      const convos = await aiService.getConversations();
      setConversations(convos);
    } catch (error) {
      console.error('Failed to load conversations', error);
    }
  };

  const loadConversation = async (id: string) => {
    try {
      const conv = await aiService.getConversation(id);
      setActiveConversation(conv);
      setMessages(conv.messages || []);
    } catch (error) {
      console.error('Failed to load conversation', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput('');
    
    // Add user message to UI immediately
    const newMsg: AIMessage = { role: 'USER', message: userMessage, id: Date.now().toString() };
    setMessages(prev => [...prev, newMsg]);
    setIsTyping(true);
    
    abortControllerRef.current = new AbortController();

    const request: ChatRequest = {
      message: userMessage,
      conversation_id: activeConversation?.id,
      // dataset_id: selectedDatasetId
    };

    let aiMessageText = '';
    
    // Create a placeholder for AI message
    const aiMsgId = (Date.now() + 1).toString();
    setMessages(prev => [...prev, { role: 'AI', message: '', id: aiMsgId }]);

    try {
      await aiService.chatStream(
        request,
        (chunk) => {
          aiMessageText += chunk;
          setMessages(prev => 
            prev.map(msg => msg.id === aiMsgId ? { ...msg, message: aiMessageText } : msg)
          );
        },
        abortControllerRef.current.signal
      );
      
      // If it was a new conversation, refresh the list
      if (!activeConversation) {
        fetchConversations();
      }
    } catch (error) {
      console.error('Chat error', error);
      setMessages(prev => 
        prev.map(msg => msg.id === aiMsgId ? { ...msg, message: 'Sorry, I encountered an error.' } : msg)
      );
    } finally {
      setIsTyping(false);
      abortControllerRef.current = null;
    }
  };

  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsTyping(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      {/* Sidebar */}
      <div className="w-64 border-r border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950 flex flex-col">
        <div className="p-4 border-b border-gray-200 dark:border-gray-800">
          <button 
            onClick={() => { setActiveConversation(null); setMessages([]); }}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            + New Chat
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-2">
          {conversations.map(conv => (
            <div 
              key={conv.id} 
              onClick={() => loadConversation(conv.id)}
              className={`p-3 mb-1 rounded-lg cursor-pointer truncate ${activeConversation?.id === conv.id ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300' : 'hover:bg-gray-100 dark:hover:bg-gray-800'}`}
            >
              {conv.title}
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative">
        {/* Header */}
        <header className="p-4 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950 flex justify-between items-center shadow-sm z-10">
          <h2 className="text-lg font-semibold">{activeConversation?.title || 'New AI Analysis'}</h2>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-gray-400">
              <svg className="w-16 h-16 mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
              <p className="text-xl font-medium text-gray-600 dark:text-gray-300">How can I help you analyze your business data today?</p>
              
              <div className="mt-8 grid grid-cols-2 gap-4 max-w-2xl">
                {["Why did revenue fall last quarter?", "What customer segments are at risk?", "Summarize the latest dashboard metrics."].map((suggestion, i) => (
                   <button key={i} onClick={() => setInput(suggestion)} className="p-3 text-left bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl hover:shadow-md transition-all text-sm">
                     {suggestion}
                   </button>
                ))}
              </div>
            </div>
          )}
          
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'USER' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-3xl rounded-2xl p-4 ${msg.role === 'USER' ? 'bg-blue-600 text-white shadow-md' : 'bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 shadow-sm'}`}>
                {msg.role === 'AI' && <div className="flex items-center gap-2 mb-2"><span className="font-semibold text-sm bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">AI Analyst</span></div>}
                <div className="whitespace-pre-wrap">{msg.message}</div>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
               <div className="max-w-3xl rounded-2xl p-4 bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 flex items-center gap-2">
                 <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                 <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                 <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
               </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-white dark:bg-gray-950 border-t border-gray-200 dark:border-gray-800">
           <form onSubmit={handleSubmit} className="max-w-4xl mx-auto relative">
             <div className="relative flex items-center">
               <input
                 type="text"
                 value={input}
                 onChange={e => setInput(e.target.value)}
                 placeholder="Ask about your analytics or dashboards..."
                 disabled={isTyping}
                 className="w-full bg-gray-100 dark:bg-gray-900 border-none rounded-full py-4 pl-6 pr-24 focus:ring-2 focus:ring-blue-500 focus:outline-none disabled:opacity-50"
               />
               <div className="absolute right-2 flex items-center">
                 {isTyping ? (
                   <button type="button" onClick={handleStop} className="p-2 bg-red-100 text-red-600 hover:bg-red-200 rounded-full transition-colors mr-2">
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clipRule="evenodd" /></svg>
                   </button>
                 ) : (
                   <button type="submit" disabled={!input.trim()} className="p-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 disabled:opacity-50 transition-colors shadow-md">
                     <svg className="w-5 h-5 ml-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" /></svg>
                   </button>
                 )}
               </div>
             </div>
             <div className="text-center mt-2 text-xs text-gray-500">
                AI can make mistakes. Verify critical business numbers.
             </div>
           </form>
        </div>
      </div>
    </div>
  );
};

export default AIChatPage;
