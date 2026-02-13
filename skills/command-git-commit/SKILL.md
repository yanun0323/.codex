---
name: command-git-commit
description: Use this skill only when the user explicitly asks to invoke the `command-git-commit` skill. Inspect uncommitted repository changes, summarize the pending commit, and run `git commit` safely.
---

# Git Commit Command

## When to Use
- Use this skill only when the user explicitly asks to invoke `$command-git-commit`.
- Use when the user wants to commit current uncommitted repository changes.

## Goals
- Detect all local uncommitted changes in a Git repository.
- Produce a concise, evidence-based summary of what will be committed.
- Execute `git commit` with a clear commit message.
- Return deterministic commit results (commit hash + summary).

## Inputs
- Optional explicit commit message from the user.
- Optional scope override from the user (if unspecified, commit all tracked and untracked changes).

## Command Workflow
1. Validate repository context.
   - Run `git rev-parse --is-inside-work-tree`.
   - If not inside a Git repository, stop and report the reason.
2. Check commit blockers.
   - Run `git diff --name-only --diff-filter=U`.
   - If unresolved merge conflicts exist, stop and report conflicted paths.
3. Inspect pending changes.
   - Run `git status --porcelain=v1 --untracked-files=all`.
   - If there are no changes, stop and report `nothing to commit`.
4. Stage commit scope.
   - Default behavior: run `git add -A`.
   - If user provides a scoped commit request, stage only requested paths.
5. Build pre-commit summary.
   - Run `git diff --cached --name-status`.
   - Run `git diff --cached --stat`.
   - Summarize file-level impact and dominant change themes.
6. Prepare commit message.
   - If user provided a message, use it.
   - Otherwise generate a concise message from staged changes:
     - Subject line in imperative style, max 72 chars.
     - Prefer Conventional Commit prefix (`feat:`, `fix:`, `chore:`, `refactor:`, `test:`, `docs:`) when clear.
     - Optional body bullets for important change groups.

### Commit Message Rules (Mandatory)
- Message precedence:
  - User-provided message has highest priority.
  - Do not rewrite user-provided message unless the user explicitly asks for reformatting.
- Subject format:
  - Preferred format is `<type>(<scope>): <subject>`.
  - `<scope>` is optional. If omitted, use `<type>: <subject>`.
  - Allowed `<type>` values: `feat`, `fix`, `chore`, `refactor`, `test`, `docs`.
  - If `<type>` is ambiguous, default to `chore`.
- Subject quality constraints:
  - Use imperative mood.
  - Keep subject length to 72 characters or fewer.
  - Avoid trailing period (`.`) in the subject.
- Body inclusion rules:
  - Add body only when there are multiple change groups, notable risks, or migration notes.
  - Keep body lines at 72 characters or fewer.
  - Use concise bullet points for grouped changes when body is present.
- Language and banned terms:
  - Commit message text must be English.
  - Avoid low-information subjects such as `update`, `misc`, `wip`, or `tmp`.
7. Execute commit.
   - Run `git commit -m "<subject>"` when no body is needed.
   - Run `git commit -m "<subject>" -m "<body>"` when body exists.
8. Report results.
   - Run `git show --stat --summary --oneline -1`.
   - Return commit hash, subject, files changed, and insertion/deletion summary.

## Constraints
- Do not run `git push`, `git commit --amend`, `git rebase`, or history-rewrite commands unless explicitly requested.
- Do not fabricate summary details; summaries must come from Git command output.
- If commit hooks fail, report hook output and stop without forced bypass.
- If generated summary could expose secrets, redact sensitive values and mention redaction.

## Output Expectations
- Always show a short pre-commit summary before presenting commit success output.
- Include exact committed file list and diff stat in the final response.
- If no commit is created, clearly state why and what the user can do next.
