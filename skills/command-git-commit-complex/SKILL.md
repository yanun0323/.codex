---
name: command-git-commit-complex
description: Use this skill only when the user explicitly asks to invoke the `command-git-commit-complex` skill. Analyze uncommitted repository changes by business logic and scope, split them into 1-5 commits, and run `git commit` safely.
---

# Git Commit Command

## When to Use
- Use this skill only when the user explicitly asks to invoke `$command-git-commit-complex`.
- Use when the user wants to commit current uncommitted repository changes.

## Goals
- Detect all local uncommitted changes in a Git repository.
- Analyze uncommitted changes by business logic and implementation scope.
- Split changes into `1-5` coherent commits, each independently meaningful.
- Execute `git commit` with clear per-commit messages.
- Return deterministic commit plan and per-commit results.

## Inputs
- Optional user intent (for example: feature area, bug context, or preferred split).
- Optional explicit message overrides for one or more commit groups.
- Optional scope constraints (if unspecified, analyze all tracked and untracked changes).

## Invariants
- `INV-1`: Every commit must map to one dominant business intent.
- `INV-2`: Commit count must be between `1` and `5`.
- `INV-3`: Commit order must preserve build/runtime dependency.
- `INV-4`: No interactive Git staging commands (`git add -p`, interactive rebase).
- `INV-5`: Do not fabricate summary content; claims must come from Git output.
- `INV-6`: Preserve user-provided commit message text when explicitly supplied.

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
4. Collect grouping evidence.
   - Run `git diff --name-status`.
   - Run `git diff --stat`.
   - Run `git diff --numstat`.
   - For ambiguous files, inspect targeted diffs with `git diff -- <path>`.
5. Build commit groups by business logic.
   - Cluster files by shared business objective and execution scope (for example: API behavior change, domain logic fix, infra/config, tests/docs).
   - Keep each cluster independently explainable and safe to review.
   - Keep dependency-safe ordering, usually: prerequisites -> core logic -> adapters/integration -> tests/docs.
6. Normalize cluster count to `1-5` commits.
   - If only one coherent scope exists, create `1` commit.
   - If proposed groups exceed `5`, merge nearest related groups by business objective and dependency.
   - If deterministic non-interactive split is impossible (for example mixed concerns in one file), merge affected scopes and document the reason.
7. Present pre-commit plan.
   - Show planned groups `G1..Gn` with:
     - Business intent
     - Included files
     - Commit message draft
   - If user gave explicit mapping, apply it before execution.
8. Execute commits per group (non-interactive).
   - Before each group, run `git reset` to clear staged state only.
   - Stage scoped files via `git add <paths...>`.
   - Validate staged scope via `git diff --cached --name-status` and `git diff --cached --stat`.
   - If staged content violates group boundary, unstage and regroup deterministically.
9. Prepare commit message for each group.
   - Use user-provided message for that group when available.
   - Otherwise generate message from group intent:
     - Subject line in imperative style, max 72 chars.
     - Prefer Conventional Commit prefix (`feat:`, `fix:`, `chore:`, `refactor:`, `test:`, `docs:`) when clear.
     - Add body bullets only when necessary (risk notes, migration notes, or multiple sub-points).
10. Execute commit.
   - Run `git commit -m "<subject>"` when no body is needed.
   - Run `git commit -m "<subject>" -m "<body>"` when body exists.
11. Capture per-commit evidence.
   - Run `git show --stat --summary --oneline -1` after each commit.
   - Record commit hash, subject, file list, and insertion/deletion stats.
12. Return consolidated result.
   - Report the final split plan actually executed (`n` commits, `1 <= n <= 5`).
   - Include per-commit rationale and evidence.

### Commit Message Rules (Mandatory)
- Message precedence:
  - User-provided message for a group has highest priority.
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
  - Add body only when the current group has notable risks, migration notes, or multiple sub-points.
  - Keep body lines at 72 characters or fewer.
  - Use concise bullet points for grouped changes when body is present.
- Language and banned terms:
  - Commit message text must be English.
  - Avoid low-information subjects such as `update`, `misc`, `wip`, or `tmp`.

## Constraints
- Do not run `git push`, `git commit --amend`, `git rebase`, or history-rewrite commands unless explicitly requested.
- Do not use interactive Git workflows for splitting (for example `git add -p`).
- Do not fabricate summary details; summaries must come from Git command output.
- If commit hooks fail, report hook output and stop without forced bypass.
- If generated summary could expose secrets, redact sensitive values and mention redaction.

## Output Expectations
- Always show a pre-commit split plan before executing commits.
- Include exact file list and diff stat for each commit.
- Include the final commit count and grouping rationale.
- If no commit is created, clearly state why and what the user can do next.
