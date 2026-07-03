from difflib import SequenceMatcher

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import IntakeSignal

PROBABLE_DUPLICATE_THRESHOLD = 0.88


async def apply_deduplication(session: AsyncSession, signal: IntakeSignal) -> IntakeSignal:
    exact = await _find_exact_duplicate(session, signal)
    if exact is not None:
        signal.signal_status = "duplicate"
        signal.dedupe_status = "exact_duplicate"
        signal.duplicate_of_signal_id = exact.id
        signal.dedupe_score = 1.0
        return signal

    probable, score = await _find_probable_duplicate(session, signal)
    if probable is not None:
        signal.signal_status = "probable_duplicate"
        signal.dedupe_status = "probable_duplicate"
        signal.duplicate_of_signal_id = probable.id
        signal.dedupe_score = score
        return signal

    signal.signal_status = "unique"
    signal.dedupe_status = "unique"
    signal.duplicate_of_signal_id = None
    signal.dedupe_score = 0.0
    return signal


async def _find_exact_duplicate(
    session: AsyncSession, signal: IntakeSignal
) -> IntakeSignal | None:
    candidates: list[IntakeSignal] = []
    if signal.content_hash:
        result = await session.execute(
            select(IntakeSignal)
            .where(
                IntakeSignal.id != signal.id,
                IntakeSignal.content_hash == signal.content_hash,
            )
            .order_by(IntakeSignal.created_at.asc())
            .limit(1)
        )
        candidates.extend(result.scalars().all())

    if signal.url_canonical:
        result = await session.execute(
            select(IntakeSignal)
            .where(
                IntakeSignal.id != signal.id,
                IntakeSignal.url_canonical == signal.url_canonical,
            )
            .order_by(IntakeSignal.created_at.asc())
            .limit(1)
        )
        candidates.extend(result.scalars().all())

    return candidates[0] if candidates else None


async def _find_probable_duplicate(
    session: AsyncSession, signal: IntakeSignal
) -> tuple[IntakeSignal | None, float | None]:
    if signal.dedupe_key:
        result = await session.execute(
            select(IntakeSignal)
            .where(
                IntakeSignal.id != signal.id,
                IntakeSignal.dedupe_key == signal.dedupe_key,
            )
            .order_by(IntakeSignal.created_at.asc())
            .limit(1)
        )
        candidate = result.scalar_one_or_none()
        if candidate is not None:
            return candidate, 0.95

    if not signal.normalized_title:
        return None, None

    result = await session.execute(
        select(IntakeSignal)
        .where(IntakeSignal.id != signal.id)
        .order_by(IntakeSignal.created_at.asc())
    )
    best_candidate: IntakeSignal | None = None
    best_score = 0.0
    title = signal.normalized_title.lower()
    for candidate in result.scalars().all():
        if not candidate.normalized_title:
            continue
        score = SequenceMatcher(None, title, candidate.normalized_title.lower()).ratio()
        if score > best_score:
            best_score = score
            best_candidate = candidate

    if best_candidate is not None and best_score >= PROBABLE_DUPLICATE_THRESHOLD:
        return best_candidate, round(best_score, 4)
    return None, None
