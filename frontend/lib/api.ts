const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8000/api/v1";

export interface CitationSource {
  citation_index: number;
  document_name: string;
  section: string;
  url?: string;
  snippet: string;
}

export interface ChatResponse {
  answer: string;
  confidence: "high" | "low";
  escalated: boolean;
  sources: CitationSource[];
  session_id?: string;
}

export interface DocumentMeta {
  source_id: string;
  document_name: string;
  chunks_count: number;
  format: string;
  category?: string;
  url?: string;
}

export async function sendMessage(
  question: string,
  sessionId?: string,
  filters?: { category?: string }
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, session_id: sessionId, filters }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? "Chat request failed");
  }
  return res.json();
}

export async function listDocuments(): Promise<{ documents: DocumentMeta[]; total: number }> {
  const res = await fetch(`${API_BASE}/documents`);
  if (!res.ok) throw new Error("Failed to fetch documents");
  return res.json();
}

export async function ingestDocument(
  file: File,
  meta: { documentName?: string; url?: string; category?: string }
): Promise<{ status: string; document_id: string; chunks_created: number }> {
  const form = new FormData();
  form.append("file", file);
  if (meta.documentName) form.append("document_name", meta.documentName);
  if (meta.url) form.append("url", meta.url);
  if (meta.category) form.append("category", meta.category);
  const res = await fetch(`${API_BASE}/ingest`, { method: "POST", body: form });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? "Ingestion failed");
  }
  return res.json();
}