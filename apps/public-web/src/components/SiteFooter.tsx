import Link from "next/link";
import { SITE_NAME, SITE_DESCRIPTION } from "@/lib/site";

export function SiteFooter() {
  const year = new Date().getFullYear();
  return (
    <footer className="mt-16 border-t border-line bg-paper-card">
      <div className="mx-auto max-w-content px-4 py-10 md:px-6">
        <div className="flex flex-col gap-6 md:flex-row md:items-start md:justify-between">
          <div className="max-w-sm">
            <p className="font-serif text-xl font-bold text-ink">{SITE_NAME}</p>
            <p className="mt-2 text-sm text-ink-muted">{SITE_DESCRIPTION}</p>
          </div>
          <nav aria-label="Pie" className="flex flex-col gap-2 text-sm">
            <Link href="/news" className="text-ink-soft hover:text-accent">Últimas noticias</Link>
            <Link href="/categorias" className="text-ink-soft hover:text-accent">Categorías</Link>
            <Link href="/buscar" className="text-ink-soft hover:text-accent">Buscar</Link>
            <Link href="/acerca" className="text-ink-soft hover:text-accent">Acerca de</Link>
            <a href="/rss.xml" className="text-ink-soft hover:text-accent">RSS</a>
          </nav>
        </div>
        <p className="mt-8 border-t border-line pt-6 text-xs text-ink-muted">
          © {year} {SITE_NAME}. Cobertura editorial verificada. Esto no es asesoría financiera.
        </p>
      </div>
    </footer>
  );
}
