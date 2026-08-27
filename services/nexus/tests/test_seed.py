from sqlalchemy import func, select

from app.database import SessionLocal
from app.models import Account, Call, Document, Task, TranscriptTurn
from app.seed.generate import seed


def test_seed_is_repeatable_without_duplicates() -> None:
    with SessionLocal() as session:
        first = seed(session)
        second = seed(session)
        counts = {
            "accounts": session.scalar(select(func.count()).select_from(Account)),
            "calls": session.scalar(select(func.count()).select_from(Call)),
            "transcript_turns": session.scalar(select(func.count()).select_from(TranscriptTurn)),
            "documents": session.scalar(select(func.count()).select_from(Document)),
            "tasks": session.scalar(select(func.count()).select_from(Task)),
        }

    assert first == second
    assert counts == first
