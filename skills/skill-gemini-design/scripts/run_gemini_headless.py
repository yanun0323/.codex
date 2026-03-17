#!/usr/bin/env python3
"""Run gemini in direct-edit mode for design workflows."""

from __future__ import annotations

import argparse
import os
import signal
import shutil
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run gemini safely in direct-edit mode for skill-gemini-design.",
    )
    parser.add_argument(
        "--prompt",
        help="Prompt text to send to gemini.",
    )
    parser.add_argument(
        "--prompt-file",
        help="Path to a file containing the full prompt.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        help="Maximum time to wait for gemini before terminating it.",
    )
    parser.add_argument(
        "--model",
        help="Optional gemini model override.",
    )
    parser.add_argument(
        "--include-directory",
        action="append",
        default=[],
        help="Directory to expose to Gemini edit mode. Repeatable.",
    )
    parser.add_argument(
        "--approval-mode",
        choices=("auto_edit", "yolo"),
        default="auto_edit",
        help="Approval mode to use in edit mode. Defaults to auto_edit.",
    )
    return parser.parse_args()


def load_prompt(args: argparse.Namespace) -> str:
    sources = [args.prompt is not None, args.prompt_file is not None]
    if sum(sources) > 1:
        raise ValueError("Use only one of --prompt or --prompt-file.")

    if args.prompt is not None:
        prompt = args.prompt
    elif args.prompt_file is not None:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    else:
        prompt = sys.stdin.read()

    prompt = prompt.strip()
    if not prompt:
        raise ValueError("Prompt content is empty.")
    return prompt


def resolve_timeout_seconds(args: argparse.Namespace) -> int:
    if args.timeout_seconds is not None:
        return args.timeout_seconds
    return 900


def build_command(args: argparse.Namespace, prompt: str) -> list[str]:
    gemini_path = shutil.which("gemini")
    if not gemini_path:
        raise FileNotFoundError("gemini executable not found in PATH.")

    cmd = [gemini_path, "-p", prompt, "-o", "text"]
    if args.model:
        cmd.extend(["-m", args.model])
    cmd.extend(["--approval-mode", args.approval_mode, "--sandbox", "true"])
    include_directories = args.include_directory or [str(Path.cwd())]
    for directory in include_directories:
        cmd.extend(["--include-directories", str(Path(directory).resolve())])
    return cmd


def terminate_process(process: subprocess.Popen[str]) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    except OSError:
        process.terminate()
    try:
        process.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            return
        except OSError:
            process.kill()
        try:
            process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            return


def run_gemini(cmd: list[str], timeout_seconds: int) -> tuple[str, str]:
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )

    try:
        stdout, stderr = process.communicate(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        terminate_process(process)
        raise TimeoutError(
            f"gemini timed out after {timeout_seconds} seconds."
        ) from None

    if process.returncode != 0:
        detail = stderr.strip() or stdout.strip() or "gemini exited without details."
        raise RuntimeError(f"gemini failed with exit code {process.returncode}: {detail}")

    return stdout, stderr


def validate_output(stdout: str) -> str:
    content = stdout.strip()
    if not content:
        raise ValueError("gemini returned empty stdout.")

    return content


def main() -> int:
    try:
        args = parse_args()
        prompt = load_prompt(args)
        timeout_seconds = resolve_timeout_seconds(args)
        cmd = build_command(args, prompt)
        stdout, stderr = run_gemini(cmd, timeout_seconds)
        content = validate_output(stdout)
    except (FileNotFoundError, ValueError, RuntimeError, TimeoutError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Error: failed to run gemini: {exc}", file=sys.stderr)
        return 1

    if stderr.strip():
        print(stderr.strip(), file=sys.stderr)
    print(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
