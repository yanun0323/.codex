#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  find_pr_task.sh --thread-key <key> [options]

Options:
  --root <dir>           Task root directory (default: ./.vscode/pull-request-task)
  --thread-key <key>     Current conversation thread key (required)
  --explicit-path <path> Candidate source PR file path from conversation context
  --rebind               Move explicit PR file to current thread folder and update metadata
  --help                 Show this help message

Output (key=value lines):
  result=FOUND|NOT_FOUND|AMBIGUOUS|ERROR
  resolved_path=<absolute_source_md_path>   # present when FOUND
  source=explicit|explicit_rebound|thread_scan
  status=<status_value_from_pr_metadata>
  candidate=<path>                          # repeated when AMBIGUOUS
  message=<error_message>                   # present when ERROR
EOF
}

ROOT="./.vscode/pull-request-task"
THREAD_KEY=""
EXPLICIT_PATH=""
REBOUND=0

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
    --explicit-path)
      EXPLICIT_PATH="${2:-}"
      shift 2
      ;;
    --rebind)
      REBOUND=1
      shift
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

to_abs() {
  local path="$1"
  if [[ -d "$path" ]]; then
    printf '%s\n' "$(cd "$path" && pwd -P)"
  elif [[ "$path" = /* ]]; then
    printf '%s\n' "$path"
  else
    printf '%s/%s\n' "$(pwd -P)" "$path"
  fi
}

to_abs_existing_file() {
  local path="$1"
  local dir base
  dir="$(dirname "$path")"
  base="$(basename "$path")"
  if [[ "$path" = /* ]]; then
    printf '%s/%s\n' "$(cd "$dir" && pwd -P)" "$base"
  else
    printf '%s/%s\n' "$(cd "$dir" && pwd -P)" "$base"
  fi
}

is_under_root() {
  local path="$1"
  case "$path/" in
    "$ROOT_ABS/"*) return 0 ;;
    *) return 1 ;;
  esac
}

status_of_file() {
  local file="$1"
  local status
  status="$(
    awk '
      NR <= 120 {
        if ($0 ~ /^status:[[:space:]]*/) {
          sub(/^status:[[:space:]]*/, "", $0)
          gsub(/^[[:space:]]+|[[:space:]]+$/, "", $0)
          print tolower($0)
          exit
        }
      }
    ' "$file"
  )"
  if [[ -n "$status" ]]; then
    printf '%s\n' "$status"
  else
    printf 'unknown\n'
  fi
}

mtime_of_file() {
  local file="$1"
  if stat -f %m "$file" >/dev/null 2>&1; then
    stat -f %m "$file"
  else
    stat -c %Y "$file"
  fi
}

normalize_source_path() {
  local file="$1"
  printf '%s\n' "$file"
}

