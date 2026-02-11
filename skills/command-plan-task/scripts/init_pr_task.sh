#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  init_pr_task.sh [options]

Options:
  --root <dir>           Task root directory (default: ./.vscode/pull-request-task)
  --thread-key <key>     Current conversation thread key (fallback: CODEX_THREAD_ID)
  --title <text>         Task title used for metadata and slug generation
  --description <text>   Optional short task description
  --task-slug <slug>     Optional explicit slug (otherwise derived from title)
  --pr-id <id>           Optional explicit PR ID (default: PR-YYYYMMDD-HHMMSS)
  --help                 Show this help message

Output (key=value lines):
  result=CREATED|ERROR
  thread_key=<resolved_thread_key>
  source_path=<absolute_source_md_path>
  mirror_path=<absolute_tw_md_path>
  pr_id=<pr_id>
  task_slug=<task_slug>
EOF
}

ROOT="./.vscode/pull-request-task"
THREAD_KEY=""
TITLE=""
DESCRIPTION=""
TASK_SLUG=""
PR_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)
      ROOT="${2:-}"
      shift 2
      ;;
    --thread-key)
      THREAD_KEY="${2:-}"
      shift 2
      ;;
    --title)
      TITLE="${2:-}"
      shift 2
      ;;
    --description)
      DESCRIPTION="${2:-}"
      shift 2
      ;;
    --task-slug)
      TASK_SLUG="${2:-}"
      shift 2
      ;;
    --pr-id)
      PR_ID="${2:-}"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "result=ERROR"
      echo "message=Unknown argument: $1"
      exit 2
      ;;
  esac
done

if [[ -z "$THREAD_KEY" ]]; then
  THREAD_KEY="${CODEX_THREAD_ID:-}"
fi

if [[ -z "$THREAD_KEY" ]]; then
  echo "result=ERROR"
  echo "message=thread_key is required (--thread-key or CODEX_THREAD_ID)"
  exit 2
fi

if [[ -z "$TITLE" ]]; then
  TITLE="New Task"
fi

yaml_quote() {
  local text="$1"
  printf '%s' "$text" | tr '\n' ' ' | sed 's/\\/\\\\/g; s/"/\\"/g'
}

slugify() {
  local text="$1"
  local slug
  slug="$(printf '%s' "$text" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-+/-/g')"
  if [[ -z "$slug" ]]; then
    slug="task"
  fi
  printf '%s\n' "$slug"
}

to_abs_dir() {
  local path="$1"
  if [[ -d "$path" ]]; then
    printf '%s\n' "$(cd "$path" && pwd -P)"
  elif [[ "$path" = /* ]]; then
    printf '%s\n' "$path"
  else
    printf '%s/%s\n' "$(pwd -P)" "$path"
  fi
}

unique_source_path() {
  local thread_dir="$1"
  local slug="$2"
  local candidate idx
  candidate="$thread_dir/$slug.md"
  if [[ ! -e "$candidate" ]]; then
    printf '%s\n' "$candidate"
    return
  fi
  idx=2
  while true; do
    candidate="$thread_dir/$slug-$(printf '%02d' "$idx").md"
    if [[ ! -e "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return
    fi
    idx=$((idx + 1))
  done
}

if [[ -z "$TASK_SLUG" ]]; then
  TASK_SLUG="$(slugify "$TITLE")"
else
  TASK_SLUG="$(slugify "$TASK_SLUG")"
fi

if [[ -z "$PR_ID" ]]; then
  PR_ID="PR-$(date -u +%Y%m%d-%H%M%S)"
fi

ROOT_ABS="$(to_abs_dir "$ROOT")"
THREAD_DIR="$ROOT_ABS/$THREAD_KEY"
mkdir -p "$THREAD_DIR"

SOURCE_PATH="$(unique_source_path "$THREAD_DIR" "$TASK_SLUG")"
FINAL_SLUG="$(basename "$SOURCE_PATH" .md)"
MIRROR_PATH="${SOURCE_PATH%.md}_TW.md"

NOW_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
TITLE_YAML="$(yaml_quote "$TITLE")"
DESC_YAML="$(yaml_quote "$DESCRIPTION")"

cat >"$SOURCE_PATH" <<EOF
---
workflow_version: v2
pr_id: $PR_ID
thread_key: $THREAD_KEY
title: "$TITLE_YAML"
task_slug: $FINAL_SLUG
stage: A
status: active
created_at: $NOW_UTC
updated_at: $NOW_UTC
description: "$DESC_YAML"
---

# PR Change Card
Business Goal:
Out of Scope:
Architecture Gate:
- Schema change: Yes/No
- Auth/Permission change: Yes/No
- Cross-service contract change: Yes/No
- Critical invariant impact: Yes/No
- Migration required: Yes/No
- Rollback path defined: Yes/No

Acceptance Tests (<=8):
1.
2.

Critical Invariants (<=5):
1.
2.

# CR Checklist
| CR-ID | Scope | Goal | Path(Fast/Guarded) | Status | Evidence Link | Commit Hash |
|------|-------|------|---------------------|--------|---------------|-------------|
| CR-001 | A |  | Fast | todo |  |  |
EOF

cp "$SOURCE_PATH" "$MIRROR_PATH"

echo "result=CREATED"
echo "thread_key=$THREAD_KEY"
echo "source_path=$SOURCE_PATH"
echo "mirror_path=$MIRROR_PATH"
echo "pr_id=$PR_ID"
echo "task_slug=$FINAL_SLUG"
