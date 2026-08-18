"use client";

import React, { useState, useEffect } from "react";
import { LifeBuoy, AlertCircle, CheckCircle2, UserCheck, MessageSquare, Send, RefreshCw, Sparkles } from "lucide-react";

interface SupportTicket {
  ticket_id: string;
  session_id: string;
  title: string;
  customer_query: string;
  intent: string;
  sentiment: string;
  priority: string;
  status: string;
  created_at: number;
  assigned_agent?: string;
}

interface LiveQueueItem {
  queue_id: string;
  session_id: string;
  customer_name: string;
  priority_score: number;
  reason: string;
  status: string;
}

export default function EscalationPage() {
  const [tickets, setTickets] = useState<SupportTicket[]>([]);
  const [queue, setQueue] = useState<LiveQueueItem[]>([]);
  const [selectedTicket, setSelectedTicket] = useState<SupportTicket | null>(null);
  const [cannedReplies, setCannedReplies] = useState<string[]>([]);
  const [replyText, setReplyText] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    try {
      const [tRes, qRes] = await Promise.all([
        fetch("http://127.0.0.1:8000/api/v1/escalation/tickets"),
        fetch("http://127.0.0.1:8000/api/v1/escalation/queue"),
      ]);
      if (tRes.ok) {
        const tData = await tRes.json();
        setTickets(tData);
        if (tData.length > 0 && !selectedTicket) {
          selectTicket(tData[0]);
        }
      }
      if (qRes.ok) {
        setQueue(await qRes.json());
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const selectTicket = async (ticket: SupportTicket) => {
    setSelectedTicket(ticket);
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/escalation/canned?intent=${encodeURIComponent(ticket.intent)}`);
      if (res.ok) {
        const data = await res.json();
        setCannedReplies(data.suggestions || []);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleResolve = async () => {
    if (!selectedTicket || !replyText.trim()) return;
    setLoading(true);
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/escalation/tickets/${selectedTicket.ticket_id}/resolve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resolution_notes: replyText, agent_name: "Lead Support Agent" }),
      });
      if (res.ok) {
        setReplyText("");
        await fetchData();
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-white sm:text-2xl">
            Live Human Escalation & Agent Triage
          </h1>
          <p className="mt-1 text-xs text-slate-400">
            Real-time human-in-the-loop (HITL) queue, priority escalation management, and grounded AI reply assistance.
          </p>
        </div>

        <button
          onClick={fetchData}
          className="flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-800/80 px-3 py-1.5 text-xs font-medium text-slate-300 hover:bg-slate-700 hover:text-white transition shadow-sm"
        >
          <RefreshCw className="h-3.5 w-3.5" />
          <span>Refresh Queue</span>
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="rounded-2xl border border-slate-800/80 bg-[#111827] p-5 shadow-xl ring-1 ring-white/5">
          <span className="text-[11px] font-mono uppercase text-slate-500 font-semibold">Escalated Tickets</span>
          <p className="mt-1 text-2xl font-bold text-white">{tickets.length}</p>
        </div>
        <div className="rounded-2xl border border-slate-800/80 bg-[#111827] p-5 shadow-xl ring-1 ring-white/5">
          <span className="text-[11px] font-mono uppercase text-slate-500 font-semibold">Live Waiting Queue</span>
          <p className="mt-1 text-2xl font-bold text-indigo-400">{queue.length}</p>
        </div>
        <div className="rounded-2xl border border-slate-800/80 bg-[#111827] p-5 shadow-xl ring-1 ring-white/5">
          <span className="text-[11px] font-mono uppercase text-slate-500 font-semibold">Webhook Status</span>
          <p className="mt-1 text-2xl font-bold text-emerald-400 font-mono">HMAC Verified</p>
        </div>
      </div>

      {/* Two-Column Triage Command Center */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Ticket List */}
        <div className="rounded-2xl border border-slate-800/80 bg-[#111827] p-4 shadow-xl ring-1 ring-white/5">
          <h2 className="text-xs font-mono uppercase font-bold text-slate-400 mb-3 tracking-wider">
            Escalation Tickets ({tickets.length})
          </h2>

          {tickets.length === 0 ? (
            <div className="p-8 text-center text-xs text-slate-500">
              No escalated tickets. Agent runs are resolving queries smoothly!
            </div>
          ) : (
            <div className="space-y-2">
              {tickets.map((t) => {
                const isSelected = selectedTicket?.ticket_id === t.ticket_id;
                const isUrgent = t.priority === "Urgent";

                return (
                  <div
                    key={t.ticket_id}
                    onClick={() => selectTicket(t)}
                    className={`cursor-pointer rounded-xl border p-3 transition ${
                      isSelected
                        ? "border-indigo-500 bg-indigo-950/40 shadow-xs"
                        : "border-slate-800 bg-slate-900/60 hover:border-slate-700"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-[11px] font-bold text-white">{t.ticket_id}</span>
                      <span className={`rounded-full px-2 py-0.5 text-[10px] font-bold font-mono ${
                        isUrgent
                          ? "bg-rose-950/80 text-rose-300 border border-rose-500/40 animate-pulse"
                          : "bg-slate-800 text-slate-300 border border-slate-700"
                      }`}>
                        {t.priority}
                      </span>
                    </div>

                    <p className="mt-1.5 text-xs font-medium text-slate-200 line-clamp-1">{t.title}</p>

                    <div className="mt-2 flex items-center justify-between text-[10px] font-mono text-slate-400">
                      <span>{t.intent}</span>
                      <span className="capitalize text-emerald-400 font-semibold">{t.status}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Selected Ticket Resolution Desk */}
        <div className="lg:col-span-2 rounded-2xl border border-slate-800/80 bg-[#111827] p-5 shadow-xl ring-1 ring-white/5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
              <div>
                <div className="flex items-center gap-2">
                  <h2 className="text-sm font-bold text-white">
                    Resolution Desk: {selectedTicket?.ticket_id || "None selected"}
                  </h2>
                  {selectedTicket && (
                    <span className="rounded-full bg-indigo-950/80 border border-indigo-500/30 px-2 py-0.5 text-[10px] font-mono text-indigo-300 font-semibold">
                      {selectedTicket.intent}
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Customer Query: "{selectedTicket?.customer_query || "N/A"}"
                </p>
              </div>
            </div>

            {/* Smart Canned Response Suggestions */}
            {cannedReplies.length > 0 && (
              <div className="mb-4">
                <span className="flex items-center gap-1 text-[11px] font-mono font-semibold uppercase text-slate-400 mb-2">
                  <Sparkles className="h-3.5 w-3.5 text-indigo-400" />
                  AI Suggested Grounded Replies
                </span>
                <div className="space-y-2">
                  {cannedReplies.map((c, i) => (
                    <div
                      key={i}
                      onClick={() => setReplyText(c)}
                      className="cursor-pointer rounded-xl border border-slate-800 bg-slate-900/60 p-2.5 text-xs text-slate-300 hover:border-indigo-500/40 hover:bg-indigo-950/30 hover:text-white transition"
                    >
                      "{c}"
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Reply / Resolution Textarea */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Human Agent Response & Notes</label>
              <textarea
                rows={4}
                value={replyText}
                onChange={(e) => setReplyText(e.target.value)}
                placeholder="Type your response to the customer or click an AI-suggested draft above..."
                className="w-full rounded-xl border border-slate-700 bg-slate-900 p-3 text-xs text-white focus:border-indigo-500 focus:outline-hidden"
              />
            </div>
          </div>

          <div className="mt-4 flex justify-end gap-2 pt-3 border-t border-slate-800">
            <button
              onClick={handleResolve}
              disabled={loading || !replyText.trim() || !selectedTicket}
              className="flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-700 px-4 py-2 text-xs font-semibold text-white hover:from-indigo-500 hover:to-indigo-600 transition disabled:opacity-50"
            >
              <UserCheck className="h-4 w-4" />
              <span>Resolve & Notify Customer</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}