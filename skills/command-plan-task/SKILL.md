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

## Command Workflow
1. Resolve `thread_key`.
2. Derive `task_slug` from title/description using a filesystem-safe format.
3. Create a new PR source file `${task_slug}.md` using the fixed PR template in this document.
4. Create `${task_slug}_TW.md` by translating the source file for RD review.
5. If slug collision happens, append a stable suffix (for example `-02` or short `pr_id`) and retry.
6. Immediately delegate to `$rule-find-task`, which will locate the active PR and invoke `$rule-execute-task`.

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
Use this exact structure when creating `${task_slug}.md`:

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

## Output Expectations
- Return the absolute path of the created source PR file.
- Return the absolute path of the generated `_TW` mirror.
- Confirm that control has been handed off to `$rule-find-task`.
