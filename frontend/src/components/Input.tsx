'use client';

import React, { useState } from 'react';
import { Paperclip, ArrowRight, Bot } from 'lucide-react';

export function Input({ onSend, isLoading }: { onSend: (msg: string) => void, isLoading: boolean }) {
  const [value, setValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (value.trim() && !isLoading) {
      onSend(value);
      setValue('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative bg-[#202020] border border-white/10 rounded-[28px] p-2 flex flex-col shadow-xl">
      <div className="flex flex-col w-full">
        <textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="| Ask about your order, returns, or policies"
          disabled={isLoading}
          rows={1}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
          className="w-full bg-transparent text-gray-200 placeholder-gray-500 focus:outline-none px-4 py-3 resize-none max-h-32 custom-scrollbar"
        />
      </div>
      
      <div className="flex items-center justify-between mt-1 px-2 pb-1">
        <div className="flex items-center gap-2">          
          <div className="flex items-center gap-2 px-3 py-1 rounded-full border border-white/10 bg-white/5 cursor-pointer hover:bg-white/10 transition-colors">
            <Bot size={14} className="text-[#00A67E]" />
            <span className="text-[11px] font-medium text-gray-300">Open AI</span>
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading || !value.trim()}
          className="w-8 h-8 rounded-full bg-white flex items-center justify-center text-black hover:bg-gray-200 disabled:bg-white/20 disabled:text-white/50 transition-colors shadow-sm"
        >
          <ArrowRight size={18} strokeWidth={2.5} />
        </button>
      </div>
    </form>
  );
}
