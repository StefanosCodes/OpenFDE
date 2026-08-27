#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
service_dir="$repo_root/services/nexus"
contract_tmp_dir="$(mktemp -d)"
trap 'rm -rf "$contract_tmp_dir"' EXIT

export NEXUS_API_KEY="${NEXUS_API_KEY:-openfde-contract-generation-key}"

cd "$service_dir"
"$service_dir/.venv/bin/python" -m scripts.export_openapi \
  --output "$contract_tmp_dir/openapi.json"
cd "$repo_root"
pnpm --dir studio exec openapi-typescript "$contract_tmp_dir/openapi.json" \
  --output "$contract_tmp_dir/nexus.generated.ts"

cmp "$contract_tmp_dir/openapi.json" "$service_dir/openapi.json"
cmp "$contract_tmp_dir/nexus.generated.ts" "$repo_root/studio/src/api/nexus.generated.ts"
