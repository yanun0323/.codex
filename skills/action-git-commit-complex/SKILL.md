---
name: action-git-commit-complex
description: Use this skill only when the user explicitly asks to invoke the `action-git-commit-complex` skill. Analyze uncommitted repository changes by business logic and scope, split them into 1-5 commits, and run `git commit` safely.
---

# Complex Git Commit Action

Split pending changes into 1-5 coherent, dependency-safe commits.

## Invariants

- Each commit has one dominant business intent.
- Order preserves build/runtime dependencies.
- No interactive staging (`git add -p`) or history rewrite.
- User-supplied messages are preserved.
- Claims come from Git output.

## Workflow

1. Verify repo, stop on conflicts, and stop if no changes.
2. Collect `git status --porcelain=v1 --untracked-files=all`, `git diff --name-status`, `--stat`, `--numstat`; inspect targeted diffs when grouping is ambiguous.
3. Group by business objective and scope; merge groups if over 5 or if one file mixes inseparable concerns.
4. Present plan `G1..Gn`: intent, files, draft English message.
5. For each group: `git reset` staged state, `git add <paths...>`, verify `git diff --cached --name-status`/`--stat`, then commit.
6. Capture `git show --stat --summary --oneline -1` after each commit.
7. Return final count, rationale, hashes, subjects, file lists, and stats.

## Message Rules

Prefer `<type>(<scope>): <subject>`; allowed types `feat|fix|chore|refactor|test|docs`; default `chore`; imperative, <=72 chars, no trailing period. Body only for risks, migrations, or multiple subpoints.

## Constraints

No `push`, amend, rebase, history rewrite, interactive split, fabricated summaries, or `--no-verify` unless explicitly requested. Redact secrets in output.
