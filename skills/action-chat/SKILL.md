---
name: action-chat
description: Use this skill only when the user explicitly asks to invoke the `action-chat` skill. This mode is strictly read-only - never create, modify, rename, or delete files. Only inspect local files and optionally search the web to answer questions.
---

# Read-Only Chat Action

Answer from read-only local context and web sources when needed. Keep the workspace unchanged.

## Allowed

- Inspect files, repository state, and read-only command output.
- Search the web when facts are time-sensitive, uncertain, or requested; cite sources.
- Explain, compare, summarize, propose plans, and cite file paths/lines.

## Forbidden

- Create, edit, rename, move, delete, install, format, generate, mutate lockfiles, or change git history.
- Run write patterns: `>`, `>>`, `tee`, `touch`, `mkdir`, `cp`, `mv`, `rm`, `sed -i`, `perl -pi`, patch tools, destructive git.
- Run any command whose write behavior is unclear.

If the user requests changes, state that this mode is read-only and provide analysis or ask them to switch modes.

Use concise, evidence-based replies and keep following global security/language rules.
