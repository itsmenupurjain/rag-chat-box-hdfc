'use client';

import { useState, useRef, useEffect } from 'react';

export default function Home() {
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant', content: string }[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Default to relative '/api' in production/monorepo, fallback to env variable or local port
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 
    (typeof window !== 'undefined' && window.location.hostname !== 'localhost' ? '/api' : 'http://localhost:8000');

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = async (e?: React.FormEvent, text?: string) => {
    e?.preventDefault();
    const query = text || input;
    if (!query.trim()) return;

    setMessages(prev => [...prev, { role: 'user', content: query }]);
    if (!text) setInput('');
    setLoading(true);

    try {
      const res = await fetch(`${backendUrl}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      
      if (!res.ok) throw new Error('Backend error');
      
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'I encountered an error connecting to the intelligence vault. Please ensure the backend is running.' }]);
    } finally {
      setLoading(false);
    }
  };

  const triggers = [
    { label: 'LATEST NAV', query: 'What is the latest NAV of HDFC Mid Cap Fund?' },
    { label: 'EXIT LOADS', query: 'Exit load for HDFC ELSS Fund?' },
    { label: 'FUND MANAGERS', query: 'Who is the manager of HDFC Focused Fund?' },
  ];

  return (
    <main className="max-w-4xl mx-auto px-4 py-12 min-h-screen flex flex-col">
      <header className="text-center mb-12">
        <h1 className="text-5xl font-black tracking-tighter mb-2">🏦 HDFC AI</h1>
        <p className="text-white/60 text-lg">Ultra-Premium Factual Mutual Fund Intel.</p>
      </header>

      {/* Triggers */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-12">
        {triggers.map((t, i) => (
          <button
            key={i}
            onClick={() => handleSubmit(undefined, t.query)}
            className="glossy-card text-center group"
          >
            <div className="text-sm font-bold tracking-widest mb-2 group-hover:text-blue-400 transition-colors">
              {t.label}
            </div>
            <div className="text-xs text-white/40">{t.query}</div>
          </button>
        ))}
      </div>

      {/* Chat Area */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto mb-32 space-y-4 pr-2 scroll-smooth"
      >
        {messages.length === 0 && (
          <div className="text-center text-white/20 mt-20 italic">
            Awaiting your query...
          </div>
        )}
        {messages.map((m, i) => (
          <div 
            key={i} 
            className={`chat-message ${m.role === 'user' ? 'ml-12 border-white/20' : 'mr-12 border-blue-500/30'}`}
          >
            <div className="text-[10px] uppercase tracking-widest opacity-40 mb-2">
              {m.role === 'user' ? 'User' : 'Assistant'}
            </div>
            <div className="whitespace-pre-wrap text-sm leading-relaxed">{m.content}</div>
          </div>
        ))}
        {loading && (
          <div className="chat-message mr-12 border-blue-500/30 animate-pulse flex items-center gap-3">
             <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
             <div className="text-sm text-blue-400">Retrieving facts from vault...</div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="fixed bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-[#020408] via-[#020408]/80 to-transparent">
        <form 
          onSubmit={handleSubmit}
          className="max-w-4xl mx-auto relative"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about any HDFC scheme..."
            className="w-full bg-white/5 border border-white/10 rounded-full py-4 px-6 focus:outline-none focus:border-white/30 focus:bg-white/10 transition-all backdrop-blur-2xl text-white placeholder:text-white/20"
          />
          <button 
            type="submit"
            disabled={loading}
            className="absolute right-2 top-1/2 -translate-y-1/2 bg-white text-black rounded-full px-6 py-2 font-bold text-xs hover:bg-blue-400 hover:text-white transition-all disabled:opacity-50 disabled:hover:bg-white disabled:hover:text-black"
          >
            {loading ? '...' : 'SEND'}
          </button>
        </form>
        <div className="text-center mt-6 text-[9px] tracking-[0.3em] opacity-30 uppercase font-bold">
          Secure • Factual • Non-Advisory
        </div>
      </div>
    </main>
  );
}
