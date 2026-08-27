import os

os.environ.setdefault("NEXUS_API_KEY", "openfde-test-service-key")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.database import SessionLocal, engine
from app.main import app
from app.seed.generate import seed


@pytest.fixture(autouse=True)
def reset_database() -> None:
    with engine.begin() as connection:
        connection.execute(
            text(
                "TRUNCATE TABLE agent_results, tasks, transcript_turns, documents, "
                "calls, accounts CASCADE"
            )
        )
    with SessionLocal() as session:
        seed(session)


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer openfde-test-service-key"}
