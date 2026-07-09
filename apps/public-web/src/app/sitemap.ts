import type { MetadataRoute } from "next";
import { listNews, listCategories } from "@/lib/api";
import { SITE_URL, categorySlug } from "@/lib/site";

export const revalidate = 300;

// Site-domain sitemap built from the real public news + categories.
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const [news, categories] = await Promise.all([listNews({ limit: 200 }), listCategories()]);

  const staticRoutes: MetadataRoute.Sitemap = [
    { url: `${SITE_URL}/`, changeFrequency: "hourly", priority: 1 },
    { url: `${SITE_URL}/news`, changeFrequency: "hourly", priority: 0.9 },
    { url: `${SITE_URL}/categorias`, changeFrequency: "weekly", priority: 0.4 },
    { url: `${SITE_URL}/acerca`, changeFrequency: "yearly", priority: 0.2 },
  ];

  const categoryRoutes: MetadataRoute.Sitemap = categories.map((cat) => ({
    url: `${SITE_URL}/categoria/${categorySlug(cat)}`,
    changeFrequency: "daily",
    priority: 0.5,
  }));

  const articleRoutes: MetadataRoute.Sitemap = news.map((item) => ({
    url: item.canonical_url || `${SITE_URL}/news/${item.slug}`,
    lastModified: item.updated_at || item.published_at || undefined,
    changeFrequency: "weekly",
    priority: 0.7,
  }));

  return [...staticRoutes, ...categoryRoutes, ...articleRoutes];
}
