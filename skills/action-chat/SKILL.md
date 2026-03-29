---
name: action-chat
description: Use this skill only when the user explicitly asks to invoke the `action-chat` skill. This mode is strictly read-only - never create, modify, rename, or delete files. Only inspect local files and optionally search the web to answer questions.
---

# Read-Only Chat Action


## Goals
- Answer questions accurately using local read-only context and web sources when needed.
- Keep the workspace unchanged.
- Prefer fast, evidence-based responses over speculative output.

## Operating Mode (HARD: Read-Only)

### Allowed Actions
- Read local files and repository state.
- Run read-only shell commands for inspection.
- Search the web and cite sources when external verification is needed.
- Summarize, compare, explain, and propose options in chat.

### Forbidden Actions
- Do not create, edit, rename, move, or delete any file or directory.
- Do not run write operations, including redirection or patch tools.
- Do not run commands that install dependencies, mutate lockfiles, or change git history.
- Do not run destructive commands (`rm`, `mv`, `git reset`, `git checkout --`, etc.).

If a command might write to disk and safety is unclear, do not run it.

## Read-Only Command Guidance
Prefer read-only commands such as:
- `pwd`, `ls`, `find`, `rg`, `cat`, `sed -n`, `head`, `tail`, `wc`, `stat`
- `git status`, `git log`, `git show`, `git diff` (read-only usage only)

Avoid any command pattern that writes:
- `>`, `>>`, `tee`, `touch`, `mkdir`, `cp`, `mv`, `rm`
- `sed -i`, `perl -pi`, formatters or generators that modify files
- `apply_patch` or any equivalent write/edit mechanism

## Web Research Rules
- Use web search when information may be time-sensitive, uncertain, or explicitly requested.
- Prefer primary and official sources when available.
- Include source links in responses that rely on external information.
- Distinguish verified facts from inference.

## If the User Requests File Changes
- Explain that `action-chat` mode is read-only and cannot change files.
- Provide either:
  - a read-only analysis/plan, or
  - a clear instruction that the user should switch to a non-read-only coding mode for implementation.

## Response Style
- Follow `rule-global` language policy for conversation and artifact language.
- Keep responses concise, actionable, and evidence-oriented.
- For repository questions, cite concrete file paths and relevant lines when possible.

## Hard Rules
- Follow `rule-global` priority, security, and language policies.
- Preserve workspace state exactly as found.
- Never perform write operations, even if the user asks, while this skill is active.
