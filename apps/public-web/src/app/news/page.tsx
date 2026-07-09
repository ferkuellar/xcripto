import type { Metadata } from "next";
import { listNews } from "@/lib/api";
import { NewsCard } from "@/components/NewsCard";

export const revalidate = 60;

export const metadata: Metadata = {
  title: "Últimas noticias",
  description: "Cobertura editorial verificada de cripto: mercados, regulación y activos digitales.",
  alternates: { canonical: "/news" },
};

export default async function NewsListPage({
  searchParams,
}: {
  searchParams: { page?: string };
}) {
  const page = Math.max(1, Number(searchParams.page ?? "1") || 1);
  const limit = 24;
  const offset = (page - 1) * limit;
  const items = await listNews({ limit, offset });

  return (
    <div className="mx-auto max-w-content px-4 py-8 md:px-6">
      <header className="mb-8 border-b border-line pb-3">
        <h1 className="font-serif text-2xl font-bold text-ink">Últimas noticias</h1>
        <p className="mt-1 text-sm text-ink-muted">Cobertura verificada, ordenada por actualización.</p>
      </header>

      {items.length === 0 ? (
        <p className="border border-dashed border-line bg-paper-card p-10 text-center text-ink-muted">
          {page > 1 ? "No hay más noticias." : "Aún no hay noticias publicadas."}
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
          <a href={`/news?page=${page - 1}`} className="text-ink hover:text-accent">← Anteriores</a>
        ) : (
          <span />
        )}
        {items.length === limit && (
          <a href={`/news?page=${page + 1}`} className="text-ink hover:text-accent">Siguientes →</a>
        )}
      </nav>
    </div>
  );
}
