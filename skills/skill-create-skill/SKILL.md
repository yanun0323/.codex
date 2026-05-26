---
name: skill-create-skill
description: Create or update skills with strict Action/Rule/Skill normalization. Use this when users ask to create a new skill, modify an existing skill, migrate naming conventions, or enforce folder/frontmatter/icon/agents metadata consistency.
---

# Skill Creator

Create or update skill folders with deterministic naming, metadata, icons, and validation. Keep every `SKILL.md` as short as possible without reducing goal achievement; move bulky variants into `references/` or scripts.

## Resources

- Rules: `references/normalization-rules.md`
- YAML: `references/openai_yaml.md`
- Icons: `references/icons/{action,rule,skill}-small.svg`
- Scripts: `scripts/init_skill.py`, `generate_openai_yaml.py`, `normalize_skill_catalog.rb`, `quick_validate.py`

## Type Rules

Classify before editing:

- `Action`: folder/name prefix `action-`; copy `assets/action-small.svg`; `openai.yaml` display `"Action - Xxx Xxx"` and icon `"./assets/action-small.svg"`; description must include `Use this skill only when the user explicitly asks to invoke`.
- `Rule`: folder/name prefix `rule-`; copy `assets/rule-small.svg`; display `"Rule - Xxx Xxx"`; icon `"./assets/rule-small.svg"`.
- `Skill`: folder/name prefix `skill-`; copy `assets/skill-small.svg`; display `"Skill - Xxx Xxx"`; icon `"./assets/skill-small.svg"`.
- Normalize legacy `agents-*` names to `rule-*`.

## Workflow

1. Identify create/update/migrate request and target type.
2. Plan only needed `scripts/`, `references/`, and `assets/`.
3. For new skills, run:

```bash
python3 skills/skill-create-skill/scripts/init_skill.py <name> --kind <action|rule|skill> --path <skills-root>
```

4. Edit `SKILL.md`: frontmatter only `name` and `description`; body procedural, concise, and trigger-oriented.
5. Update or regenerate `agents/openai.yaml` only as needed:

```bash
python3 skills/skill-create-skill/scripts/generate_openai_yaml.py <skill-folder> --interface display_name="..." --interface short_description="..."
```

6. Validate:

```bash
python3 skills/skill-create-skill/scripts/quick_validate.py <skill-folder>
ruby skills/skill-create-skill/scripts/normalize_skill_catalog.rb --check
```

## Constraints

Keep artifacts in English. Do not remove unrelated `agents/openai.yaml` fields. Normalize hidden skill folders containing `SKILL.md`. Do not create extra docs unless required.
