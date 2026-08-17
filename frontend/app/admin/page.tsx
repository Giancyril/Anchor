"use client";

import React, { useState, useEffect } from "react";
import { listDocuments, DocumentMeta } from "@/lib/api";
import { DocumentTable } from "@/components/admin/DocumentTable";
import { UploadModal } from "@/components/admin/UploadModal";
import { Database, Plus, RefreshCw, Layers, ShieldCheck, Cpu } from "lucide-react";

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
          <h1 className="text-xl font-bold tracking-tight text-slate-900 sm:text-2xl">
            Knowledge Base Management
          </h1>
          <p className="mt-1 text-xs text-slate-500">
            Ingest, chunk, and embed company documentation into the Pinecone serverless vector index.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={fetchDocs}
            className="flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-50 transition shadow-2xs"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${loading ? "animate-spin" : ""}`} />
            <span>Refresh</span>
          </button>
          <button
            onClick={() => setIsUploadOpen(true)}
            className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3.5 py-1.5 text-xs font-semibold text-white shadow-brand hover:bg-indigo-500 active:scale-95 transition"
          >
            <Plus className="h-3.5 w-3.5" />
            <span>Ingest Document</span>
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <span className="text-[11px] font-mono uppercase text-slate-400">Total Indexed Documents</span>
          <p className="mt-1 text-2xl font-bold text-slate-900">{documents.length}</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <span className="text-[11px] font-mono uppercase text-slate-400">Total Vector Chunks</span>
          <p className="mt-1 text-2xl font-bold text-slate-900">{totalChunks}</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <span className="text-[11px] font-mono uppercase text-slate-400">Embedding Dimension</span>
          <p className="mt-1 text-2xl font-bold text-slate-900 font-mono">1,536-dim</p>
        </div>
      </div>

      {/* Table Container */}
      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xs">
        <div className="border-b border-slate-100 px-6 py-4">
          <h2 className="text-sm font-semibold text-slate-900">Ingested Sources</h2>
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