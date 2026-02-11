# Extraction Contract for `command-plan-task`

Use this contract to transform conversation context into deterministic PR fields.

## Field Definitions

1. `title`
- Short and concrete.
- Prefer verb + object form.
- Example: `Define staged CR workflow for RD-gated commits`

2. `description`
- 1-2 sentences only.
- Summarize context and why this PR exists.

3. `business_goal`
- One complete sentence.
- Must describe measurable or observable impact.
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

6. `acceptance_tests_lines`
- Numbered markdown lines (`1.`, `2.`, ...).
- Between 2 and 8 lines.
- Must be testable statements.

7. `critical_invariants_lines`
- Numbered markdown lines (`1.`, `2.`, ...).
- Between 1 and 5 lines.

8. `cr_rows`
- Pipe-table rows matching:
  `| CR-001 | A | <goal> | Fast | todo |  |  |`
- At least one row.

## Normalization Rules

1. Never use placeholders like `TBD`, `N/A`, or `as discussed`.
2. Do not invent business domain details not present in conversation.
3. Keep terms consistent across title, goal, acceptance tests, and CR rows.
4. Keep generated content concise and reviewable.
