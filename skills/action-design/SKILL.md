---
name: action-design
description: "Use this skill only when the user explicitly asks to invoke the `action-design` skill. Install one curated design reference into the current project by copying it to `./.design/` and updating `AGENTS.md` with mandatory design instructions."
---

# Action Design

Install exactly one bundled design pack from `references/<slug>/` into the current project.

## Workflow

1. List available slugs in `references/`.
2. Ask which slug to install.
3. If `./.design/` exists and no mode was specified, ask `Replace`, `Merge`, or `Cancel`.
4. Run:

```bash
python3 "$CODEX_HOME/skills/action-design/scripts/load_design_into_project.py" \
  --project-root "$PWD" \
  --design <slug>
```

5. Verify `./.design/` contains the copied pack and `AGENTS.md` has one managed `action-design` block.

## Rules

- Do not synthesize packs or silently overwrite `./.design/`.
- Treat copied `./.design/` as source of truth.
- Keep `AGENTS.md` idempotent via loader markers.
- If slug is invalid, stop and ask for a catalog entry.

Maintenance: rebuild catalog with `scripts/build_reference_catalog.py` from an `awesome-design-md` checkout.
