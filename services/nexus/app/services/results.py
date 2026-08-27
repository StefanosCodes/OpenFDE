from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions import ResourceNotFoundError
from app.models import AgentResult
from app.schemas import AgentResultCreate


def create_result(session: Session, payload: AgentResultCreate) -> AgentResult:
    result = AgentResult(**payload.model_dump(mode="python"))
    session.add(result)
    session.commit()
    session.refresh(result)
    return result


def get_result(session: Session, result_id: UUID) -> AgentResult:
    result = session.get(AgentResult, result_id)
    if result is None:
        raise ResourceNotFoundError("Agent result not found.")
    return result
