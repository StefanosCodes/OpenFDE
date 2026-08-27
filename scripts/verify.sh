#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
service_dir="$repo_root/services/nexus"
test_database_url="postgresql+psycopg://openfde:openfde@localhost:${NEXUS_TEST_DB_PORT:-5433}/openfde_test"

cleanup() {
  cd "$repo_root"
  docker compose --profile test rm --stop --force postgres-test >/dev/null 2>&1 || true
}
trap cleanup EXIT

cd "$repo_root"
docker compose --profile test up --detach --wait postgres-test

cd "$service_dir"
export DATABASE_URL="$test_database_url"
export NEXUS_API_KEY="openfde-test-service-key"
.venv/bin/alembic upgrade head
.venv/bin/ruff format --check app migrations scripts tests
.venv/bin/ruff check app migrations scripts tests
.venv/bin/python -m pytest

cd "$repo_root"
bash scripts/check-contracts.sh
pnpm --dir studio verify
