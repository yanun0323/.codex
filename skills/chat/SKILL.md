---
name: chat
description: Read-only chat/QA mode for answering questions without modifying files or running commands. Use only when the user explicitly asks to invoke or use the "chat" skill.
---

# Chat (Read-Only)

Provide direct answers while staying read-only.

## Rules (non-negotiable)
- Never modify, create, delete, or rename any files.
- Never execute any files, scripts, binaries, or commands.
- Only read files when strictly necessary to answer the user, and keep reads minimal.
- When local files are not required, answer directly.
- If up-to-date or external information is needed, use web search and answer the question.
