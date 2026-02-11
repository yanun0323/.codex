---
name: command-plan-task
description: Use this skill only when the user explicitly asks to invoke. Initialize a thread-bound PR task document and then delegate continuation to rule-find-task.
---

# Plan Task Command

## When to Use
- Use this skill only when the user explicitly asks to invoke `$command-plan-task`.
- Use when the user wants to start a new task workflow in the current conversation and create a fresh PR task document.

## Goals
- Create one new PR source file under `./.vscode/pull-request-task/${thread_key}/`.
- Create and keep a Traditional Chinese mirror file in sync for RD review.
- Delegate all workflow execution logic to `$rule-find-task` without duplicating rule logic in this command.

## Inputs
- Conversation context that describes the task intent.
- Optional explicit task title and description.
- Optional explicit `thread_key` from caller.
- Optional explicit PR template fields (if user provides them).

## Thread Binding
Resolve `thread_key` in this order:
1. `CODEX_THREAD_ID`
2. Explicit caller value (`thread_key` or `conversation_id`)
3. Generated UUID for first-time initialization

## File Paths
- Root: `./.vscode/pull-request-task/`
- Thread directory: `./.vscode/pull-request-task/${thread_key}/`
- Source of truth file: `./.vscode/pull-request-task/${thread_key}/${task_slug}.md`
- RD mirror file: `./.vscode/pull-request-task/${thread_key}/${task_slug}_TW.md`

## Script
- Path: `./skills/command-plan-task/scripts/init_pr_task.sh`
- Purpose: initialize a new thread-bound PR source file and `_TW` mirror with deterministic metadata and template.

## Command Workflow
1. Resolve `thread_key`.
2. Run init script:
   - `bash ./skills/command-plan-task/scripts/init_pr_task.sh --root ./.vscode/pull-request-task --thread-key "$thread_key" --title "$task_title" --description "$task_description"`
3. Parse script output:
   - `result=CREATED` with `source_path` and `mirror_path`
   - `result=ERROR` with `message`
4. Delegate to `$rule-find-task` with the returned `source_path`, then continue via `$rule-execute-task` when found.

## Required Metadata in Source File
- `workflow_version`
- `pr_id`
- `thread_key`
- `title`
- `task_slug`
- `stage`
- `status`
- `created_at`
- `updated_at`

## Fixed PR Template (Source File)
`init_pr_task.sh` creates `${task_slug}.md` with this structure:

```md
---
workflow_version: v2
pr_id: PR-YYYYMMDD-001
thread_key: <thread_key>
title: <title>
task_slug: <task_slug>
stage: A
status: active
created_at: <ISO8601>
updated_at: <ISO8601>
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
```

## Constraints
- Do not duplicate any stage execution logic that belongs to `$rule-find-task` or `$rule-execute-task`.
- Keep `${task_slug}.md` as the only executable state source.
- `${task_slug}_TW.md` is a review-only mirror and must never become state authority.
- Keep the PR skeleton concise: max 25 lines for Change Card, max 8 acceptance tests, max 5 invariants, max 10 CR rows.
- Use `./skills/command-plan-task/scripts/init_pr_task.sh` for initialization instead of embedding creation logic in prompts.
- Do not call `./skills/rule-find-task/scripts/find_pr_task.sh` from this command.

## Output Expectations
- Return `source_path` and `mirror_path` from the init script output.
- Confirm that control has been handed off to `$rule-find-task`.
