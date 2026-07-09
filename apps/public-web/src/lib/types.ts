// Mirror of the backend public contract (backend/app/schemas/public_news.py).
// Consume real fields only — do not invent.

export interface PublicNews {
  id: string;
  slug: string;
  title: string;
  summary: string;
  category: string;
  source_name: string;
  source_url: string;
  status: string;
  author: string | null;
  published_at: string | null;
  created_at: string;
  updated_at: string;
  cover_image_url: string | null;
  tags: string[];
  canonical_url: string;
  seo_title: string;
  seo_description: string;
  og_title: string;
  og_description: string;
  og_image: string | null;
  json_ld_type: string; // "NewsArticle"
}

export interface PublicArticle extends PublicNews {
  body: string;
  body_format: "markdown" | "html" | "plain";
}
