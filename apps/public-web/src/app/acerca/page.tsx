import type { Metadata } from "next";
import { SITE_NAME, SITE_DESCRIPTION } from "@/lib/site";

export const metadata: Metadata = {
  title: "Acerca de",
  description: SITE_DESCRIPTION,
  alternates: { canonical: "/acerca" },
};

export default function AboutPage() {
  return (
    <div className="mx-auto max-w-prose px-4 py-12 md:px-6">
      <h1 className="font-serif text-3xl font-bold text-ink">Acerca de {SITE_NAME}</h1>
      <div className="prose prose-lg mt-6 max-w-none prose-headings:font-serif prose-headings:text-ink prose-p:text-ink-soft prose-a:text-accent">
        <p>
          {SITE_NAME} es una agencia de noticias enfocada en el ecosistema cripto: mercados,
          regulación y activos digitales. Publicamos cobertura editorial verificada, con
          trazabilidad de fuentes y un proceso de revisión antes de publicar.
        </p>
        <h2>Cómo trabajamos</h2>
        <p>
          Cada nota pasa por un flujo editorial: detección de señales, verificación de fuentes,
          revisión de riesgo y aprobación editorial. Solo el contenido aprobado se publica en el
          sitio público.
        </p>
        <h2>Aviso</h2>
        <p>
          El contenido de {SITE_NAME} es informativo y no constituye asesoría financiera, legal ni
          de inversión. Realiza tu propia investigación antes de tomar decisiones.
        </p>
      </div>
    </div>
  );
}
