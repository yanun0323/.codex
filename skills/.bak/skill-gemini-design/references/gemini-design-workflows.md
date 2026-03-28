# Gemini Design Workflows

Use these templates when invoking Gemini to directly modify design-facing files. Replace bracketed placeholders with repo-specific details and keep the final prompt grounded in local context.

## Execution Rule

Do not call `gemini -p ...` directly from this skill. Always use the wrapper.

```bash
python3 skills/skill-gemini-design/scripts/run_gemini_headless.py --include-directory . --prompt-file prompt.txt
cat prompt.txt | python3 skills/skill-gemini-design/scripts/run_gemini_headless.py --include-directory .
```

The wrapper defaults to a longer timeout and uses `--approval-mode auto_edit`. If the task is tightly scoped and Gemini still needs broader autonomous tool use, add `--approval-mode yolo` explicitly.

If the shell tool yields partial output or a session id, keep polling until the wrapper exits. Do not treat progress lines such as `Loaded cached credentials.` as completion.

## UI or Frontend Skeleton

Use this when the task needs layout direction, component structure, or a visual system before implementation.

```text
You are helping define a frontend design skeleton for an existing codebase.

Task:
[Describe the feature or screen]

Audience and intent:
[Who uses it and what they need to accomplish]

Repo and technical constraints:
[Framework, design system, existing components, responsive requirements, accessibility constraints]

Current context:
[Relevant files, existing patterns, screenshots, or rough notes]

Files Gemini may edit:
[List specific files or folders Gemini is allowed to touch]

Edit the target files directly and then return a concise text summary with:
- files_changed
- layout_changes
- style_system_changes
- follow_up_for_agent

Rules:
- Focus on visual structure and frontend skeleton only.
- Do not invent business logic or backend behavior.
- Keep business logic intact.
- Make the design specific to the provided context, not generic.
```

Suggested execution:

```bash
python3 skills/skill-gemini-design/scripts/run_gemini_headless.py --include-directory . --prompt-file ui-prompt.txt
```

## Static Visual Direction

Use this for posters, slides, one-pagers, visual compositions, or other non-interactive design tasks.

```text
You are defining a visual direction for a static design artifact.

Artifact type:
[Poster, slide, report cover, hero visual, etc.]

Goal:
[What the artifact needs to communicate]

Audience:
[Who will see it]

Constraints:
[Dimensions, format, amount of text, brand limits, production needs]

Context:
[Reference material, subject matter, tone, examples to avoid]

If editable source files already exist, modify them directly and then return a concise text summary with:
- files_changed
- concept
- composition
- palette
- typography
- follow_up_for_agent

Rules:
- Prioritize composition, hierarchy, and stylistic clarity.
- Keep the direction distinctive and specific.
- Avoid generic "clean modern" advice.
- Make sure the recommendations can be executed in the target format.
```

Suggested execution:

```bash
python3 skills/skill-gemini-design/scripts/run_gemini_headless.py --include-directory . --prompt-file visual-prompt.txt
```
