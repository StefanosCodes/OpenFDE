from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient


def test_health_is_public_and_database_backed(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ready", "database": "ready"}


def test_v1_requires_valid_service_authentication(client: TestClient) -> None:
    missing = client.get("/v1/accounts")
    invalid = client.get("/v1/accounts", headers={"Authorization": "Bearer definitely-wrong"})

    assert missing.status_code == 401
    assert invalid.status_code == 401
    assert missing.headers["www-authenticate"] == "Bearer"


def test_account_search_get_and_cursor_pagination(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    first = client.get("/v1/accounts?limit=2", headers=auth_headers)

    assert first.status_code == 200
    assert len(first.json()["items"]) == 2
    assert first.json()["next_cursor"]
    assert "metadata" in first.json()["items"][0]

    second = client.get(
        "/v1/accounts",
        params={"limit": 2, "cursor": first.json()["next_cursor"]},
        headers=auth_headers,
    )
    assert second.status_code == 200
    first_ids = {item["id"] for item in first.json()["items"]}
    second_ids = {item["id"] for item in second.json()["items"]}
    assert first_ids.isdisjoint(second_ids)

    search = client.get("/v1/accounts?q=Acme", headers=auth_headers)
    assert [item["name"] for item in search.json()["items"]] == ["Acme Health"]

    account_id = search.json()["items"][0]["id"]
    assert client.get(f"/v1/accounts/{account_id}", headers=auth_headers).status_code == 200
    assert client.get("/v1/accounts/not-a-uuid", headers=auth_headers).status_code == 422
    assert client.get("/v1/accounts?cursor=bad", headers=auth_headers).status_code == 422


def test_call_filters_get_and_bounded_transcript(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    accounts = client.get("/v1/accounts?q=Acme", headers=auth_headers).json()["items"]
    account_id = accounts[0]["id"]
    calls = client.get(
        "/v1/calls", params={"account_id": account_id, "limit": 2}, headers=auth_headers
    )

    assert calls.status_code == 200
    assert len(calls.json()["items"]) == 2
    call = calls.json()["items"][0]
    assert "transcript" not in call
    assert client.get(f"/v1/calls/{call['id']}", headers=auth_headers).status_code == 200

    transcript = client.get(
        f"/v1/calls/{call['id']}/transcript",
        params={"start_turn": 2, "limit": 3},
        headers=auth_headers,
    )
    assert transcript.status_code == 200
    assert [turn["turn_index"] for turn in transcript.json()["items"]] == [2, 3, 4]
    assert transcript.json()["next_start_turn"] == 5
    assert (
        client.get(f"/v1/calls/{call['id']}/transcript?limit=251", headers=auth_headers).status_code
        == 422
    )


def test_document_filters_and_get(client: TestClient, auth_headers: dict[str, str]) -> None:
    response = client.get("/v1/documents", params={"document_type": "sop"}, headers=auth_headers)

    assert response.status_code == 200
    assert len(response.json()["items"]) == 1
    document = response.json()["items"][0]
    assert document["name"] == "Discovery Call SOP"
    assert (
        client.get(f"/v1/documents/{document['id']}", headers=auth_headers).json()["content"]
        == document["content"]
    )


def _task_payload(client: TestClient, auth_headers: dict[str, str]) -> dict[str, object]:
    account = client.get("/v1/accounts?q=Acme", headers=auth_headers).json()["items"][0]
    call = client.get(
        "/v1/calls", params={"account_id": account["id"]}, headers=auth_headers
    ).json()["items"][0]
    return {
        "account_id": account["id"],
        "source_call_id": call["id"],
        "title": "Confirm renewal owner",
        "description": "Follow up using the cited call evidence.",
        "due_at": (datetime.now(UTC) + timedelta(days=3)).isoformat(),
        "created_by_run_id": "run-test-001",
    }


def test_task_creation_is_idempotent_and_detects_key_reuse(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    payload = _task_payload(client, auth_headers)
    headers = {**auth_headers, "Idempotency-Key": "test-create-task-001"}

    created = client.post("/v1/tasks", json=payload, headers=headers)
    replay = client.post("/v1/tasks", json=payload, headers=headers)
    changed = client.post("/v1/tasks", json={**payload, "title": "Different work"}, headers=headers)

    assert created.status_code == 201
    assert replay.status_code == 200
    assert replay.json()["id"] == created.json()["id"]
    assert "idempotency_key" not in created.json()
    assert changed.status_code == 409
    assert client.post("/v1/tasks", json=payload, headers=auth_headers).status_code == 422
    assert (
        client.post(
            "/v1/tasks",
            json={**payload, "status": "completed"},
            headers={**auth_headers, "Idempotency-Key": "test-invalid-status-001"},
        ).status_code
        == 422
    )

    open_tasks = client.get("/v1/tasks?status=open&limit=50", headers=auth_headers)
    assert open_tasks.status_code == 200
    assert all(task["status"] == "open" for task in open_tasks.json()["items"])


def test_task_transitions_and_terminal_protection(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    payload = _task_payload(client, auth_headers)
    created = client.post(
        "/v1/tasks",
        json=payload,
        headers={**auth_headers, "Idempotency-Key": "test-transition-001"},
    ).json()

    started = client.patch(
        f"/v1/tasks/{created['id']}", json={"status": "in_progress"}, headers=auth_headers
    )
    completed = client.patch(
        f"/v1/tasks/{created['id']}", json={"status": "completed"}, headers=auth_headers
    )
    terminal_change = client.patch(
        f"/v1/tasks/{created['id']}", json={"due_at": None}, headers=auth_headers
    )

    assert started.json()["status"] == "in_progress"
    assert completed.json()["status"] == "completed"
    assert terminal_change.status_code == 409
    assert (
        client.patch(f"/v1/tasks/{created['id']}", json={}, headers=auth_headers).status_code == 422
    )


def test_agent_result_round_trip(client: TestClient, auth_headers: dict[str, str]) -> None:
    payload = {
        "agent_name": "structured-tool",
        "agent_version": "0.1.0",
        "skill_name": "resolve-account",
        "source_type": "call",
        "result_type": "resolution",
        "result": {"confidence": 0.91, "evidence_turns": [1, 4]},
        "artifact_paths": ["artifacts/example.json"],
        "trace_id": "trace-test-001",
    }
    created = client.post("/v1/agent-results", json=payload, headers=auth_headers)

    assert created.status_code == 201
    fetched = client.get(f"/v1/agent-results/{created.json()['id']}", headers=auth_headers)
    assert fetched.status_code == 200
    assert fetched.json()["result"] == payload["result"]


def test_openapi_contains_exact_product_operations(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()
    product_operations = [
        operation
        for path, methods in schema["paths"].items()
        if path.startswith("/v1/")
        for method, operation in methods.items()
        if method in {"get", "post", "patch"}
    ]

    assert len(product_operations) == 12
    assert all(operation["security"] == [{"HTTPBearer": []}] for operation in product_operations)
