"use client";

import React, { useState, useEffect } from "react";
import { Users, Clock, Smile, Frown, MessageSquare, AlertTriangle, RefreshCw } from "lucide-react";

interface SessionMessage {
  role: string;
  content: string;
  timestamp: number;
  confidence?: string;
  intent?: string;
  sentiment?: string;
}

interface SessionData {
  session_id: string;
  created_at: number;
  updated_at: number;
  messages: SessionMessage[];
  primary_intent: string;
  sentiment_history: string[];
}

export default function SessionsPage() {
  const [sessions, setSessions] = useState<SessionData[]>([]);
  const [selectedSession, setSelectedSession] = useState<SessionData | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchSessions = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/sessions");
      if (res.ok) {
        const data = await res.json();
        setSessions(data);
        if (data.length > 0 && !selectedSession) {
          setSelectedSession(data[0]);
        }
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  const totalSessions = sessions.length;
  const churnRiskCount = sessions.filter((s) => s.primary_intent.includes("Churn") || s.sentiment_history.some((st) => st.includes("Frustrated"))).length;

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-white sm:text-2xl">
            Customer Session Explorer & Intent Analytics
          </h1>
          <p className="mt-1 text-xs text-slate-400">
            Multi-turn conversation histories, zero-shot intent categorization, and customer sentiment trajectory.
          </p>
        </div>

        <button
          onClick={fetchSessions}
          className="flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-800/80 px-3 py-1.5 text-xs font-medium text-slate-300 hover:bg-slate-700 hover:text-white transition shadow-sm"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${loading ? "animate-spin" : ""}`} />
          <span>Refresh</span>
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="rounded-2xl border border-slate-800/80 bg-[#111827] p-5 shadow-xl ring-1 ring-white/5">
          <span className="text-[11px] font-mono uppercase text-slate-500 font-semibold">Tracked Conversations</span>
          <p className="mt-1 text-2xl font-bold text-white">{totalSessions}</p>
        </div>
        <div className="rounded-2xl border border-slate-800/80 bg-[#111827] p-5 shadow-xl ring-1 ring-white/5">
          <span className="text-[11px] font-mono uppercase text-slate-500 font-semibold">Frustration / Escalation Dips</span>
          <p className="mt-1 text-2xl font-bold text-amber-400">{churnRiskCount}</p>
        </div>
        <div className="rounded-2xl border border-slate-800/80 bg-[#111827] p-5 shadow-xl ring-1 ring-white/5">
          <span className="text-[11px] font-mono uppercase text-slate-500 font-semibold">Context Window Mode</span>
          <p className="mt-1 text-2xl font-bold text-indigo-400 font-mono">Sliding 10-Turn</p>
        </div>
      </div>

      {/* Two-Column Explorer Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Sessions List */}
        <div className="rounded-2xl border border-slate-800/80 bg-[#111827] p-4 shadow-xl ring-1 ring-white/5">
          <h2 className="text-xs font-mono uppercase font-bold text-slate-400 mb-3 tracking-wider">
            Active Sessions ({sessions.length})
          </h2>

          {sessions.length === 0 ? (
            <div className="p-8 text-center text-xs text-slate-500">
              No sessions recorded yet. Ask a question in Support Chat!
            </div>
          ) : (
            <div className="space-y-2">
              {sessions.map((s) => {
                const isSelected = selectedSession?.session_id === s.session_id;
                const hasFrustration = s.sentiment_history.some((st) => st.includes("Frustrated"));

                return (
                  <div
                    key={s.session_id}
                    onClick={() => setSelectedSession(s)}
                    className={`cursor-pointer rounded-xl border p-3 transition ${
                      isSelected
                        ? "border-indigo-500 bg-indigo-950/40 shadow-xs"
                        : "border-slate-800 bg-slate-900/60 hover:border-slate-700"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-[11px] font-semibold text-slate-300">
                        {s.session_id.slice(0, 8)}...
                      </span>
                      <span className="rounded-full border border-slate-700 bg-slate-800 px-2 py-0.5 text-[10px] font-medium text-slate-300">
                        {s.primary_intent}
                      </span>
                    </div>

                    <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400">
                      <span>{s.messages.length} messages</span>
                      {hasFrustration && (
                        <span className="flex items-center gap-1 text-amber-400 font-semibold">
                          <AlertTriangle className="h-3 w-3" /> Frustrated
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Selected Session Transcript */}
        <div className="lg:col-span-2 rounded-2xl border border-slate-800/80 bg-[#111827] p-5 shadow-xl ring-1 ring-white/5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
              <div>
                <h2 className="text-sm font-bold text-white">
                  Transcript Inspector: {selectedSession?.session_id || "None selected"}
                </h2>
                <p className="text-[11px] font-mono text-slate-400 mt-0.5">
                  Primary Intent: <span className="font-semibold text-indigo-400">{selectedSession?.primary_intent}</span>
                </p>
              </div>
            </div>

            {/* Transcript Messages */}
            {selectedSession?.messages && selectedSession.messages.length > 0 ? (
              <div className="space-y-3 max-h-[450px] overflow-y-auto pr-2">
                {selectedSession.messages.map((m, idx) => (
                  <div
                    key={idx}
                    className={`rounded-xl p-3 text-xs leading-relaxed ${
                      m.role === "user"
                        ? "bg-gradient-to-r from-indigo-600 to-indigo-700 text-white ml-8"
                        : "bg-slate-900 border border-slate-800 text-slate-200 mr-8"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1 opacity-70 text-[10px] font-mono">
                      <span>{m.role === "user" ? "Customer" : "Assistant"}</span>
                      {m.sentiment && <span>Sentiment: {m.sentiment}</span>}
                    </div>
                    <p>{m.content}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-12 text-center text-xs text-slate-500">
                Select a session on the left to inspect its conversation turns.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}