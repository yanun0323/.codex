#!/usr/bin/env python3
"""
Skill Initializer - Creates a new Action/Rule/Skill from template.

Usage:
    init_skill.py <name> --kind <action|rule|skill> --path <path>
      [--resources scripts,references,assets] [--examples] [--interface key=value]
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

from generate_openai_yaml import write_openai_yaml

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_RESOURCES = {"scripts", "references", "assets"}
KNOWN_PREFIXES = ("action-", "command-", "rule-", "skill-", "agents-")

KIND_CONFIG = {
    "action": {
        "prefix": "action-",
        "label": "Action",
        "icon": "action-small.svg",
    },
    "rule": {
        "prefix": "rule-",
        "label": "Rule",
        "icon": "rule-small.svg",
    },
    "skill": {
        "prefix": "skill-",
        "label": "Skill",
        "icon": "skill-small.svg",
    },
}

DESCRIPTION_TEMPLATE = (
    "TODO: Complete and informative explanation of what this item does and when to use it. "
    "Include specific trigger scenarios, file types, or tasks."
)

ACTION_TRIGGER_SENTENCE = (
    "Use this skill only when the user explicitly asks to invoke the `{skill_name}` skill."
)

SKILL_TEMPLATE = """---
name: {skill_name}
description: "{description_text}"
---

# {skill_title}

## Overview

[TODO: 1-2 sentences explaining what this item enables]

## Structuring This Skill

[TODO: Choose the structure that best fits this skill's purpose. Common patterns:

**1. Workflow-Based** (best for sequential processes)
- Works well when there are clear step-by-step procedures
- Example: DOCX skill with "Workflow Decision Tree" -> "Reading" -> "Creating" -> "Editing"
- Structure: ## Overview -> ## Workflow Decision Tree -> ## Step 1 -> ## Step 2...

**2. Task-Based** (best for tool collections)
- Works well when the skill offers different operations/capabilities
- Example: PDF skill with "Quick Start" -> "Merge PDFs" -> "Split PDFs" -> "Extract Text"
- Structure: ## Overview -> ## Quick Start -> ## Task Category 1 -> ## Task Category 2...

**3. Reference/Guidelines** (best for standards or specifications)
- Works well for brand guidelines, coding standards, or requirements
- Example: Brand styling with "Brand Guidelines" -> "Colors" -> "Typography" -> "Features"
- Structure: ## Overview -> ## Guidelines -> ## Specifications -> ## Usage...

**4. Capabilities-Based** (best for integrated systems)
- Works well when the skill provides multiple interrelated features
- Example: Product Management with "Core Capabilities" -> numbered capability list
- Structure: ## Overview -> ## Core Capabilities -> ### 1. Feature -> ### 2. Feature...

Patterns can be mixed and matched as needed. Most skills combine patterns (e.g., start with task-based, add workflow for complex operations).

Delete this entire "Structuring This Skill" section when done - it's just guidance.]

## [TODO: Replace with the first main section based on chosen structure]

[TODO: Add content here. Include concrete examples and references to scripts/references/assets as needed.]

## Resources (optional)

Create only the resource directories this skill actually needs. Delete this section if no resources are required.

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

### references/
Documentation and reference material intended to be loaded into context to inform Codex's process and thinking.

### assets/
Files not intended to be loaded into context, but rather used within the output Codex produces.

---

**Not every skill requires all three types of resources.**
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example helper script for {skill_name}

This is a placeholder script that can be executed directly.
Replace with actual implementation or delete if not needed.
"""


def main():
    print("This is an example script for {skill_name}")


if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference Documentation for {skill_title}

This is a placeholder for detailed reference documentation.
Replace with actual reference content or delete if not needed.

## Suggested Structure

- Prerequisites
- Step-by-step instructions
- Common patterns
- Troubleshooting
- Best practices
"""

EXAMPLE_ASSET = """# Example Asset File

This placeholder represents where asset files would be stored.
Replace with actual asset files (templates, images, fonts, etc.) or delete if not needed.
"""


def normalize_skill_name(skill_name):
    """Normalize a skill name to lowercase hyphen-case."""
    normalized = skill_name.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized


def strip_known_prefix(name):
    for prefix in KNOWN_PREFIXES:
        if name.startswith(prefix):
            return name[len(prefix) :]
    return name


def enforce_kind_prefix(name, kind):
    config = KIND_CONFIG[kind]
    stem = strip_known_prefix(name)
    stem = normalize_skill_name(stem)
    if not stem:
        return None
    return f"{config['prefix']}{stem}"


def title_case_skill_name(skill_name):
    return " ".join(word.capitalize() for word in skill_name.split("-") if word)


def parse_resources(raw_resources):
    if not raw_resources:
        return []
    resources = [item.strip() for item in raw_resources.split(",") if item.strip()]
    invalid = sorted({item for item in resources if item not in ALLOWED_RESOURCES})
    if invalid:
        allowed = ", ".join(sorted(ALLOWED_RESOURCES))
        print(f"[ERROR] Unknown resource type(s): {', '.join(invalid)}")
        print(f"   Allowed: {allowed}")
        sys.exit(1)
    deduped = []
    seen = set()
    for resource in resources:
        if resource not in seen:
            deduped.append(resource)
            seen.add(resource)
    return deduped


def create_resource_dirs(skill_dir, skill_name, skill_title, resources, include_examples):
    for resource in resources:
        resource_dir = skill_dir / resource
        resource_dir.mkdir(exist_ok=True)
        if resource == "scripts":
            if include_examples:
                example_script = resource_dir / "example.py"
                example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
                example_script.chmod(0o755)
                print("[OK] Created scripts/example.py")
            else:
                print("[OK] Created scripts/")
        elif resource == "references":
            if include_examples:
                example_reference = resource_dir / "api_reference.md"
                example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
                print("[OK] Created references/api_reference.md")
            else:
                print("[OK] Created references/")
        elif resource == "assets":
            if include_examples:
                example_asset = resource_dir / "example_asset.txt"
                example_asset.write_text(EXAMPLE_ASSET)
                print("[OK] Created assets/example_asset.txt")
            else:
                print("[OK] Created assets/")


def build_description_text(kind, skill_name):
    if kind == "action":
        return f"{DESCRIPTION_TEMPLATE} {ACTION_TRIGGER_SENTENCE.format(skill_name=skill_name)}"
    return DESCRIPTION_TEMPLATE


def display_name_for_kind(kind, skill_name):
    config = KIND_CONFIG[kind]
    prefix = config["prefix"]
    stem = skill_name[len(prefix) :] if skill_name.startswith(prefix) else skill_name
    return f"{config['label']} - {title_case_skill_name(stem)}"


def ensure_kind_icon(skill_dir, kind):
    config = KIND_CONFIG[kind]
    tool_root = Path(__file__).resolve().parents[1]
    src = tool_root / "references" / "icons" / config["icon"]
    if not src.exists():
        print(f"[ERROR] Missing icon source: {src}")
        return False

    assets_dir = skill_dir / "assets"
    assets_dir.mkdir(exist_ok=True)
    dst = assets_dir / config["icon"]
    shutil.copyfile(src, dst)
    print(f"[OK] Ensured assets/{config['icon']}")
    return True


def build_interface_overrides(kind, skill_name, raw_interface_overrides):
    config = KIND_CONFIG[kind]
    defaults = [
        f"display_name={display_name_for_kind(kind, skill_name)}",
        f"icon_small=./assets/{config['icon']}",
    ]
    return defaults + list(raw_interface_overrides)


def init_skill(skill_name, kind, path, resources, include_examples, interface_overrides):
    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"[ERROR] Skill directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"[OK] Created skill directory: {skill_dir}")
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Error creating directory: {exc}")
        return None

    skill_title = title_case_skill_name(skill_name)
    description_text = build_description_text(kind, skill_name).replace('"', "'")
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        description_text=description_text,
        skill_title=skill_title,
    )

    skill_md_path = skill_dir / "SKILL.md"
    try:
        skill_md_path.write_text(skill_content)
        print("[OK] Created SKILL.md")
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Error creating SKILL.md: {exc}")
        return None

    try:
        result = write_openai_yaml(skill_dir, skill_name, interface_overrides)
        if not result:
            return None
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Error creating agents/openai.yaml: {exc}")
        return None

    if not ensure_kind_icon(skill_dir, kind):
        return None

    if resources:
        try:
            create_resource_dirs(skill_dir, skill_name, skill_title, resources, include_examples)
        except Exception as exc:  # noqa: BLE001
            print(f"[ERROR] Error creating resource directories: {exc}")
            return None

    print(f"\n[OK] {KIND_CONFIG[kind]['label']} '{skill_name}' initialized successfully at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md to complete TODO items and finalize trigger-based description")
    print("2. Confirm assets/ and agents/openai.yaml match the target type")
    print(
        "3. Run: python3 skills/skill-create-skill/scripts/quick_validate.py "
        f"{skill_dir}"
    )

    return skill_dir


