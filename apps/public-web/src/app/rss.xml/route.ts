// Serves RSS on the site domain (/rss.xml) by proxying the backend public feed
// (backend GET /api/v1/public/rss.xml). Reuses the backend's feed generation so
// there is a single source of truth. Degrades to an empty valid feed on failure.
export const revalidate = 300;

const API_BASE = (process.env.XCRIPTO_API_URL ?? "http://localhost:8000").replace(/\/$/, "");

const EMPTY_FEED = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>XCripto News</title><description>XCripto public news feed</description></channel></rss>`;

export async function GET(): Promise<Response> {
  let xml = EMPTY_FEED;
  try {
    const res = await fetch(`${API_BASE}/api/v1/public/rss.xml`, { next: { revalidate } });
    if (res.ok) xml = await res.text();
  } catch {
    // keep empty feed
  }
  return new Response(xml, {
    headers: {
      "Content-Type": "application/rss+xml; charset=utf-8",
      "Cache-Control": "public, max-age=300, s-maxage=300",
    },
  });
}
