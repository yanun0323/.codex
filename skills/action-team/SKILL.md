---
name: action-team
description: "Use this skill only when the user explicitly asks to invoke the `action-team` skill. Runs an Anthropic-style orchestrator-workers workflow for bounded local repo work."
---

# Action Team

Use an orchestrator-workers workflow for nontrivial local repo work.

## Core Rule

The parent agent remains the orchestrator. It owns task framing, risk decisions, integration, verification strategy, and the final answer.

Start with `team_architect` for substantial or ambiguous work unless the task is already narrow and file ownership is obvious.

## Routing

- `team_architect`: read-only decomposition, risk mapping, worker prompts, and ownership boundaries.
- `team_builder`: complex or multi-file implementation with explicit ownership.
- `team_fast_worker`: small bounded implementation with explicit ownership.
- `team_test`: test discovery, narrow checks, and focused test edits when explicitly assigned.
- `team_researcher`: current documentation, API behavior, and source-backed facts.
- `team_critic`: read-only review after a patch, design, or plan exists.

## Worker Contract

Every worker prompt must include:

- objective
- allowed files, modules, or read-only scope
- forbidden files, modules, or behaviors
- expected output format
- stop condition
- verification expectation

Write-capable workers must have non-overlapping ownership. If ownership overlaps, do not spawn parallel writers.

## Execution Policy

- Do not spawn workers reflexively. Keep small tasks local.
- Use read-only workers for exploration and review when possible.
- Keep the critical path local when waiting would slow the task.
- Parallelize only independent work with clear boundaries.
- Tell every worker it is not alone in the codebase and must not revert unrelated changes.
- The parent agent integrates or rejects worker output; workers do not decide final scope.

## Final Response

Include:

- subagents used
- why each was used
- key result from each
- what the parent integrated, changed, or rejected
- verification result
