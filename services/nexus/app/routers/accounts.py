from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies import SessionDep
from app.schemas import AccountRead, Page
from app.services import accounts as account_service

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=Page[AccountRead], operation_id="list_accounts")
def list_accounts(
    session: SessionDep,
    q: Annotated[str | None, Query(max_length=200)] = None,
    health_status: Annotated[str | None, Query(max_length=100)] = None,
    segment: Annotated[str | None, Query(max_length=100)] = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
    cursor: Annotated[str | None, Query(max_length=1000)] = None,
) -> Page[AccountRead]:
    items, next_cursor = account_service.list_accounts(
        session,
        q=q,
        health_status=health_status,
        segment=segment,
        limit=limit,
        cursor=cursor,
    )
    return Page(items=items, next_cursor=next_cursor)


@router.get("/{account_id}", response_model=AccountRead, operation_id="get_account")
def get_account(account_id: UUID, session: SessionDep) -> AccountRead:
    return AccountRead.model_validate(account_service.get_account(session, account_id))
