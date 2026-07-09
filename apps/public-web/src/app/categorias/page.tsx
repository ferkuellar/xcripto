import type { Metadata } from "next";
import Link from "next/link";
import { listCategories } from "@/lib/api";
import { categorySlug } from "@/lib/site";
import { categoryTone } from "@/lib/tone";

export const revalidate = 300;

export const metadata: Metadata = {
  title: "Categorías",
  description: "Explora la cobertura de XCripto por categoría.",
  alternates: { canonical: "/categorias" },
};

export default async function CategoriesPage() {
  const categories = await listCategories();

  return (
    <div className="mx-auto max-w-content px-4 py-8 md:px-6">
      <header className="mb-8 border-b border-line pb-3">
        <h1 className="font-serif text-2xl font-bold text-ink">Categorías</h1>
        <p className="mt-1 text-sm text-ink-muted">Cobertura organizada por tema.</p>
      </header>

      {categories.length === 0 ? (
        <p className="text-ink-muted">Aún no hay categorías con noticias publicadas.</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {categories.map((cat) => (
            <Link
              key={cat}
              href={`/categoria/${categorySlug(cat)}`}
              className={`flex aspect-[16/6] items-end ${categoryTone(cat)} transition-transform hover:-translate-y-0.5`}
            >
              <span className="p-4 font-serif text-lg font-semibold capitalize text-white">{cat}</span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
