"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  MessageSquare,
  Database,
  Search,
  Users,
  RefreshCw,
  LifeBuoy,
  Activity,
  Sparkles,
  ChevronLeft,
  ChevronRight,
  Shield,
  Zap,
} from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  const navGroups = [
    {
      title: "Core Agent",
      items: [
        { label: "Support Chat", href: "/", icon: MessageSquare, badge: "Grounded" },
        { label: "Knowledge Base", href: "/admin", icon: Database },
      ],
    },
    {
      title: "RAG & Retrieval",
      items: [
        { label: "Hybrid Search", href: "/search", icon: Search, badge: "BM25+Dense" },
        { label: "Auto-Sync & Diffs", href: "/sync", icon: RefreshCw },
      ],
    },
    {
      title: "Operations & HITL",
      items: [
        { label: "Customer Sessions", href: "/sessions", icon: Users },
        { label: "Live Escalations", href: "/escalation", icon: LifeBuoy, badge: "Queue" },
        { label: "RAG Observatory", href: "/telemetry", icon: Activity },
      ],
    },
  ];

  return (
    <aside
      className={`sticky top-0 h-screen flex flex-col justify-between border-r border-slate-200 bg-white transition-all duration-300 z-40 ${
        collapsed ? "w-18" : "w-64"
      }`}
    >
      {/* Top Brand & Header */}
      <div>
        <div className="flex h-16 items-center justify-between px-4 border-b border-slate-100">
          <Link href="/" className="flex items-center gap-2.5 overflow-hidden">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-brand">
              <Sparkles className="h-5 w-5" />
            </div>
            {!collapsed && (
              <div className="flex flex-col">
                <span className="text-sm font-bold tracking-tight text-slate-900 leading-none">
                  Anchor<span className="text-indigo-600">AI</span>
                </span>
                <span className="text-[10px] font-mono text-slate-400 mt-0.5">RAG Agent v2.0</span>
              </div>
            )}
          </Link>

          <button
            onClick={() => setCollapsed(!collapsed)}
            className="hidden sm:flex h-7 w-7 items-center justify-center rounded-lg border border-slate-200 text-slate-400 hover:bg-slate-50 hover:text-slate-700 transition"
          >
            {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
          </button>
        </div>

        {/* Navigation Items */}
        <div className="p-3 space-y-6 overflow-y-auto max-h-[calc(100vh-140px)]">
          {navGroups.map((group, gIdx) => (
            <div key={gIdx} className="space-y-1">
              {!collapsed && (
                <span className="px-3 text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400">
                  {group.title}
                </span>
              )}
              <nav className="space-y-1">
                {group.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = pathname === item.href;

                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      title={collapsed ? item.label : undefined}
                      className={`flex items-center gap-3 rounded-xl px-3 py-2 text-xs font-medium transition group relative ${
                        isActive
                          ? "bg-indigo-50/80 text-indigo-700 font-semibold shadow-2xs"
                          : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                      }`}
                    >
                      <Icon
                        className={`h-4 w-4 shrink-0 transition ${
                          isActive ? "text-indigo-600" : "text-slate-400 group-hover:text-slate-600"
                        }`}
                      />
                      {!collapsed && (
                        <div className="flex flex-1 items-center justify-between truncate">
                          <span className="truncate">{item.label}</span>
                          {item.badge && (
                            <span
                              className={`rounded-full px-1.5 py-0.2 text-[9px] font-mono font-semibold ${
                                isActive
                                  ? "bg-indigo-100 text-indigo-800"
                                  : "bg-slate-100 text-slate-500"
                              }`}
                            >
                              {item.badge}
                            </span>
                          )}
                        </div>
                      )}
                    </Link>
                  );
                })}
              </nav>
            </div>
          ))}
        </div>
      </div>

      {/* Bottom Status Card */}
      <div className="p-3 border-t border-slate-100">
        {!collapsed ? (
          <div className="rounded-xl border border-slate-200 bg-slate-50/70 p-3 text-xs">
            <div className="flex items-center justify-between mb-1.5">
              <span className="font-mono text-[10px] uppercase font-bold text-slate-400">System Status</span>
              <span className="inline-flex items-center gap-1 text-[10px] font-medium text-emerald-600">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
                Live
              </span>
            </div>
            <p className="text-[11px] text-slate-600 leading-tight">
              Pinecone Serverless + OpenAI RAG Hybrid Engine
            </p>
          </div>
        ) : (
          <div className="flex justify-center">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" title="System Live" />
          </div>
        )}
      </div>
    </aside>
  );
}