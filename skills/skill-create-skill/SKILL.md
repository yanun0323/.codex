---
name: skill-create-skill
description: Create or update skills in this repository and normalize all folders under skills/. Use when asked to create a new skill, migrate existing skill naming, or enforce metadata conventions.synchronized SKILL.md frontmatter name, standardized icon assets, and standardized agents/openai.yaml display_name and icon_small.
---

# Skill Create Skill

## Overview

Use this skill to create new skills and to normalize existing skills so naming, icons, and UI metadata stay consistent.
Follow the same six-step creation lifecycle used by `skills/.system/skill-creator` (understand, plan resources, initialize, edit, validate, iterate).

Read `references/normalization-rules.md` before making edits.

## Required Resources

- Rules: `references/normalization-rules.md`
- Shared icons: `references/icons/rule-small.svg`, `references/icons/command-small.svg`, `references/icons/skill-small.svg`
- Automation: `scripts/normalize_skill_catalog.rb`

## Workflow

1. Discover all skills by scanning for `skills/**/SKILL.md`.
2. Classify each skill by folder name:
   - `agents-*` => `rule-*`
   - `command-*` => `command-*`
   - Any other prefix => `skill-*`
3. Rename folders to match the classification.
4. Update `SKILL.md` frontmatter `name` to match the folder name exactly.
5. Copy the correct icon file into each skill `assets/` directory:
   - `rule-*` => `rule-small.svg`
   - `command-*` => `command-small.svg`
   - `skill-*` => `skill-small.svg`
6. Ensure `agents/openai.yaml` exists and enforce:
   - `interface.display_name` format: `Rule - Xxx Xxx`, `Command - Xxx Xxx`, or `Skill - Xxx Xxx`
   - `interface.icon_small`: `./assets/<icon-file>`
7. Update `AGENTS.md` index entries if naming or inventory changed.
8. Verify results with `--check` mode.

## Commands

Apply normalization:

```bash
ruby skills/skill-create-skill/scripts/normalize_skill_catalog.rb
```

Validate without changes:

```bash
ruby skills/skill-create-skill/scripts/normalize_skill_catalog.rb --check
```

Normalize a different root:

```bash
ruby skills/skill-create-skill/scripts/normalize_skill_catalog.rb --skills-root path/to/skills
```

## Constraints

- Keep repository artifacts in English.
- Do not remove existing `openai.yaml` fields other than updating required interface fields.
- Treat hidden skill folders (for example `skills/.system/*`) as normal skills if they contain `SKILL.md`.
