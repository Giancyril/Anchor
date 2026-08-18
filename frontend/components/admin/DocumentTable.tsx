"use client";

import React from "react";
import { DocumentMeta } from "@/lib/api";
import { FileText, ExternalLink, CheckCircle2, Layers } from "lucide-react";

interface DocumentTableProps {
  documents: DocumentMeta[];
  loading: boolean;
}

export function DocumentTable({ documents, loading }: DocumentTableProps) {
  if (loading) {
    return (
      <div className="p-8 text-center text-xs text-slate-400">
        Loading knowledge base documents...
      </div>
    );
  }

  if (documents.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-center">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-800 text-slate-400">
          <Layers className="h-6 w-6" />
        </div>
        <h3 className="mt-3 text-sm font-semibold text-slate-200">No documents ingested yet</h3>
        <p className="mt-1 text-xs text-slate-500 max-w-sm">
          Upload markdown, PDF, or text documentation to populate the Pinecone vector index for grounded RAG retrieval.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-xs">
        <thead className="border-b border-slate-800 bg-slate-900/60 font-mono text-[11px] uppercase tracking-wider text-slate-400">
          <tr>
            <th className="px-6 py-3">Document Name</th>
            <th className="px-6 py-3">Format</th>
            <th className="px-6 py-3">Category</th>
            <th className="px-6 py-3">Chunks</th>
            <th className="px-6 py-3">Status</th>
            <th className="px-6 py-3 text-right">Source Link</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800 text-slate-300">
          {documents.map((doc) => (
            <tr key={doc.source_id} className="hover:bg-slate-800/40 transition">
              <td className="px-6 py-3.5 font-medium text-white flex items-center gap-2">
                <FileText className="h-4 w-4 text-indigo-400 shrink-0" />
                <span>{doc.document_name}</span>
              </td>
              <td className="px-6 py-3.5 font-mono uppercase text-[11px] text-slate-400">
                {doc.format}
              </td>
              <td className="px-6 py-3.5">
                <span className="rounded-full border border-slate-700 bg-slate-800 px-2 py-0.5 text-[10px] font-medium text-slate-300">
                  {doc.category || "General"}
                </span>
              </td>
              <td className="px-6 py-3.5 font-mono text-slate-300">
                {doc.chunks_count} vectors
              </td>
              <td className="px-6 py-3.5">
                <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-400">
                  <CheckCircle2 className="h-3.5 w-3.5" /> Indexed
                </span>
              </td>
              <td className="px-6 py-3.5 text-right font-mono">
                {doc.url ? (
                  <a
                    href={doc.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-indigo-400 hover:text-indigo-300 hover:underline"
                  >
                    <span>View</span>
                    <ExternalLink className="h-3 w-3" />
                  </a>
                ) : (
                  <span className="text-slate-600">—</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}