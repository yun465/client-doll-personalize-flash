#!/usr/bin/env python3
"""Validate the public Codex skill package using only the standard library."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SENSITIVE_SUFFIXES = {
    ".aac",
    ".bin",
    ".elf",
    ".key",
    ".m4a",
    ".map",
    ".mp3",
    ".nvs",
    ".pcm",
    ".pem",
    ".secret",
    ".wav",
}


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    errors: list[str] = []

    required_files = [
        "README.md",
        "README.zh-CN.md",
        "SKILL.md",
        "LICENSE",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "agents/openai.yaml",
        "assets/social-preview.jpg",
        "examples/demo-persona/persona-preview.md",
        "references/project-adaptation.md",
    ]
    for relative_path in required_files:
        if not (ROOT / relative_path).is_file():
            errors.append(f"missing required file: {relative_path}")

    skill = read_text("SKILL.md")
    frontmatter = re.match(r"\A---\s*\n(.*?)\n---\s*\n", skill, re.DOTALL)
    if not frontmatter:
        errors.append("SKILL.md must start with YAML frontmatter")
    else:
        yaml_text = frontmatter.group(1)
        if not re.search(r"^name:\s*client-doll-personalize-flash\s*$", yaml_text, re.MULTILINE):
            errors.append("SKILL.md has an unexpected skill name")
        description = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', yaml_text, re.MULTILINE)
        if not description or not description.group(1).startswith("Use when"):
            errors.append('SKILL.md description must start with "Use when"')
        if len(yaml_text) > 1024:
            errors.append("SKILL.md frontmatter exceeds 1024 characters")

    for forbidden in ("require_escalated", r"client\software\customers"):
        if forbidden in skill:
            errors.append(f"SKILL.md contains a machine-specific instruction: {forbidden}")

    readme = read_text("README.md")
    for marker in (
        "README.zh-CN.md",
        "Quick start",
        "Prerequisites",
        "What is included",
        "Project integration",
        "Limitations",
        "assets/social-preview.jpg",
    ):
        if marker not in readme:
            errors.append(f"README.md is missing: {marker}")

    for source_path in ["README.md", "README.zh-CN.md", "SKILL.md", *[str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT / "references").glob("*.md")]]:
        if not (ROOT / source_path).is_file():
            continue
        content = read_text(source_path)
        for target in re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", content):
            if "://" in target or target.startswith("mailto:"):
                continue
            resolved = ((ROOT / source_path).parent / target).resolve()
            if not resolved.exists():
                errors.append(f"broken relative link in {source_path}: {target}")

    for tracked in tracked_files():
        normalized = tracked.replace("\\", "/").lower()
        if "/private_data/" in f"/{normalized}/" or Path(normalized).suffix in SENSITIVE_SUFFIXES:
            errors.append(f"sensitive artifact is tracked: {tracked}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed: public skill package is structurally complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
