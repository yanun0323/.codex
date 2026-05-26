---
name: skill-create-skill
description: Create or update skills with strict Action/Rule/Skill normalization. Use this when users ask to create a new skill, modify an existing skill, migrate naming conventions, or enforce folder/frontmatter/icon/agents metadata consistency.
---

# Skill Creator

Create/update skill folders with deterministic naming, metadata, icons, and validation. Keep `SKILL.md` minimal; move bulky variants to `references/` or scripts.

## Resources

- `references/normalization-rules.md`, `references/openai_yaml.md`
- `references/icons/{action,rule,skill}-small.svg`
- `scripts/init_skill.py`, `generate_openai_yaml.py`, `normalize_skill_catalog.rb`, `quick_validate.py`

## Type Rules

- Action: `action-`; action icon; display `"Action - Xxx"`; description includes `Use this skill only when the user explicitly asks to invoke`.
- Rule: `rule-`; rule icon; display `"Rule - Xxx"`.
- Skill: `skill-`; skill icon; display `"Skill - Xxx"`.
- Normalize legacy `agents-*` folders to `rule-*`.

## Workflow

1. Identify create/update/migrate target and type.
2. Add only needed `scripts/`, `references/`, `assets/`.
3. For new skills:

```bash
python3 skills/skill-create-skill/scripts/init_skill.py <name> --kind <action|rule|skill> --path <skills-root>
```

4. Edit `SKILL.md`: frontmatter only `name`/`description`; body concise, procedural, trigger-oriented.
5. Update `agents/openai.yaml` only as needed:

```bash
python3 skills/skill-create-skill/scripts/generate_openai_yaml.py <skill-folder> --interface display_name="..." --interface short_description="..."
```

6. Validate:

```bash
python3 skills/skill-create-skill/scripts/quick_validate.py <skill-folder>
ruby skills/skill-create-skill/scripts/normalize_skill_catalog.rb --check
```

Keep artifacts English. Preserve unrelated YAML fields. Normalize hidden folders with `SKILL.md`. Do not add docs unless required.
