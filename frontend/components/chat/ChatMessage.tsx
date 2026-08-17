"use client";

import React from "react";
import { CitationSource } from "@/lib/api";
import { CitationChip } from "./CitationChip";
import { EscalationBanner } from "./EscalationBanner";
import { User, Sparkles, FileText, CheckCircle2, AlertCircle } from "lucide-react";

export interface MessageProps {
  role: "user" | "assistant";
  content: string;
  confidence?: "high" | "low";
  escalated?: boolean;
  sources?: CitationSource[];
}

export function ChatMessage({ role, content, confidence, escalated, sources = [] }: MessageProps) {
  const isUser = role === "user";
  const sourceMap = new Map<number, CitationSource>(sources.map((s) => [s.citation_index, s]));

  // Parse inline citations [1], [2] in text and render CitationChip
  const renderFormattedText = (text: string) => {
    const parts = text.split(/(\[\d+\])/g);
    return parts.map((part, i) => {
      const match = part.match(/^\[(\d+)\]$/);
      if (match) {
        const idx = parseInt(match[1], 10);
        return <CitationChip key={i} index={idx} source={sourceMap.get(idx)} />;
      }
      return <span key={i}>{part}</span>;
    });
  };

  return (
    <div className={`flex gap-3 text-sm animate-slide-up ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-xs">
          <Sparkles className="h-4 w-4" />
        </div>
      )}

      <div className={`max-w-2xl rounded-2xl p-4 shadow-chat ${
        isUser
          ? "bg-indigo-600 text-white"
          : "border border-slate-200 bg-white text-slate-900"
      }`}>
        {/* Header tags for assistant messages */}
        {!isUser && (
          <div className="flex items-center justify-between mb-2 pb-2 border-b border-slate-100 text-xs">
            <div className="flex items-center gap-1.5 font-medium text-slate-700">
              <span>Support Assistant</span>
            </div>

            {confidence && (
              <span className={`inline-flex items-center gap-1 text-[10px] font-medium font-mono px-2 py-0.5 rounded-full ${
                confidence === "high"
                  ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                  : "bg-amber-50 text-amber-700 border border-amber-200"
              }`}>
                {confidence === "high" ? (
                  <>
                    <CheckCircle2 className="h-3 w-3" />
                    <span>Grounded</span>
                  </>
                ) : (
                  <>
                    <AlertCircle className="h-3 w-3" />
                    <span>Low Confidence</span>
                  </>
                )}
              </span>
            )}
          </div>
        )}

        {/* Message body */}
        <div className={`leading-relaxed whitespace-pre-wrap ${isUser ? "text-white" : "text-slate-800"}`}>
          {renderFormattedText(content)}
        </div>

        {/* Low confidence escalation banner */}
        {!isUser && escalated && <EscalationBanner />}

        {/* Cited Sources List (Footer) */}
        {!isUser && sources.length > 0 && (
          <div className="mt-4 pt-3 border-t border-slate-100">
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-semibold block mb-2">
              Verified Sources ({sources.length})
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {sources.map((src) => (
                <div
                  key={src.citation_index}
                  className="rounded-lg border border-slate-200 bg-slate-50/70 p-2 text-xs flex items-start gap-2"
                >
                  <span className="flex h-4 min-w-4 items-center justify-center rounded bg-indigo-100 font-mono text-[10px] font-bold text-indigo-700">
                    {src.citation_index}
                  </span>
                  <div className="overflow-hidden">
                    <p className="font-medium text-slate-900 truncate">{src.document_name}</p>
                    <p className="text-[11px] text-slate-500 truncate">§ {src.section}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {isUser && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-slate-200 text-slate-600">
          <User className="h-4 w-4" />
        </div>
      )}
    </div>
  );
}