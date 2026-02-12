---
name: command-plan-task
description: Use this skill only when the user explicitly asks to invoke. Create a new thread-bound PR document by extracting task context from conversation and filling reference templates, then delegate to rule-find-task.
---

# Plan Task Command

## When to Use
- Use this skill only when the user explicitly asks to invoke `$command-plan-task`.
- Use when the user wants a new PR task document created from the current conversation.

## Goals
- Create one PR source file under `./.vscode/pull-request-task/${thread_key}/`.
- Delegate continuation to `$rule-find-task` after creation.
- Keep PR as internal execution memory, not as RD-facing review document.
- Capture only minimal planning state needed for staged execution.
- Seed requirement clarification items for implementation-risk confirmation.
- Complete CR decomposition inside `Requirement Definition` (no separate stage at creation time).

## Inputs
- Current conversation content.
- Optional explicit title/description from user.
- Optional explicit `thread_key`.
- Optional file paths provided by user for requirement extraction.

## Thread Binding
Resolve `thread_key` in this order:
1. `CODEX_THREAD_ID`
2. Explicit caller value (`thread_key` or `conversation_id`)
3. Generated UUID for first-time initialization

## File Paths
- Root: `./.vscode/pull-request-task/`
- Thread directory: `./.vscode/pull-request-task/${thread_key}/`
- Source file: `./.vscode/pull-request-task/${thread_key}/PR_${task_slug}.md`

## Reference Templates
Use these references to build files:
1. `./skills/command-plan-task/references/pr_source_template.md`
2. `./skills/command-plan-task/references/extraction_contract.md`

## Conversation Extraction Contract
Before writing files, extract and normalize:
1. `title`: concise task title.
2. `description`: 1-2 sentence context summary.
3. `business_goal`: complete sentence describing intended business impact.
4. `out_of_scope`: explicit non-goals; if unknown use `- None identified yet.`
5. `planning_notes`: concise internal memory notes (optional).
6. `referenced_files`: file evidence from user-provided paths.
7. `open_questions`: unresolved requirement questions.
8. `clarification_items`: implementation-risk clarification items with status.
9. `acceptance_tests`: 2-8 testable statements.
10. `critical_invariants`: 1-5 invariants.
11. `initial_cr_rows`: at least one CR row, with explicit `Scope Seq` and `CR Type`.

Rules:
1. Never leave `Business Goal` blank.
2. Do not use placeholders like `TBD` or `as discussed`.
3. Keep extraction faithful to user intent; do not invent business logic.
4. When user provides files, read those files first and use them as the primary source for planning.
5. Keep planning notes concise; PR is memory, not human review artifact.
6. Perform CR decomposition inside `Requirement Definition`; do not create a separate `CR Decomposition` stage.
7. Enforce scope-level test-first planning: each scope must start with a `test` CR before any `impl` CR.
8. Do not generate `impl` CR rows for a scope unless a preceding `test` CR row exists in the same scope.
9. Seed initial clarification items for known implementation risks; max 3 items at creation.

## Command Workflow
1. Resolve `thread_key`.
2. Collect user-provided file paths from conversation (if any) and read relevant content before drafting.
3. Extract required fields from conversation and file evidence using `references/extraction_contract.md`.
4. Derive metadata:
   - `pr_id` (UTC timestamp-based identifier)
   - `task_slug` (filesystem-safe from title)
   - `created_at` and `updated_at` in ISO8601 UTC
5. Build initial CR Checklist rows in the same pass.
   - Ensure each scope sequence starts with `CR Type=test`.
   - Ensure all implementation rows use `CR Type=impl` and appear after the scope test row.
6. Load `references/pr_source_template.md` and fill placeholders for minimal PR memory schema.
7. Write source file `PR_${task_slug}.md`; if filename collision occurs, append suffix (`-02`, `-03`, ...).
8. Initialize stage as `Requirement Definition`, then delegate to `$rule-find-task` with the created source path.
9. Let `$rule-execute-task` infer and update later stage transitions from conversation and PR state automatically.

## Constraints
- Do not use scripts to create PR files in this command.
- Keep `PR_${task_slug}.md` as the only executable state source.
- Keep PR Change Card within limits: max 25 lines.
- Keep Requirement Memory (`planning_notes`, `referenced_files`, `open_questions`, `clarification_items`) within 28 lines total.
- Keep Acceptance Tests within limits: max 10 acceptance tests, max 5 invariants.
- Keep CR Checklist within limits: max 20 CR rows.
- Ensure CR Checklist uses `Scope Seq` and `CR Type`.
- Ensure each scope has a committed path that starts with test-first planning (`test` before `impl`).
- Clarification items must be decision-oriented and concise.

## Output Expectations
- Return absolute `source_path`.
- Confirm handoff to `$rule-find-task`.
