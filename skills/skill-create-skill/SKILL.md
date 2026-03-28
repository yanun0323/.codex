---
name: skill-create-skill
description: Create or update skills with strict Command/Rule/Skill normalization. Use this when users ask to create a new skill, modify an existing skill, migrate naming conventions, or enforce folder/frontmatter/icon/agents metadata consistency.
---

# Skill Skill Creator

This skill guides Codex to create and maintain skills with consistent naming, metadata, and packaging.

## Overview

Use this skill to create or update skill folders and enforce deterministic conventions for:

- Folder naming and `SKILL.md` frontmatter `name`
- `assets/` icon selection by type
- `agents/openai.yaml` display and icon fields
- Command-specific description constraints

Use the same six-step lifecycle for reliable outcomes:

1. Understand the request and classify target type
2. Plan reusable resources
3. Initialize or migrate the skill
4. Edit resources and instructions
5. Validate
6. Iterate

## Required Resources

- Rules: `references/normalization-rules.md`
- OpenAI YAML reference: `references/openai_yaml.md`
- Shared icons:
  - `references/icons/rule-small.svg`
  - `references/icons/command-small.svg`
  - `references/icons/skill-small.svg`
- Automation:
  - `scripts/init_skill.py`
  - `scripts/generate_openai_yaml.py`
  - `scripts/normalize_skill_catalog.rb`
  - `scripts/quick_validate.py`

## Type Rules (Mandatory)

Always classify the user request as one of these types before editing files.

- `Command`
  - Folder and frontmatter name must use `command-` prefix.
  - `assets/command-small.svg` must exist.
  - `agents/openai.yaml` must use:
    - `interface.display_name: "Command - Xxx Xxx"`
    - `interface.icon_small: "./assets/command-small.svg"`
  - `SKILL.md` frontmatter description must include:
    - `Use this skill only when the user explicitly asks to invoke`

- `Rule`
  - Folder and frontmatter name must use `rule-` prefix.
  - `assets/rule-small.svg` must exist.
  - `agents/openai.yaml` must use:
    - `interface.display_name: "Rule - Xxx Xxx"`
    - `interface.icon_small: "./assets/rule-small.svg"`

- `Skill`
  - Folder and frontmatter name must use `skill-` prefix.
  - `assets/skill-small.svg` must exist.
  - `agents/openai.yaml` must use:
    - `interface.display_name: "Skill - Xxx Xxx"`
    - `interface.icon_small: "./assets/skill-small.svg"`

Compatibility mapping for older names:

- `agents-*` must be normalized to `rule-*`.

## Workflow

### Step 1: Understand and Classify

Identify whether the user is creating/updating a `Command`, `Rule`, or `Skill`.
If the requested name does not match the target prefix, normalize it.

### Step 2: Plan Reusable Resources

For each concrete example, decide whether to include:

- `scripts/` for deterministic execution
- `references/` for large procedural or domain docs
- `assets/` for templates/icons/artifacts used in output

Keep SKILL instructions concise. Move variant-heavy details into `references/`.

### Step 3: Initialize or Migrate

For new skills, initialize with type-aware naming:

```bash
python3 skills/skill-create-skill/scripts/init_skill.py <name> --kind <command|rule|skill> --path <skills-root>
```

Useful variants:

```bash
python3 skills/skill-create-skill/scripts/init_skill.py interface-design-audit --kind command --path skills --resources scripts,references,assets
python3 skills/skill-create-skill/scripts/init_skill.py global --kind rule --path skills
python3 skills/skill-create-skill/scripts/init_skill.py doc-coauthoring --kind skill --path skills --interface short_description="Draft and refine documentation"
```

For existing catalogs, normalize all folders:

```bash
ruby skills/skill-create-skill/scripts/normalize_skill_catalog.rb
```

### Step 4: Edit Skill Contents

After initialization:

- Complete `SKILL.md` with clear trigger-oriented description.
- Ensure frontmatter contains only `name` and `description`.
- Keep body procedural and concise.
- Update or regenerate `agents/openai.yaml` as needed.
- Ensure icon files in `assets/` match type.
- For Command skills, keep the explicit invoke-only description sentence.

Regenerate UI metadata when needed:

```bash
python3 skills/skill-create-skill/scripts/generate_openai_yaml.py <path/to/skill-folder> --interface display_name="..." --interface short_description="..."
```

### Step 5: Validate

Run both validators:

```bash
python3 skills/skill-create-skill/scripts/quick_validate.py <path/to/skill-folder>
ruby skills/skill-create-skill/scripts/normalize_skill_catalog.rb --check
```

Expected validation outcomes:

- `SKILL.md` frontmatter is valid and constrained.
- Folder name and frontmatter `name` are aligned.
- Correct icon exists in `assets/`.
- `agents/openai.yaml` uses proper `display_name` and `icon_small`.
- Command descriptions contain the explicit invoke-only sentence.

### Step 6: Iterate

Refine based on real usage feedback:

1. Apply the skill on real tasks.
2. Note friction points or repetitive edits.
3. Move repetitive logic into scripts.
4. Re-run validations.

## Constraints

- Keep repository artifacts in English.
- Do not remove unrelated fields from `agents/openai.yaml`.
- Normalize hidden skill folders too if they contain `SKILL.md`.
- Do not create extra documentation files that are not required by the workflow.
