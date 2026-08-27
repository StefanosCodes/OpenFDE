from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import ConflictError, ResourceNotFoundError
from app.models import Account, Call, Task
from app.pagination import InvalidCursorError, decode_cursor, encode_cursor
from app.schemas import TaskCreate, TaskStatus, TaskUpdate

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    TaskStatus.OPEN: {TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED, TaskStatus.CANCELED},
    TaskStatus.IN_PROGRESS: {TaskStatus.COMPLETED, TaskStatus.CANCELED},
    TaskStatus.COMPLETED: set(),
    TaskStatus.CANCELED: set(),
}


def list_tasks(
    session: Session,
    *,
    account_id: UUID | None,
    status: TaskStatus | None,
    limit: int,
    cursor: str | None,
) -> tuple[list[Task], str | None]:
    statement = select(Task)
    if account_id:
        statement = statement.where(Task.account_id == account_id)
    if status:
        statement = statement.where(Task.status == status)
    if cursor:
        decoded = decode_cursor(cursor)
        try:
            cursor_created_at = datetime.fromisoformat(decoded.value)
            cursor_id = UUID(decoded.resource_id)
        except ValueError as exc:
            raise InvalidCursorError("The cursor is invalid.") from exc
        statement = statement.where(
            or_(
                Task.created_at < cursor_created_at,
                and_(Task.created_at == cursor_created_at, Task.id < cursor_id),
            )
        )
    rows = list(
        session.scalars(statement.order_by(Task.created_at.desc(), Task.id.desc()).limit(limit + 1))
    )
    has_more = len(rows) > limit
    items = rows[:limit]
    next_cursor = None
    if has_more and items:
        next_cursor = encode_cursor(items[-1].created_at.isoformat(), str(items[-1].id))
    return items, next_cursor


def _validate_references(session: Session, payload: TaskCreate) -> None:
    if session.get(Account, payload.account_id) is None:
        raise ResourceNotFoundError("Account not found.")
    if payload.source_call_id is not None:
        source_call = session.get(Call, payload.source_call_id)
        if source_call is None:
            raise ResourceNotFoundError("Source call not found.")
        if source_call.account_id != payload.account_id:
            raise ConflictError("The source call does not belong to the task account.")


def _same_request(task: Task, payload: TaskCreate) -> bool:
    return (
        task.account_id == payload.account_id
        and task.source_call_id == payload.source_call_id
        and task.title == payload.title
        and task.description == payload.description
        and task.status == TaskStatus.OPEN
        and task.due_at == payload.due_at
        and task.created_by_run_id == payload.created_by_run_id
    )


def create_task(
    session: Session, *, payload: TaskCreate, idempotency_key: str
) -> tuple[Task, bool]:
    existing = session.scalar(select(Task).where(Task.idempotency_key == idempotency_key))
    if existing is not None:
        if not _same_request(existing, payload):
            raise ConflictError("The idempotency key was already used for a different task.")
        return existing, False

    _validate_references(session, payload)
    values = payload.model_dump(mode="python")
    values["status"] = TaskStatus.OPEN.value
    task = Task(**values, idempotency_key=idempotency_key)
    session.add(task)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        existing = session.scalar(select(Task).where(Task.idempotency_key == idempotency_key))
        if existing is None or not _same_request(existing, payload):
            raise ConflictError(
                "The idempotency key was already used for a different task."
            ) from None
        return existing, False
    session.refresh(task)
    return task, True


def update_task(session: Session, *, task_id: UUID, payload: TaskUpdate) -> Task:
    task = session.get(Task, task_id)
    if task is None:
        raise ResourceNotFoundError("Task not found.")

    requested_status = payload.status.value if payload.status else None
    status_changes = requested_status is not None and requested_status != task.status
    due_changes = "due_at" in payload.model_fields_set and payload.due_at != task.due_at
    if task.status in {TaskStatus.COMPLETED, TaskStatus.CANCELED} and (
        status_changes or due_changes
    ):
        raise ConflictError("Terminal tasks cannot be changed.")
    if status_changes and requested_status not in ALLOWED_TRANSITIONS[task.status]:
        raise ConflictError(
            f"Task status cannot transition from {task.status} to {requested_status}."
        )

    if requested_status is not None:
        task.status = requested_status
    if "due_at" in payload.model_fields_set:
        task.due_at = payload.due_at
    session.commit()
    session.refresh(task)
    return task
