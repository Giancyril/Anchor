"use client";

import { usePathname } from "next/navigation";
import { ShieldCheck, Cpu } from "lucide-react";

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
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-slate-800/80 bg-[#0c101c]/80 px-6 backdrop-blur-md">
      <div className="flex items-center gap-3">
        <h1 className="text-sm font-bold text-white tracking-tight">{currentTitle}</h1>
        <span className="rounded-full border border-slate-800 bg-slate-900 px-2 py-0.5 text-[10px] font-mono font-medium text-slate-400">
          FastAPI + Next.js
        </span>
      </div>

      <div className="flex items-center gap-3">
        <span className="hidden sm:inline-flex items-center gap-1.5 rounded-full border border-indigo-500/20 bg-indigo-950/40 px-3 py-1 text-[11px] font-medium text-indigo-300">
          <ShieldCheck className="h-3.5 w-3.5 text-indigo-400" />
          <span>Similarity Gate Active (0.75)</span>
        </span>
      </div>
    </header>
  );
}