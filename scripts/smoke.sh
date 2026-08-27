#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dev_log="$(mktemp)"

cleanup() {
  if [[ -n "${dev_pid:-}" ]]; then
    kill "$dev_pid" >/dev/null 2>&1 || true
    wait "$dev_pid" >/dev/null 2>&1 || true
  fi
  cd "$repo_root"
  docker compose down >/dev/null 2>&1 || true
  rm -f "$dev_log"
}
trap cleanup EXIT

cd "$repo_root"
pnpm dev >"$dev_log" 2>&1 &
dev_pid=$!

for _ in {1..60}; do
  if curl --fail --silent http://localhost:5173 >/dev/null \
    && curl --fail --silent http://localhost:8000/health >/dev/null; then
    pnpm --dir studio test:e2e
    exit 0
  fi
  sleep 1
done

cat "$dev_log"
exit 1

