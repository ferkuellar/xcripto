import Link from "next/link";
import { listNews } from "@/lib/api";
import { NewsCard } from "@/components/NewsCard";
import { JsonLd } from "@/components/JsonLd";
import { itemListJsonLd } from "@/lib/jsonld";
import { SITE_TAGLINE } from "@/lib/site";

// Homepage revalidates so newly published news appears without a redeploy.
export const revalidate = 60;

export default async function HomePage() {
  const items = await listNews({ limit: 13 });
  const [lead, ...rest] = items;

  return (
    <div className="mx-auto max-w-content px-4 py-8 md:px-6">
      {items.length > 0 && <JsonLd data={itemListJsonLd(items)} />}

      <div className="mb-8 flex items-baseline justify-between border-b border-line pb-3">
        <h1 className="font-serif text-xl font-bold text-ink">Portada</h1>
        <p className="text-xs uppercase tracking-[0.14em] text-ink-muted">{SITE_TAGLINE}</p>
      </div>

      {items.length === 0 ? (
        <EmptyState />
      ) : (
        <div className="grid gap-8 lg:grid-cols-3">
          <div className="lg:col-span-2">{lead && <NewsCard item={lead} priority />}</div>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-1">
            {rest.slice(0, 4).map((item) => (
              <NewsCard key={item.id} item={item} />
            ))}
          </div>
          {rest.length > 4 && (
            <div className="lg:col-span-3">
              <h2 className="mb-4 mt-4 border-b border-line pb-2 font-serif text-lg font-semibold text-ink">
                Más noticias
              </h2>
              <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
                {rest.slice(4).map((item) => (
                  <NewsCard key={item.id} item={item} />
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      <div className="mt-10 text-center">
        <Link
          href="/news"
          className="inline-block border border-ink px-5 py-2 text-sm font-medium text-ink hover:border-accent hover:text-accent"
        >
          Ver todas las noticias
        </Link>
      </div>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="border border-dashed border-line bg-paper-card p-10 text-center">
      <p className="font-serif text-lg text-ink">Aún no hay noticias publicadas</p>
      <p className="mt-2 text-sm text-ink-muted">
        La redacción publicará cobertura verificada en breve. Vuelve pronto.
      </p>
    </div>
  );
}
