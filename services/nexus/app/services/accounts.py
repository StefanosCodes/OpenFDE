from uuid import UUID

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session

from app.exceptions import ResourceNotFoundError
from app.models import Account
from app.pagination import InvalidCursorError, decode_cursor, encode_cursor


def list_accounts(
    session: Session,
    *,
    q: str | None,
    health_status: str | None,
    segment: str | None,
    limit: int,
    cursor: str | None,
) -> tuple[list[Account], str | None]:
    statement = select(Account)
    if q:
        pattern = f"%{q.strip()}%"
        statement = statement.where(or_(Account.name.ilike(pattern), Account.domain.ilike(pattern)))
    if health_status:
        statement = statement.where(Account.health_status == health_status)
    if segment:
        statement = statement.where(Account.segment == segment)

    if cursor:
        decoded = decode_cursor(cursor)
        try:
            cursor_id = UUID(decoded.resource_id)
        except ValueError as exc:
            raise InvalidCursorError("The cursor is invalid.") from exc
        lowered_name = func.lower(Account.name)
        statement = statement.where(
            or_(
                lowered_name > decoded.value,
                and_(lowered_name == decoded.value, Account.id > cursor_id),
            )
        )

    rows = list(
        session.scalars(statement.order_by(func.lower(Account.name), Account.id).limit(limit + 1))
    )
    has_more = len(rows) > limit
    items = rows[:limit]
    next_cursor = None
    if has_more and items:
        next_cursor = encode_cursor(items[-1].name.lower(), str(items[-1].id))
    return items, next_cursor


def get_account(session: Session, account_id: UUID) -> Account:
    account = session.get(Account, account_id)
    if account is None:
        raise ResourceNotFoundError("Account not found.")
    return account
