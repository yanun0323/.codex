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
10. `detailed_business_logic`: step-by-step business logic with branching rules.
11. `functional_requirements`: concrete feature requirements.
12. `non_functional_requirements`: reliability/performance/security/operability requirements.
13. `decision_rules`: deterministic rule set and boundary conditions.
14. `process_flow`: ordered business flow.
15. `edge_cases`: exceptional scenarios and failure handling.
16. `question_summary`: neutral summary of user request.
17. `referenced_files`: file evidence from user-provided paths.
18. `open_questions`: unresolved requirement questions.
19. `initial_cr_rows`: at least one CR row.

Rules:
1. Never leave `Business Goal` blank.
2. Do not use placeholders like `TBD` or `as discussed`.
3. Keep extraction faithful to user intent; do not invent business logic.
4. When user provides files, read those files first and use them as the primary source for business logic and business requirements.

## Command Workflow
1. Resolve `thread_key`.
2. Collect user-provided file paths from conversation (if any) and read relevant content before drafting.
3. Extract required fields from conversation and file evidence using `references/extraction_contract.md`.
4. Derive metadata:
   - `pr_id` (UTC timestamp-based identifier)
   - `task_slug` (filesystem-safe from title)
   - `created_at` and `updated_at` in ISO8601 UTC
5. Load `references/pr_source_template.md` and fill placeholders, including `# Business Specification` sections.
6. Write source file `${task_slug}.md`; if filename collision occurs, append suffix (`-02`, `-03`, ...).
7. Build `_TW` mirror by translating headings and narrative text to Traditional Chinese while preserving metadata keys, enum-like values, IDs, and table structure.
8. Delegate to `$rule-find-task` with the created source path.

## Constraints
- Do not use scripts to create PR files in this command.
- Keep `${task_slug}.md` as the only executable state source.
- Keep `${task_slug}_TW.md` as review-only mirror.
- Keep PR Change Card within limits: max 25 lines, max 8 acceptance tests, max 5 invariants, max 15 CR rows.
- Ensure `# Business Specification` is detailed and grounded in user question/files.

## Output Expectations
- Return absolute `source_path`.
- Return absolute `mirror_path`.
- Confirm handoff to `$rule-find-task`.