def main():
    parser = argparse.ArgumentParser(
        description="Create a new action/rule/skill directory with a SKILL.md template.",
    )
    parser.add_argument("skill_name", help="Name to normalize and prefix")
    parser.add_argument(
        "--kind",
        choices=sorted(KIND_CONFIG.keys()),
        default="skill",
        help="Target type and prefix rule",
    )
    parser.add_argument("--path", required=True, help="Output directory for the skill")
    parser.add_argument(
        "--resources",
        default="",
        help="Comma-separated list: scripts,references,assets",
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Create example files inside selected resource directories",
    )
    parser.add_argument(
        "--interface",
        action="append",
        default=[],
        help="Interface override in key=value format (repeatable)",
    )
    args = parser.parse_args()

    raw_name = args.skill_name
    normalized_name = normalize_skill_name(raw_name)
    if not normalized_name:
        print("[ERROR] Skill name must include at least one letter or digit.")
        sys.exit(1)

    skill_name = enforce_kind_prefix(normalized_name, args.kind)
    if not skill_name:
        print("[ERROR] Unable to normalize skill name after prefix enforcement.")
        sys.exit(1)

    if len(skill_name) > MAX_SKILL_NAME_LENGTH:
        print(
            f"[ERROR] Skill name '{skill_name}' is too long ({len(skill_name)} characters). "
            f"Maximum is {MAX_SKILL_NAME_LENGTH} characters."
        )
        sys.exit(1)

    if skill_name != raw_name:
        print(f"Note: Normalized skill name from '{raw_name}' to '{skill_name}'.")

    resources = parse_resources(args.resources)
    if args.examples and not resources:
        print("[ERROR] --examples requires --resources to be set.")
        sys.exit(1)

    interface_overrides = build_interface_overrides(args.kind, skill_name, args.interface)

    print(f"Initializing {KIND_CONFIG[args.kind]['label']}: {skill_name}")
    print(f"   Location: {args.path}")
    if resources:
        print(f"   Resources: {', '.join(resources)}")
        if args.examples:
            print("   Examples: enabled")
    else:
        print("   Resources: none (create as needed)")
    print()

    result = init_skill(
        skill_name=skill_name,
        kind=args.kind,
        path=args.path,
        resources=resources,
        include_examples=args.examples,
        interface_overrides=interface_overrides,
    )

    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
