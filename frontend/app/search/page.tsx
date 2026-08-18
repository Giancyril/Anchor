"use client";

import React, { useState } from "react";
import { Search, Sparkles, Loader2 } from "lucide-react";

interface SearchResult {
  document_name: string;
  section: string;
  url?: string;
  content: string;
  final_score: number;
  breakdown: {
    dense_rank?: number;
    dense_score?: number;
    sparse_rank?: number;
    sparse_score?: number;
    rrf_score?: number;
    reranked_score?: number;
  };
}

export default function HybridSearchPage() {
  const [query, setQuery] = useState("refund policy for annual billing plans");
  const [alpha, setAlpha] = useState(0.5);
  const [enableRerank, setEnableRerank] = useState(true);
  const [decompose, setDecompose] = useState(false);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [subQueries, setSubQueries] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/search/hybrid", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          alpha,
          top_k: 4,
          enable_rerank: enableRerank,
          decompose,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setResults(data.results);
        setSubQueries(data.sub_queries || [query]);
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
            Hybrid Retrieval Inspector
          </h1>
          <p className="mt-1 text-xs text-slate-400">
            Simulate and inspect Reciprocal Rank Fusion (RRF) combining dense Pinecone vectors and sparse BM25 keyword matching.
          </p>
        </div>
      </div>

      {/* Query & Controls Card */}
      <div className="rounded-2xl border border-slate-800/80 bg-[#111827] p-5 shadow-xl ring-1 ring-white/5">
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="flex items-center gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search error codes, product SKUs, or procedural questions..."
                className="w-full rounded-xl border border-slate-700 bg-slate-900 pl-9 pr-4 py-2.5 text-xs text-white placeholder:text-slate-500 focus:border-indigo-500 focus:outline-hidden"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-700 px-4 py-2.5 text-xs font-semibold text-white shadow-md shadow-indigo-600/30 hover:from-indigo-500 hover:to-indigo-600 transition disabled:opacity-50"
            >
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
              <span>Execute Fusion</span>
            </button>
          </div>

          {/* Sliders & Parameters */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 border-t border-slate-800 pt-3">
            <div>
              <div className="flex justify-between text-xs font-medium text-slate-300 mb-1">
                <span>Dense vs. Sparse Balance (α)</span>
                <span className="font-mono text-indigo-400 font-bold">{alpha.toFixed(2)}</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={alpha}
                onChange={(e) => setAlpha(parseFloat(e.target.value))}
                className="w-full accent-indigo-500"
              />
              <div className="flex justify-between text-[10px] text-slate-500 font-mono mt-0.5">
                <span>0.0 (100% BM25)</span>
                <span>0.5 (Balanced)</span>
                <span>1.0 (100% Vector)</span>
              </div>
            </div>

            <div className="flex items-center justify-between sm:justify-center gap-4">
              <label className="flex items-center gap-2 text-xs font-medium text-slate-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={enableRerank}
                  onChange={(e) => setEnableRerank(e.target.checked)}
                  className="rounded border-slate-700 bg-slate-900 text-indigo-600 focus:ring-indigo-500"
                />
                <span>Cross-Encoder Reranker</span>
              </label>
            </div>

            <div className="flex items-center justify-between sm:justify-center gap-4">
              <label className="flex items-center gap-2 text-xs font-medium text-slate-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={decompose}
                  onChange={(e) => setDecompose(e.target.checked)}
                  className="rounded border-slate-700 bg-slate-900 text-indigo-600 focus:ring-indigo-500"
                />
                <span>Multi-Query Expansion</span>
              </label>
            </div>
          </div>
        </form>
      </div>

      {/* Sub-Queries Badge List */}
      {subQueries.length > 1 && (
        <div className="flex items-center gap-2 flex-wrap text-xs">
          <span className="font-mono text-[10px] uppercase text-slate-500 font-semibold">Decomposed Sub-Queries:</span>
          {subQueries.map((sq, i) => (
            <span key={i} className="rounded-full border border-indigo-500/30 bg-indigo-950/50 px-2.5 py-0.5 text-[11px] font-mono text-indigo-300">
              {sq}
            </span>
          ))}
        </div>
      )}

      {/* Results List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {results.map((res, idx) => (
          <div key={idx} className="rounded-2xl border border-slate-800/80 bg-[#111827] p-5 shadow-xl ring-1 ring-white/5 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="flex h-5 w-5 items-center justify-center rounded-full bg-indigo-950 border border-indigo-500/30 font-mono text-[10px] font-bold text-indigo-300">
                    #{idx + 1}
                  </span>
                  <h3 className="text-xs font-bold text-white">{res.document_name}</h3>
                </div>
                <span className="rounded-full border border-emerald-500/30 bg-emerald-950/60 px-2 py-0.5 font-mono text-[10px] font-semibold text-emerald-400">
                  Score: {res.final_score}
                </span>
              </div>

              <p className="mt-1 font-mono text-[11px] text-indigo-400">§ {res.section}</p>
              <p className="mt-2 text-xs text-slate-300 leading-relaxed bg-slate-900/80 p-2.5 rounded-xl border border-slate-800 line-clamp-4">
                "{res.content}"
              </p>
            </div>

            {/* Score Breakdown Footer */}
            <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-[10px] font-mono text-slate-400">
              {res.breakdown.dense_rank !== undefined && (
                <span>Dense: #{res.breakdown.dense_rank}</span>
              )}
              {res.breakdown.sparse_rank !== undefined && (
                <span>Sparse: #{res.breakdown.sparse_rank}</span>
              )}
              {res.breakdown.rrf_score !== undefined && (
                <span>RRF: {res.breakdown.rrf_score.toFixed(4)}</span>
              )}
              {res.breakdown.reranked_score !== undefined && (
                <span className="font-semibold text-indigo-400">Logit: {res.breakdown.reranked_score}</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}