---
name: skill-generate-2d-map
description: "Generate and revise production-oriented 2D game maps with built-in image generation as the default visual asset source, choosing a visual model, runtime object model, collision model, art direction, and engine/export target. Use when Codex needs to create or integrate RPG maps, monster-taming maps, tactical arenas, battle backgrounds, side-scroller/parallax scenes, tilemaps, layered raster maps, clean HD hand-painted maps, pixel-inspired maps, prop packs, collision zones, walkable areas, or map previews."
---

# Generate 2D Map

Build the smallest map bundle that satisfies gameplay.

## Pipeline Axes

Choose, or infer from the game:

- `visual_model`: `baked_raster`, `layered_raster`, `tilemap`, `layered_tilemap`, `parallax_layers`
- `runtime_object_model`: `none`, `separate_props`, `y_sorted_props`, `interactive_entities`, `foreground_occluders`
- `collision_model`: `none`, `coarse_shapes`, `precise_shapes`, `tile_collision`, `polygon_walkmesh`, `trigger_zones`
- `engine_target`: `raw_canvas`, `Phaser`, `Tiled_JSON`, `LDtk`, `Godot_TileMap`, `Unity_Tilemap`, project-native

Read `references/map-strategies.md` when unclear; `references/layered-map-contract.md` for layered rasters; `references/prop-pack-contract.md` for prop sheets.

## Defaults

Use built-in `image_gen` for visual map art unless the user explicitly requests existing assets or procedural placeholders. Write creative prompts yourself; scripts may assemble, slice, crop, chroma-key, validate, compose previews, emit metadata, and wire engine files, but not create final art.

- Battle/title/menu/cutscene/fixed arena: `baked_raster + coarse_shapes`.
- Top-down exploration with tall props/occlusion/interactables: `layered_raster + y_sorted_props + precise_shapes`.
- Tilemap only if engine/editor already uses tiles or user asks.
- Side-scroller: `parallax_layers`.
- `clean_hd` unless project/user asks pixel art; `pixel_inspired` only for pixel-adjacent; `retro_pixel` only for explicit 16-bit/retro.

## Workflow

1. Inspect camera, dimensions, coordinate system, render order, assets, collision, zones, and map formats.
2. Select pipeline axes, art style, asset source, and output format.
3. Generate or reuse visual assets first:
   - baked: one map image plus optional collision/zones
   - layered: ground-only base -> make visible -> dressed reference -> props/placements -> preview
   - tilemap: generated/reused tileset art first, then layers/objects/collision
   - parallax: generate visual layers first, then scroll metadata
4. Store placements, spawns, interactables, blockers, walk bounds, encounters, exits, triggers as structured data.
5. Validate files, dimensions, alpha, JSON, referenced assets, collisions/zones, critical walk points, and flattened preview.

## Props

Use `skill-generate-2d-sprite` for transparent reusable props, but write prompts yourself and match map style.

- `one_by_one`: important, large, animated, irregular, identity-critical props.
- `prop_pack_2x2/3x3/4x4`: repeated simple props; avoid buildings, gates, wide trees, characters/statues, hero objects.
- For prop packs, use solid `#FF00FF`, then `scripts/extract_prop_pack.py`; chroma-key first if needed.
- Compose previews with `scripts/compose_layered_preview.py`.

## Deliverables

Baked: `assets/map/<name>.png`, optional prompt/collision/zones, loading code.

Layered: base/prompt, optional dressed reference, prop PNGs, props/collision/zones JSON, layered preview, loading/y-sort/collision code.

Tilemap: visual tileset, atlas metadata, engine-native layers/objects, preview. Never script-draw final tiles unless placeholder requested.
