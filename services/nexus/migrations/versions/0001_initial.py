"""Create the six Nexus V1 tables."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("domain", sa.Text(), nullable=True),
        sa.Column("segment", sa.Text(), nullable=True),
        sa.Column("health_status", sa.Text(), nullable=True),
        sa.Column("owner_name", sa.Text(), nullable=True),
        sa.Column(
            "metadata", postgresql.JSONB(), server_default=sa.text("'{}'::jsonb"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_accounts_health_segment", "accounts", ["health_status", "segment"])
    op.create_index("ix_accounts_name_id", "accounts", ["name", "id"])

    op.create_table(
        "calls",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("external_id", sa.Text(), nullable=True),
        sa.Column("call_type", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("duration_seconds", sa.Integer(), nullable=False),
        sa.Column("outcome", sa.Text(), nullable=True),
        sa.Column(
            "participants",
            postgresql.JSONB(),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column(
            "metadata", postgresql.JSONB(), server_default=sa.text("'{}'::jsonb"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint("duration_seconds >= 0", name="ck_calls_duration_nonnegative"),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("external_id"),
    )
    op.create_index("ix_calls_account_started", "calls", ["account_id", "started_at"])
    op.create_index("ix_calls_started_id", "calls", ["started_at", "id"])
    op.create_index("ix_calls_type_outcome", "calls", ["call_type", "outcome"])

    op.create_table(
        "documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("document_type", sa.Text(), nullable=False),
        sa.Column("version", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "metadata", postgresql.JSONB(), server_default=sa.text("'{}'::jsonb"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_documents_type_version", "documents", ["document_type", "version"])

    op.create_table(
        "transcript_turns",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("call_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("turn_index", sa.Integer(), nullable=False),
        sa.Column("speaker", sa.Text(), nullable=False),
        sa.Column("started_ms", sa.Integer(), nullable=True),
        sa.Column("ended_ms", sa.Integer(), nullable=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column(
            "metadata", postgresql.JSONB(), server_default=sa.text("'{}'::jsonb"), nullable=False
        ),
        sa.CheckConstraint("turn_index >= 0", name="ck_transcript_turn_index_nonnegative"),
        sa.ForeignKeyConstraint(["call_id"], ["calls.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("call_id", "turn_index", name="uq_transcript_turn_call_index"),
    )
    op.create_index("ix_transcript_turn_call_index", "transcript_turns", ["call_id", "turn_index"])

    op.create_table(
        "tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_call_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("idempotency_key", sa.String(length=255), nullable=True),
        sa.Column("created_by_run_id", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint(
            "status IN ('open', 'in_progress', 'completed', 'canceled')",
            name="ck_tasks_status",
        ),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["source_call_id"], ["calls.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("idempotency_key"),
    )
    op.create_index("ix_tasks_account_status", "tasks", ["account_id", "status"])
    op.create_index("ix_tasks_created_id", "tasks", ["created_at", "id"])

    op.create_table(
        "agent_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("agent_name", sa.Text(), nullable=False),
        sa.Column("agent_version", sa.Text(), nullable=False),
        sa.Column("skill_name", sa.Text(), nullable=True),
        sa.Column("source_type", sa.Text(), nullable=False),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("result_type", sa.Text(), nullable=False),
        sa.Column("result", postgresql.JSONB(), nullable=False),
        sa.Column(
            "artifact_paths",
            postgresql.JSONB(),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column("trace_id", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_agent_results_agent_created", "agent_results", ["agent_name", "created_at"])
    op.create_index("ix_agent_results_source", "agent_results", ["source_type", "source_id"])


def downgrade() -> None:
    op.drop_table("agent_results")
    op.drop_table("tasks")
    op.drop_table("transcript_turns")
    op.drop_table("documents")
    op.drop_table("calls")
    op.drop_table("accounts")
