---
name: rule-find-task
description: Lightweight always-read rule that discovers or rebinds a PR task file for the current thread and invokes rule-execute-task when a PR is found.
---

# Find Task Rule

## When to Use
- Always load this rule in this repository.
- Use this rule as the workflow entry gate before loading `$rule-execute-task`.

## Goals
- Keep token usage low by doing only lightweight PR file discovery in this rule.
- Resolve one active PR source file for current conversation `thread_key`.
- Invoke `$rule-execute-task` only when a valid PR source file is found.

## Thread Binding
Resolve `thread_key` in this order:
1. `CODEX_THREAD_ID`
2. Explicit caller value (`thread_key` or `conversation_id`)
3. Existing PR metadata only for migration fallback

## Discovery Root
- `./.vscode/pull-request-task/`

## Discovery Logic
1. If conversation explicitly includes a PR file path under `./.vscode/pull-request-task/`, use it as first candidate.
2. Otherwise scan `./.vscode/pull-request-task/${thread_key}/` for PR source files (`*_TW.md` excluded).
3. If multiple candidates exist:
   - Prefer non-done PR.
   - Then prefer most recently updated.
   - If still ambiguous, ask user to select.

## Cross-Thread Rebinding
If explicit PR file belongs to a different thread folder:
1. Move source PR file into current `./.vscode/pull-request-task/${thread_key}/`.
2. Move paired `_TW.md` mirror if it exists.
3. Update source metadata `thread_key` to current thread.
4. Keep original `pr_id`.

## Invocation Contract
- If PR source file is found (by thread or explicit path), invoke `$rule-execute-task`.
- Pass the resolved source PR path as execution input.
- If no PR file is found, do not invoke `$rule-execute-task` and continue with normal non-workflow behavior.

## Boundary
- This rule does not execute stage logic.
- This rule does not initialize new PR files.
- New PR creation belongs to `$command-plan-task`.
