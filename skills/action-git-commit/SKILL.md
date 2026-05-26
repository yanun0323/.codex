---
name: action-git-commit
description: Use this skill only when the user explicitly asks to invoke the `action-git-commit` skill. Review uncommitted changes, summarize the commit scope, and run `git commit` safely.
---

# Git Commit Action

Create one safe commit from pending changes.

## Workflow

1. Verify repo: `git rev-parse --is-inside-work-tree`.
2. Stop on conflicts: `git diff --name-only --diff-filter=U`.
3. Inspect changes: `git status --porcelain=v1 --untracked-files=all`; stop if none.
4. Stage requested scope, else `git add -A`.
5. Summarize staged evidence: `git diff --cached --name-status` and `--stat`.
6. Use user message as-is when provided; otherwise generate English Conventional Commit subject (`feat|fix|chore|refactor|test|docs`, imperative, <=72 chars, no trailing period). Add a short body only for multiple themes, risks, or migrations.
7. Commit with `git commit -m`.
8. Report `git show --stat --summary --oneline -1`.

## Constraints

- No `push`, amend, rebase, history rewrite, or `--no-verify` unless explicitly requested.
- Derive summaries from Git output; redact secrets if they appear.
- If hooks fail, report output and stop.
- Always show pre-commit summary; if no commit, state why and next action.
