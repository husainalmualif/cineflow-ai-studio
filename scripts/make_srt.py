#!/usr/bin/env python3
"""Build an .srt from package overlays. Usage: make_srt.py PACKAGE.json OUT.srt"""
import json, sys
if len(sys.argv) != 3 or sys.argv[1] in ("-h", "--help"):
    print(__doc__); sys.exit(0)
with open(sys.argv[1], encoding="utf-8") as f:
    d = json.load(f)
def ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"
rows = [o for o in d.get("overlays", []) if o.get("text_ar")]
with open(sys.argv[2], "w", encoding="utf-8") as f:
    for i, o in enumerate(rows, 1):
        f.write(f"{i}\n{ts(o['start_s'])} --> {ts(o['end_s'])}\n{o['text_ar']}\n\n")
print(f"wrote {len(rows)} cues to {sys.argv[2]}")
