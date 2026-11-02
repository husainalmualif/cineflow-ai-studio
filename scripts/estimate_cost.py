#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Estimate 3-stage credits for a production package or compiled blueprint.
Usage: python scripts/estimate_cost.py PACKAGE.json CREDITS_PER_GENERATION [EXPECTED_REROLLS_PER_BLOCK=1.0]

CREDITS_PER_GENERATION must be a positive number verified on the target platform screen.
Fixes fragile_tools.estimate_cost_py:
- Rejects negative/zero credit cost or negative reroll factor.
- Supports both `blocks` and `scene_breakdown` blueprints.
- Reports Stage 1 (0-credit refs), Stage 2 (0.25x draft), and Stage 3 (master render + Extend count).
- Scales worst-case dynamically with `max_rerolls = max(2.0, rr * 2.0)`.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_package import convert_scene_breakdown_to_package  # noqa: E402


def estimate_package_cost(
    raw_data: Any,
    credits_per_generation: float,
    expected_rerolls_per_block: float = 1.0,
) -> Dict[str, Any]:
    """Calculates 3-stage credit estimates and validates inputs."""
    if not isinstance(raw_data, dict):
        raise ValueError("Package JSON must be a dictionary/object.")
    if credits_per_generation <= 0:
        raise ValueError(f"credits_per_generation must be > 0, got {credits_per_generation}")
    if expected_rerolls_per_block < 0:
        raise ValueError(f"expected_rerolls_per_block must be >= 0, got {expected_rerolls_per_block}")

    d = convert_scene_breakdown_to_package(raw_data)
    blocks = d.get("blocks", [])
    if not isinstance(blocks, list) or not blocks:
        raise ValueError("Package contains 0 blocks.")

    n = len(blocks)
    extend_blocks = sum(1 for b in blocks if isinstance(b, dict) and b.get("mode") == "Extend")
    base_blocks = n - extend_blocks

    stage1_refs_cost = 0.0  # Nano Banana 2 Lite / Google Labs 0-credit reference plates
    stage2_draft_cost = round(n * (credits_per_generation * 0.25), 2)  # Omni 1.1 Flash 360p->720p draft

    lo = round(n * credits_per_generation, 2)
    exp = round(n * (1.0 + expected_rerolls_per_block) * credits_per_generation, 2)
    max_rerolls = max(2.0, expected_rerolls_per_block * 2.0)
    hi = round(n * (1.0 + max_rerolls) * credits_per_generation, 2)

    return {
        "blocks": n,
        "base_blocks": base_blocks,
        "extend_blocks": extend_blocks,
        "stage1_reference_credits": stage1_refs_cost,
        "stage2_draft_credits": stage2_draft_cost,
        "minimum": lo,
        "expected": exp,
        "worst_case": hi,
        "max_rerolls_per_block": max_rerolls,
    }


def main() -> None:
    """CLI entry point for estimating package credit costs."""
    if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            raw_data = json.load(f)
        cost = float(sys.argv[2])
        rr = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        est = estimate_package_cost(raw_data, cost, rr)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    print(
        f"blocks={est['blocks']} (base={est['base_blocks']}, extend={est['extend_blocks']}) | "
        f"stage1_refs={est['stage1_reference_credits']:g} | "
        f"stage2_draft={est['stage2_draft_credits']:g} | "
        f"minimum={est['minimum']:g} | "
        f"expected={est['expected']:g} (reroll avg {rr:g}) | "
        f"worst-case ({est['max_rerolls_per_block']:g} rerolls/block)={est['worst_case']:g} credits"
    )


if __name__ == "__main__":
    main()
