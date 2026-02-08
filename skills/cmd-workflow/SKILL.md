---
name: cmd-workflow
description: Primary end-to-end workflow for repo changes - intake + TASK_CONTRACT/QUALITY_PROFILE docs + risk-based TDD build loop + critic verification + REVIEW_PACKET handoff. Use this skill only when the user explicitly asks to invoke or use the `workflow` skill.
---

# Exception-Driven Delivery Workflow

## When to Use
- Use this skill only when the user explicitly asks to invoke or use the `workflow` skill.
- Use for delivery tasks where the team wants high correctness with low developer interruption.

## Goals
- Reduce developer cognitive load by escalating only high-value decisions.
- Increase execution correctness through machine-verifiable quality gates.
- Shift validation left with risk-based TDD before review.
- Keep delivery fast by letting low-risk work proceed autonomously.

## Required Inputs
- User task request and constraints.
- Existing repo conventions and domain skills (`agents-go`, `agents-solid`, `agents-ui`, `agents-infra`, `agents-make`) when relevant.
- Current verification commands available in the repo.

## Artifact Set
Use these templates from `references/`:
- `task-contract-template.md`
- `quality-profile-template.md`
- `review-packet-template.md`

Default artifact path:
- `tmp/workflow/<task-slug>/TASK_CONTRACT.md`
- `tmp/workflow/<task-slug>/QUALITY_PROFILE.md`
- `tmp/workflow/<task-slug>/REVIEW_PACKET.md`

If the repo already has a task-doc convention, follow it instead.

## Stage 0 - Task Contract Gate
Objective:
- Align on scope and acceptance criteria before implementation.

Actions:
1. Create `TASK_CONTRACT` from template.
2. Define measurable acceptance criteria.
3. Mark out-of-scope items.
4. Record assumptions and confidence.

Exit Criteria:
- Every acceptance criterion has a concrete verification method.
- Scope boundaries are explicit.
- Confidence is stated.

## Stage 1 - Risk and Quality Profile Gate
Objective:
- Convert quality expectations into explicit checks.

Actions:
1. Classify risk level: `Low`, `Medium`, or `High`.
2. Create `QUALITY_PROFILE` from template.
3. Select TDD enforcement mode from risk level:
   - Low: TDD optional.
   - Medium: Test-first for touched business logic.
   - High: Test-first for all behavior-changing logic and critical edge cases.
4. Map each quality rule and TDD gate to a verification command or checklist item.
5. Define rollback strategy for medium/high risk.

Exit Criteria:
- Required gates are defined for the chosen risk level.
- Required TDD obligations are explicit for the chosen risk level.
- Verification commands and success criteria are documented.

## Stage 2 - Autonomous Build Loop (TDD-Aware)
Objective:
- Implement efficiently without unnecessary developer review cycles.

Actions:
1. Run internal role loop: Architect -> Builder -> Critic.
2. For medium/high risk, execute Red -> Green -> Refactor per behavior change:
   - Write failing test(s) first for targeted acceptance criteria.
   - Implement minimal code to pass.
   - Refactor while keeping tests green.
3. For low risk, test-first is optional and test-after is acceptable.
4. Make incremental code changes with minimal scope.
5. If test-first is blocked, document the blocker, fallback verification, and risk impact.
6. Use pseudo code/comments only for complex logic handoff, then remove temporary comments before final handoff.
7. Keep assumptions synchronized with the task contract.

Exit Criteria:
- Implementation matches acceptance criteria and scope.
- Required medium/high-risk TDD evidence is captured.
- No unresolved critic findings remain at the current iteration.

## Stage 3 - Critic and Verification Loop
Objective:
- Validate correctness before human review.

Actions:
1. Run all required checks from `QUALITY_PROFILE`.
2. Fix failures and rerun until passing.
3. Record evidence for each gate, including TDD red/green evidence where required.
4. If checks cannot run in the environment, record exact commands and expected outcomes.

Exit Criteria:
- All mandatory gates pass, or blocked checks are explicitly documented with reason and impact.

## Stage 4 - Exception-Only Escalation
Objective:
- Ask the developer only when judgment is required.

Escalate only if one of these is true:
- Security/auth/privacy boundary ambiguity.
- Data-loss or irreversible migration risk.
- Business rule conflict that changes expected behavior.
- Confidence below safe threshold after investigation.

Escalation format:
1. Decision required (single sentence).
2. Recommended option and tradeoff.
3. Alternative option and tradeoff.

## Stage 5 - Review Packet Handoff
Objective:
- Provide a decision-ready summary for fast developer review.

Actions:
1. Create `REVIEW_PACKET` from template.
2. Include behavior diff, verification evidence, and residual risks.
3. Link each acceptance criterion to evidence.

Exit Criteria:
- Developer can approve/reject without re-reading full implementation history.

## Stage 6 - Post-Merge Calibration (Optional but Recommended)
Objective:
- Improve workflow quality over time.

Track:
- First-pass acceptance rate.
- Defect leakage after merge.
- Developer interruption count per task.
- Rework caused by requirement misunderstanding.
- TDD compliance rate by risk level.

Use findings to tune:
- Risk thresholds.
- Gate strictness.
- TDD gate policy.
- Escalation triggers.

## Hard Rules
- Follow `agents-global` priority, security, and language policies.
- Do not introduce new dependencies without explicit approval.
- Never hardcode secrets or expose sensitive internals in outputs.
- Keep repository artifacts in English.
- Do not skip required medium/high-risk TDD gates unless the user explicitly approves an exception.
