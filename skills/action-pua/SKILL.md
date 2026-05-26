---
name: action-pua
description: "Use this skill only when the user explicitly asks to invoke the `action-pua` skill. Force exhaustive, evidence-driven execution when the agent is stuck, passive, looping, or about to deflect without proof."
---

# Action Pua

Use when work is stalled, looping, weakly verified, or about to be deflected.

## Trigger

Apply if the same task failed twice, the approach is looping, the agent is giving up without proof, the user says to try harder, or the task is hard debugging/config/deploy/integration/environment work.

## Rules

- Inspect concrete evidence before asking: errors, logs, code, configs, docs, runtime state.
- Exhaust realistic options; change strategy after each failed attempt.
- Verify every fix with commands, tests, requests, logs, or runtime output.
- Check nearby code, dependencies, edge cases, and failure paths.
- Deliver end-to-end results or a rigorous failure handoff.

## Escalation

- Attempt 2: stop the loop and switch approach.
- Attempt 3: search/read source and list three hypotheses.
- Attempt 4: verify three new hypotheses and complete adjacent-impact checks.
- Attempt 5+: deliver working result or handoff verified facts, eliminated causes, narrowed scope, and next directions.

Start responses with `[Auto-select: <mode> | Because: <pattern> | Escalate to: <next>]`, then list concrete actions and verification.
