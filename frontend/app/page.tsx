"use client";

import React, { useState, useRef, useEffect } from "react";
import { sendMessage, ChatResponse, CitationSource } from "@/lib/api";
import { ChatMessage, MessageProps } from "@/components/chat/ChatMessage";
import { TypingIndicator } from "@/components/chat/TypingIndicator";
import { Send, Sparkles, RefreshCw, HelpCircle, Shield, CreditCard, Key } from "lucide-react";

export default function ChatPage() {
  const [messages, setMessages] = useState<MessageProps[]>([
    {
      role: "assistant",
      content: "Hello! I am your AI Support Assistant. I can answer questions regarding billing, integrations, security, pricing, and troubleshooting based directly on our company documentation. How can I help you today?",
      confidence: "high",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (questionToSend?: string) => {
    const q = questionToSend ?? input;
    if (!q.trim() || loading) return;

    const userMessage: MessageProps = { role: "user", content: q };
    setMessages((prev) => [...prev, userMessage]);
    if (!questionToSend) setInput("");
    setLoading(true);

    try {
      const res: ChatResponse = await sendMessage(q, sessionId);
      if (res.session_id) setSessionId(res.session_id);

      const assistantMessage: MessageProps = {
        role: "assistant",
        content: res.answer,
        confidence: res.confidence,
        escalated: res.escalated,
        sources: res.sources,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `An error occurred while retrieving answers: ${err.message || "Backend connection failed"}. Please check if the backend server is running.`,
          confidence: "low",
          escalated: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const samplePrompts = [
    { label: "What is your refund policy for annual plans?", icon: CreditCard },
    { label: "How do I generate an API key and what are the rate limits?", icon: Key },
    { label: "What authentication and MFA methods are supported?", icon: Shield },
    { label: "What features are included in the Pro plan?", icon: Sparkles },
  ];

  return (
    <div className="flex flex-col gap-6 max-w-4xl mx-auto">
      {/* Header Banner */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-900 sm:text-2xl">
              Customer Support Knowledge Assistant
            </h1>
            <p className="mt-1 text-xs text-slate-500">
              Retrieval-Augmented Generation grounded strictly in company documentation with Perplexity-style inline citations.
            </p>
          </div>
          <button
            onClick={() => {
              setMessages([
                {
                  role: "assistant",
                  content: "Conversation reset. How can I assist you with our documentation?",
                  confidence: "high",
                },
              ]);
              setSessionId(undefined);
            }}
            className="flex items-center gap-1.5 rounded-lg border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900 transition"
          >
            <RefreshCw className="h-3.5 w-3.5" />
            <span>New Chat</span>
          </button>
        </div>

        {/* Suggested Prompts */}
        {messages.length <= 2 && (
          <div className="mt-5 border-t border-slate-100 pt-4">
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block mb-2 font-semibold">
              Suggested Questions
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {samplePrompts.map(({ label, icon: Icon }) => (
                <button
                  key={label}
                  onClick={() => handleSend(label)}
                  disabled={loading}
                  className="flex items-center gap-2.5 rounded-xl border border-slate-200 bg-slate-50/50 p-2.5 text-left text-xs font-medium text-slate-700 hover:border-indigo-300 hover:bg-indigo-50/30 hover:text-indigo-900 transition disabled:opacity-50"
                >
                  <Icon className="h-4 w-4 text-indigo-600 shrink-0" />
                  <span className="truncate">{label}</span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Messages Thread */}
      <div className="flex flex-col gap-4 min-h-[350px]">
        {messages.map((msg, idx) => (
          <ChatMessage key={idx} {...msg} />
        ))}
        {loading && (
          <div className="flex gap-3 text-sm animate-slide-up">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-indigo-600 text-white">
              <Sparkles className="h-4 w-4" />
            </div>
            <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-chat">
              <TypingIndicator />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Box */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="sticky bottom-6 rounded-2xl border border-slate-200 bg-white p-2 shadow-card focus-within:border-indigo-500 focus-within:ring-2 focus-within:ring-indigo-100 transition"
      >
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about billing, refunds, integrations, security..."
            disabled={loading}
            className="flex-1 bg-transparent px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-hidden disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-brand transition hover:bg-indigo-500 active:scale-95 disabled:opacity-40 disabled:pointer-events-none"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
      </form>
    </div>
  );
}