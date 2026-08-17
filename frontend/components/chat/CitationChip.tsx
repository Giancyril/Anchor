"use client";

import React, { useState } from "react";
import { CitationSource } from "@/lib/api";
import { ExternalLink, FileText } from "lucide-react";

interface CitationChipProps {
  index: number;
  source?: CitationSource;
}

export function CitationChip({ index, source }: CitationChipProps) {
  const [showTooltip, setShowTooltip] = useState(false);

  if (!source) {
    return (
      <span className="inline-flex items-center justify-center mx-0.5 h-4 min-w-4 px-1 rounded bg-indigo-50 text-[10px] font-mono font-semibold text-indigo-700 border border-indigo-200">
        {index}
      </span>
    );
  }

  return (
    <span className="relative inline-block mx-0.5">
      <button
        type="button"
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        onClick={() => setShowTooltip(!showTooltip)}
        className="inline-flex items-center justify-center h-4 min-w-4 px-1 rounded bg-indigo-50 hover:bg-indigo-100 text-[10px] font-mono font-semibold text-indigo-700 border border-indigo-200 transition-colors shadow-xs"
      >
        {index}
      </button>

      {/* Popover Preview (Perplexity style) */}
      {showTooltip && (
        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 z-50 w-72 rounded-xl border border-slate-200 bg-white p-3 shadow-xl text-left text-xs animate-fade-in pointer-events-auto">
          <div className="flex items-center gap-1.5 font-medium text-slate-900 mb-1 border-b border-slate-100 pb-1.5">
            <FileText className="h-3.5 w-3.5 text-indigo-600 shrink-0" />
            <span className="truncate">{source.document_name}</span>
          </div>

          <div className="text-[11px] font-mono text-indigo-600 mb-1.5">
            § {source.section}
          </div>

          <p className="text-slate-600 text-[11px] leading-relaxed line-clamp-3 bg-slate-50 p-1.5 rounded border border-slate-100">
            "{source.snippet}"
          </p>

          {source.url && (
            <a
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-2 inline-flex items-center gap-1 text-[11px] font-medium text-indigo-600 hover:text-indigo-700 hover:underline"
            >
              <span>View Source Documentation</span>
              <ExternalLink className="h-3 w-3" />
            </a>
          )}
        </div>
      )}
    </span>
  );
}