---
name: skill-mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
license: Complete terms in LICENSE.txt
---

# MCP Server Development Guide

Build MCP servers that let agents complete real tasks through clear, safe tools.

## Research and Plan

1. Review current MCP docs. Start with `https://modelcontextprotocol.io/sitemap.xml`, then fetch relevant `.md` pages.
2. Prefer TypeScript for broad SDK/runtime support; Python/FastMCP is fine when repo context favors it.
3. Read only needed references:
   - `reference/mcp_best_practices.md`
   - `reference/node_mcp_server.md`
   - `reference/python_mcp_server.md`
   - `reference/evaluation.md`
   - SDK READMEs from official GitHub when needed.
4. Study target API docs: auth, pagination, rate limits, data models, errors.
5. Prefer comprehensive API coverage; add workflow tools only for common multi-step tasks.

## Tool Design

- Use consistent action-oriented names with service prefix.
- Keep descriptions concise and discoverable.
- Use Zod (TypeScript) or Pydantic (Python) schemas with constraints and examples.
- Return focused results with pagination/filtering.
- Use structured output when supported.
- Add annotations: `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`.
- Errors must be actionable with next steps.
- Never expose secrets; model auth and destructive actions explicitly.

## Implementation

Create shared API client, auth, error handling, response formatting, and pagination. Use async I/O. Avoid duplicated code while preserving clear tool boundaries. Follow language guide project structure and build scripts.

## Test

- TypeScript: `npm run build`; inspect with `npx @modelcontextprotocol/inspector`.
- Python: `python -m py_compile ...`; inspect with MCP Inspector.
- Verify representative success, empty, pagination, auth/error, and destructive-safety cases.

## Evaluations

After implementation, create 10 read-only, independent, realistic, complex, stable, verifiable questions. First inspect tools and explore data yourself; verify each answer. Store as:

```xml
<evaluation>
  <qa_pair>
    <question>...</question>
    <answer>...</answer>
  </qa_pair>
</evaluation>
```
