"""Enforcement de la SOURCE_QUALITY_POLICY (niveles S1-S5).

Traduce `SourceReference.trust_level` a un nivel de fuente S1-S5 y decide si una
fuente puede sostener la publicación de una noticia *como hecho*. Es un módulo
puro (sin acceso a base de datos) para poder probar la política en aislamiento;
la resolución de la fuente de una noticia vive en `source_service`.

Referencia normativa: ``backend/docs/SOURCE_QUALITY_POLICY.md``.

Regla central (doc §1): nada se publica sin fuente y la calidad de la fuente
determina el techo de certeza. Ante duda entre dos niveles se asigna el más
bajo (fail closed, doc §5).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import SourceReference, VerificationRecord

# Mapeo trust_level -> nivel de fuente (doc §4: T0≈S1, T1≈S2, T2≈S3, T3≈S4/S5).
# T3 cubre S4 y S5; sin poder distinguirlos por trust_level se asume S4 (el más
# alto de los dos) y el estado de la fuente / verificación decide el resto.
TRUST_LEVEL_TO_SOURCE_LEVEL: dict[str, str] = {
    "T0": "S1",
    "T1": "S2",
    "T2": "S3",
    "T3": "S4",
}

# Fallback fail-closed para un trust_level inesperado: se trata como rumor.
DEFAULT_SOURCE_LEVEL = "S5"

SOURCE_LEVELS = ("S1", "S2", "S3", "S4", "S5")

# Niveles primaria / secundaria confiable: pueden alimentar una noticia directa.
PRIMARY_OR_TRUSTED_LEVELS = frozenset({"S1", "S2"})
# Niveles que solo son señal: nunca confirman por sí solos (doc §3).
SIGNAL_ONLY_LEVELS = frozenset({"S4", "S5"})

# source_status que descalifica a la fuente como sostén único (doc §4).
DISQUALIFYING_SOURCE_STATUSES = frozenset({"blocked", "restricted"})

# Contribución al readiness (peso máximo del componente source = 10).
_READINESS_SCORE_BY_LEVEL: dict[str, float] = {
    "S1": 10.0,
    "S2": 9.0,
    "S3": 7.0,
    "S4": 3.0,
    "S5": 0.0,
}

# Evidencia considerada "fuerte" para corroborar una fuente débil (S3/S4).
STRONG_EVIDENCE_LEVELS = frozenset({"E3", "E4", "E5"})


def source_level_for(source: SourceReference) -> str:
    """Nivel S1-S5 de una fuente a partir de su trust_level (fail closed)."""
    return TRUST_LEVEL_TO_SOURCE_LEVEL.get(source.trust_level, DEFAULT_SOURCE_LEVEL)


def is_disqualified(source: SourceReference) -> bool:
    """La fuente está bloqueada/restringida y no sostiene una noticia por sí sola."""
    return source.source_status in DISQUALIFYING_SOURCE_STATUSES


def readiness_score_for_source(source: SourceReference) -> float:
    """Aporte al score de readiness según el nivel de la fuente."""
    if is_disqualified(source):
        return 0.0
    return _READINESS_SCORE_BY_LEVEL.get(source_level_for(source), 0.0)


def is_strong_verification(record: VerificationRecord | None) -> bool:
    """¿La verificación es suficientemente fuerte para sostener una fuente débil?

    Una fuente S3/S4 nunca es confirmación única (doc §3): exige verificación
    ``verified``, sin contradicciones y con corroboración independiente
    (evidencia E3+ o al menos dos referencias de fuente).
    """
    if record is None:
        return False
    if record.verification_status != "verified":
        return False
    if record.contradictions:
        return False
    strong_evidence = record.evidence_level in STRONG_EVIDENCE_LEVELS
    independent_corroboration = len(record.source_refs or []) >= 2
    return strong_evidence or independent_corroboration


def evaluate_publication_source_gate(
    source: SourceReference | None,
    *,
    verification_strong: bool,
) -> list[str]:
    """Razones por las que la calidad de fuente bloquea la publicación.

    Lista vacía => la fuente no bloquea. Si no hay ``SourceReference`` registrada
    la política no puede graduar la calidad y delega en el gate de ``AuditCheck``
    (no se bloquea aquí para no invalidar noticias con fuente denormalizada; es
    una limitación documentada en la SOURCE_QUALITY_POLICY).
    """
    if source is None:
        return []
    if is_disqualified(source):
        return [
            f"source '{source.source_name}' is {source.source_status} and cannot "
            "sustain publication (SOURCE_QUALITY_POLICY)"
        ]
    level = source_level_for(source)
    if level == "S5":
        return [
            f"source '{source.source_name}' is level S5 (rumor/opaque) and cannot "
            "be published as fact (SOURCE_QUALITY_POLICY)"
        ]
    if level in {"S3", "S4"} and not verification_strong:
        return [
            f"source '{source.source_name}' is level {level} and requires strong "
            "independent verification before publication (SOURCE_QUALITY_POLICY)"
        ]
    return []
