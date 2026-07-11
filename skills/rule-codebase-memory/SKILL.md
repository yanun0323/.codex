---
name: rule-codebase-memory
description: Rules for graph-first code discovery, architecture analysis, call tracing, and change-impact analysis through a bundled macOS codebase-memory-mcp CLI without MCP integration.
---

# Codebase Memory CLI Rules

## Scope

Use the bundled `scripts/cbm` wrapper as a local code-intelligence backend for repository exploration. Resolve it relative to this skill directory and invoke it by absolute path. Never call a `codebase-memory-mcp` binary from `PATH`. The wrapper allows only `--version` and `cli`, preventing MCP server mode and agent configuration commands. This rule covers code discovery and read-only analysis; normal file tools remain the source of truth for edits.

Before first use in a task, read [references/cli-workflow.md](references/cli-workflow.md). Run `scripts/cbm --version` and per-tool `--help`; CLI flags can change when the bundled binary is updated.

## Availability and Indexing

- Require macOS arm64. If the platform differs or the bundled binary is missing, report the incompatibility. Do not install, replace, or update it without user authorization.
- Run `scripts/cbm cli list_projects` before querying. Use the returned project name exactly.
- If the repository is missing, index its absolute root with `index_repository`. Prefer `full`; use `moderate` or `fast` only for an explicit speed/resource tradeoff.
- Check `index_status` before completeness-sensitive analysis. Re-index when the stored root, git context, or coverage is stale for the task.
- Keep `persistence=false` unless the user explicitly requests a shareable repository artifact.

## Discovery Order

1. `get_architecture` for unfamiliar repository structure and boundaries.
2. `search_graph` for symbols, definitions, routes, ranked concepts, and relationship filters.
3. `trace_path` for callers, callees, data flow, and impact paths.
4. `get_code_snippet` only after resolving an exact qualified name with `search_graph`.
5. `query_graph` for bounded multi-hop or aggregate questions not covered by a specialized command.
6. `search_code` or `rg` for literals, errors, configuration, generated code, and other text-level evidence.

Use the graph before broad `rg`, `find`, or file-by-file reads when locating code definitions or relationships. Narrow by project, label, file pattern, and limit. Page `search_graph` while `has_more` is true.

## Command Rules

- Prefer typed flags: `codebase-memory-mcp cli <tool> --flag value`. Raw JSON arguments are deprecated in current releases.
- Repeat array flags once per value, for example `--aspects overview --aspects dependencies`. Use `--help` to identify array-typed flags.
- Use `--json` only when machine-readable envelopes are needed. Do not assume undocumented `--raw` support.
- Quote regexes and Cypher queries. Keep Cypher read-only and add `LIMIT` to broad queries.
- Treat `delete_project`, `manage_adr` updates, `ingest_traces`, installation, update, and configuration changes as explicit user-authorized operations only.

## Verification and Fallback

Graph results are derived evidence, not source truth. Inspect the actual source before changing it. If `index_status` reports skipped or partially parsed files, also search those files and flagged ranges with `rg`. Fall back to normal file tools for dynamic dispatch, reflection, macros, generated sources, ignored files, unsupported syntax, or any graph/source disagreement. State coverage limitations in conclusions that depend on completeness.
