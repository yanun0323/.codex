---
name: rule-mermaid-diagrams
description: Rules for creating readable Mermaid diagrams in Markdown, especially flowchart and graph diagrams.
---

# Mermaid Diagram Rules

Use this rule when creating, editing, or reviewing Mermaid diagrams in Markdown.

## Markdown

- Put Mermaid diagrams in fenced `mermaid` code blocks.
- Add a short paragraph before or after each diagram explaining its purpose.

## Flowchart / Graph Limits

- For `flowchart` and `graph`, keep each diagram to 12 nodes or fewer.
- Count every unique visible node as one node.
- `subgraph` labels do not count as nodes, but nodes inside them do.
- If a diagram would exceed 12 nodes, split it into multiple diagrams.

## Splitting Large Flows

When splitting a large flow, use separate diagrams for different views, such as:

- overview
- happy path
- error path
- data flow
- actor handoff
- state transition

Each split diagram must be understandable on its own and clearly relate to the overall flow.

## Readability

- Use short node labels.
- Prefer stable, readable node IDs.
- Choose `TD` for top-down flows and `LR` for left-to-right flows.
- Avoid dense cross-links, deeply nested subgraphs, and overloaded labels.
