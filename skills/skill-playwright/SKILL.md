---
name: "skill-playwright"
description: "Use when the task requires automating a real browser from the terminal (navigation, form filling, snapshots, screenshots, data extraction, UI-flow debugging) via `playwright-cli` or the bundled wrapper script."
---

# Playwright CLI Skill

CLI-first browser automation. Prefer the bundled wrapper; do not switch to `@playwright/test` unless asked.

## Setup

Check `npx` first:

```bash
command -v npx >/dev/null 2>&1
```

If missing, ask the user to install Node.js/npm, then:

```bash
npm install -g @playwright/cli@latest
playwright-cli --help
```

Set paths:

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/skill-playwright/scripts/playwright_cli.sh"
```

## Loop

```bash
"$PWCLI" open https://example.com --headed
"$PWCLI" snapshot
"$PWCLI" click e3
"$PWCLI" type "text"
"$PWCLI" press Enter
"$PWCLI" screenshot
```

1. Open page.
2. Snapshot for stable refs.
3. Interact using latest refs.
4. Re-snapshot after navigation, substantial DOM changes, modals, menus, or tab switches.
5. Capture screenshot/pdf/traces when useful.

## Guardrails

- Always snapshot before using refs like `e12`; stale refs require a new snapshot.
- Prefer explicit commands over `eval`/`run-code`.
- Use `--headed` for visual checks.
- Store artifacts in `output/playwright/`.
- References: `references/cli.md`, `references/workflows.md`.
