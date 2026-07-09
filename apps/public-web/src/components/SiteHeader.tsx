import Link from "next/link";
import { SITE_NAME, SITE_TAGLINE, categorySlug } from "@/lib/site";
import { SearchForm } from "./SearchForm";

// Editorial masthead. Categories come from the real backend catalog.
export function SiteHeader({ categories }: { categories: string[] }) {
  const nav = categories.slice(0, 6);
  return (
    <header className="border-b border-line bg-paper-card">
      <div className="mx-auto flex max-w-content flex-col gap-3 px-4 py-4 md:px-6">
        <div className="flex items-center justify-between gap-4">
          <Link href="/" className="group flex flex-col leading-none">
            <span className="font-serif text-2xl font-bold tracking-tight text-ink md:text-3xl">
              {SITE_NAME}
            </span>
            <span className="mt-1 text-[11px] uppercase tracking-[0.18em] text-ink-muted">
              {SITE_TAGLINE}
            </span>
          </Link>
          <div className="hidden w-full max-w-xs md:block">
            <SearchForm />
          </div>
        </div>
        <nav aria-label="Categorías" className="flex flex-wrap items-center gap-x-5 gap-y-2 border-t border-line pt-3">
          <Link href="/news" className="text-sm font-medium text-ink hover:text-accent">
            Últimas
          </Link>
          {nav.map((cat) => (
            <Link
              key={cat}
              href={`/categoria/${categorySlug(cat)}`}
              className="text-sm text-ink-soft capitalize hover:text-accent"
            >
              {cat}
            </Link>
          ))}
          <Link href="/categorias" className="text-sm text-ink-muted hover:text-accent">
            Todas
          </Link>
          <Link href="/acerca" className="ml-auto text-sm text-ink-muted hover:text-accent">
            Acerca de
          </Link>
        </nav>
        <div className="md:hidden">
          <SearchForm />
        </div>
      </div>
    </header>
  );
}
