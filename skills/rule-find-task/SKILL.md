---
name: rule-find-task
description: Always load this skill for any task. Lightweight always-read rule that runs scripts/find_pr_task.sh to discover or rebind a PR task file and invokes rule-execute-task only when found.
---

# Find Task Rule


## Goals
- Keep token usage low by using a bash script for discovery and rebinding logic.
- Resolve one active PR source file for current conversation `thread_key`.
- Invoke `$rule-execute-task` only when a valid PR source file is found.
- Let `$rule-execute-task` infer and update stage automatically from conversation and PR content.

## Script
- Path: `scripts/find_pr_task.sh`
- Purpose: resolve one source PR file, optionally rebind cross-thread files, and return structured `key=value` output.
- Naming convention:
  - Source PR file: `PR_*.md`

## Required Inputs
- `thread_key` (or `CODEX_THREAD_ID`)
- Optional explicit PR file path from conversation context
- Task root path (default `./.vscode/pull-request-task/`)

## Execution
1. Resolve `thread_key`:
   - `CODEX_THREAD_ID`
   - explicit `thread_key` or `conversation_id`
2. Run finder script:
   - Thread scan mode:
     - `bash scripts/find_pr_task.sh --root ./.vscode/pull-request-task --thread-key "$thread_key"`
   - Explicit path mode with rebinding:
     - `bash scripts/find_pr_task.sh --root ./.vscode/pull-request-task --thread-key "$thread_key" --explicit-path "$pr_path" --rebind`
3. Parse output `result=` and branch:
   - `FOUND`: invoke `$rule-execute-task` with `resolved_path`
   - `NOT_FOUND`: no-op and continue normal non-workflow behavior
   - `AMBIGUOUS`: ask user to choose one candidate
   - `ERROR`: surface `message` and stop workflow invocation
4. Do not wait for explicit stage-change commands from user; pass control immediately so `$rule-execute-task` can infer and update stage.

## Output Contract
- `result=FOUND|NOT_FOUND|AMBIGUOUS|ERROR`
- `resolved_path=<absolute_source_md_path>` when found
- `source=explicit|explicit_rebound|thread_scan` when found
- `status=<status_from_frontmatter>` when found
- `candidate=<absolute_path>` repeated for ambiguous results
- `message=<error_message>` for errors

## Boundary
- This rule does not execute stage logic.
- This rule does not initialize new PR files.
- New PR creation belongs to `$command-plan-task`.
