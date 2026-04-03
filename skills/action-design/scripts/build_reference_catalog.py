#!/usr/bin/env python3

import argparse
import functools
import http.server
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

README_LINK_RE = re.compile(
    r"https://github\.com/VoltAgent/awesome-design-md/blob/main/design-md/([^/]+)/([^)\s]+)"
)

README_IMAGE_RE = re.compile(
    r"https://pub-[^)\s]+/designs/([^/]+)/((?:preview(?:-dark)?-screenshot)\.png)"
)

CLI_RESULT_RE = re.compile(r"### Result\s*\n(.+)")
INITIAL_VIEWPORT_WIDTH = 1280
INITIAL_VIEWPORT_HEIGHT = 720
FULL_HEIGHT_EXPR = (
    "Math.max("
    "document.body ? document.body.scrollHeight : 0,"
    "document.documentElement ? document.documentElement.scrollHeight : 0,"
    "document.body ? document.body.offsetHeight : 0,"
    "document.documentElement ? document.documentElement.offsetHeight : 0,"
    "document.body ? document.body.clientHeight : 0,"
    "document.documentElement ? document.documentElement.clientHeight : 0"
    ")"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the bundled action-design references catalog."
    )
    parser.add_argument(
        "--source-repo",
        type=Path,
        required=True,
        help="Path to the awesome-design-md repository.",
    )
    parser.add_argument(
        "--skill-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Path to the action-design skill directory.",
    )
    parser.add_argument(
        "--design",
        action="append",
        dest="designs",
        help="Optional design slug to build. Repeat for multiple slugs.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove the existing reference catalog before rebuilding.",
    )
    return parser.parse_args()


def find_pwcli() -> Path:
    codex_home = Path.home() / ".codex"
    pwcli = codex_home / "skills" / "skill-playwright" / "scripts" / "playwright_cli.sh"
    if not pwcli.is_file():
        raise FileNotFoundError(f"Playwright CLI wrapper not found: {pwcli}")
    return pwcli


def available_designs(source_repo: Path) -> list[str]:
    design_root = source_repo / "design-md"
    return sorted(path.name for path in design_root.iterdir() if path.is_dir())


def rewrite_readme(content: str) -> str:
    content = README_LINK_RE.sub(lambda match: f"./{match.group(2)}", content)
    content = README_IMAGE_RE.sub(lambda match: f"./{match.group(2)}", content)
    return content


def reserve_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        return


class ServerContext:
    def __init__(self, directory: Path, port: int) -> None:
        handler = functools.partial(QuietHandler, directory=str(directory))
        self._server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    def __enter__(self) -> "ServerContext":
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc, exc_tb) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=5)


def latest_png(temp_dir: Path) -> Path:
    screenshots = sorted(
        (temp_dir / ".playwright-cli").glob("*.png"),
        key=lambda path: path.stat().st_mtime,
    )
    if not screenshots:
        raise FileNotFoundError(f"No screenshots generated in {temp_dir / '.playwright-cli'}")
    return screenshots[-1]


def run_pwcli(pwcli: Path, session: str, args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        [str(pwcli), "--session", session, *args],
        cwd=str(cwd),
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def parse_cli_result(stdout: str) -> str:
    match = CLI_RESULT_RE.search(stdout)
    if not match:
        raise ValueError(f"Unable to parse CLI result from output:\n{stdout}")
    return match.group(1).strip()


def read_full_height(pwcli: Path, session: str, cwd: Path) -> int:
    stdout = run_pwcli(pwcli, session, ["eval", FULL_HEIGHT_EXPR], cwd)
    height = int(parse_cli_result(stdout))
    if height <= INITIAL_VIEWPORT_HEIGHT:
        raise ValueError(
            f"Expected full-page height greater than {INITIAL_VIEWPORT_HEIGHT}, got {height}"
        )
    return height


def capture_screenshot(
    pwcli: Path,
    session: str,
    url: str,
    output_path: Path,
) -> None:
    with tempfile.TemporaryDirectory(prefix="action-design-") as temp_name:
        temp_dir = Path(temp_name)
        try:
            run_pwcli(pwcli, session, ["open"], temp_dir)
            run_pwcli(
                pwcli,
                session,
                ["resize", str(INITIAL_VIEWPORT_WIDTH), str(INITIAL_VIEWPORT_HEIGHT)],
                temp_dir,
            )
            run_pwcli(pwcli, session, ["goto", url], temp_dir)
            time.sleep(1.2)
            full_height = read_full_height(pwcli, session, temp_dir)
            run_pwcli(
                pwcli,
                session,
                ["resize", str(INITIAL_VIEWPORT_WIDTH), str(full_height)],
                temp_dir,
            )
            time.sleep(0.2)
            run_pwcli(pwcli, session, ["screenshot"], temp_dir)
            shutil.copy2(latest_png(temp_dir), output_path)
        finally:
            subprocess.run(
                [str(pwcli), "--session", session, "close"],
                cwd=str(temp_dir),
                capture_output=True,
                text=True,
            )


def build_reference(source_repo: Path, skill_root: Path, design: str, pwcli: Path, port: int) -> None:
    source_dir = source_repo / "design-md" / design
    target_dir = skill_root / "references" / design
    target_dir.mkdir(parents=True, exist_ok=True)

    for file_name in ("DESIGN.md", "preview.html", "preview-dark.html"):
        shutil.copy2(source_dir / file_name, target_dir / file_name)

    readme = (source_dir / "README.md").read_text(encoding="utf-8")
    (target_dir / "README.md").write_text(rewrite_readme(readme), encoding="utf-8")

    session_base = re.sub(r"[^a-z0-9]+", "-", design.casefold()).strip("-")
    capture_screenshot(
        pwcli,
        f"{session_base}-light",
        f"http://127.0.0.1:{port}/design-md/{design}/preview.html",
        target_dir / "preview-screenshot.png",
    )
    capture_screenshot(
        pwcli,
        f"{session_base}-dark",
        f"http://127.0.0.1:{port}/design-md/{design}/preview-dark.html",
        target_dir / "preview-dark-screenshot.png",
    )


def main() -> int:
    args = parse_args()
    source_repo = args.source_repo.resolve()
    skill_root = args.skill_root.resolve()
    reference_root = skill_root / "references"

    if not (source_repo / "design-md").is_dir():
        print(f"Invalid source repo: {source_repo}", file=sys.stderr)
        return 1

    if args.clean and reference_root.exists():
        shutil.rmtree(reference_root)
    reference_root.mkdir(parents=True, exist_ok=True)

    designs = available_designs(source_repo)
    selected_designs = args.designs or designs
    missing = sorted(set(selected_designs) - set(designs))
    if missing:
        print(f"Unknown designs: {', '.join(missing)}", file=sys.stderr)
        return 1

    pwcli = find_pwcli()
    port = reserve_port()

    with ServerContext(source_repo, port):
        for design in selected_designs:
            print(f"Building {design}...")
            build_reference(source_repo, skill_root, design, pwcli, port)

    print(f"Built {len(selected_designs)} design references in {reference_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
