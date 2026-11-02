#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate an SRT subtitle file from a production package or compiled blueprint.
Usage: python scripts/make_srt.py PACKAGE.json OUT.srt

Fixes fragile_tools.make_srt_py:
- Extracts subtitles from spoken `dialogue_ar` in `blocks[].shots[]` (timed via block offset + `t_range`),
  falling back to `overlays` only when no spoken dialogue exists.
- Validates numeric `start_s` and `end_s` (`0 <= start_s < end_s`) without raising KeyError.
- Verifies chronological ordering and rejects overlapping or invalid timestamps.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_package import (  # noqa: E402
    T_RANGE_RE,
    convert_scene_breakdown_to_package,
    is_number,
)


def fmt_srt_time(seconds: float) -> str:
    """Formats seconds into SRT timestamp HH:MM:SS,mmm."""
    ms = int(round((seconds - int(seconds)) * 1000))
    total_s = int(seconds)
    if ms >= 1000:
        total_s += 1
        ms -= 1000
    hrs = total_s // 3600
    mins = (total_s % 3600) // 60
    secs = total_s % 60
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{ms:03d}"


def extract_validated_cues(raw_data: Any) -> List[Tuple[float, float, str]]:
    """
    Extracts and validates `(start_s, end_s, text_ar)` cues from spoken `dialogue_ar`
    (or `overlays` when explicitly provided or as fallback).
    Raises ValueError on malformed timestamps, negative times, `start_s >= end_s`, or out-of-order overlays.
    """
    if not isinstance(raw_data, dict):
        raise ValueError("Input JSON must be a dictionary/object.")

    d = convert_scene_breakdown_to_package(raw_data)

    # Always validate overlays if present so malformed overlays are caught
    overlays = d.get("overlays")
    overlay_cues: List[Tuple[float, float, str]] = []
    if overlays is not None:
        if not isinstance(overlays, list):
            raise ValueError("overlays must be a list.")
        prev_start = -1.0
        for idx, ov in enumerate(overlays, start=1):
            if not isinstance(ov, dict):
                raise ValueError(f"overlay #{idx} must be an object/dict.")
            if "start_s" not in ov or "end_s" not in ov:
                raise ValueError(f"overlay #{idx} missing required start_s or end_s.")
            st = ov["start_s"]
            en = ov["end_s"]
            if not is_number(st) or not is_number(en):
                raise ValueError(f"overlay #{idx} start_s and end_s must be numbers.")
            st_f, en_f = float(st), float(en)
            if st_f < 0 or st_f >= en_f:
                raise ValueError(f"overlay #{idx} invalid timing: start_s={st_f} must be >= 0 and < end_s={en_f}.")
            if st_f < prev_start:
                raise ValueError(
                    f"overlay #{idx} out of chronological order: start_s={st_f} < previous start_s={prev_start}."
                )
            prev_start = st_f
            txt = str(ov.get("text_ar") or "").strip()
            if txt:
                overlay_cues.append((st_f, en_f, txt))

    # Extract spoken dialogue cues from blocks[].shots[]
    dialogue_cues: List[Tuple[float, float, str]] = []
    blocks = d.get("blocks", [])
    if isinstance(blocks, list):
        block_offset = 0.0
        for b in blocks:
            if not isinstance(b, dict):
                continue
            b_dur = b.get("duration_s", 0)
            if not is_number(b_dur) or b_dur <= 0:
                raise ValueError(f"block {b.get('block_id')} has invalid duration_s: {b_dur!r}")
            b_dur_f = float(b_dur)
            shots = b.get("shots", [])
            if isinstance(shots, list):
                for s in shots:
                    if not isinstance(s, dict):
                        continue
                    dl_ar = str(s.get("dialogue_ar") or "").strip()
                    if not dl_ar:
                        continue
                    t_range = str(s.get("t_range") or f"0-{b_dur_f:g}")
                    m_range = T_RANGE_RE.match(t_range)
                    if not m_range:
                        raise ValueError(f"shot {s.get('shot_id')} has invalid t_range '{t_range}'.")
                    s_start = block_offset + float(m_range.group(1))
                    s_end = block_offset + float(m_range.group(2))
                    if s_start < 0 or s_start >= s_end or s_end > block_offset + b_dur_f + 0.01:
                        raise ValueError(
                            f"shot {s.get('shot_id')} t_range '{t_range}' out of bounds for block duration {b_dur_f}s."
                        )
                    clean_dl = dl_ar.replace("[0.3s pause]", "").replace("..", " ").strip()
                    clean_dl = " ".join(clean_dl.split())
                    if clean_dl:
                        dialogue_cues.append((s_start, s_end, clean_dl))
            block_offset += b_dur_f

    cues = dialogue_cues if dialogue_cues else overlay_cues
    if not cues:
        raise ValueError("No spoken dialogue_ar or overlay cues found to build SRT.")

    cues.sort(key=lambda item: (item[0], item[1]))
    return cues


def build_srt_string(raw_data: Any) -> str:
    """Builds the formatted SRT file content from package data."""
    cues = extract_validated_cues(raw_data)
    out_blocks: List[str] = []
    for idx, (st, en, txt) in enumerate(cues, start=1):
        out_blocks.append(f"{idx}\n{fmt_srt_time(st)} --> {fmt_srt_time(en)}\n{txt}\n")
    return "\n".join(out_blocks)


def main() -> None:
    """CLI entry point for generating an SRT file."""
    if len(sys.argv) != 3 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            raw_data = json.load(f)
        srt_content = build_srt_string(raw_data)
        with open(sys.argv[2], "w", encoding="utf-8") as out:
            out.write(srt_content)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
    print(f"wrote {sys.argv[2]}")


if __name__ == "__main__":
    main()
