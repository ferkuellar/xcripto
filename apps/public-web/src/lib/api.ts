import "server-only";

import type { PublicArticle, PublicNews } from "./types";
import { SITE_URL } from "./site";

// Server-side client for the XMIP public API. All reads are unauthenticated
// (the /api/v1/public/* surface is public). Fetches degrade gracefully: list
// endpoints return [] on failure so pages render an empty state instead of 500.

const API_BASE = (process.env.XCRIPTO_API_URL ?? "http://localhost:8000").replace(/\/$/, "");

// Revalidate cached responses periodically so published news stays fresh
// without hammering the backend on every request.
const REVALIDATE_SECONDS = 60;

// Tell the backend our public host so it builds canonical/OG URLs for the public
// site (not the internal api origin). The backend also honours a PUBLIC_SITE_URL
// setting which, when set, takes precedence over this header.
const SITE_HOST = (() => {
  try {
    return new URL(SITE_URL).host;
  } catch {
    return "";
  }
})();

function baseHeaders(): Record<string, string> {
  const h: Record<string, string> = { Accept: "application/json" };
  if (SITE_HOST) h["X-Forwarded-Host"] = SITE_HOST;
  return h;
}

function apiUrl(path: string): string {
  return `${API_BASE}${path}`;
}

async function getJson<T>(path: string, fallback: T): Promise<T> {
  try {
    const res = await fetch(apiUrl(path), {
      next: { revalidate: REVALIDATE_SECONDS },
      headers: baseHeaders(),
    });
    if (!res.ok) return fallback;
    return (await res.json()) as T;
  } catch {
    return fallback;
  }
}

export interface ListParams {
  q?: string;
  category?: string;
  limit?: number;
  offset?: number;
}

function query(params: ListParams): string {
  const sp = new URLSearchParams();
  if (params.q) sp.set("q", params.q);
  if (params.category) sp.set("category", params.category);
  sp.set("limit", String(params.limit ?? 50));
  sp.set("offset", String(params.offset ?? 0));
  return sp.toString();
}

export function listNews(params: ListParams = {}): Promise<PublicNews[]> {
  return getJson<PublicNews[]>(`/api/v1/public/news?${query(params)}`, []);
}

export function searchNews(q: string, params: ListParams = {}): Promise<PublicNews[]> {
  const sp = new URLSearchParams({ q, limit: String(params.limit ?? 50), offset: String(params.offset ?? 0) });
  return getJson<PublicNews[]>(`/api/v1/public/search?${sp.toString()}`, []);
}

export function listCategories(): Promise<string[]> {
  return getJson<string[]>(`/api/v1/public/categories`, []);
}

// Article by slug. Returns null when the item is missing OR has no approved
// content piece (backend returns 404) — the article page renders notFound().
export async function getArticleBySlug(slug: string): Promise<PublicArticle | null> {
  try {
    const res = await fetch(apiUrl(`/api/v1/public/news/${encodeURIComponent(slug)}`), {
      next: { revalidate: REVALIDATE_SECONDS },
      headers: baseHeaders(),
    });
    if (!res.ok) return null;
    return (await res.json()) as PublicArticle;
  } catch {
    return null;
  }
}
