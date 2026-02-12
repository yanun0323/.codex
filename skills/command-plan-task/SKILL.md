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
- Create a `_TW` mirror for RD review from the same extracted task context.
- Delegate continuation to `$rule-find-task` after creation.
- Produce a detailed business-specification section from user question and provided files.
- Analyze existing code before drafting business logic and CR planning.
- Complete CR decomposition inside `Requirement Definition` (no separate stage at creation time).

## Inputs
- Current conversation content.
- Optional explicit title/description from user.
- Optional explicit `thread_key`.
- Optional file paths provided by user for business-spec extraction.

## Thread Binding
Resolve `thread_key` in this order:
1. `CODEX_THREAD_ID`
2. Explicit caller value (`thread_key` or `conversation_id`)
3. Generated UUID for first-time initialization

## File Paths
- Root: `./.vscode/pull-request-task/`
- Thread directory: `./.vscode/pull-request-task/${thread_key}/`
- Source file: `./.vscode/pull-request-task/${thread_key}/${task_slug}.md`
- Mirror file: `./.vscode/pull-request-task/${thread_key}/${task_slug}_TW.md`

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
5. `acceptance_tests`: 2-8 testable statements.
6. `critical_invariants`: 1-5 invariants.
7. `problem_statement`: clear current problem and desired outcome.
8. `business_context`: background and constraints.
9. `user_roles`: impacted actors and owners.
10. `existing_code_analysis`: summary of current code behavior, boundaries, and touched modules/files.
11. `detailed_business_logic`: step-by-step business logic with branching rules.
12. `functional_requirements`: concrete feature requirements.
13. `non_functional_requirements`: reliability/performance/security/operability requirements.
14. `decision_rules`: deterministic rule set and boundary conditions.
15. `process_flow`: ordered business flow.
16. `edge_cases`: exceptional scenarios and failure handling.
17. `requirement_definition_cr_plan`: ordered CR plan produced during requirement definition.
18. `question_summary`: neutral summary of user request.
19. `referenced_files`: file evidence from user-provided paths.
20. `open_questions`: unresolved requirement questions.
21. `initial_cr_rows`: at least one CR row, with explicit `Scope Seq` and `CR Type`.

Rules:
1. Never leave `Business Goal` blank.
2. Do not use placeholders like `TBD` or `as discussed`.
3. Keep extraction faithful to user intent; do not invent business logic.
4. When user provides files, read those files first and use them as the primary source for business logic and business requirements.
5. Analyze relevant existing code before finalizing business logic and CR plan.
6. Perform CR decomposition inside `Requirement Definition`; do not create a separate `CR Decomposition` stage.
7. Enforce scope-level test-first planning: each scope must start with a `test` CR before any `impl` CR.
8. Do not generate `impl` CR rows for a scope unless a preceding `test` CR row exists in the same scope.

## Command Workflow
1. Resolve `thread_key`.
2. Collect user-provided file paths from conversation (if any) and read relevant content before drafting.
3. Analyze existing code paths related to the request and capture findings in `existing_code_analysis`.
4. Extract required fields from conversation and file evidence using `references/extraction_contract.md`.
5. Derive metadata:
   - `pr_id` (UTC timestamp-based identifier)
   - `task_slug` (filesystem-safe from title)
   - `created_at` and `updated_at` in ISO8601 UTC
6. Build `requirement_definition_cr_plan` and initial CR Checklist rows in the same pass.
   - Ensure each scope sequence starts with `CR Type=test`.
   - Ensure all implementation rows use `CR Type=impl` and appear after the scope test row.
7. Load `references/pr_source_template.md` and fill placeholders, including `# Business Specification` sections.
8. Write source file `${task_slug}.md`; if filename collision occurs, append suffix (`-02`, `-03`, ...).
9. Build `_TW` mirror by translating headings and narrative text to Traditional Chinese while preserving metadata keys, enum-like values, IDs, and table structure.
10. Initialize stage as `Requirement Definition`, then delegate to `$rule-find-task` with the created source path.
11. Let `$rule-execute-task` infer and update later stage transitions from conversation and PR state automatically.

## Constraints
- Do not use scripts to create PR files in this command.
- Keep `${task_slug}.md` as the only executable state source.
- Keep `${task_slug}_TW.md` as review-only mirror.
- Keep PR Change Card within limits: max 35 lines.
- Keep Acceptance Tests within limits: max 10 acceptance tests, max 5 invariants.
- Keep CR Checklist within limits: max 20 CR rows.
- Ensure `# Business Specification` is detailed and grounded in user question/files.
- Ensure `existing_code_analysis` and `requirement_definition_cr_plan` are populated before handoff.
- Ensure CR Checklist uses `Scope Seq` and `CR Type`.
- Ensure each scope has a committed path that starts with test-first planning (`test` before `impl`).

## Output Expectations
- Return absolute `source_path`.
- Return absolute `mirror_path`.
- Confirm handoff to `$rule-find-task`.
