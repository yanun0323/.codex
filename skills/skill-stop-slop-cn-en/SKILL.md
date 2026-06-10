---
name: skill-stop-slop-cn-en
description: Use when editing Chinese or bilingual prose to remove AI-sounding phrasing, preserve factual boundaries, and produce natural writing for articles, research notes, social posts, documentation, and chat replies.
---

# Skill - Stop Slop CN-EN

Use this skill to revise Chinese, English, or bilingual prose so it reads like a specific human wrote it, not like a model completed a template.

## When to Use

Use when the user asks to:

- Make Chinese or bilingual writing more natural, less AI-sounding, less templated, or less "slop".
- Diagnose whether a passage sounds AI-written and identify concrete problems.
- Rewrite research notes, public articles, social posts, product copy, documentation, PR descriptions, README text, email, or chat replies.
- Turn technical, financial, macro, company, econometrics, or AI-tool analysis into readable public-facing Chinese while keeping precision.
- Do a final anti-template pass on a long response before delivering it.

Do not use when the user explicitly wants machine-style output, strict SOPs, legal clauses, exam answers, highly structured reports, or verbatim preservation.

## References

Load only what the task needs:

- `references/phrases-cn.md`: high-frequency Chinese AI-sounding phrases.
- `references/structures-cn.md`: structural patterns that make Chinese prose feel templated.
- `references/examples-cn.md`: rewrite examples.
- `references/checklist-cn.md`: final review checklist.

## Workflow

1. Identify the target format: academic, public article, social post, README, technical documentation, investment research, email, or chat reply.
2. Separate facts, inferences, unknowns, and user-provided claims. Do not invent data, examples, quotes, sources, or business logic.
3. Remove meta-announcements, generic praise, over-polite chat filler, abstract slogans, and unsupported significance claims.
4. Reduce mechanical list structure unless the target format needs lists or steps.
5. Replace vague words with concrete actions, actors, dates, scope, evidence, and constraints when the source text supports them.
6. Vary rhythm with short judgment sentences, medium explanatory sentences, and longer causal sentences where needed.
7. Preserve domain precision. For finance, macro, legal, academic, or company research text, keep source boundaries and uncertainty explicit.
8. Run the final checklist before output.

## Output Modes

Choose the smallest useful output:

- Rewrite only: provide the revised text directly.
- Diagnosis plus rewrite: list the main issues, then provide the revised text.
- Strict review: give AI-sounding risk level, quote tight problem locations, explain why, then rewrite.
- File edit: state the file sections being changed, patch the file, then summarize the diff and verification.

## Style Rules

- Prefer direct claims over "this article will analyze" framing.
- Use continuous prose for public articles unless bullets are clearly useful.
- Keep lists for technical documentation, README instructions, and ordered procedures.
- Do not turn academic or research prose into casual speech.
- Do not add unsupported color, stories, examples, or emotional language to make text feel human.
- Keep endings concrete: a judgment, caveat, risk, or open question beats a generic uplifting summary.

## Verification

Before final output, check:

- No "below I will", "overall", "worth noting", or similar empty meta-transition remains unless necessary.
- Lists, bold labels, and headings are not mechanically overused.
- Abstract claims have evidence or are removed.
- Facts, inferences, and missing data remain distinguishable.
- English AI phrasing has not been translated directly into awkward Chinese.
- The result matches the target platform and domain.

## Attribution

Adapted from `hardikpandya/stop-slop` under the MIT License, with Chinese and bilingual writing rules preserved in `references/`.
