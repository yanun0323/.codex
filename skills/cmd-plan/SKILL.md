---
name: cmd-plan
description: Create a concise execution plan for coding tasks using task-contract thinking, risk classification, and verification-first acceptance criteria. Use this skill only when the user explicitly asks to invoke or use the `plan` skill.
---

# Planning Workflow Skill

## When to Use
- Use this skill only when the user explicitly asks to invoke or use the `plan` skill.
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
5. Define risk level and required verification checks.
6. List open questions only when they block safe execution.

## Quality Bar for a Good Plan
- Every acceptance criterion is measurable.
- Each implementation step maps to at least one acceptance criterion.
- Verification commands/checklists are included.
- Risks and rollback approach are stated for medium/high-risk tasks.
- Plan length remains concise; avoid speculative design details.

## Escalation Policy
Ask before implementation only when:
- Security/privacy/auth boundaries are unclear.
- Money/order/data-loss risk exists.
- Competing interpretations would produce materially different behavior.

Otherwise, proceed with safest assumptions and document them.

## Hard Rules
- Follow `agents-global` rule priority, language policy, and security baseline.
- Keep repository artifacts in English.
- Do not introduce new dependencies during planning.
