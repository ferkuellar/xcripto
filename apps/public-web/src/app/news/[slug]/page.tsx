import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getArticleBySlug } from "@/lib/api";
import { ArticleBody } from "@/components/ArticleBody";
import { CoverImage } from "@/components/CoverImage";
import { JsonLd } from "@/components/JsonLd";
import { articleJsonLd } from "@/lib/jsonld";
import { formatDate, categorySlug, authorSlug } from "@/lib/site";

export const revalidate = 60;

// Per-article SEO from the backend-provided fields.
export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const article = await getArticleBySlug(params.slug);
  if (!article) return { title: "Artículo no encontrado", robots: { index: false, follow: false } };

  const images = article.og_image ? [{ url: article.og_image }] : undefined;
  return {
    title: article.seo_title || article.title,
    description: article.seo_description || article.summary,
    alternates: { canonical: article.canonical_url },
    openGraph: {
      type: "article",
      title: article.og_title || article.title,
      description: article.og_description || article.summary,
      url: article.canonical_url,
      publishedTime: article.published_at ?? undefined,
      modifiedTime: article.updated_at,
      section: article.category,
      authors: article.author ? [article.author] : undefined,
      images,
    },
    twitter: {
      card: images ? "summary_large_image" : "summary",
      title: article.og_title || article.title,
      description: article.og_description || article.summary,
    },
  };
}

export default async function ArticlePage({ params }: { params: { slug: string } }) {
  const article = await getArticleBySlug(params.slug);
  if (!article) notFound();

  const dateStr = article.published_at ?? article.created_at;

  return (
    <article className="mx-auto max-w-content px-4 py-8 md:px-6">
      <JsonLd data={articleJsonLd(article)} />

      <div className="mx-auto max-w-prose">
        <nav className="mb-4 text-sm" aria-label="Ruta">
          <Link href="/news" className="text-ink-muted hover:text-accent">Noticias</Link>
          <span className="mx-2 text-ink-muted" aria-hidden>/</span>
          <Link href={`/categoria/${categorySlug(article.category)}`} className="text-accent hover:underline">
            {article.category}
          </Link>
        </nav>

        <h1 className="font-serif text-3xl font-bold leading-tight text-ink md:text-4xl">
          {article.title}
        </h1>
        <p className="mt-3 text-lg text-ink-soft">{article.summary}</p>

        <div className="mt-4 flex flex-wrap items-center gap-x-3 gap-y-1 border-y border-line py-3 text-sm text-ink-muted">
          {article.author && (
            <Link href={`/autor/${authorSlug(article.author)}`} className="font-medium text-ink hover:text-accent">
              {article.author}
            </Link>
          )}
          {article.author && dateStr && <span aria-hidden>·</span>}
          {dateStr && <time dateTime={dateStr}>{formatDate(dateStr)}</time>}
        </div>
      </div>

      <div className="mx-auto mt-6 max-w-content">
        <CoverImage src={article.cover_image_url} category={article.category} title={article.title} size="hero" />
      </div>

      <div className="mx-auto mt-8 max-w-prose">
        <ArticleBody article={article} />

        <footer className="mt-10 border-t border-line pt-6 text-sm text-ink-muted">
          <p>
            Fuente:{" "}
            <a href={article.source_url} rel="nofollow noopener noreferrer" target="_blank" className="text-accent hover:underline">
              {article.source_name}
            </a>
          </p>
          <p className="mt-2 text-xs">
            Cobertura editorial de XCripto. Esto no constituye asesoría financiera.
          </p>
        </footer>
      </div>
    </article>
  );
}
