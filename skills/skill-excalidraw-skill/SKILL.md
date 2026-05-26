---
name: skill-excalidraw-skill
description: Programmatic canvas toolkit for creating, editing, and refining Excalidraw diagrams via MCP tools with real-time canvas sync. Use when an agent needs to (1) draw or lay out diagrams on a live canvas, (2) iteratively refine diagrams using describe_scene and get_canvas_screenshot to see its own work, (3) export/import .excalidraw files or PNG/SVG images, (4) save/restore canvas snapshots, (5) convert Mermaid to Excalidraw, or (6) perform element-level CRUD, alignment, distribution, grouping, duplication, and locking. Requires a running canvas server (EXPRESS_SERVER_URL, default http://localhost:3000).
---

# Excalidraw Skill

Programmatically create/refine Excalidraw diagrams. Prefer MCP tools; fallback to REST at `http://localhost:3000`.

If neither works, tell the user to start the canvas server:

```bash
git clone https://github.com/yctimlin/mcp_excalidraw && cd mcp_excalidraw
npm ci && npm run build
PORT=3000 npm run canvas
```

## Mode Differences

- MCP labels: `"text": "Label"`; REST labels: `"label": {"text": "Label"}`.
- MCP arrows: `startElementId`/`endElementId`; REST arrows: `"start": {"id": ...}` / `"end": {"id": ...}`.
- `fontFamily` must be a string or omitted.
- REST updates should re-include `label`.

## Layout Rules

- Coordinates: origin `(0,0)`, x right, y down.
- Plan grid before JSON. Tier gaps 80-120px; sibling gaps 40-60px.
- Shape width `max(160, label chars * 9)`; height 60 single-line, 80 two-line.
- Background zones need 50px padding.
- Do not put labels on large background rectangles; use free-standing text at zone top.
- Avoid cross-zone arrows through content; route along edges with elbow/waypoints.
- Use arrow labels sparingly and keep them <=12 chars.

## Create Workflow

Use Mermaid conversion for existing Mermaid or clean flow/sequence/ER structures. Use direct element creation for precise/custom architecture diagrams.

MCP:

1. Optionally `read_diagram_guide`.
2. Plan tiers/x positions.
3. Optional `clear_canvas`.
4. `batch_create_elements` with stable ids.
5. Bind arrows with `startElementId`/`endElementId`.
6. `set_viewport(scrollToContent: true)`.
7. `get_canvas_screenshot`, inspect, fix, repeat.

REST: same plan, using `/api/elements/batch`, `/api/viewport`, `/api/export/image`.

## Quality Loop

After every batch/update, inspect screenshot for text truncation, overlap, arrow crossing, arrow-label collision, cramped spacing, small fonts, and zone-label mistakes. If any issue appears, stop, fix, and re-screenshot before continuing.

Use `describe_scene` for ids/positions/connections and `get_canvas_screenshot` for rendered quality. Identify elements by id/label, not coordinates.

## Operations

- Refine: `describe_scene` -> `update_element`/`delete_element` -> screenshot.
- Mermaid: `create_from_mermaid`, then viewport + screenshot; reposition if auto-layout is poor.
- File I/O: `export_scene`, `import_scene`, `export_to_image`, `export_to_excalidraw_url`; REST/CLI equivalents in `references/cheatsheet.md`.
- Snapshots: `snapshot_scene` before risky changes; `restore_snapshot` to roll back.
- Duplicate repeated layouts with `duplicate_elements`.

## Recovery

Off-screen: set viewport to content. Bad arrows: verify ids and bindings. Locked elements: unlock first. Duplicate bound text: delete text elements with `containerId`, wait for sync, and avoid labels on background zones.
