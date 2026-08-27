from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Header, HTTPException, Query, Response, status

from app.dependencies import SessionDep
from app.schemas import Page, TaskCreate, TaskRead, TaskStatus, TaskUpdate
from app.services import tasks as task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=Page[TaskRead], operation_id="list_tasks")
def list_tasks(
    session: SessionDep,
    account_id: UUID | None = None,
    task_status: Annotated[TaskStatus | None, Query(alias="status")] = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
    cursor: Annotated[str | None, Query(max_length=1000)] = None,
) -> Page[TaskRead]:
    items, next_cursor = task_service.list_tasks(
        session,
        account_id=account_id,
        status=task_status,
        limit=limit,
        cursor=cursor,
    )
    return Page(items=items, next_cursor=next_cursor)


@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_200_OK: {"model": TaskRead}},
    operation_id="create_task",
)
def create_task(
    payload: TaskCreate,
    response: Response,
    session: SessionDep,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=1, max_length=255)],
) -> TaskRead:
    idempotency_key = idempotency_key.strip()
    if not idempotency_key:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Idempotency-Key cannot be blank.",
        )
    task, created = task_service.create_task(
        session,
        payload=payload,
        idempotency_key=idempotency_key,
    )
    response.status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
    return TaskRead.model_validate(task)


@router.patch("/{task_id}", response_model=TaskRead, operation_id="update_task")
def update_task(task_id: UUID, payload: TaskUpdate, session: SessionDep) -> TaskRead:
    return TaskRead.model_validate(
        task_service.update_task(session, task_id=task_id, payload=payload)
    )
