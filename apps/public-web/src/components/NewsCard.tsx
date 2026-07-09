import Link from "next/link";
import type { PublicNews } from "@/lib/types";
import { formatDate, categorySlug } from "@/lib/site";
import { CoverImage } from "./CoverImage";

// Standard article teaser card.
export function NewsCard({ item, priority = false }: { item: PublicNews; priority?: boolean }) {
  return (
    <article className="group flex flex-col overflow-hidden border border-line bg-paper-card">
      <Link href={`/news/${item.slug}`} tabIndex={-1} aria-hidden className="block">
        <CoverImage src={item.cover_image_url} category={item.category} title={item.title} size={priority ? "hero" : "card"} />
      </Link>
      <div className="flex flex-1 flex-col gap-2 p-4">
        <Link
          href={`/categoria/${categorySlug(item.category)}`}
          className="text-xs font-semibold uppercase tracking-[0.12em] text-accent hover:underline"
        >
          {item.category}
        </Link>
        <h3 className={`font-serif font-semibold text-ink ${priority ? "text-2xl" : "text-lg"}`}>
          <Link href={`/news/${item.slug}`} className="hover:text-accent">
            {item.title}
          </Link>
        </h3>
        <p className="line-clamp-3 text-sm text-ink-soft">{item.summary}</p>
        <div className="mt-auto flex items-center gap-2 pt-2 text-xs text-ink-muted">
          {item.author && <span>{item.author}</span>}
          {item.author && (item.published_at || item.created_at) && <span aria-hidden>·</span>}
          {(item.published_at || item.created_at) && (
            <time dateTime={item.published_at ?? item.created_at}>
              {formatDate(item.published_at ?? item.created_at)}
            </time>
          )}
        </div>
      </div>
    </article>
  );
}
