"use client";

import React, { useState, useEffect } from "react";
import { listDocuments, DocumentMeta } from "@/lib/api";
import { DocumentTable } from "@/components/admin/DocumentTable";
import { UploadModal } from "@/components/admin/UploadModal";
import { Database, Plus, RefreshCw, Layers } from "lucide-react";

export default function AdminPage() {
  const [documents, setDocuments] = useState<DocumentMeta[]>([]);
  const [loading, setLoading] = useState(true);
  const [isUploadOpen, setIsUploadOpen] = useState(false);

  const fetchDocs = async () => {
    setLoading(true);
    try {
      const data = await listDocuments();
      setDocuments(data.documents);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocs();
  }, []);

  const totalChunks = documents.reduce((acc, d) => acc + d.chunks_count, 0);

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-white sm:text-2xl">
            Knowledge Base Management
          </h1>
          <p className="mt-1 text-xs text-slate-400">
            Ingest, chunk, and embed company documentation into the Pinecone serverless vector index.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={fetchDocs}
            className="flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-800/80 px-3 py-1.5 text-xs font-medium text-slate-300 hover:bg-slate-700 hover:text-white transition shadow-sm"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${loading ? "animate-spin" : ""}`} />
            <span>Refresh</span>
          </button>
          <button
            onClick={() => setIsUploadOpen(true)}
            className="flex items-center gap-1.5 rounded-lg bg-gradient-to-r from-indigo-600 to-indigo-700 px-3.5 py-1.5 text-xs font-semibold text-white shadow-md shadow-indigo-600/30 hover:from-indigo-500 hover:to-indigo-600 active:scale-95 transition"
          >
            <Plus className="h-3.5 w-3.5" />
            <span>Ingest Document</span>
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="rounded-2xl border border-slate-800/80 bg-[#111827] p-5 shadow-lg ring-1 ring-white/5">
          <span className="text-[11px] font-mono uppercase text-slate-500 font-semibold">Total Indexed Documents</span>
          <p className="mt-1 text-2xl font-bold text-white">{documents.length}</p>
        </div>
        <div className="rounded-2xl border border-slate-800/80 bg-[#111827] p-5 shadow-lg ring-1 ring-white/5">
          <span className="text-[11px] font-mono uppercase text-slate-500 font-semibold">Total Vector Chunks</span>
          <p className="mt-1 text-2xl font-bold text-white">{totalChunks}</p>
        </div>
        <div className="rounded-2xl border border-slate-800/80 bg-[#111827] p-5 shadow-lg ring-1 ring-white/5">
          <span className="text-[11px] font-mono uppercase text-slate-500 font-semibold">Embedding Dimension</span>
          <p className="mt-1 text-2xl font-bold text-indigo-400 font-mono">1,536-dim</p>
        </div>
      </div>

      {/* Table Container */}
      <div className="overflow-hidden rounded-2xl border border-slate-800/80 bg-[#111827] shadow-lg ring-1 ring-white/5">
        <div className="border-b border-slate-800/80 px-6 py-4">
          <h2 className="text-sm font-bold text-white">Ingested Sources</h2>
        </div>
        <DocumentTable documents={documents} loading={loading} />
      </div>

      {/* Upload Modal */}
      <UploadModal
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
        onSuccess={fetchDocs}
      />
    </div>
  );
}