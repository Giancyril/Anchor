"use client";

import { usePathname } from "next/navigation";
import { Sparkles, ShieldCheck } from "lucide-react";

export function Header() {
  const pathname = usePathname();

  const titleMap: Record<string, string> = {
    "/": "Customer Support Chat",
    "/admin": "Knowledge Base Management",
    "/search": "Hybrid Search Inspector",
    "/sessions": "Customer Session Explorer",
    "/sync": "Auto-Sync & Diffs",
    "/escalation": "Live Agent Triage",
    "/telemetry": "RAG Triad Observatory",
  };

  const currentTitle = titleMap[pathname] || "Support AI Platform";

  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-slate-200 bg-white/80 px-6 backdrop-blur-md">
      <div className="flex items-center gap-3">
        <h1 className="text-sm font-bold text-slate-900">{currentTitle}</h1>
        <span className="rounded-full border border-slate-200 bg-slate-100 px-2 py-0.5 text-[10px] font-mono font-medium text-slate-600">
          FastAPI + Next.js
        </span>
      </div>

      <div className="flex items-center gap-3">
        <span className="hidden sm:inline-flex items-center gap-1.5 rounded-full border border-indigo-100 bg-indigo-50/80 px-3 py-1 text-[11px] font-medium text-indigo-700">
          <ShieldCheck className="h-3.5 w-3.5" />
          <span>Similarity Gate Active (0.75)</span>
        </span>
      </div>
    </header>
  );
}