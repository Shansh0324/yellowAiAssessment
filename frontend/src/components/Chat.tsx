'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Message } from './Message';
import { Input } from './Input';
import { sendMessage, getCustomerSessions, getSession, deleteSession } from '../lib/api';
import { SquarePen, Trash2, X, Search, MoreHorizontal, Lock, Bot, Paperclip, Send, Truck, Layers, Calculator, ArrowRight, PanelLeft } from 'lucide-react';

type Msg = { role: 'user' | 'assistant', content: string };

export function Chat() {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionList, setSessionList] = useState<any[]>([]);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const sessionId = useRef(`sess-${Math.random().toString(36).substring(2, 9)}`);
  const customerId = 'C-101'; 

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const fetchSessions = () => {
    getCustomerSessions(customerId)
      .then(data => setSessionList(data.sessions || []))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    fetchSessions();
    const savedId = localStorage.getItem('trendly_session_id');
    if (savedId) {
      loadSession(savedId);
    } else {
      localStorage.setItem('trendly_session_id', sessionId.current);
    }
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadSession = async (id: string) => {
    try {
      const data = await getSession(id);
      sessionId.current = id;
      localStorage.setItem('trendly_session_id', id);
      setMessages(data.messages || []);
    } catch (error) {
      console.error(error);
    }
  };

  const handleDeleteSession = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    try {
      await deleteSession(id);
      setSessionList(prev => prev.filter(s => s.session_id !== id));
      if (sessionId.current === id) {
        setMessages([]);
        const newId = `sess-${Math.random().toString(36).substring(2, 9)}`;
        sessionId.current = newId;
        localStorage.setItem('trendly_session_id', newId);
      }
    } catch (error) {
      console.error("Failed to delete session", error);
    }
  };

  const handleSend = async (text: string) => {
    const userMsg: Msg = { role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const data = await sendMessage(sessionId.current, customerId, text);
      setMessages(prev => [...prev, { role: 'assistant', content: data.message }]);
      
      // If this was the first message in a new session, refresh the sidebar
      if (messages.length === 0) {
        fetchSessions();
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I am having trouble connecting to the server.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-[100dvh] w-full bg-[#0A0A0A] text-white font-sans overflow-hidden">
      
      {/* Sidebar Overlay (Mobile) */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-20 md:hidden transition-opacity"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div 
        className={`
          fixed md:relative top-0 left-0 h-full bg-[#121212] border-r border-white/5 z-30
          transition-all duration-300 ease-in-out shrink-0 overflow-hidden
          ${isSidebarOpen ? 'w-[85vw] sm:w-[320px] translate-x-0 opacity-100' : 'w-0 -translate-x-full md:translate-x-0 md:w-0 border-none opacity-0'}
        `}
      >
        <div className="w-[85vw] sm:w-[320px] h-full flex flex-col p-4">
          {/* Sidebar Header */}
          <div className="flex items-center justify-between mb-6 px-2 mt-2">
            <div className="flex items-center gap-4 text-gray-400">
              <SquarePen 
                size={18} 
                className="cursor-pointer hover:text-white transition-colors" 
                onClick={() => {
                  setMessages([]);
                  const newId = `sess-${Math.random().toString(36).substring(2, 9)}`;
                  sessionId.current = newId;
                  localStorage.setItem('trendly_session_id', newId);
                }}
              />
            </div>
            <X onClick={() => setIsSidebarOpen(false)} size={20} className="text-gray-400 cursor-pointer hover:text-white transition-colors" />
          </div>

        {/* Search */}
        <div className="relative mb-6">
          <Search size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" />
          <input 
            type="text" 
            placeholder="Search" 
            className="w-full bg-[#1C1C1C] text-sm text-gray-200 rounded-full py-2.5 pl-11 pr-4 focus:outline-none focus:ring-1 focus:ring-white/20"
          />
        </div>

        {/* History List */}
        <div className="flex-1 overflow-y-auto space-y-2 pr-1 custom-scrollbar">
          <h3 className="text-xs font-medium text-gray-400 px-2 mb-3">Recent Chats</h3>
          {sessionList.length === 0 ? (
            <div className="text-xs text-gray-500 px-2">No previous conversations.</div>
          ) : (
            sessionList.map((s) => (
              <div 
                key={s.session_id}
                onClick={() => loadSession(s.session_id)}
                className="group flex items-center justify-between bg-[#1C1C1C] rounded-full px-4 py-2.5 text-sm text-gray-300 cursor-pointer hover:bg-[#252525] transition-colors"
              >
                <span className="truncate pr-2 flex-1">{s.summary}</span>
                <button 
                  onClick={(e) => handleDeleteSession(e, s.session_id)}
                  className="text-gray-500 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))
          )}
        </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 relative flex flex-col min-w-0 h-[100dvh]">
        {/* Background Grid Pattern & Glow */}
        <div className="absolute inset-0 pointer-events-none" 
          style={{
            backgroundImage: 'linear-gradient(to right, #333 1px, transparent 1px), linear-gradient(to bottom, #333 1px, transparent 1px)',
            backgroundSize: '40px 40px',
            opacity: 0.1
          }}
        />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-yellow-500/10 rounded-full blur-[120px] pointer-events-none" />

        {/* Top bar */}
        <div className="flex items-center justify-between p-4 sm:p-6 z-10 shrink-0">
          <div className="flex items-center gap-3 sm:gap-4">
            {!isSidebarOpen && (
              <button 
                onClick={() => setIsSidebarOpen(true)}
                className="p-1.5 hover:bg-white/10 rounded-md transition-colors text-gray-400 hover:text-white"
              >
                <PanelLeft size={20} />
              </button>
            )}
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-yellow-500 rounded flex items-center justify-center text-black font-bold text-xs">T</div>
              <span className="font-semibold text-base sm:text-lg tracking-tight">Trendly</span>
            </div>
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1 flex flex-col z-10 overflow-hidden relative">
          {messages.length === 0 ? (
            <div className="flex-1 flex flex-col items-center justify-center px-4 sm:px-8 mb-10 sm:mb-20">
              {/* Glowing Orb */}
              <div className="relative w-20 h-20 sm:w-24 sm:h-24 mb-6 sm:mb-8">
                <div className="absolute inset-0 rounded-full border border-yellow-500/30" />
                <div className="absolute inset-2 rounded-full border border-yellow-400/50" />
                <div className="absolute inset-0 bg-yellow-500/20 rounded-full blur-md" />
                <div className="absolute inset-4 bg-gradient-to-br from-yellow-300 to-yellow-600 rounded-full blur-sm" />
                <div className="absolute inset-4 bg-black rounded-full mix-blend-overlay opacity-50" />
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_30%,rgba(255,255,255,0.8),transparent_50%)] rounded-full" />
              </div>
              
              <h1 className="text-3xl sm:text-4xl font-semibold mb-3 text-center">
                <span className="text-yellow-500">Welcome to </span>
                <span className="text-white">Trendly Support!</span>
              </h1>
              <p className="text-gray-400 text-xs sm:text-sm mb-12 text-center">How can I assist you with your order today?</p>
            </div>
          ) : (
            <div className="flex-1 px-4 sm:px-6 md:px-8 pb-4 space-y-4 overflow-y-auto w-full max-w-4xl mx-auto [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
              {messages.map((m, i) => (
                <Message key={i} role={m.role} content={m.content} />
              ))}
              {isLoading && (
                 <div className="flex w-full mb-4 justify-start">
                   <div className="bg-[#1C1C1C] border border-white/5 rounded-2xl rounded-bl-none p-4 shadow-sm text-white">
                     <div className="flex gap-1.5">
                       <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                       <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                       <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                     </div>
                   </div>
                 </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}

          {/* Input Area */}
          <div className="px-4 sm:px-6 md:px-8 pb-6 sm:pb-8 lg:pb-12 pt-2 w-full max-w-3xl mx-auto shrink-0 bg-[#0A0A0A] sm:bg-transparent relative z-20">
            <Input onSend={handleSend} isLoading={isLoading} />
          </div>
        </div>
      </div>
    </div>
  );
}
