import { categoryTone } from "@/lib/tone";

// og_image / cover_image_url are null in the current backend contract, so we
// render a branded editorial placeholder keyed on the category instead of a
// broken image. When the backend starts returning a cover, we use it.
export function CoverImage({
  src,
  category,
  title,
  size = "card",
}: {
  src: string | null;
  category: string;
  title: string;
  size?: "card" | "hero";
}) {
  const tall = size === "hero" ? "aspect-[16/7]" : "aspect-[16/9]";
  if (src) {
    // eslint-disable-next-line @next/next/no-img-element
    return <img src={src} alt={title} className={`w-full ${tall} object-cover`} loading="lazy" />;
  }
  const tone = categoryTone(category);
  return (
    <div
      className={`flex w-full ${tall} items-end ${tone} `}
      role="img"
      aria-label={`${category} — XCripto`}
    >
      <span className="p-4 font-serif text-sm font-semibold uppercase tracking-[0.14em] text-white/90">
        {category}
      </span>
    </div>
  );
}
