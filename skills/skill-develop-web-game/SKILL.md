---
name: "skill-develop-web-game"
description: "Use when Codex is building or iterating on a web game (HTML/JS) and needs a reliable development + testing loop: implement small changes, run a Playwright-based test script with short input bursts and intentional pauses, inspect screenshots/text, and review console errors with render_game_to_text."
---

# Develop Web Game

Iterate as: implement small -> act -> pause -> observe -> fix.

## Paths

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export WEB_GAME_CLIENT="$CODEX_HOME/skills/skill-develop-web-game/scripts/web_game_playwright_client.js"
export WEB_GAME_ACTIONS="$CODEX_HOME/skills/skill-develop-web-game/references/action_payloads.json"
```

## Required Game Hooks

- Single centered canvas preferred.
- Expose `window.render_game_to_text()` returning concise JSON for visible/interactive state: mode, coordinate system, player position/velocity, obstacles/enemies, collectibles, timers/cooldowns, score, flags.
- Strongly expose `window.advanceTime(ms)` for deterministic frame stepping.
- Fullscreen toggle: prefer `f`, `Esc` exits; resize canvas/input mapping correctly.

## Workflow

1. Pick one feature/behavior.
2. Read existing `progress.md`; if missing create it with `Original prompt: <prompt>`. Append meaningful updates, findings, tests, TODOs.
3. Make the smallest change.
4. Verify Playwright (`npx` or local dependency).
5. Run `$WEB_GAME_CLIENT` after each meaningful change using actions from `$WEB_GAME_ACTIONS`.
6. Capture screenshots and `render_game_to_text`; open the latest screenshots and visually inspect gameplay, not only menus.
7. Exercise all important controls and multi-step outcomes end-to-end: movement, jump, attack/shoot, interact, menus, pause/resume, restart, specials, win/lose, score/health/resources, boundaries/collisions.
8. Compare text state to screen state.
9. Review console errors; fix the first new one before continuing.
10. Reset between distinct scenarios. Change one variable at a time and rerun until stable.

Example:

```bash
node "$WEB_GAME_CLIENT" --url http://localhost:5173 --actions-file "$WEB_GAME_ACTIONS" --click-selector "#start-btn" --iterations 3 --pause-ms 250
```

## Visual/Game Rules

- Keep in-play text minimal; show controls on start/menu screens.
- Avoid overly dark scenes unless required; key elements must be readable.
- Draw background on canvas, not only CSS.
- If screenshots or text state reveal missing/broken behavior, it is broken; fix and rerun.

## Signoff

Verify new features plus affected existing areas. Final `progress.md` must include remaining TODOs/gotchas for the next agent.
