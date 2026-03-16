#!/usr/bin/env python3
"""Quick validation script for prompts and skills."""

import re
import sys
from pathlib import Path

MAX_ITEM_NAME_LENGTH = 64


def strip_wrapping_quotes(value):
    if len(value) >= 2 and (
        (value.startswith('"') and value.endswith('"'))
        or (value.startswith("'") and value.endswith("'"))
    ):
        return value[1:-1]
    return value


def parse_frontmatter_map(frontmatter_text):
    """
    Parse top-level YAML-like key/value pairs.
    This validator intentionally focuses on common scalar frontmatter patterns.
    """
    parsed = {}
    top_level_keys = []

    for raw_line in frontmatter_text.splitlines():
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue
        if raw_line[0].isspace():
            continue
        match = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", raw_line)
        if not match:
            continue
        key = match.group(1).strip()
        value = strip_wrapping_quotes(match.group(2).strip())
        top_level_keys.append(key)
        parsed[key] = value

    return parsed, top_level_keys


def validate_skill(skill_path):
    """Basic validation of a skill."""
    skill_path = Path(skill_path)

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)
    frontmatter, top_level_keys = parse_frontmatter_map(frontmatter_text)

    allowed_properties = {"name", "description", "license", "allowed-tools", "metadata"}

    unexpected_keys = set(top_level_keys) - allowed_properties
    if unexpected_keys:
        allowed = ", ".join(sorted(allowed_properties))
        unexpected = ", ".join(sorted(unexpected_keys))
        return (
            False,
            f"Unexpected key(s) in SKILL.md frontmatter: {unexpected}. Allowed properties are: {allowed}",
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name", "").strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return (
                False,
                f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)",
            )
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return (
                False,
                f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
            )
        if len(name) > MAX_ITEM_NAME_LENGTH:
            return (
                False,
                f"Name is too long ({len(name)} characters). "
                f"Maximum is {MAX_ITEM_NAME_LENGTH} characters.",
            )

    description = frontmatter.get("description", "").strip()
    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return (
                False,
                f"Description is too long ({len(description)} characters). Maximum is 1024 characters.",
            )

    return True, "Skill is valid!"


def validate_prompt(prompt_path):
    """Basic validation of a Codex prompt file."""
    prompt_path = Path(prompt_path)

    if not prompt_path.exists():
        return False, "Prompt file not found"
    if prompt_path.suffix != ".md":
        return False, "Prompt file must use the .md extension"

    content = prompt_path.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)
    frontmatter, top_level_keys = parse_frontmatter_map(frontmatter_text)
    allowed_properties = {"description"}

    unexpected_keys = set(top_level_keys) - allowed_properties
    if unexpected_keys:
        allowed = ", ".join(sorted(allowed_properties))
        unexpected = ", ".join(sorted(unexpected_keys))
        return (
            False,
            f"Unexpected key(s) in prompt frontmatter: {unexpected}. Allowed properties are: {allowed}",
        )

    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    description = frontmatter.get("description", "").strip()
    if not description:
        return False, "Description cannot be empty"
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets (< or >)"
    if len(description) > 1024:
        return (
            False,
            f"Description is too long ({len(description)} characters). Maximum is 1024 characters.",
        )

    body = content[match.end() :].strip()
    if not body:
        return False, "Prompt body cannot be empty"

    return True, "Prompt is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory_or_prompt_file>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if target.is_dir():
        valid, message = validate_skill(target)
    else:
        valid, message = validate_prompt(target)

    print(message)
    sys.exit(0 if valid else 1)
