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
      <span className="inline-flex items-center justify-center mx-0.5 h-4 min-w-4 px-1 rounded bg-indigo-950 text-[10px] font-mono font-semibold text-indigo-300 border border-indigo-500/30">
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
        className="inline-flex items-center justify-center h-4 min-w-4 px-1 rounded bg-indigo-950/80 hover:bg-indigo-900 text-[10px] font-mono font-semibold text-indigo-300 border border-indigo-500/30 hover:border-indigo-400/50 transition-colors shadow-xs"
      >
        {index}
      </button>

      {/* Dark Popover Preview */}
      {showTooltip && (
        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 z-50 w-72 rounded-xl border border-slate-800 bg-slate-900/95 backdrop-blur-md p-3 shadow-2xl text-left text-xs animate-fade-in pointer-events-auto ring-1 ring-white/10">
          <div className="flex items-center gap-1.5 font-medium text-white mb-1 border-b border-slate-800 pb-1.5">
            <FileText className="h-3.5 w-3.5 text-indigo-400 shrink-0" />
            <span className="truncate">{source.document_name}</span>
          </div>

          <div className="text-[11px] font-mono text-indigo-400 mb-1.5">
            § {source.section}
          </div>

          <p className="text-slate-300 text-[11px] leading-relaxed line-clamp-3 bg-slate-950/80 p-2 rounded-lg border border-slate-800/80">
            "{source.snippet}"
          </p>

          {source.url && (
            <a
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-2 inline-flex items-center gap-1 text-[11px] font-medium text-indigo-400 hover:text-indigo-300 hover:underline"
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