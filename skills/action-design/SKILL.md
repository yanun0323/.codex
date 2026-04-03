---
name: action-design
description: "Use this skill only when the user explicitly asks to invoke the `action-design` skill. Install one curated design reference into the current project by copying it to `./.design/` and updating `AGENTS.md` with mandatory design instructions."
---

# Action Design

## Overview

Use this action to install a design pack from this skill's `references/` catalog into the current project. The action copies the selected design into `./.design/` and creates or updates a managed block in `AGENTS.md` that forces future design and frontend work to follow `./.design/`.

## Workflow

1. List available designs from `references/`.
2. Ask the developer which design slug to install.
3. Run the loader script:

```bash
python3 "$CODEX_HOME/skills/action-design/scripts/load_design_into_project.py" \
  --project-root "$PWD" \
  --design apple
```

4. If `./.design/` already exists and the developer has not specified a mode, ask whether to `Replace`, `Merge`, or `Cancel`.
5. Confirm that:
   - `./.design/` contains the selected reference files.
   - `AGENTS.md` contains exactly one managed `action-design` block.

## Runtime Rules

- Only install from `references/<slug>/`. Do not synthesize or partially recreate a design pack.
- Treat the copied `./.design/` files as the source of truth after installation.
- Keep `AGENTS.md` updates idempotent by using the managed block markers from the loader script.
- Do not overwrite an existing `./.design/` directory silently. If the user did not specify a mode, ask first.
- If the selected slug does not exist, stop and ask the developer to choose one of the actual catalog entries.

## Maintenance

To rebuild the bundled catalog from the `awesome-design-md` repository, run:

```bash
python3 "$CODEX_HOME/skills/action-design/scripts/build_reference_catalog.py" \
  --source-repo /absolute/path/to/awesome-design-md
```

The build script copies all design assets into `references/`, rewrites README links to local relative paths, and captures `preview.html` plus `preview-dark.html` screenshots using the Playwright CLI wrapper from `$CODEX_HOME/skills/skill-playwright/scripts/playwright_cli.sh`.

## Files

- `scripts/load_design_into_project.py`: Installs one design into the current project and updates `AGENTS.md`.
- `scripts/build_reference_catalog.py`: Rebuilds the bundled `reference/` catalog from the source repository.
- `references/<slug>/`: Bundled design pack copied into target projects.
