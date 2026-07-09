import type { Metadata } from "next";
import { searchNews } from "@/lib/api";
import { NewsCard } from "@/components/NewsCard";
import { SearchForm } from "@/components/SearchForm";

export const revalidate = 30;

export const metadata: Metadata = {
  title: "Buscar",
  description: "Busca noticias en XCripto.",
  alternates: { canonical: "/buscar" },
  robots: { index: false, follow: true },
};

export default async function SearchPage({ searchParams }: { searchParams: { q?: string } }) {
  const q = (searchParams.q ?? "").trim();
  const results = q ? await searchNews(q, { limit: 30 }) : [];

  return (
    <div className="mx-auto max-w-content px-4 py-8 md:px-6">
      <header className="mb-6 border-b border-line pb-4">
        <h1 className="mb-3 font-serif text-2xl font-bold text-ink">Buscar</h1>
        <div className="max-w-lg">
          <SearchForm defaultValue={q} />
        </div>
      </header>

      {!q ? (
        <p className="text-ink-muted">Escribe un término para buscar noticias.</p>
      ) : results.length === 0 ? (
        <p className="border border-dashed border-line bg-paper-card p-10 text-center text-ink-muted">
          Sin resultados para <span className="font-medium text-ink">“{q}”</span>.
        </p>
      ) : (
        <>
          <p className="mb-6 text-sm text-ink-muted">
            {results.length} resultado{results.length === 1 ? "" : "s"} para{" "}
            <span className="font-medium text-ink">“{q}”</span>
          </p>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {results.map((item) => (
              <NewsCard key={item.id} item={item} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
