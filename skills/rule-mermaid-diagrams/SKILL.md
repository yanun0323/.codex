---
name: rule-mermaid-diagrams
description: Rules for creating readable Mermaid diagrams in Markdown, especially flowchart and graph diagrams.
---

# Mermaid Diagram Rules

- Put diagrams in fenced `mermaid` blocks and add a short purpose sentence.
- For `flowchart`/`graph`, keep each diagram to 12 visible nodes or fewer; split larger flows.
- Useful splits: overview, happy path, error path, data flow, actor handoff, state transition.
- Each split diagram must stand alone and relate clearly to the whole.
- Use short labels, stable node IDs, `TD` for top-down, `LR` for left-right.
- Avoid dense cross-links, deep subgraphs, and overloaded labels.
