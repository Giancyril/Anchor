"use client";

import React, { useState } from "react";
import { ingestDocument } from "@/lib/api";
import { Upload, X, Loader2, AlertCircle } from "lucide-react";
import { CustomSelect } from "@/components/ui/CustomSelect";

interface UploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

const CATEGORY_OPTIONS = [
  { value: "General", label: "General" },
  { value: "Billing", label: "Billing" },
  { value: "Security", label: "Security" },
  { value: "Integrations", label: "Integrations" },
  { value: "Pricing", label: "Pricing" },
];

export function UploadModal({ isOpen, onClose, onSuccess }: UploadModalProps) {
  const [file, setFile] = useState<File | null>(null);
  const [docName, setDocName] = useState("");
  const [category, setCategory] = useState("General");
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);
    try {
      await ingestDocument(file, {
        documentName: docName || file.name,
        category,
        url,
      });
      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.message || "Failed to ingest document");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-xs p-4 animate-fade-in">
      <div className="relative w-full max-w-md rounded-2xl border border-slate-800 bg-[#111827] p-6 shadow-2xl ring-1 ring-white/10">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h2 className="text-sm font-semibold text-white">Ingest Knowledge Document</h2>
          <button onClick={onClose} className="rounded-lg p-1 text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition">
            <X className="h-4 w-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="mt-4 space-y-3.5">
          {error && (
            <div className="flex items-center gap-2 rounded-lg border border-rose-500/30 bg-rose-950/40 p-2.5 text-xs text-rose-300">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* File Picker */}
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Document File (.md, .pdf, .txt, .html)</label>
            <input
              type="file"
              accept=".md,.pdf,.txt,.html,.htm"
              required
              onChange={(e) => {
                const f = e.target.files?.[0];
                if (f) {
                  setFile(f);
                  if (!docName) setDocName(f.name.replace(/\.[^/.]+$/, ""));
                }
              }}
              className="w-full text-xs text-slate-400 file:mr-3 file:rounded-lg file:border-0 file:bg-indigo-950 file:px-3 file:py-1.5 file:text-xs file:font-semibold file:text-indigo-300 hover:file:bg-indigo-900 transition"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Document Title</label>
            <input
              type="text"
              value={docName}
              onChange={(e) => setDocName(e.target.value)}
              placeholder="e.g. Billing and Refund Policy"
              required
              className="w-full rounded-xl border border-slate-700 bg-slate-900 px-3 py-2 text-xs text-white focus:border-indigo-500 focus:outline-hidden transition"
            />
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Category</label>
              <CustomSelect
                options={CATEGORY_OPTIONS}
                value={category}
                onChange={setCategory}
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Source URL (Optional)</label>
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://docs.company.com/..."
                className="w-full rounded-xl border border-slate-700 bg-slate-900 px-3 py-2 text-xs text-white focus:border-indigo-500 focus:outline-hidden transition"
              />
            </div>
          </div>

          <div className="mt-5 flex justify-end gap-2 pt-2 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="rounded-xl border border-slate-700 px-3 py-1.5 text-xs font-medium text-slate-300 hover:bg-slate-800 hover:text-white transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || !file}
              className="flex items-center gap-1.5 rounded-xl bg-indigo-600 px-4 py-1.5 text-xs font-semibold text-white hover:bg-indigo-500 disabled:opacity-50 transition"
            >
              {loading ? (
                <>
                  <Loader2 className="h-3.5 w-3.5 animate-spin" />
                  <span>Embedding Chunks...</span>
                </>
              ) : (
                <>
                  <Upload className="h-3.5 w-3.5" />
                  <span>Ingest & Upsert</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}