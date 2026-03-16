#!/usr/bin/env bash
set -euo pipefail

workspace="${1:-.}"

if [[ ! -d "$workspace" ]]; then
  echo "[FAIL] workspace dir not found: $workspace" >&2
  exit 2
fi

cd "$workspace"

echo "== SROS Claude Code MVP checklist =="
echo "workspace: $(pwd)"
echo

missing=0

need_file() {
  local f="$1"
  if [[ -f "$f" ]]; then
    echo "[OK]   $f"
  else
    echo "[MISS] $f"
    missing=1
  fi
}

need_cmd() {
  local c="$1"
  if command -v "$c" >/dev/null 2>&1; then
    echo "[OK]   cmd: $c ($(command -v "$c"))"
  else
    echo "[MISS] cmd: $c"
    missing=1
  fi
}

need_file ".clauderc"
need_file "CLAUDE.md"
need_file "draft.md"

echo
need_cmd "sros"

echo
echo "Next steps (no Claude required):"
cat <<'EOF'
  1) Start gateway:
       sros start -w . -p 8000

  2) Verify MCP SSE (writes report to logs/claude_mvp_verification.json):
       sros verify --port 8000

Claude Code (optional E2E):"
  - Install Claude Code per official docs, then run the CLI from this workspace.
  - If the command is available, you can check:
       claude --version
EOF

echo
if [[ $missing -ne 0 ]]; then
  echo "[WARN] Some items are missing. If this is a fresh workspace, run:" 
  echo "       sros init <project> --target claude-code"
  exit 1
fi

echo "[OK] Checklist looks good."
