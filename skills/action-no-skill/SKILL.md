---
name: action-no-skill
description: "Use this skill only when the user explicitly asks to invoke the `action-no-skill` skill. Disable optional skill loading for the current and subsequent work until the user explicitly changes mode."
---

# No Skill Action

Use this action to prevent skill-based behavior from being loaded automatically.

## Operating Mode

- Do not load, open, or apply any other skill because a task appears to match it.
- Do not inspect other `SKILL.md` files, skill references, skill scripts, or skill assets unless the user explicitly requests that exact file or skill.
- Continue following system, developer, AGENTS, security, repository, and direct user instructions.
- Use normal tools and repository conventions to complete the task without skill-specific workflows.

## Duration

- This mode remains active for later work in the conversation until the user explicitly invokes another skill, asks to stop `action-no-skill`, or gives a higher-priority instruction that requires a skill.
- If another skill would normally trigger, proceed without it and mention the skipped skill only when it affects risk, verification, or user expectations.

## Conflict Handling

If a system or developer instruction mandates a specific skill, follow the higher-priority instruction and briefly state the conflict.
