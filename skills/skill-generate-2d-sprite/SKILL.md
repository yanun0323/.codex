---
name: skill-generate-2d-sprite
description: "Generate and postprocess general 2D game assets and animation sheets: pixel-art sprites, clean HD map props, creatures, characters, NPCs, spells, projectiles, impacts, props, summons, and transparent GIF exports. Use when Codex should infer the asset plan from a natural-language request, match a reference or map art style, call built-in `image_gen` for solid-magenta raw sheets, and use the local processor only for chroma-key cleanup, frame extraction, alignment, QC, and transparent exports."
---

# Generate 2D Sprite

Create self-contained 2D sprites, props, FX, and animation sheets. For whole maps/content packs, use the map/game-pack workflow instead.

## Infer

Choose the smallest useful plan:

- `asset_type`: player, npc, creature, character, spell, projectile, impact, prop, summon, fx
- `action`: single, idle, cast, attack, hurt, combat, walk, run, hover, charge, projectile, impact, explode, death
- `view`: topdown, side, 3/4
- `sheet`: auto, 1x4, 2x2, 2x3, 3x3, 4x4
- `bundle`: single_asset, unit_bundle, spell_bundle, combat_bundle, line_bundle
- `art_style`: pixel_art, clean_hd, pixel_inspired, retro_pixel, map_style, project-native
- plus frames, effect policy, anchor, margin, reference role, prompt, name

Read `references/modes.md` when ambiguous.

## Rules

- Decide plan yourself; do not force sheet/frame details when implied.
- Write the art prompt manually using `references/prompt-rules.md`; do not use prompt-builder scripts.
- Use built-in `image_gen` for raw images.
- Local/reference images must be visible in conversation first (`view_image` for local files).
- Match map/reference style before forcing pixel art.
- Scripts are only deterministic processors: magenta cleanup, frame splitting, component filtering, scaling, alignment, QC, transparent sheet/GIF export.
- Keep solid `#FF00FF` background unless the user asks for a different workflow.

## Workflow

1. Infer asset plan. Examples: four-direction hero -> player sheet; wizard orb -> cast sheet + projectile + impact; monster line -> 1-3 forms with needed sheets.
2. Write prompt with exact sheet shape, same identity/scale/bounding box, full containment, solid magenta background. For references, preserve silhouette, palette, face/eyes, costume marks, accessories, materials; change only requested action/evolution.
3. Generate raw image with `image_gen`; keep original and copy/reference into output folder.
4. Run `scripts/generate2dsprite.py process` choosing rows/cols, fit, align, shared scale, component mode/padding, edge-touch strategy.
5. QC: edge touch, inconsistent resize, noise components, animation coherence. Rerun processor or regenerate if needed.
6. Return bundle.

## Defaults

- idle: small/medium `2x2`, boss `3x3`
- cast `2x3`; projectile `1x4`; impact/explode `2x2`
- topdown walk `4x4`; side walk `2x2`
- use shared scale for multi-frame consistency
- use largest component when detached sparkles/debris confuse extraction

Outputs: raw, clean, transparent sheet, frame PNGs, GIF, prompt, metadata; player sheets also direction strips/GIFs; bundles use one folder per asset.
