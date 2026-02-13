# Extraction Contract for `command-plan-task`

Use this contract to transform conversation context into deterministic PR memory fields.

## Field Definitions

1. `title`
- Short and concrete.
- Prefer verb + object form.
- Example: `Add scope-level test-first checkout validation`

2. `description`
- 1-2 sentences only.
- Summarize context and why this task exists.

3. `business_goal`
- One complete sentence.
- Must describe observable impact.
- Must not be empty.

4. `out_of_scope_lines`
- Markdown bullet lines.
- If unknown, use:
  - `- None identified yet.`

5. `architecture_gate` booleans
- Use `Yes` or `No`:
  - `schema_change`
  - `auth_permission_change`
  - `cross_service_contract_change`
  - `critical_invariant_impact`
  - `migration_required`
  - `rollback_path_defined`

6. `planning_notes_lines`
- Optional markdown bullet lines.
- Keep concise implementation memory only (for example touched module hints, assumptions, dependency notes).
- Use `- None at this stage.` when no useful notes.

7. `referenced_files_lines`
- Bullet lines of file paths explicitly provided by user or discovered from request context.
- If none, use `- None provided.`
- When files are provided, extract requirements from those files before planning.

8. `open_questions_lines`
- Bullet lines for unresolved items that block implementation or validation.
- If none, use `- None at this stage.`

9. `clarification_items_lines`
- Bullet lines with status tag and decision context.
- Format examples:
  - `- [open][blocking=yes] Q-001 | Risk: <risk> | Impact: <impact> | Default: <proposal> | Need: <user decision>`
  - `- [resolved] Q-001 | Decision: <final decision> | By: user`
  - `- [accepted-risk] Q-002 | Decision: <accepted with reason> | By: user`
- At creation time: 0-3 items.
- Include only high-value implementation-risk questions.
- Avoid low-signal or generic questions.

10. `acceptance_tests_lines`
- Numbered markdown lines (`1.`, `2.`, ...).
- Between 2 and 8 lines.
- Must be testable statements.

11. `critical_invariants_lines`
- Numbered markdown lines (`1.`, `2.`, ...).
- Between 1 and 5 lines.

12. `cr_rows`
- Pipe-table rows matching:
  `| CR-001 | A | 1 | test | <goal> | Fast | todo |  |  |`
- At least one row.
- Required columns:
  - `Scope` (for example `A`, `B`)
  - `Scope Seq` (integer starting from `1` inside each scope)
  - `CR Type` (`test` or `impl`)
- `CR Type=impl` is not allowed before a `CR Type=test` row in the same scope.

## Normalization Rules

1. Never use placeholders like `TBD`, `N/A`, or `as discussed`.
2. Do not invent business-domain details not present in conversation or referenced files.
3. Keep terms consistent across title, goal, acceptance tests, and CR rows.
4. Keep generated content concise and machine-friendly.
5. Requirement Definition memory must include:
   - PR Change Card fields (`business_goal`, `out_of_scope_lines`, `architecture_gate`)
   - `clarification_items_lines`
   - `acceptance_tests_lines`
   - `critical_invariants_lines`
   - `cr_rows`
6. Clarification loop readiness:
   - Any `blocking=yes` item with status `open` prevents leaving `Requirement Definition`.
   - Prefer explicit user decision over inferred assumptions.
7. Enforce scope-level test-first decomposition:
   - Every scope starts with a `test` CR row at `Scope Seq=1`.
   - No `impl` CR row is valid unless a preceding `test` CR exists in the same scope.
