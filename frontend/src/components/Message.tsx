import React from 'react';

export function Message({ role, content }: { role: 'user' | 'assistant', content: string }) {
  return (
    <div className={`flex w-full mb-4 ${role === 'user' ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[85%] sm:max-w-[75%] md:max-w-[70%] rounded-2xl p-4 shadow-sm ${
        role === 'user' 
          ? 'bg-yellow-500 text-black rounded-br-none font-medium' 
          : 'bg-[#1C1C1C] border border-white/5 text-gray-200 rounded-bl-none'
      }`}>
        <p className="text-[15px] leading-relaxed whitespace-pre-wrap">{content}</p>
      </div>
    </div>
  );
}
