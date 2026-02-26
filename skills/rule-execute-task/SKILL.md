---
name: rule-execute-task
description: Execute staged PR workflow only when invoked by rule-find-task after a PR source file has been resolved.
---

# Execute Task Rule


## Inputs (Required)
- Absolute path to resolved PR source file returned by `scripts/find_pr_task.sh`
- Current PR metadata and sections from the source file.
- Latest conversation messages for approval and stage-inference signals.
- CR Checklist table with columns:
  - `CR-ID`
  - `Scope`
  - `Scope Seq`
  - `CR Type (test/impl)`
  - `Goal`
  - `Path(Fast/Guarded)`
  - `Status`
  - `Evidence Link`
  - `Commit Hash`

## Goals
- Continue workflow from the PR file's current `stage` and `status`.
- Enforce that every CR is RD-reviewed before commit.
- Treat PR source file as internal workflow memory; RD review happens from code diff and agent explanations.

## Workflow Stages
1. Stage `Requirement Definition`: define requirements and business logic, analyze existing code, and complete CR decomposition in the same stage.
2. Stage `CR Implementation`: CR implementation loop.
3. Stage `Validation`: final validation and merge readiness.

## Stage Transition Table
| Current Stage | Exit Condition | Next Stage |
|---|---|---|
| `Requirement Definition` | PR Change Card fields are complete, acceptance/invariant checks are defined, CR checklist/decomposition is complete, and requirement clarification has no open blocking items with RD-aligned feedback | `CR Implementation` |
| `CR Implementation` | All CR rows are `committed` | `Validation` |
| `Validation` | Final validation complete and RD approves merge | done |

## Automatic Stage Management
Stage updates must be automatic and inferred by the agent. Explicit user commands like "change stage" are not required.

Inference rules:
1. Normalize legacy stage values (`A/B/C/D`) to named stages (`Requirement Definition` / `CR Implementation` / `Validation` / `done`) when loading PR files.
2. While in `Requirement Definition`, keep stage unchanged until all are true:
   - `Business Goal` is populated.
   - `Architecture Gate` fields are all set to `Yes` or `No`.
   - `Acceptance Tests` and `Critical Invariants` are populated.
   - CR decomposition is populated in `CR Checklist`.
   - `Clarification Items` has no `open` entry with `blocking=yes`.
   - Latest user/RD feedback does not request additional requirement-definition changes.
3. Move to `CR Implementation` immediately when rule 2 is satisfied.
4. Move to `Validation` when every CR row is `committed`.
5. Move to `done` when validation evidence is complete and RD gives merge approval.
6. If later conversation feedback changes requirements or introduces new blocking ambiguity, automatically move stage back to `Requirement Definition` and update PR sections.

## Requirement Clarification Loop (Requirement Definition)
Before exiting `Requirement Definition`, run clarification loop:
1. Perform implementation-risk scan against current requirements, invariants, and planned CR order.
2. Raise at most 3 clarification questions per round.
3. Each question must include:
   - Risk
   - Impact
   - Default proposal
   - Decision needed from user
   - Blocking flag (`yes` or `no`)
4. Ask user in chat and wait for response.
5. Update `Clarification Items` statuses in PR memory:
   - `open`
   - `resolved`
   - `accepted-risk`
6. If an item is `open` and `blocking=yes`, do not leave `Requirement Definition`.
7. Maximum 2 rounds; if still unresolved, request explicit user decision and mark outcome.

## Scope Test-First Gate
Before starting any `impl` CR, enforce all conditions:
1. A `test` CR exists in the same `Scope`.
2. That `test` CR has a lower `Scope Seq` than the target `impl` CR.
3. That `test` CR status is `committed`.
4. The `test` CR has evidence showing test code creation or update for the same scope intent.

If any condition fails:
1. Do not start the `impl` CR.
2. Mark the implementation CR as blocked (or keep `todo`) and add a note in evidence/comments.
3. Request creation/completion of the missing scope `test` CR first.

## CR Status Transition Table
| Current Status | Trigger | Next Status |
|---|---|---|
| `todo` | Agent starts CR | `in_progress` |
| `in_progress` | Agent submits evidence for review | `in_review` |
| `in_review` | RD requests changes | `changes` |
| `changes` | Agent updates and resubmits | `in_review` |
| `in_review` | RD approves then agent commits without further edits | `committed` |

Rules:
1. If content changes after RD approval signal and before commit hash write, status must return to `in_review`.
2. Commit hash is written only after commit is finished.
3. `committed` is immutable unless RD explicitly reopens the CR.

## Stage `CR Implementation` Fixed Loop
`Pick next CR -> Apply scope test-first gate -> Agent implements -> Run checks -> Explain implementation to RD -> Wait RD decision -> Commit -> Update Checklist -> Next CR`

RD decision values:
- `approved`: `approved` or `approve`
- `changes`: `changes` or `change` or other decision, feedback, modify request

## Fast vs Guarded
- Both paths require RD review.
- Fast path uses minimal evidence.
- Guarded path requires deeper evidence and deeper review.

## Evidence Contract per CR Review
Required fields:
1. `CR-ID`
2. `Summary` (1-2 lines)
3. `Checks Run` (fixed standard commands)
4. `Result` (`PASS` or `FAIL`)
5. `Key Output` (one line)
6. `Evidence Link` (CI/artifact/log path or URL)

Do not paste long raw logs in review threads.

## Mandatory CR Explanation (Pair-Programming Style)
After each CR implementation and before RD decision, the agent must explain in chat (not only in PR file):
1. `Where changed`: key files/modules and what logic was added or modified.
2. `Why implemented this way`: design intent and code-level rationale.
3. `Business logic considered`: rules, invariants, and edge cases handled.
4. `Tradeoffs`: alternatives considered and why rejected.
5. `Risk check`: possible regressions and how current checks/tests mitigate them.

This explanation is mandatory for every CR review cycle, including resubmissions after `changes`.

## DoD Before RD Review
Each CR must be:
1. Buildable
2. Testable
3. Revertable by default
4. Independently understandable
5. Not partial
6. For `impl` CRs: scope-level test-first gate must be satisfied.

## High-Risk Exceptions
For migration/schema/contract-breaking or irreversible operations:
1. Require explicit runbook.
2. Require non-git-revert rollback strategy.
3. Require extra reviewer.

## Git Constraints
1. Preserve CR commit history.
2. Disallow rebase merge.
3. Disallow squash merge.
4. Prefer merge commit.
5. Do not rewrite reviewed commit history.
6. Commit messages must describe product/technical change in plain engineering language.
7. Commit messages must not mention workflow-specific terms such as `CR`, `PR checklist`, `stage`, `Fast/Guarded`, or similar internal process labels.

## Rule Boundary
- This rule does not discover or migrate PR files.
- File discovery and thread rebinding belong to `$rule-find-task`.
- New PR initialization belongs to `$command-plan-task`.
- Stage transition commands from user are optional; stage progression is inferred and updated by this rule.
- This rule must not bypass scope-level test-first gating.
