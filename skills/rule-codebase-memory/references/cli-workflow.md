# Native CLI Workflow

This reference translates the upstream MCP tool model into direct local CLI usage through the bundled macOS arm64 wrapper. It must not configure or launch MCP.

## Bootstrap

```bash
CBM="${CODEX_HOME:-$HOME/.codex}/skills/rule-codebase-memory/scripts/cbm"
"$CBM" --version
"$CBM" cli list_projects
"$CBM" cli index_repository --repo-path /absolute/repository/path --mode full
"$CBM" cli index_status --project exact-project-name
```

Use `"$CBM" cli <tool> --help` as the bundled version's parameter authority. The wrapper rejects MCP server, install, update, config, and other non-CLI modes. Do not bypass it. Binary provenance and update requirements are in [vendor-binary.md](vendor-binary.md).

## Query Selection

| Question | Command | Primary inputs |
| --- | --- | --- |
| What is this repository's shape? | `get_architecture` | `--project`, optional `--path`, `--aspects` |
| Where is a symbol or concept? | `search_graph` | `--project`, `--query` or `--name-pattern`, optional `--label`, `--file-pattern` |
| Who calls this, or what does it call? | `trace_path` | `--project`, `--function-name`, `--direction`, `--depth` |
| How does a value move? | `trace_path` | `--mode data_flow`, optional `--parameter-name` |
| What source belongs to this graph node? | `get_code_snippet` | exact `--qualified-name`, `--project` |
| What changed and what may break? | `detect_changes` | `--project`, optional `--scope`, `--depth`, `--base-branch` or `--since` |
| What multi-hop pattern exists? | `query_graph` | `--project`, bounded `--query` |
| Where is literal text? | `search_code` | `--project`, `--pattern`, optional file/path filters |
| What labels and edges exist here? | `get_graph_schema` | `--project` |

## Examples

```bash
"$CBM" cli get_architecture \
  --project my-project \
  --aspects overview \
  --aspects dependencies \
  --aspects boundaries

"$CBM" cli search_graph \
  --project my-project \
  --query 'update settings' \
  --label Function \
  --limit 50

"$CBM" cli search_graph \
  --project my-project \
  --name-pattern '.*OrderHandler.*' \
  --file-pattern '.*internal/.*'

"$CBM" cli trace_path \
  --project my-project \
  --function-name ProcessOrder \
  --direction inbound \
  --depth 3 \
  --risk-labels true

"$CBM" cli get_code_snippet \
  --project my-project \
  --qualified-name my-project.internal.orders.ProcessOrder

"$CBM" cli query_graph \
  --project my-project \
  --query 'MATCH (f:Function)-[:CALLS]->(g:Function) RETURN f.qualified_name, g.qualified_name LIMIT 100'

"$CBM" cli search_code \
  --project my-project \
  --pattern 'permission denied' \
  --path-filter '^src/' \
  --limit 20
```

## Interpretation

- `search_graph --query` performs ranked keyword discovery. `--name-pattern` is for exact regex-oriented symbol matching. Consult `--help` before using semantic search because its input shape and index-mode requirements are version-sensitive.
- Array-typed flags accumulate through repetition: `--semantic-query send --semantic-query publish`. Do not pass a JSON array string to a typed flag.
- `trace_path` is breadth-first and depth-bounded. Start at depth 2 or 3; increase only when the returned path warrants it.
- `get_code_snippet` is a reader, not a discovery command. Resolve ambiguity through `search_graph` first.
- `query_graph` supports a Cypher-like read subset, not arbitrary database mutation. Query the schema first when labels or edge types are uncertain.
- Default compact output is best for agent context. Use `--json` only for reliable parsing; parse `structuredContent` from the result envelope.
- For paginated graph search, inspect `total` and `has_more`, then increase `offset` by `limit` until complete or until enough evidence exists.

## Coverage Boundary

The graph may omit ignored, oversized, unreadable, or partially parsed code. `index_status` distinguishes deliberate exclusions from detected indexing failures. Absence of a warning is not proof of completeness. Confirm security-, migration-, concurrency-, money-, or deletion-sensitive conclusions in source and tests. Use `rg` for string literals and inside every reported coverage gap.
