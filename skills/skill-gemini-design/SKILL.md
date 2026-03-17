---
name: skill-gemini-design
description: "Use this skill when a task is design-led and Gemini should directly edit design-facing files before the agent continues with repo-specific logic work."
---

# Skill Gemini Design

## Overview

Use this skill when the task is primarily about design decisions rather than business logic, and Gemini should directly modify design-facing files. It covers UI, websites, dashboards, apps, posters, slides, and static visual tasks.

This skill is a design orchestration layer focused on direct edits. It uses the local `gemini` CLI to modify design-facing files in the workspace before the agent reviews the diff and continues with repo-specific logic work.

## When to Use

Use this skill whenever the user asks for:
- UI or visual design direction
- frontend layout or component structure
- posters, slides, or static visual composition
- style system, palette, typography, spacing, or component hierarchy decisions
- redesign or normalization of an existing interface for clarity, consistency, or aesthetics

Prefer this skill when the user wants Gemini to directly restyle or restructure files. After Gemini edits the workspace, continue with the normal implementation workflow.

## Workflow

Follow this sequence:
1. Collect local context first. Inspect the repo, current design system, screenshots, relevant files, constraints, and existing patterns.
2. Decide which design-facing files Gemini is allowed to edit.
3. Invoke the local wrapper with a specific, context-rich prompt.
4. Inspect the changed files or diff before continuing.
5. Implement or integrate the result using the repo's normal tools and workflows.

Do not send Gemini a one-line vague request. Always provide context, constraints, goals, and deliverable format.

## UI/Frontend Rule

For UI or frontend tasks, Gemini may directly edit design-facing files, but only within the presentation layer:
- information architecture
- visual hierarchy
- layout structure
- component breakdown
- design tokens
- static markup or TSX skeletons
- styling direction and interaction intent
- presentational CSS, layout code, and component structure

The agent remains responsible for:
- application logic
- data flow
- state management
- events and user actions
- API integration
- validation rules
- auth, permissions, and business behavior
- adapting the generated skeleton to the actual codebase

Do not ask Gemini to own the full production implementation when the task contains non-trivial runtime logic. Use it to define the shape and visual system first, then finish the feature yourself.

## Gemini Invocation

Use `scripts/run_gemini_headless.py` instead of calling `gemini` directly. The wrapper closes child stdin, waits for the process to exit, and always runs Gemini in direct-edit mode.

```bash
python3 skills/skill-gemini-design/scripts/run_gemini_headless.py --include-directory . --prompt-file context.txt
```

The wrapper defaults to a longer timeout and uses `--approval-mode auto_edit`. If Gemini needs broader autonomous tool use inside a tightly scoped workspace, you may explicitly pass `--approval-mode yolo`.

When the prompt is long, build the context locally and pass it by file or wrapper stdin:

```bash
python3 skills/skill-gemini-design/scripts/run_gemini_headless.py --include-directory . --prompt-file context.txt
cat context.txt | python3 skills/skill-gemini-design/scripts/run_gemini_headless.py --include-directory .
```

In every invocation:
- name the files Gemini may edit
- tell Gemini to keep business logic intact
- instruct Gemini to summarize the files changed and the design decisions made
- review the resulting diff before continuing with logic work

## Waiting Rule

For long-running Gemini requests, do not treat partial shell output as completion. Lines such as `Loaded cached credentials.` are only progress output.

If the shell tool returns a session id or partial output, keep polling until one of these happens:
- the wrapper process exits successfully
- the wrapper returns a timeout error
- the wrapper returns a non-zero exit code

Do not call `gemini -p ...` directly, and do not assume a yield or poll boundary means the model is done.

Load `references/gemini-design-workflows.md` when you need reusable prompt templates.

## Fallback

If any of the following happens, do not block the task:
- the wrapper cannot find `gemini`
- authentication is unavailable
- the wrapper times out
- the wrapper returns a non-zero exit code
- output is generic or low quality after one focused retry

Fallback behavior:
1. State briefly that Gemini could not be used successfully for this task.
2. Continue with the existing workflow using local reasoning and any relevant design skills.
3. Preserve forward progress instead of treating Gemini as a hard dependency.

## Integration

This skill can be combined with other design skills:
- Use with `skill-frontend-design` for distinctive website or frontend execution.
- Use with `skill-interface-design` for app, dashboard, or product UI work.
- Use with `skill-canvas-design` for poster-like or static visual output.

Recommended order:
1. Use `$skill-gemini-design` when Gemini should directly restyle or restructure design-facing files.
2. Inspect the changed files or diff, then continue with the most relevant implementation skill or the default agent workflow.
3. Keep the Gemini result as guidance, not as an unquestioned source of truth.
