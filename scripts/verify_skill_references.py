#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dynamic Skill & Documentation Reference Verifier for CineFlow AI Studio.

Replaces static `test -f` lists in CI by parsing `SKILL.md` and `README.md` to verify:
1. `SKILL.md` declares `name: cineflow-ai-studio`.
2. Every local repository path referenced in markdown links or backticks (`scripts/`, `references/`,
   `templates/`, `resources/`, `examples/`, `evals/`, `mcp/`, `tests/`) exists on disk.
3. `evals/evals.json` and `resources/evals.json` remain synchronized.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Set

ROOT_DIR = Path(__file__).resolve().parent.parent
CHECKED_PREFIXES = (
    "scripts/",
    "references/",
    "templates/",
    "resources/",
    "examples/",
    "evals/",
    "mcp/",
    "tests/",
)

# Paths in CLI snippets that are intentionally ephemeral runtime outputs
EPHEMERAL_PATHS = {
    "examples/out_subtitles.srt",
    "examples/beat_grid_128bpm.json",
}

BACKTICK_RE = re.compile(r"`([^`\n]+)`")
MD_LINK_RE = re.compile(r"\]\(([^)\n]+)\)")


def extract_referenced_paths(markdown_text: str) -> Set[str]:
    """Extracts repo-relative file/directory paths from markdown backticks and links."""
    found: Set[str] = set()
    candidates = BACKTICK_RE.findall(markdown_text) + MD_LINK_RE.findall(markdown_text)
    for raw in candidates:
        token = raw.strip().split("#")[0].strip()
        # If a backtick contains a CLI command, inspect its whitespace-delimited tokens too
        parts = [token] + token.split()
        for part in parts:
            cleaned = part.strip("()[]{}'\",;:")
            if cleaned.startswith("./"):
                cleaned = cleaned[2:]
            if any(cleaned.startswith(prefix) for prefix in CHECKED_PREFIXES):
                if "*" in cleaned or "<" in cleaned or ">" in cleaned or "$" in cleaned:
                    continue
                if cleaned in EPHEMERAL_PATHS:
                    continue
                found.add(cleaned)
    return found


def verify_repository_references(root: Path = ROOT_DIR) -> List[str]:
    """Returns a list of validation errors (empty list if everything passes)."""
    errors: List[str] = []

    skill_md = root / "SKILL.md"
    readme_md = root / "README.md"

    if not skill_md.is_file():
        errors.append("Missing required SKILL.md at repository root.")
        return errors
    if not readme_md.is_file():
        errors.append("Missing required README.md at repository root.")
        return errors

    skill_text = skill_md.read_text(encoding="utf-8")
    if "name: cineflow-ai-studio" not in skill_text:
        errors.append("SKILL.md frontmatter is missing `name: cineflow-ai-studio`.")

    for doc_path in (skill_md, readme_md):
        text = doc_path.read_text(encoding="utf-8")
        refs = sorted(extract_referenced_paths(text))
        for rel_path in refs:
            target = root / rel_path
            if not target.exists():
                errors.append(
                    f"{doc_path.name} references non-existent path: '{rel_path}'"
                )

    # Verify every top-level markdown file in references/*.md is referenced in SKILL.md (no orphan references)
    skill_refs = extract_referenced_paths(skill_text)
    refs_dir = root / "references"
    if refs_dir.is_dir():
        for ref_file in sorted(refs_dir.glob("*.md")):
            rel_ref = f"references/{ref_file.name}"
            if rel_ref not in skill_refs:
                errors.append(
                    f"Orphan reference file not listed in SKILL.md routing table: '{rel_ref}'"
                )

    # Verify version consistency across pyproject.toml, README.md, and CHANGELOG.md
    pyproject_toml = root / "pyproject.toml"
    changelog_md = root / "CHANGELOG.md"
    if pyproject_toml.is_file() and changelog_md.is_file():
        py_text = pyproject_toml.read_text(encoding="utf-8")
        rm_text = readme_md.read_text(encoding="utf-8")
        ch_text = changelog_md.read_text(encoding="utf-8")
        m_py = re.search(r'^version\s*=\s*"([^"]+)"', py_text, re.M)
        m_rm = re.search(r"الإصدار\s*`([^`]+)`", rm_text)
        m_ch = re.search(r"^##\s*\[([^\]]+)\]", ch_text, re.M)
        v_py = m_py.group(1) if m_py else None
        v_rm = m_rm.group(1) if m_rm else None
        v_ch = m_ch.group(1) if m_ch else None
        if not (v_py and v_rm and v_ch) or len({v_py, v_rm, v_ch}) != 1:
            errors.append(
                f"Version mismatch across files: pyproject.toml={v_py}, README.md={v_rm}, CHANGELOG.md={v_ch}"
            )

    # Verify evals/evals.json and resources/evals.json are synchronized
    evals_a = root / "evals" / "evals.json"
    evals_b = root / "resources" / "evals.json"
    if not evals_a.is_file() or not evals_b.is_file():
        errors.append("Both evals/evals.json and resources/evals.json must exist.")
    else:
        data_a = json.loads(evals_a.read_text(encoding="utf-8"))
        data_b = json.loads(evals_b.read_text(encoding="utf-8"))
        if data_a != data_b:
            errors.append(
                "evals/evals.json and resources/evals.json have diverged; keep them synchronized."
            )

    return errors


def main() -> int:
    """CLI entry point for verifying repository file references."""
    parser = argparse.ArgumentParser(
        description="Verify all file paths referenced in SKILL.md and README.md exist on disk."
    )
    parser.add_argument(
        "--sync-evals",
        action="store_true",
        help="Copy resources/evals.json to evals/evals.json before validating.",
    )
    args = parser.parse_args()

    if args.sync_evals:
        src = ROOT_DIR / "resources" / "evals.json"
        dst = ROOT_DIR / "evals" / "evals.json"
        if src.is_file():
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    errors = verify_repository_references(ROOT_DIR)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    print("OK: All SKILL.md & README.md file references exist and evals JSON files are synchronized.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
