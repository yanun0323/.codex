---
name: action-git-commit
description: Use this skill only when the user explicitly asks to invoke the `action-git-commit` skill. Review uncommitted changes, summarize the commit scope, and run `git commit` safely.
---

# Git Commit Action


## Goals
- Detect all local uncommitted Git changes.
- Summarize exactly what will be committed.
- Run `git commit` with a valid message.
- Return deterministic result (`commit` hash + summary).

## Inputs
- Optional user-provided commit message.
- Optional path scope; default is all tracked + untracked (`git add -A`).

## Command Workflow
1. Validate repository context.
   - Run `git rev-parse --is-inside-work-tree`.
   - If false, stop and report.
2. Check commit blockers.
   - Run `git diff --name-only --diff-filter=U`.
   - If conflicts exist, stop and list conflicted paths.
3. Inspect pending changes.
   - Run `git status --porcelain=v1 --untracked-files=all`.
   - If none, stop and report `nothing to commit`.
4. Stage commit scope.
   - Default: `git add -A`.
   - If scoped request is given, stage only requested paths.
5. Build pre-commit summary.
   - Run `git diff --cached --name-status`.
   - Run `git diff --cached --stat`.
   - Summarize file impact and dominant themes.
6. Prepare commit message (mandatory rules below).
   - Use user message if provided.
   - Otherwise generate from staged diff:
     - Imperative subject, <=72 chars.
     - Prefer `feat|fix|chore|refactor|test|docs`, format `<type>(<scope>): <subject>` when clear.
     - Add bullet body only if useful.

### Commit Message Rules (Mandatory)
- Priority: use user-provided message as-is unless reformat is explicitly requested.
- Subject:
  - Preferred `<type>(<scope>): <subject>`; fallback `<type>: <subject>`.
  - Allowed types: `feat`, `fix`, `chore`, `refactor`, `test`, `docs`.
  - If ambiguous, use `chore`.
  - Must be imperative, English, <=72 chars, no trailing period.
- Body:
  - Add only for multiple change groups, risks, or migration notes.
  - Use concise bullets, lines <=72 chars.
- Avoid low-value subjects: `update`, `misc`, `wip`, `tmp`.
7. Execute commit.
   - `git commit -m "<subject>"`
   - `git commit -m "<subject>" -m "<body>"` when body exists.
8. Report results.
   - Run `git show --stat --summary --oneline -1`.
   - Return commit hash, subject, files changed, and insert/delete summary.

## Constraints
- Do not run `git push`, `git commit --amend`, `git rebase`, or history-rewrite commands unless requested.
- Do not invent summaries; derive from Git output.
- If hooks fail, report hook output and stop (no `--no-verify`).
- If output could expose secrets, redact and mention it.

## Output Expectations
- Always show a short pre-commit summary before commit success output.
- Include exact committed file list and diff stat.
- If no commit is created, clearly state reason and next action.
