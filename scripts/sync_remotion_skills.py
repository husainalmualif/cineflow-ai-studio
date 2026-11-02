#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync & Attribution Utility for Official Remotion Skills (`references/remotion_skills_official/`).

Copies rule files from a local checkout of `remotion-dev/remotion` (`packages/skills/skills/remotion`)
into `references/remotion_skills_official/` and writes `UPSTREAM_ATTRIBUTION.md`.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DEST_DIR = ROOT_DIR / "references" / "remotion_skills_official"
UPSTREAM_REPO_URL = "https://github.com/remotion-dev/remotion"
UPSTREAM_SUBPATH = "packages/skills/skills/remotion"
DEFAULT_VERSION = "v4.0.539"


def write_attribution_file(dest: Path, version: str) -> None:
    """Writes UPSTREAM_ATTRIBUTION.md documenting source, version, and license."""
    content = (
        "# Upstream Attribution — Official Remotion Agent Skills\n\n"
        "- **Source Repository**: https://github.com/remotion-dev/remotion\n"
        f"- **Upstream Path**: `{UPSTREAM_SUBPATH}`\n"
        f"- **Pinned Version**: `{version}`\n"
        "- **License**: Remotion License / MIT (for documentation & agent skill templates; see https://github.com/remotion-dev/remotion/blob/main/LICENSE.md)\n"
        "- **Refresh Command**:\n"
        "  ```bash\n"
        "  python scripts/sync_remotion_skills.py --source /path/to/remotion/packages/skills/skills/remotion --version v4.0.539\n"
        "  ```\n"
    )
    (dest / "UPSTREAM_ATTRIBUTION.md").write_text(content, encoding="utf-8")


def sync_from_local_checkout(source_dir: Path, dest_dir: Path, version: str) -> int:
    """Copies SKILL.md and rules/ from source_dir into dest_dir."""
    if not source_dir.is_dir():
        print(f"ERROR: Source directory does not exist: {source_dir}", file=sys.stderr)
        return 1

    dest_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for item in source_dir.rglob("*"):
        if item.is_file():
            rel = item.relative_to(source_dir)
            target = dest_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            count += 1

    write_attribution_file(dest_dir, version)
    print(f"OK: Synced {count} files from {source_dir} to {dest_dir} (version {version}).")
    return 0


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Sync official Remotion skill rules into references/remotion_skills_official/."
    )
    parser.add_argument(
        "--source",
        type=str,
        default="",
        help="Path to local checkout of remotion/packages/skills/skills/remotion.",
    )
    parser.add_argument(
        "--version",
        type=str,
        default=DEFAULT_VERSION,
        help="Upstream Remotion release tag (default: v4.0.539).",
    )
    parser.add_argument(
        "--attribution-only",
        action="store_true",
        help="Only regenerate UPSTREAM_ATTRIBUTION.md without copying files.",
    )
    args = parser.parse_args()

    if args.attribution_only or not args.source:
        DEST_DIR.mkdir(parents=True, exist_ok=True)
        write_attribution_file(DEST_DIR, args.version)
        print(f"OK: Updated {DEST_DIR / 'UPSTREAM_ATTRIBUTION.md'} for {args.version}.")
        return 0

    return sync_from_local_checkout(Path(args.source), DEST_DIR, args.version)


if __name__ == "__main__":
    sys.exit(main())
