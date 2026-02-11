---
name: rule-execute-task
description: Execute staged PR workflow only when invoked by rule-find-task after a PR source file has been resolved.
---

# Execute Task Rule

## When to Use
- Use this rule only when `$rule-find-task` has already found and selected one PR source file.
- Use when the assistant must continue workflow execution from the current stage in that resolved PR file.

## Inputs (Required)
- Absolute path to resolved PR source file returned by `/scripts/find_pr_task.sh`
- Current PR metadata and sections from the source file.

## Goals
- Continue workflow from the PR file's current `stage` and `status`.
- Enforce that every CR is RD-reviewed before commit.
- Keep source and `_TW` mirror synchronized after each source update.

## Workflow Stages
1. Stage A: Requirement definition via PR Change Card.
2. Stage B: CR decomposition via CR Checklist.
3. Stage C: CR implementation loop.
4. Stage D: Final validation and merge readiness.

## Stage Transition Table
| Current Stage | Exit Condition | Next Stage |
|---|---|---|
| A | PR Change Card approved by RD | B |
| B | CR Checklist approved by RD | C |
| C | All CR rows are `done` | D |
| D | Final validation complete and RD approves merge | done |

## CR Status Transition Table
| Current Status | Trigger | Next Status |
|---|---|---|
| `todo` | Agent starts CR | `in_progress` |
| `in_progress` | Agent submits evidence for review | `in_review` |
| `in_review` | RD requests changes | `changes_requested` |
| `changes_requested` | Agent updates and resubmits | `in_review` |
| `in_review` | RD approves | `approved` |
| `approved` | Agent commits without further edits | `committed` |
| `committed` | Checklist and metadata updated | `done` |

Rules:
1. If content changes after `approved`, status must return to `in_review`.
2. Commit hash is written only after commit is finished.
3. `done` is immutable unless RD explicitly reopens the CR.

## Stage C Fixed Loop
`Pick next CR -> Agent implements -> Run checks -> Wait RD decision -> Commit -> Update Checklist -> Next CR`

RD decision values:
- `approved`
- `changes_requested`

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

## DoD Before RD Review
Each CR must be:
1. Buildable
2. Testable
3. Revertable by default
4. Independently understandable
5. Not partial

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

## Translation Mirror Sync
Whenever source PR file is updated:
1. Regenerate or update `${task_slug}_TW.md`.
2. Keep source `.md` as the only executable state.
3. Treat `_TW.md` as RD-facing mirror only.

## Rule Boundary
- This rule does not discover or migrate PR files.
- File discovery and thread rebinding belong to `$rule-find-task`.
- New PR initialization belongs to `$command-plan-task`.
