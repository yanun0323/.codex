---
name: action-fusion
description: "Use this skill only when the user explicitly asks to invoke the `action-fusion` skill. Runs a read-only Fusion-style subagent panel for research, review, and decisions."
---

# Action Fusion

Run a read-only Fusion-style panel. This does not call the OpenRouter API.

## Core Rule

Use this for decisions, comparisons, architecture options, research synthesis, and multi-perspective review. Do not use it for direct file edits.

The parent agent owns integration and the final recommendation. Panel agents provide independent analysis only.

## Panel

- `fusion_gemini_pro`: alternative design, implementation tradeoffs, and hidden-assumption checks.
- `fusion_claude_opus`: deep critique, risk analysis, and weak-claim detection.
- `fusion_gpt55`: repo-aware synthesis perspective, execution feasibility, and decision framing.

With `max_threads = 3`, run all three panel agents in parallel when the question benefits from all perspectives.

## Panel Prompt Contract

Every panel prompt must include:

- decision or question
- context and constraints
- options to compare, if known
- requested perspective
- output format

Panel agents must remain read-only. They may inspect local files and search current sources when useful, but must not create, edit, delete, install, format, or mutate files.

## Parent Integration

After panel results return, the parent agent integrates them directly. The parent final answer must include:

- consensus
- disagreements
- blind spots
- recommendation
- confidence
- next action

## Final Response

Separate sourced facts from inference and state whether implementation should proceed through `$action-team`, normal local work, or no action.
