"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { MessageSquare, Database, Search, Users, Sparkles } from "lucide-react";

export function Navbar() {
  const pathname = usePathname();

  const navItems = [
    { label: "Support Chat", href: "/", icon: MessageSquare },
    { label: "Knowledge Base", href: "/admin", icon: Database },
    { label: "Hybrid Search", href: "/search", icon: Search },
    { label: "Sessions", href: "/sessions", icon: Users },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4 sm:px-6">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <Link href="/" className="flex items-center gap-2 transition hover:opacity-90">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600 text-white shadow-sm shadow-indigo-600/30">
              <Sparkles className="h-4 w-4" />
            </div>
            <div>
              <span className="text-sm font-semibold tracking-tight text-slate-900">
                Support<span className="text-indigo-600">AI</span>
              </span>
              <span className="hidden sm:inline-block ml-2 rounded-full border border-slate-200 bg-slate-100 px-2 py-0.5 text-[10px] font-medium text-slate-600 font-mono">
                v2.0
              </span>
            </div>
          </Link>
        </div>

        {/* Center Nav */}
        <nav className="flex items-center gap-1">
          {navItems.map(({ label, href, icon: Icon }) => {
            const isActive = pathname === href;
            return (
              <Link
                key={href}
                href={href}
                className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-medium transition ${
                  isActive
                    ? "bg-slate-100 text-slate-900 font-semibold"
                    : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
                }`}
              >
                <Icon className="h-3.5 w-3.5" />
                <span>{label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Right Status */}
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 rounded-full border border-emerald-200 bg-emerald-50 px-2.5 py-0.5 text-[11px] font-medium text-emerald-700">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
            Memory Active
          </span>
        </div>
      </div>
    </header>
  );
}