import Link from "next/link";

export default function NotFound() {
  return (
    <div className="mx-auto flex max-w-prose flex-col items-center px-4 py-20 text-center md:px-6">
      <p className="font-serif text-5xl font-bold text-ink">404</p>
      <h1 className="mt-4 font-serif text-2xl font-semibold text-ink">Página no encontrada</h1>
      <p className="mt-2 text-ink-muted">
        La nota que buscas no existe o aún no ha sido publicada.
      </p>
      <div className="mt-8 flex gap-3">
        <Link href="/" className="border border-ink px-5 py-2 text-sm font-medium text-ink hover:border-accent hover:text-accent">
          Ir a portada
        </Link>
        <Link href="/news" className="border border-line px-5 py-2 text-sm font-medium text-ink-soft hover:text-accent">
          Ver noticias
        </Link>
      </div>
    </div>
  );
}
