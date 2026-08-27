from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.exceptions import ResourceNotFoundError
from app.models import Document


def list_documents(
    session: Session,
    *,
    q: str | None,
    document_type: str | None,
    version: str | None,
    limit: int,
) -> list[Document]:
    statement = select(Document)
    if q:
        pattern = f"%{q.strip()}%"
        statement = statement.where(
            or_(Document.name.ilike(pattern), Document.content.ilike(pattern))
        )
    if document_type:
        statement = statement.where(Document.document_type == document_type)
    if version:
        statement = statement.where(Document.version == version)
    return list(session.scalars(statement.order_by(Document.name, Document.id).limit(limit)))


def get_document(session: Session, document_id: UUID) -> Document:
    document = session.get(Document, document_id)
    if document is None:
        raise ResourceNotFoundError("Document not found.")
    return document
