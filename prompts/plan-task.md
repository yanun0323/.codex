---
description: Create a thread-bound PR task file from the conversation and hand it off to the staged execution workflow.
---

Create the internal PR task file for this conversation and prepare it for execution.

Workflow:
1. Resolve the thread key from `CODEX_THREAD_ID`, explicit input, or a generated fallback.
2. Read any user-provided file paths before drafting requirements.
3. Extract a concise title, description, business goal, non-goals, file evidence, open questions, acceptance tests, and critical invariants.
4. Create one PR source file under `.vscode/pull-request-task/<thread_key>/`.
5. Keep the file concise and usable as workflow memory, not as user-facing documentation.
6. If the repository includes finder or executor rules, hand off to that workflow after creation.

Constraints:
- Do not invent business logic.
- Do not leave business goal blank.
- Keep the plan minimal, concrete, and implementation-oriented.
- Use test-first decomposition when the workflow supports CR-style execution.
