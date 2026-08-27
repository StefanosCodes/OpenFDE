from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.dependencies import SessionDep
from app.schemas import CallRead, Page, TranscriptPage
from app.services import calls as call_service

router = APIRouter(prefix="/calls", tags=["calls"])


@router.get("", response_model=Page[CallRead], operation_id="list_calls")
def list_calls(
    session: SessionDep,
    q: Annotated[str | None, Query(max_length=200)] = None,
    account_id: UUID | None = None,
    call_type: Annotated[str | None, Query(max_length=100)] = None,
    outcome: Annotated[str | None, Query(max_length=100)] = None,
    started_after: datetime | None = None,
    started_before: datetime | None = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
    cursor: Annotated[str | None, Query(max_length=1000)] = None,
) -> Page[CallRead]:
    if started_after and started_before and started_after > started_before:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="started_after must not be later than started_before.",
        )
    items, next_cursor = call_service.list_calls(
        session,
        q=q,
        account_id=account_id,
        call_type=call_type,
        outcome=outcome,
        started_after=started_after,
        started_before=started_before,
        limit=limit,
        cursor=cursor,
    )
    return Page(items=items, next_cursor=next_cursor)


@router.get("/{call_id}", response_model=CallRead, operation_id="get_call")
def get_call(call_id: UUID, session: SessionDep) -> CallRead:
    return CallRead.model_validate(call_service.get_call(session, call_id))


@router.get(
    "/{call_id}/transcript",
    response_model=TranscriptPage,
    operation_id="get_call_transcript",
)
def get_call_transcript(
    call_id: UUID,
    session: SessionDep,
    start_turn: Annotated[int | None, Query(ge=0)] = None,
    end_turn: Annotated[int | None, Query(ge=0)] = None,
    limit: Annotated[int, Query(ge=1, le=250)] = 250,
) -> TranscriptPage:
    if start_turn is not None and end_turn is not None and start_turn > end_turn:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="start_turn must not be greater than end_turn.",
        )
    items, next_start_turn = call_service.get_transcript(
        session,
        call_id=call_id,
        start_turn=start_turn,
        end_turn=end_turn,
        limit=limit,
    )
    return TranscriptPage(items=items, next_start_turn=next_start_turn)
