---
name: "skill-imagegen"
description: "Generate or edit raster images when the task benefits from AI-created bitmap visuals such as photos, illustrations, textures, sprites, mockups, or transparent-background cutouts. Use when Codex should create a brand-new image, transform an existing image, or derive visual variants from references, and the output should be a bitmap asset rather than repo-native code or vector. Do not use when the task is better handled by editing existing SVG/vector/code-native assets, extending an established icon or logo system, or building the visual directly in HTML/CSS/canvas."
---

# Image Generation Skill

Generate/edit raster assets: photos, illustrations, textures, sprites, mockups, cutouts, UI/product visuals.

## Modes

- Default: built-in `image_gen`; no `OPENAI_API_KEY`.
- Explicit fallback only: `scripts/image_gen.py` CLI (`generate`, `edit`, `generate-batch`); requires `OPENAI_API_KEY`.

Never switch to CLI automatically. If built-in fails, mention CLI fallback and proceed only if user explicitly asks. Do not modify `scripts/image_gen.py` or create one-off SDK runners.

## When Not To Use

Prefer repo-native SVG/HTML/CSS/canvas when extending existing vector/icon/logo systems, simple shapes/diagrams/wireframes, editable native assets, or deterministic code output.

## Built-In Save Policy

Built-in outputs default under `$CODEX_HOME/generated_images/...`. If the user names a destination or the asset is project-bound, generate first, then move/copy the selected final into the workspace. Never leave project-referenced assets only in `$CODEX_HOME`. Do not overwrite existing assets unless asked; use sibling versioned names.

## Decision

Classify:

- Intent: `generate` for new/reference-only images; `edit` for modifying an existing image while preserving parts.
- Strategy: one asset, repeated built-in calls, or explicit CLI batch.
- Local edit target with built-in path: first inspect with `view_image`; do not promise arbitrary path editing through the built-in tool.

## Workflow

1. Decide mode, intent, project-bound vs preview-only, and single/batch strategy.
2. Gather prompt, exact text, constraints/avoid list, and input images.
3. Label input image roles: reference, edit target, insert/style/compositing support.
4. Use `image_gen` for raster-style requests unless vector/code-native output is clearly better.
5. Normalize specific prompts; tastefully augment generic prompts only when useful.
6. Inspect output for subject, style, composition, text accuracy, invariants, and avoid items.
7. Iterate one targeted change at a time.
8. For project-bound outputs, persist selected finals in workspace and update references.
9. Report workspace path, final prompt, and mode used.

## Prompt Rules

Use concise labeled specs when helpful:

```text
Use case: <slug>
Asset type:
Primary request:
Input images:
Scene/backdrop:
Subject:
Style/medium:
Composition/framing:
Lighting/mood:
Color palette:
Materials/textures:
Text (verbatim): "<exact text>"
Constraints:
Avoid:
```

Generate slugs: `photorealistic-natural`, `product-mockup`, `ui-mockup`, `infographic-diagram`, `logo-brand`, `illustration-story`, `stylized-concept`, `historical-scene`.

Edit slugs: `text-localization`, `identity-preserve`, `precise-object-edit`, `lighting-weather`, `background-extraction`, `style-transfer`, `compositing`, `sketch-to-render`.

For edits, repeat invariants every iteration. Quote exact text and spell tricky words. Add only materially useful details; do not invent unrelated characters, objects, brands, slogans, palettes, or story beats.

References: `references/prompting.md`, `references/sample-prompts.md`; CLI-only: `references/cli.md`, `references/image-api.md`, `references/codex-network.md`.
