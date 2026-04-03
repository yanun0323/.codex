#!/usr/bin/env python3

import argparse
import shutil
import sys
from pathlib import Path

START_MARKER = "<!-- action-design:start -->"
END_MARKER = "<!-- action-design:end -->"

MANAGED_BLOCK = """<!-- action-design:start -->
Managed by `action-design`. Update this block via the skill.

If `./.design/` exists, read `./.design/DESIGN.md` before any design or frontend implementation.
Treat all files inside `./.design/` as mandatory design instructions.
Do not introduce visual direction, components, colors, typography, spacing, or motion that conflicts with `./.design/` unless a higher-priority instruction explicitly overrides it.
When relevant, also inspect `./.design/README.md`, `./.design/preview.html`, `./.design/preview-dark.html`, `./.design/preview-screenshot.png`, and `./.design/preview-dark-screenshot.png`.
<!-- action-design:end -->
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install a bundled design reference into a project."
    )
    parser.add_argument(
        "--skill-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Path to the action-design skill directory.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Target project root. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--design",
        help="Design slug to install. If omitted, an interactive prompt is shown.",
    )
    parser.add_argument(
        "--mode",
        choices=("replace", "merge", "cancel"),
        help="Conflict strategy when .design already exists.",
    )
    return parser.parse_args()


def list_designs(reference_root: Path) -> list[str]:
    return sorted(path.name for path in reference_root.iterdir() if path.is_dir())


def resolve_design(choice: str, designs: list[str]) -> str | None:
    if choice in designs:
        return choice
    folded = {design.casefold(): design for design in designs}
    if choice.casefold() in folded:
        return folded[choice.casefold()]
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(designs):
            return designs[index]
    return None


def prompt_for_design(designs: list[str]) -> str:
    print("Available designs:")
    for index, design in enumerate(designs, start=1):
        print(f"  {index:>2}. {design}")

    while True:
        choice = input("Select a design by number or slug: ").strip()
        resolved = resolve_design(choice, designs)
        if resolved:
            return resolved
        print("Invalid selection. Choose one of the listed slugs or numbers.")


def prompt_for_mode() -> str:
    while True:
        choice = input("`./.design/` already exists. Choose Replace / Merge / Cancel: ")
        normalized = choice.strip().casefold()
        if normalized in {"replace", "merge", "cancel"}:
            return normalized
        print("Invalid mode. Enter Replace, Merge, or Cancel.")


def ensure_reference(skill_root: Path, design: str) -> Path:
    reference_dir = skill_root / "references" / design
    if not reference_dir.is_dir():
        raise FileNotFoundError(f"Design '{design}' does not exist in {skill_root / 'references'}")
    return reference_dir


def copy_reference(source: Path, target: Path, mode: str | None) -> str:
    if not target.exists():
        shutil.copytree(source, target)
        return "created"

    selected_mode = mode or prompt_for_mode()
    if selected_mode == "cancel":
        return "cancelled"
    if selected_mode == "replace":
        shutil.rmtree(target)
        shutil.copytree(source, target)
        return "replaced"

    shutil.copytree(source, target, dirs_exist_ok=True)
    return "merged"


def upsert_managed_block(agents_path: Path) -> None:
    if not agents_path.exists():
        agents_path.write_text("# Project Instructions\n\n" + MANAGED_BLOCK, encoding="utf-8")
        return

    content = agents_path.read_text(encoding="utf-8")
    if START_MARKER in content and END_MARKER in content:
        start_index = content.index(START_MARKER)
        end_index = content.index(END_MARKER) + len(END_MARKER)
        replacement = MANAGED_BLOCK.rstrip()
        updated = content[:start_index].rstrip() + "\n\n" + replacement
        tail = content[end_index:].lstrip()
        if tail:
            updated += "\n\n" + tail
        else:
            updated += "\n"
        agents_path.write_text(updated, encoding="utf-8")
        return

    content = content.rstrip()
    if content:
        content += "\n\n"
    content += MANAGED_BLOCK
    agents_path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    skill_root = args.skill_root.resolve()
    project_root = args.project_root.resolve()
    reference_root = skill_root / "references"

    if not reference_root.is_dir():
        print(f"Reference catalog not found: {reference_root}", file=sys.stderr)
        return 1

    designs = list_designs(reference_root)
    if not designs:
        print(f"No designs found in {reference_root}", file=sys.stderr)
        return 1

    selected = resolve_design(args.design, designs) if args.design else None
    if args.design and not selected:
        print(f"Unknown design '{args.design}'.", file=sys.stderr)
        print("Available designs:", ", ".join(designs), file=sys.stderr)
        return 1
    selected = selected or prompt_for_design(designs)

    source = ensure_reference(skill_root, selected)
    design_dir = project_root / ".design"
    result = copy_reference(source, design_dir, args.mode)
    if result == "cancelled":
        print("Cancelled. No files were changed.")
        return 0

    upsert_managed_block(project_root / "AGENTS.md")

    print(f"Installed design: {selected}")
    print(f".design status: {result}")
    print("AGENTS.md status: updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
