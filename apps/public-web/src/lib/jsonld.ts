import type { PublicArticle, PublicNews } from "./types";
import { SITE_NAME, SITE_URL } from "./site";

// JSON-LD for an article page. Uses the backend-provided json_ld_type
// (defaults to "NewsArticle") and canonical_url. Omits image when null.
export function articleJsonLd(article: PublicArticle): Record<string, unknown> {
  const jsonLd: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": article.json_ld_type || "NewsArticle",
    headline: article.title,
    description: article.seo_description || article.summary,
    articleSection: article.category,
    mainEntityOfPage: { "@type": "WebPage", "@id": article.canonical_url },
    url: article.canonical_url,
    datePublished: article.published_at ?? article.created_at,
    dateModified: article.updated_at,
    author: { "@type": "Person", name: article.author || SITE_NAME },
    publisher: {
      "@type": "Organization",
      name: SITE_NAME,
      url: SITE_URL,
    },
    isBasedOn: article.source_url || undefined,
  };
  if (article.og_image || article.cover_image_url) {
    jsonLd.image = [article.og_image || article.cover_image_url];
  }
  return jsonLd;
}

// JSON-LD ItemList for the homepage / list — helps news discovery.
export function itemListJsonLd(items: PublicNews[]): Record<string, unknown> {
  return {
    "@context": "https://schema.org",
    "@type": "ItemList",
    itemListElement: items.slice(0, 20).map((item, i) => ({
      "@type": "ListItem",
      position: i + 1,
      url: item.canonical_url,
      name: item.title,
    })),
  };
}
