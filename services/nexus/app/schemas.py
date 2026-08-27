from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ApiModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid", str_strip_whitespace=True)


class HealthResponse(ApiModel):
    status: str
    database: str


class AccountRead(ApiModel):
    id: UUID
    name: str
    domain: str | None
    segment: str | None
    health_status: str | None
    owner_name: str | None
    metadata: dict[str, Any] = Field(validation_alias="metadata_")
    created_at: datetime
    updated_at: datetime


class CallRead(ApiModel):
    id: UUID
    account_id: UUID
    external_id: str | None
    call_type: str
    title: str
    started_at: datetime
    duration_seconds: int
    outcome: str | None
    participants: list[dict[str, Any]]
    summary: str | None
    metadata: dict[str, Any] = Field(validation_alias="metadata_")
    created_at: datetime


class TranscriptTurnRead(ApiModel):
    id: UUID
    call_id: UUID
    turn_index: int
    speaker: str
    started_ms: int | None
    ended_ms: int | None
    text: str
    metadata: dict[str, Any] = Field(validation_alias="metadata_")


class DocumentRead(ApiModel):
    id: UUID
    name: str
    document_type: str
    version: str
    content: str
    metadata: dict[str, Any] = Field(validation_alias="metadata_")
    created_at: datetime


class TaskStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"


class TaskCreate(ApiModel):
    account_id: UUID
    source_call_id: UUID | None = None
    title: str = Field(min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=5000)
    due_at: datetime | None = None
    created_by_run_id: str | None = Field(default=None, max_length=255)


class TaskUpdate(ApiModel):
    status: TaskStatus | None = None
    due_at: datetime | None = None

    @model_validator(mode="after")
    def require_change(self) -> "TaskUpdate":
        if not self.model_fields_set:
            raise ValueError("At least one task field must be supplied.")
        return self


class TaskRead(ApiModel):
    id: UUID
    account_id: UUID
    source_call_id: UUID | None
    title: str
    description: str | None
    status: TaskStatus
    due_at: datetime | None
    created_by_run_id: str | None
    created_at: datetime
    updated_at: datetime


class AgentResultCreate(ApiModel):
    agent_name: str = Field(min_length=1, max_length=200)
    agent_version: str = Field(min_length=1, max_length=100)
    skill_name: str | None = Field(default=None, max_length=200)
    source_type: str = Field(min_length=1, max_length=100)
    source_id: UUID | None = None
    result_type: str = Field(min_length=1, max_length=100)
    result: dict[str, Any]
    artifact_paths: list[str] = Field(default_factory=list, max_length=100)
    trace_id: str | None = Field(default=None, max_length=255)


class AgentResultRead(AgentResultCreate):
    id: UUID
    created_at: datetime


class Page[ItemT](ApiModel):
    items: list[ItemT]
    next_cursor: str | None = None


class TranscriptPage(ApiModel):
    items: list[TranscriptTurnRead]
    next_start_turn: int | None = None
