#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
service_dir="$repo_root/services/nexus"

export NEXUS_API_KEY="${NEXUS_API_KEY:-openfde-contract-generation-key}"

cd "$service_dir"
"$service_dir/.venv/bin/python" -m scripts.export_openapi --output openapi.json
cd "$repo_root"
pnpm --dir studio exec openapi-typescript ../services/nexus/openapi.json \
  --output src/api/nexus.generated.ts
