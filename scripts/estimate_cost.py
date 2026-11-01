#!/usr/bin/env python3
"""Estimate credits. Usage: estimate_cost.py PACKAGE.json CREDITS_PER_GENERATION [EXPECTED_REROLLS_PER_BLOCK=1]
CREDITS_PER_GENERATION must be the value shown by the platform (verify on screen)."""
import json, sys
if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help"):
    print(__doc__); sys.exit(0)
with open(sys.argv[1], encoding="utf-8") as f:
    d = json.load(f)
cost = float(sys.argv[2]); rr = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
n = len(d.get("blocks", []))
lo, exp, hi = n * cost, n * (1 + rr) * cost, n * 3 * cost
print(f"blocks={n} | minimum={lo:g} | expected={exp:g} (reroll avg {rr:g}) | worst-case (2 rerolls/block)={hi:g} credits")
