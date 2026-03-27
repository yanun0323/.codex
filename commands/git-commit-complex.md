---
description: Analyze local changes, split them into 1-5 coherent commits, and execute the split safely.
agent: build
model: openai/gpt-5.3-codex-spark
---

Create a non-interactive multi-commit plan and execute it safely.

Goals:
- Group changes by business intent and dependency order.
- Produce between 1 and 5 commits.
- Keep every commit independently explainable and reviewable.

Hard constraints:
- No interactive staging.
- No amend, rebase, squash, push, or hook bypass.
- If a deterministic split is not possible, merge overlapping work into fewer commits and explain why.

Workflow:
1. Verify git context and check for merge conflicts.
2. Inspect all pending changes with file-level and diff-level evidence.
3. Propose commit groups with intent, file list, and draft message.
4. Order groups by dependency: prerequisites before consumers.
5. Stage, validate, and commit each group separately.
6. After each commit, capture the commit hash and diff stat.
7. Return the executed plan, not just the proposal.
