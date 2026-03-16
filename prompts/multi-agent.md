---
description: Run a disciplined research-design-implement-review-validate loop and deliver a production-ready result.
---

Run this task as a structured autonomous engineering loop.

Phase order:
1. Baseline: inspect the current implementation and constraints.
2. References: identify and freeze authoritative sources when behavior or compatibility matters.
3. Audit: challenge the design and implementation from multiple angles before changing code.
4. Design: define the minimal safe plan.
5. Implement: apply the plan without unrelated refactors.
6. Validate: run the strongest checks available in this environment.
7. Report: summarize outcome, evidence, risks, and follow-ups.

Execution rules:
- Do not stop at planning unless blocked by a real risk.
- Treat unsupported claims as unverified until backed by source evidence.
- Prefer minimal, production-grade changes over wide architectural churn.
- Surface open risks explicitly if validation cannot fully close them.
