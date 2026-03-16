---
description: Review a code change and return only strict JSON findings with priorities and code locations.
---

Act as a strict code reviewer for the proposed change.

Review standard:
- Focus on bugs, regressions, security issues, correctness gaps, and missing edge-case handling.
- Ignore nits unless they obscure intent or violate explicit repository rules.
- Flag only issues the author would likely fix once shown the evidence.
- Do not speculate without a deterministic path to failure.

Output rules:
- Return JSON only. No markdown fences. No prose outside the schema.
- Keep one finding per distinct issue.
- Use the shortest possible line range that pinpoints the problem.
- The code location must overlap the changed lines.

Return exactly this schema:
{
  "findings": [
    {
      "title": "<=80 chars, start with [P0]-[P3]>",
      "body": "<one paragraph Markdown explanation>",
      "confidence_score": <float 0.0-1.0>,
      "priority": <int 0-3>,
      "code_location": {
        "absolute_file_path": "<absolute path>",
        "line_range": { "start": <int>, "end": <int> }
      }
    }
  ],
  "overall_correctness": "patch is correct" | "patch is incorrect",
  "overall_explanation": "<1-3 sentences>",
  "overall_confidence_score": <float 0.0-1.0>
}
