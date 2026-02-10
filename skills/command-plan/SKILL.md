---
name: command-plan
description: Create a concise execution plan for coding tasks using task-contract thinking, risk classification, and risk-based TDD + verification-first acceptance criteria. Use this skill only when the user explicitly asks to invoke or use the `command-plan` skill.
---

# Planning Workflow Skill

## When to Use
- Use this skill only when the user explicitly asks to invoke or use the `command-plan` skill.
- Use when implementation should be paused and a high-signal plan is required first.

## Goals
- Produce a concise, decision-ready plan.
- Minimize ambiguity before coding starts.
- Keep plans executable, testable, and easy to review.

## Output Artifact
Use `references/plan-template.md` as the default structure.

Recommended path:
- `tmp/workflow/<task-slug>/PLAN.md`

If repository conventions already define a planning file, follow that convention instead.

## Planning Steps
1. Summarize objective and scope in a short task contract snapshot.
2. Record up to three explicit assumptions.
3. Identify impacted files or modules.
4. Define implementation steps with clear ordering.
5. Define risk level, TDD mode, and required verification checks.
6. List open questions only when they block safe execution.

## TDD Policy (Risk-Based)
- Low risk:
  - TDD is optional.
  - Test-after implementation or manual verification is allowed.
- Medium risk:
  - TDD is required for new or changed business logic in touched areas.
  - Plan the Red -> Green -> Refactor loop for each behavior-changing acceptance criterion.
- High risk:
  - TDD is required for all behavior-changing logic plus critical edge cases.
  - Plan explicit failing-test-first evidence and final passing evidence.

If failing test-first execution is blocked by environment or external dependency constraints:
- Document the blocker clearly in the plan.
- Define the nearest safe fallback (for example, contract/characterization tests before merge).
- Record residual risk and mitigation.

## Quality Bar for a Good Plan
- Every acceptance criterion is measurable.
- Each implementation step maps to at least one acceptance criterion.
- Medium/high-risk plans include acceptance-criterion-to-test mapping.
- Verification commands/checklists are included.
- Medium/high-risk plans include TDD evidence capture points.
- Risks and rollback approach are stated for medium/high-risk tasks.
- Plan length remains concise; avoid speculative design details.

## Escalation Policy
Ask before implementation only when:
- Security/privacy/auth boundaries are unclear.
- Money/order/data-loss risk exists.
- Competing interpretations would produce materially different behavior.

Otherwise, proceed with safest assumptions and document them.

## Hard Rules
- Follow `rule-global` rule priority, language policy, and security baseline.
- Keep repository artifacts in English.
- Do not introduce new dependencies during planning.
- Do not skip mandatory medium/high-risk TDD gates unless the user explicitly approves an exception.