unique_target_path() {
  local target="$1"
  local base ext idx candidate
  if [[ ! -e "$target" ]]; then
    printf '%s\n' "$target"
    return
  fi
  ext=".md"
  base="${target%$ext}"
  idx=2
  while true; do
    candidate="${base}-rebound-${idx}${ext}"
    if [[ ! -e "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return
    fi
    idx=$((idx + 1))
  done
}

update_thread_key_frontmatter() {
  local file="$1"
  local thread_key="$2"
  local tmp
  tmp="$(mktemp "${TMPDIR:-/tmp}/pr-task.XXXXXX")"
  awk -v tk="$thread_key" '
    BEGIN { in_front=0; seen=0; delim=0 }
    {
      if ($0 == "---") {
        delim++
        if (delim == 1) {
          in_front=1
          print
          next
        }
        if (delim == 2) {
          if (in_front == 1 && seen == 0) {
            print "thread_key: " tk
          }
          in_front=0
          print
          next
        }
      }

      if (in_front == 1 && $0 ~ /^thread_key:[[:space:]]*/) {
        print "thread_key: " tk
        seen=1
        next
      }

      print
    }
  ' "$file" >"$tmp"
  mv "$tmp" "$file"
}

emit_found() {
  local source_type="$1"
  local resolved="$2"
  echo "result=FOUND"
  echo "thread_key=$THREAD_KEY"
  echo "source=$source_type"
  echo "resolved_path=$resolved"
  echo "status=$(status_of_file "$resolved")"
}

emit_not_found() {
  echo "result=NOT_FOUND"
  echo "thread_key=$THREAD_KEY"
  echo "root=$ROOT_ABS"
}

ROOT_ABS="$(to_abs "$ROOT")"
THREAD_DIR="$ROOT_ABS/$THREAD_KEY"

if [[ -n "$EXPLICIT_PATH" ]]; then
  if [[ ! -f "$EXPLICIT_PATH" ]]; then
    echo "result=ERROR"
    echo "message=explicit-path not found: $EXPLICIT_PATH"
    exit 2
  fi

  EXPLICIT_ABS="$(to_abs_existing_file "$EXPLICIT_PATH")"
  if ! is_under_root "$EXPLICIT_ABS"; then
    echo "result=ERROR"
    echo "message=explicit-path must be under $ROOT_ABS"
    exit 2
  fi

  SOURCE_FILE="$(normalize_source_path "$EXPLICIT_ABS")"
  if [[ ! -f "$SOURCE_FILE" ]]; then
    echo "result=ERROR"
    echo "message=source PR file not found for explicit path: $SOURCE_FILE"
    exit 2
  fi
  if [[ "$(basename "$SOURCE_FILE")" != PR_*.md ]]; then
    echo "result=ERROR"
    echo "message=explicit-path must point to source PR file: PR_*.md"
    exit 2
  fi

  SOURCE_KIND="explicit"

  if [[ "$REBOUND" -eq 1 ]]; then
    mkdir -p "$THREAD_DIR"
    SOURCE_DIR="$(dirname "$SOURCE_FILE")"
    if [[ "$SOURCE_DIR" != "$THREAD_DIR" ]]; then
      TARGET_SOURCE="$(unique_target_path "$THREAD_DIR/$(basename "$SOURCE_FILE")")"

      mv "$SOURCE_FILE" "$TARGET_SOURCE"

      SOURCE_FILE="$TARGET_SOURCE"
      SOURCE_KIND="explicit_rebound"
    fi

    update_thread_key_frontmatter "$SOURCE_FILE" "$THREAD_KEY"
  fi

  emit_found "$SOURCE_KIND" "$SOURCE_FILE"
  exit 0
fi

if [[ ! -d "$THREAD_DIR" ]]; then
  emit_not_found
  exit 0
fi

CANDIDATES=()
while IFS= read -r file; do
  CANDIDATES+=("$file")
done < <(find "$THREAD_DIR" -maxdepth 1 -type f -name 'PR_*.md' | sort)

if [[ "${#CANDIDATES[@]}" -eq 0 ]]; then
  emit_not_found
  exit 0
fi

if [[ "${#CANDIDATES[@]}" -eq 1 ]]; then
  emit_found "thread_scan" "${CANDIDATES[0]}"
  exit 0
fi

NON_DONE=()
for file in "${CANDIDATES[@]}"; do
  if [[ "$(status_of_file "$file")" != "done" ]]; then
    NON_DONE+=("$file")
  fi
done

if [[ "${#NON_DONE[@]}" -eq 0 ]]; then
  SELECT_POOL=("${CANDIDATES[@]}")
else
  SELECT_POOL=("${NON_DONE[@]}")
fi

BEST_FILE=""
BEST_MTIME=-1
AMBIGUOUS=0
AMBIGUOUS_SET=()

for file in "${SELECT_POOL[@]}"; do
  mtime="$(mtime_of_file "$file")"
  if (( mtime > BEST_MTIME )); then
    BEST_MTIME="$mtime"
    BEST_FILE="$file"
    AMBIGUOUS=0
    AMBIGUOUS_SET=("$file")
  elif (( mtime == BEST_MTIME )); then
    AMBIGUOUS=1
    AMBIGUOUS_SET+=("$file")
  fi
done

if [[ "$AMBIGUOUS" -eq 1 ]]; then
  echo "result=AMBIGUOUS"
  echo "thread_key=$THREAD_KEY"
  for file in "${AMBIGUOUS_SET[@]}"; do
    echo "candidate=$file"
  done
  exit 0
fi

emit_found "thread_scan" "$BEST_FILE"
