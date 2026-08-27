from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.exceptions import ResourceNotFoundError
from app.models import Call, TranscriptTurn
from app.pagination import InvalidCursorError, decode_cursor, encode_cursor


def list_calls(
    session: Session,
    *,
    q: str | None,
    account_id: UUID | None,
    call_type: str | None,
    outcome: str | None,
    started_after: datetime | None,
    started_before: datetime | None,
    limit: int,
    cursor: str | None,
) -> tuple[list[Call], str | None]:
    statement = select(Call)
    if q:
        pattern = f"%{q.strip()}%"
        statement = statement.where(or_(Call.title.ilike(pattern), Call.summary.ilike(pattern)))
    if account_id:
        statement = statement.where(Call.account_id == account_id)
    if call_type:
        statement = statement.where(Call.call_type == call_type)
    if outcome:
        statement = statement.where(Call.outcome == outcome)
    if started_after:
        statement = statement.where(Call.started_at >= started_after)
    if started_before:
        statement = statement.where(Call.started_at <= started_before)

    if cursor:
        decoded = decode_cursor(cursor)
        try:
            cursor_started_at = datetime.fromisoformat(decoded.value)
            cursor_id = UUID(decoded.resource_id)
        except ValueError as exc:
            raise InvalidCursorError("The cursor is invalid.") from exc
        statement = statement.where(
            or_(
                Call.started_at < cursor_started_at,
                and_(Call.started_at == cursor_started_at, Call.id < cursor_id),
            )
        )

    rows = list(
        session.scalars(statement.order_by(Call.started_at.desc(), Call.id.desc()).limit(limit + 1))
    )
    has_more = len(rows) > limit
    items = rows[:limit]
    next_cursor = None
    if has_more and items:
        next_cursor = encode_cursor(items[-1].started_at.isoformat(), str(items[-1].id))
    return items, next_cursor


def get_call(session: Session, call_id: UUID) -> Call:
    call = session.get(Call, call_id)
    if call is None:
        raise ResourceNotFoundError("Call not found.")
    return call


def get_transcript(
    session: Session,
    *,
    call_id: UUID,
    start_turn: int | None,
    end_turn: int | None,
    limit: int,
) -> tuple[list[TranscriptTurn], int | None]:
    get_call(session, call_id)
    statement = select(TranscriptTurn).where(TranscriptTurn.call_id == call_id)
    if start_turn is not None:
        statement = statement.where(TranscriptTurn.turn_index >= start_turn)
    if end_turn is not None:
        statement = statement.where(TranscriptTurn.turn_index <= end_turn)
    rows = list(session.scalars(statement.order_by(TranscriptTurn.turn_index).limit(limit + 1)))
    has_more = len(rows) > limit
    items = rows[:limit]
    next_start_turn = items[-1].turn_index + 1 if has_more and items else None
    return items, next_start_turn
