// Server-friendly search: a plain GET form that navigates to /buscar?q=...
// No client JS required; the results page fetches server-side.
export function SearchForm({ defaultValue = "" }: { defaultValue?: string }) {
  return (
    <form action="/buscar" method="get" role="search" className="flex items-center gap-2">
      <input
        type="search"
        name="q"
        defaultValue={defaultValue}
        placeholder="Buscar noticias…"
        aria-label="Buscar noticias"
        className="w-full rounded-sm border border-line bg-paper px-3 py-1.5 text-sm text-ink outline-none placeholder:text-ink-muted focus:border-accent"
      />
      <button
        type="submit"
        className="shrink-0 rounded-sm border border-ink bg-ink px-3 py-1.5 text-sm font-medium text-paper-card hover:bg-accent hover:border-accent"
      >
        Buscar
      </button>
    </form>
  );
}
