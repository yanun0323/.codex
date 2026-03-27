---
description: Inspect local changes, summarize the commit scope, and create one safe non-interactive git commit.
agent: quick
model: openai/gpt-5.3-codex-spark
---

Create exactly one safe git commit for the current workspace.

Hard constraints:
- Work non-interactively.
- Do not amend, rebase, force, push, or bypass hooks.
- Stop if there are merge conflicts or nothing to commit.
- Use a user-provided commit message as-is unless reformatting was explicitly requested.

Workflow:
1. Verify the current directory is inside a git repository.
2. Check for unresolved conflicts.
3. Inspect unstaged, staged, and untracked changes.
4. Stage the intended scope.
5. Summarize what will be committed from git output, not assumptions.
6. Create one English commit message with an imperative subject, ideally Conventional Commit style.
7. Run `git commit`.
8. Report the commit hash, subject, file list, and diff stat.

If hooks fail, stop and report the hook output without using `--no-verify`.
