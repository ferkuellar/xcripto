import type { Metadata } from "next";
import { listNews } from "@/lib/api";
import { NewsCard } from "@/components/NewsCard";
import { SITE_NAME } from "@/lib/site";

export const revalidate = 60;

function decode(param: string): string {
  try {
    return decodeURIComponent(param);
  } catch {
    return param;
  }
}

export async function generateMetadata({ params }: { params: { category: string } }): Promise<Metadata> {
  const category = decode(params.category);
  return {
    title: `${category} — Noticias`,
    description: `Últimas noticias de ${category} en ${SITE_NAME}.`,
    alternates: { canonical: `/categoria/${params.category}` },
  };
}

export default async function CategoryPage({
  params,
  searchParams,
}: {
  params: { category: string };
  searchParams: { page?: string };
}) {
  const category = decode(params.category);
  const page = Math.max(1, Number(searchParams.page ?? "1") || 1);
  const limit = 24;
  const offset = (page - 1) * limit;
  const items = await listNews({ category, limit, offset });

  return (
    <div className="mx-auto max-w-content px-4 py-8 md:px-6">
      <header className="mb-8 border-b border-line pb-3">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-accent">Categoría</p>
        <h1 className="font-serif text-2xl font-bold capitalize text-ink">{category}</h1>
      </header>

      {items.length === 0 ? (
        <p className="border border-dashed border-line bg-paper-card p-10 text-center text-ink-muted">
          No hay noticias en esta categoría todavía.
        </p>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {items.map((item) => (
            <NewsCard key={item.id} item={item} />
          ))}
        </div>
      )}

      <nav className="mt-10 flex items-center justify-between text-sm" aria-label="Paginación">
        {page > 1 ? (
          <a href={`/categoria/${params.category}?page=${page - 1}`} className="text-ink hover:text-accent">← Anteriores</a>
        ) : (
          <span />
        )}
        {items.length === limit && (
          <a href={`/categoria/${params.category}?page=${page + 1}`} className="text-ink hover:text-accent">Siguientes →</a>
        )}
      </nav>
    </div>
  );
}
