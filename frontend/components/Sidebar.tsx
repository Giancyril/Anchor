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
  ChevronLeft,
} from "lucide-react";
import { AnchorLogo } from "@/components/AnchorLogo";

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
        { label: "Hybrid Search", href: "/search", icon: Search, badge: "BM25" },
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
      className={`relative sticky top-0 h-screen flex flex-col justify-between border-r border-slate-800/80 bg-[#0c101c] transition-all duration-300 ease-in-out z-40 shrink-0 select-none ${
        collapsed ? "w-18" : "w-64"
      }`}
    >
      {/* Floating Border Toggle Pill */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        className="absolute -right-3 top-5 z-50 flex h-6 w-6 items-center justify-center rounded-full border border-slate-700 bg-slate-900 text-slate-400 hover:bg-slate-800 hover:text-indigo-400 hover:border-indigo-500/50 transition-colors duration-200 focus:outline-none"
      >
        <ChevronLeft
          className={`h-3.5 w-3.5 transition-transform duration-300 ease-in-out ${
            collapsed ? "rotate-180" : "rotate-0"
          }`}
        />
      </button>

      {/* Top Header */}
      <div>
        <div
          className={`flex h-16 items-center border-b border-slate-800/80 overflow-hidden transition-all duration-300 ${
            collapsed ? "justify-center px-2" : "justify-start px-4"
          }`}
        >
          <Link href="/" className="flex items-center gap-3 overflow-hidden focus:outline-none">
            <AnchorLogo size="sm" className="shrink-0" />
            <div
              className={`flex flex-col transition-all duration-300 ease-in-out ${
                collapsed
                  ? "opacity-0 max-w-0 -translate-x-3 pointer-events-none"
                  : "opacity-100 max-w-xs translate-x-0"
              }`}
            >
              <span className="text-sm font-bold tracking-tight text-white leading-none whitespace-nowrap">
                Anchor<span className="text-indigo-400">AI</span>
              </span>
              <span className="text-[10px] font-mono text-slate-500 mt-1 whitespace-nowrap">
                RAG Agent v2.0
              </span>
            </div>
          </Link>
        </div>

        {/* Navigation Items */}
        <div className="p-2.5 space-y-5 overflow-y-auto max-h-[calc(100vh-140px)]">
          {navGroups.map((group, gIdx) => (
            <div key={gIdx} className="space-y-1">
              <div
                className={`overflow-hidden transition-all duration-300 ease-in-out ${
                  collapsed
                    ? "opacity-0 max-h-0 -translate-y-1 pointer-events-none"
                    : "opacity-100 max-h-6 translate-y-0"
                }`}
              >
                <span className="px-2.5 text-[10px] font-mono font-bold uppercase tracking-wider text-slate-500 whitespace-nowrap block">
                  {group.title}
                </span>
              </div>

              <nav className="space-y-0.5">
                {group.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = pathname === item.href;

                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      title={collapsed ? item.label : undefined}
                      draggable={false}
                      className={`flex items-center rounded-xl text-xs font-medium transition-colors duration-150 outline-none focus:outline-none ${
                        collapsed ? "justify-center p-2.5" : "justify-start px-3 py-2 gap-3"
                      } ${
                        isActive
                          ? "bg-indigo-600/15 text-indigo-300 font-semibold border border-indigo-500/30"
                          : "text-slate-400 hover:bg-slate-800/70 hover:text-slate-200 border border-transparent"
                      }`}
                    >
                      <Icon
                        className={`h-4 w-4 shrink-0 transition-colors duration-150 ${
                          isActive ? "text-indigo-400" : "text-slate-500 group-hover:text-slate-300"
                        }`}
                      />
                      <div
                        className={`flex flex-1 items-center justify-between overflow-hidden transition-all duration-300 ease-in-out ${
                          collapsed
                            ? "opacity-0 max-w-0 -translate-x-2 pointer-events-none"
                            : "opacity-100 max-w-xs translate-x-0"
                        }`}
                      >
                        <span className="truncate whitespace-nowrap">{item.label}</span>
                        {item.badge && (
                          <span
                            className={`rounded-full px-1.5 text-[9px] font-mono font-semibold shrink-0 ml-1.5 ${
                              isActive
                                ? "bg-indigo-500/20 text-indigo-300 border border-indigo-500/30"
                                : "bg-slate-800 text-slate-400"
                            }`}
                          >
                            {item.badge}
                          </span>
                        )}
                      </div>
                    </Link>
                  );
                })}
              </nav>
            </div>
          ))}
        </div>
      </div>

      {/* Bottom Status Card */}
      <div className="p-2.5 border-t border-slate-800/80 overflow-hidden">
        <div
          className={`rounded-xl border border-slate-800/80 bg-slate-900/60 transition-all duration-300 ease-in-out ${
            collapsed ? "p-2 flex justify-center" : "p-3"
          }`}
        >
          {collapsed ? (
            <div className="flex justify-center items-center py-1" title="System Status: Live">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-500 opacity-75" />
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-400" />
              </span>
            </div>
          ) : (
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <span className="font-mono text-[10px] uppercase font-bold text-slate-500 whitespace-nowrap">
                  System Status
                </span>
                <span className="inline-flex items-center gap-1 text-[10px] font-medium text-emerald-400 whitespace-nowrap">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  Live
                </span>
              </div>
              <p className="text-[11px] text-slate-400 leading-tight">
                Pinecone Serverless + OpenAI RAG Hybrid Engine
              </p>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}