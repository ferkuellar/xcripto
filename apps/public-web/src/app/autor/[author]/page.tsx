import type { Metadata } from "next";
import { listNews } from "@/lib/api";
import { NewsCard } from "@/components/NewsCard";
import { authorSlug, SITE_NAME } from "@/lib/site";

export const revalidate = 120;

// FALLBACK author page: the backend has no author endpoint yet (author is a
// derived field: publication owner → content owner → source name). We fetch a
// recent window and filter by author-slug match. Marked noindex until a real
// author contract exists. See docs/016-public-web gap report.
export async function generateMetadata({ params }: { params: { author: string } }): Promise<Metadata> {
  const author = decodeURIComponent(params.author).replace(/-/g, " ");
  return {
    title: `${author} — Autor`,
    description: `Notas de ${author} en ${SITE_NAME}.`,
    alternates: { canonical: `/autor/${params.author}` },
    robots: { index: false, follow: true },
  };
}

export default async function AuthorPage({ params }: { params: { author: string } }) {
  const slug = params.author;
  const recent = await listNews({ limit: 100 });
  const items = recent.filter((n) => n.author && authorSlug(n.author) === slug);
  const displayName = items[0]?.author ?? decodeURIComponent(slug).replace(/-/g, " ");

  return (
    <div className="mx-auto max-w-content px-4 py-8 md:px-6">
      <header className="mb-8 border-b border-line pb-3">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-accent">Autor</p>
        <h1 className="font-serif text-2xl font-bold capitalize text-ink">{displayName}</h1>
      </header>

      {items.length === 0 ? (
        <p className="border border-dashed border-line bg-paper-card p-10 text-center text-ink-muted">
          No hay notas recientes atribuidas a este autor.
        </p>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {items.map((item) => (
            <NewsCard key={item.id} item={item} />
          ))}
        </div>
      )}
    </div>
  );
}
