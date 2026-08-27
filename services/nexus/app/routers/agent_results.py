from uuid import UUID

from fastapi import APIRouter, status

from app.dependencies import SessionDep
from app.schemas import AgentResultCreate, AgentResultRead
from app.services import results as result_service

router = APIRouter(prefix="/agent-results", tags=["agent-results"])


@router.post(
    "",
    response_model=AgentResultRead,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_agent_result",
)
def create_agent_result(payload: AgentResultCreate, session: SessionDep) -> AgentResultRead:
    return AgentResultRead.model_validate(result_service.create_result(session, payload))


@router.get("/{result_id}", response_model=AgentResultRead, operation_id="get_agent_result")
def get_agent_result(result_id: UUID, session: SessionDep) -> AgentResultRead:
    return AgentResultRead.model_validate(result_service.get_result(session, result_id))
