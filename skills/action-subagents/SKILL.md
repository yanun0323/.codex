---
name: action-subagents
description: "Use this skill only when the user explicitly asks to invoke the `action-subagents` skill. Enables automatic Codex subagent routing for the current task based on scope, risk, and token efficiency."
---

# Action Subagents

Enable automatic subagent routing for the current task.

## Core Rule

After this action is invoked, the main agent may decide whether to spawn subagents based on task scope, risk, parallelism, and token efficiency.

Do not spawn subagents reflexively. Small tasks should usually stay local.

## Routing

- `token_explorer`: use for read-only codebase mapping when relevant files, flows, or ownership are unclear.
- `local_worker`: use for bounded implementation only after file/module ownership is explicit and non-overlapping.
- `test_scout`: use for test discovery, narrow verification, or focused test updates when the test surface is unclear.
- `critic_reviewer`: use for read-only review of correctness, security, regressions, concurrency, migrations, broad refactors, and missing tests.
- `ui_specialist`: use for bounded frontend/UI implementation, responsiveness, accessibility, and visual polish.
- `docs_researcher`: use when current official documentation, API behavior, framework behavior, or version-specific constraints affect correctness.

## Cost Policy

- Prefer one cheap read-only subagent before any write-capable worker on unfamiliar code paths.
- Do not spawn subagents for small changes that fit in one focused local pass.
- Do not spawn more than two subagents unless the task is clearly parallel and the expected coordination cost is lower than the expected context savings.
- Keep the main agent responsible for planning, risk decisions, integration, and final answer.

## Worker Safety

- Give every write-capable subagent explicit ownership: files/modules allowed, files/modules forbidden, expected output, and stop condition.
- Do not assign overlapping write scopes to multiple workers.
- Tell workers they are not alone in the codebase and must not revert unrelated changes.
- Use read-only agents for exploration and review whenever possible.

## Before Spawning

State briefly:

- agent name
- task
- scope
- reason it should save context, reduce risk, or run safely in parallel

## Final Response

Include:

- which subagents were used
- why they were used
- what they returned
- how the main agent integrated or rejected their results
