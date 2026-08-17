"use client";

import React, { useState, useEffect } from "react";
import { Globe, RefreshCw, Plus, Play, GitCompare, CheckCircle2, Clock, Loader2, ArrowRight } from "lucide-react";

interface SyncJob {
  job_id: string;
  target_url: string;
  schedule: string;
  status: string;
  last_run?: number;
  last_status?: string;
  docs_updated: number;
}

export default function SyncPage() {
  const [jobs, setJobs] = useState<SyncJob[]>([]);
  const [newUrl, setNewUrl] = useState("https://docs.company.com/changelog");
  const [schedule, setSchedule] = useState("daily");
  const [loading, setLoading] = useState(false);
  const [crawling, setCrawling] = useState(false);
  const [crawlResult, setCrawlResult] = useState<any>(null);

  // Sample Diff State
  const [oldContent, setOldContent] = useState("Refund Window: 14 days for initial purchases.\nSupport: 48-hour email response.");
  const [newContent, setNewContent] = useState("Refund Window: 30 days for initial purchases.\nSupport: 24/7 priority live chat response.");
  const [diffResult, setDiffResult] = useState<string | null>(null);

  const fetchJobs = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/sync/jobs");
      if (res.ok) {
        setJobs(await res.json());
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const handleCreateJob = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newUrl.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/sync/jobs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target_url: newUrl, schedule }),
      });
      if (res.ok) {
        setNewUrl("");
        await fetchJobs();
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunJob = async (jobId: string) => {
    try {
      await fetch(`http://127.0.0.1:8000/api/v1/sync/jobs/${jobId}/run`, { method: "POST" });
      await fetchJobs();
    } catch (err) {
      console.error(err);
    }
  };

  const handleComputeDiff = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/sync/diff", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ old_content: oldContent, new_content: newContent }),
      });
      if (res.ok) {
        const data = await res.json();
        setDiffResult(data.unified_diff);
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-slate-900 sm:text-2xl">
            Automated Knowledge Base Sync & Diffs
          </h1>
          <p className="mt-1 text-xs text-slate-500">
            Configure automated URL scrapers, sitemap crawlers, and compute chunk-level document revisions.
          </p>
        </div>

        <button
          onClick={fetchJobs}
          className="flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-50 transition shadow-2xs"
        >
          <RefreshCw className="h-3.5 w-3.5" />
          <span>Refresh</span>
        </button>
      </div>

      {/* Two-Column Top Section: Create Sync Job & Diff Simulator */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Create Sync Job Card */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-3 mb-4">
            <Globe className="h-4 w-4 text-indigo-600" />
            <h2 className="text-sm font-bold text-slate-900">Schedule Auto-Sync Crawler</h2>
          </div>

          <form onSubmit={handleCreateJob} className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">Documentation URL or Sitemap</label>
              <input
                type="url"
                required
                value={newUrl}
                onChange={(e) => setNewUrl(e.target.value)}
                placeholder="https://docs.company.com/sitemap.xml"
                className="w-full rounded-xl border border-slate-200 px-3 py-2 text-xs text-slate-900 focus:border-indigo-500 focus:outline-hidden"
              />
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Sync Frequency</label>
                <select
                  value={schedule}
                  onChange={(e) => setSchedule(e.target.value)}
                  className="w-full rounded-xl border border-slate-200 px-3 py-2 text-xs text-slate-900 focus:border-indigo-500 focus:outline-hidden"
                >
                  <option value="hourly">Hourly</option>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                </select>
              </div>

              <div className="flex items-end">
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full flex items-center justify-center gap-1.5 rounded-xl bg-indigo-600 py-2 text-xs font-semibold text-white shadow-brand hover:bg-indigo-500 transition disabled:opacity-50"
                >
                  <Plus className="h-4 w-4" />
                  <span>Register Job</span>
                </button>
              </div>
            </div>
          </form>
        </div>

        {/* Semantic Diff Engine Card */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
            <div className="flex items-center gap-2">
              <GitCompare className="h-4 w-4 text-indigo-600" />
              <h2 className="text-sm font-bold text-slate-900">Document Chunk Diff Engine</h2>
            </div>
            <button
              onClick={handleComputeDiff}
              className="flex items-center gap-1 rounded-lg bg-slate-900 px-2.5 py-1 text-[11px] font-semibold text-white hover:bg-slate-800 transition"
            >
              <span>Compute Diff</span>
            </button>
          </div>

          <div className="grid grid-cols-2 gap-2 text-xs">
            <div>
              <span className="font-mono text-[10px] text-slate-400 block mb-1">Previous Document</span>
              <textarea
                rows={3}
                value={oldContent}
                onChange={(e) => setOldContent(e.target.value)}
                className="w-full rounded-xl border border-slate-200 p-2 font-mono text-[11px] text-slate-700 bg-slate-50 focus:outline-hidden"
              />
            </div>
            <div>
              <span className="font-mono text-[10px] text-indigo-600 block mb-1">Updated Document</span>
              <textarea
                rows={3}
                value={newContent}
                onChange={(e) => setNewContent(e.target.value)}
                className="w-full rounded-xl border border-indigo-200 p-2 font-mono text-[11px] text-slate-900 bg-indigo-50/20 focus:outline-hidden"
              />
            </div>
          </div>

          {diffResult && (
            <div className="mt-3 rounded-xl bg-slate-900 p-3 font-mono text-[11px] text-slate-200 overflow-x-auto">
              <pre>{diffResult}</pre>
            </div>
          )}
        </div>
      </div>

      {/* Sync Jobs Table */}
      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xs">
        <div className="border-b border-slate-100 px-6 py-4 flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-900">Active Sync Tasks ({jobs.length})</h2>
        </div>

        {jobs.length === 0 ? (
          <div className="p-8 text-center text-xs text-slate-400">
            No recurring sync jobs configured. Register a documentation URL above.
          </div>
        ) : (
          <table className="w-full text-left text-xs">
            <thead className="border-b border-slate-200 bg-slate-50/80 font-mono text-[11px] uppercase tracking-wider text-slate-500">
              <tr>
                <th className="px-6 py-3">Job ID</th>
                <th className="px-6 py-3">Target URL</th>
                <th className="px-6 py-3">Schedule</th>
                <th className="px-6 py-3">Status</th>
                <th className="px-6 py-3">Docs Updated</th>
                <th className="px-6 py-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {jobs.map((job) => (
                <tr key={job.job_id} className="hover:bg-slate-50/60 transition">
                  <td className="px-6 py-3.5 font-mono text-slate-500">{job.job_id}</td>
                  <td className="px-6 py-3.5 font-mono text-indigo-600 font-medium">{job.target_url}</td>
                  <td className="px-6 py-3.5 capitalize font-medium">{job.schedule}</td>
                  <td className="px-6 py-3.5">
                    <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-600">
                      <CheckCircle2 className="h-3 w-3" /> {job.status}
                    </span>
                  </td>
                  <td className="px-6 py-3.5 font-mono text-slate-700">{job.docs_updated} runs</td>
                  <td className="px-6 py-3.5 text-right">
                    <button
                      onClick={() => handleRunJob(job.job_id)}
                      className="inline-flex items-center gap-1 rounded-lg bg-indigo-50 border border-indigo-200 px-2.5 py-1 text-[11px] font-semibold text-indigo-700 hover:bg-indigo-100 transition"
                    >
                      <Play className="h-3 w-3 fill-indigo-700" />
                      <span>Sync Now</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}