from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies import SessionDep
from app.schemas import DocumentRead, Page
from app.services import documents as document_service

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_model=Page[DocumentRead], operation_id="list_documents")
def list_documents(
    session: SessionDep,
    q: Annotated[str | None, Query(max_length=200)] = None,
    document_type: Annotated[str | None, Query(max_length=100)] = None,
    version: Annotated[str | None, Query(max_length=100)] = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
) -> Page[DocumentRead]:
    items = document_service.list_documents(
        session,
        q=q,
        document_type=document_type,
        version=version,
        limit=limit,
    )
    return Page(items=items)


@router.get("/{document_id}", response_model=DocumentRead, operation_id="get_document")
def get_document(document_id: UUID, session: SessionDep) -> DocumentRead:
    return DocumentRead.model_validate(document_service.get_document(session, document_id))
