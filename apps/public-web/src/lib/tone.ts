// Deterministic muted background per category for the placeholder cover.
// Restrained editorial tones — no neon. Same category always gets the same tone.
const TONES = [
  "bg-[#232732]",
  "bg-[#2b2320]",
  "bg-[#1f2a28]",
  "bg-[#2a2530]",
  "bg-[#25292f]",
  "bg-[#2d2622]",
];

export function categoryTone(category: string): string {
  let hash = 0;
  for (let i = 0; i < category.length; i++) {
    hash = (hash * 31 + category.charCodeAt(i)) >>> 0;
  }
  return TONES[hash % TONES.length];
}
