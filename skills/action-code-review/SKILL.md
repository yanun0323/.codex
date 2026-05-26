---
name: action-code-review
description: Use this skill only when the user explicitly asks to invoke the `action-code-review` skill. Review a proposed code change and return strict JSON findings with priority and code locations.
---

# Code Review Action

Review only the proposed diff. Return strict JSON, no markdown fences or prose.

## Finding Bar

Flag issues the author would likely fix:

- Newly introduced, discrete, actionable bug.
- Meaningful impact on correctness, security, performance, or maintainability.
- Proven affected path, not speculation or style.
- Not intentional, pre-existing, or requiring rigor absent from the repo.

Use one finding per issue, with the shortest useful diff-overlapping line range. Ignore non-blocking nits.

## Comment Rules

- Title starts with `[P0]`..`[P3]`; include numeric `priority` 0..3.
- Body is one concise paragraph explaining scenario, impact, and why it is a problem.
- Keep tone factual. No praise. Code snippets max 3 lines; `suggestion` only for exact replacements.
- Output all qualifying findings; if none, return an empty array and `patch is correct`.

## Output Schema

```json
{
  "findings": [
    {
      "title": "<<= 80 chars>",
      "body": "<Markdown paragraph>",
      "confidence_score": <float>,
      "priority": <int>,
      "code_location": {
        "absolute_file_path": "<path>",
        "line_range": {"start": <int>, "end": <int>}
      }
    }
  ],
  "overall_correctness": "patch is correct" | "patch is incorrect",
  "overall_explanation": "<1-3 sentences>",
  "overall_confidence_score": <float>
}
```
