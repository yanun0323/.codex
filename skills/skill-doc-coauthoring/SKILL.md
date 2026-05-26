---
name: skill-doc-coauthoring
description: Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.
---

# Doc Co-Authoring Workflow

Guide substantial docs through three stages: context gathering, section-by-section drafting, and reader testing. Offer this workflow when users ask for docs, specs, proposals, RFCs, PRDs, decision docs, or similar; if declined, work freeform.

## Stage 1: Context

Ask initial meta-questions: doc type, audience, intended impact, template/format, constraints. If editing or using an existing file/link, read it. For images without alt text, explain the reader limitation and ask whether to generate alt text.

Invite an unstructured info dump: background, discussions, alternatives rejected, org context, timeline, architecture, dependencies, stakeholder concerns, links/channels/docs. Use available integrations when authorized; otherwise ask for pasted context.

After the dump, ask 5-10 numbered clarifying questions. Exit when you can ask edge-case/tradeoff questions without needing basics. Ask whether to add more context or move to drafting.

## Stage 2: Draft and Refine

Create a scaffold with section headers and placeholders in an artifact or markdown file. If structure is unclear, suggest 3-5 suitable sections. Start with the highest-uncertainty section; summaries usually last.

For each section:

1. Ask 5-10 section-specific questions.
2. Brainstorm 5-20 possible points.
3. Ask what to keep/remove/combine, accepting shorthand or freeform feedback.
4. Ask what is missing.
5. Replace the placeholder with drafted content.
6. Iterate with targeted edits only; do not reprint the whole doc.

After 3 low-change iterations, ask what can be removed. Near completion, reread the full doc for flow, consistency, redundancy, contradictions, generic filler, and whether every sentence earns its place.

## Stage 3: Reader Test

Goal: ensure a fresh reader can use the document.

If subagents are available, test directly:

1. Generate 5-10 likely reader questions.
2. Ask a fresh agent using only the doc.
3. Check ambiguity, hidden assumptions, contradictions, wrong answers.
4. Fix gaps and retest.

If no subagents, give manual test instructions: open a fresh Claude conversation, paste/share the doc, ask the generated questions plus ambiguity/assumption/contradiction checks, then report failures for fixing.

## Final

When reader testing passes, ask the user to do a final owner read-through, fact/link check, and impact check. Offer one final review or mark complete.
