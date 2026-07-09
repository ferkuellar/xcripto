// Shared site constants + small helpers (no server-only imports so both server
// and client components can use them).

export const SITE_NAME = process.env.NEXT_PUBLIC_SITE_NAME ?? "XCripto";
export const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000").replace(/\/$/, "");
export const SITE_TAGLINE = "Inteligencia editorial sobre cripto";
export const SITE_DESCRIPTION =
  "XCripto — agencia de noticias cripto: cobertura verificada de mercados, regulación y activos digitales.";

export function formatDate(value: string | null): string {
  if (!value) return "";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return "";
  return d.toLocaleDateString("es-MX", { year: "numeric", month: "long", day: "numeric" });
}

export function formatDateTimeISO(value: string | null): string {
  if (!value) return "";
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? "" : d.toISOString();
}

export function categorySlug(category: string): string {
  return encodeURIComponent(category.toLowerCase().trim());
}

export function authorSlug(author: string): string {
  return encodeURIComponent(author.toLowerCase().trim().replace(/\s+/g, "-"));
}
