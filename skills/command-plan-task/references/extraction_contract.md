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

9. `problem_statement`
- 2-4 sentences.
- Describe current pain point and expected solved state.

10. `business_context`
- 2-5 sentences.
- Include business domain background and why this change matters now.

11. `user_roles_lines`
- Bullet lines.
- List actors, owners, and affected stakeholders.
- At least 2 items when context allows.

12. `detailed_business_logic_lines`
- Numbered lines.
- Capture end-to-end business logic steps and decision branches.
- Target 4-10 steps.

13. `functional_requirements_lines`
- Numbered lines.
- Must be testable and concrete.
- Target 4-12 requirements.

14. `non_functional_requirements_lines`
- Bullet lines.
- Include latency, reliability, auditability, security, compliance, and operability if applicable.
- Use `- None identified yet.` only when truly unknown.

15. `decision_rules_lines`
- Numbered lines.
- Include thresholds, validation rules, allowed/disallowed transitions, and fallback behavior.

16. `process_flow_lines`
- Numbered lines representing business flow.
- Each line should be an actionable step in sequence.

17. `edge_cases_lines`
- Bullet lines for exceptional paths.
- Include failure modes, retries, invalid inputs, and data conflicts.

18. `question_summary`
- 1-2 sentences summarizing the user prompt in neutral language.

19. `referenced_files_lines`
- Bullet lines of file paths explicitly provided by user or discovered from request context.
- If none, use `- None provided.`
- When files are provided, extract spec details from those files before drafting business logic.

20. `open_questions_lines`
- Bullet lines for unresolved items that block implementation or validation.
- If none, use `- None at this stage.`

## Normalization Rules

1. Never use placeholders like `TBD`, `N/A`, or `as discussed`.
2. Do not invent business domain details not present in conversation.
3. Keep terms consistent across title, goal, acceptance tests, and CR rows.
4. Keep generated content concise and reviewable.
5. Prioritize user-provided files as source-of-truth context when available.
6. Mark every uncertain statement as an assumption instead of presenting it as fact.
