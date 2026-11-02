#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rhythmic Montage Beat Grid & Cut Map Calculator (scripts/beat_grid.py).

Computes beat timestamps (`beats_s`), bar downbeats (`downbeats_s`), pattern-driven
cut points (`cut_points_s`), exact frame indices (`frame_indices`), speed ramps,
and beat-locked SFX cues for post-production rhythmic montage (`FFmpeg` / `Remotion` / `HyperFrames`).

Usage:
    python scripts/beat_grid.py --bpm 120 --time-signature 4/4 --fps 30 --duration 15 --pattern build_up
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from studio_config import (  # noqa: E402
    MAX_RAMP_SPEED,
    MAX_RAMPS_PER_CLIP,
    MAX_SFX_PER_TWO_BEATS,
    MIN_RAMP_SPEED,
    SNAP_TOLERANCE_MS,
    VALID_MONTAGE_STYLES,
)

CUT_CADENCE_PATTERNS: Dict[str, List[float]] = {
    "steady": [1.0, 1.0, 1.0, 1.0],
    "build_up": [4.0, 2.0, 2.0, 1.0, 1.0, 0.5, 0.5],
    "call_response": [2.0, 1.0, 1.0, 2.0, 1.0, 1.0],
    "breathe": [4.0, 4.0, 8.0],
}

SUPPORTED_TIME_SIGNATURES: Dict[str, Tuple[int, int]] = {
    "2/4": (2, 4),
    "3/4": (3, 4),
    "4/4": (4, 4),
    "6/8": (6, 8),
    "12/8": (12, 8),
}

STANDARD_FPS_VALUES = {24.0, 25.0, 29.97, 30.0, 50.0, 59.94, 60.0, 120.0}


def _is_valid_number(val: Any) -> bool:
    """Returns True if val is a finite int or float (excluding bool)."""
    return isinstance(val, (int, float)) and not isinstance(val, bool) and math.isfinite(float(val))


def compute_beat_grid(
    bpm: float,
    time_signature: str = "4/4",
    fps: float = 30.0,
    duration_s: float = 15.0,
    pattern: str = "build_up",
    source: str = "estimated",
    confidence: float = 0.85,
) -> Dict[str, Any]:
    """
    Computes the beat grid, cut points, frame indices, and warnings.
    Raises ValueError with a descriptive message on invalid inputs:
    - invalid or non-positive BPM (`<= 0` or `> 300`)
    - zero or negative `duration_s` (`<= 0`)
    - unsupported `time_signature`
    - non-positive or unexpected `fps` (`<= 0` or `> 240`)
    - unknown `pattern`
    """
    if not _is_valid_number(bpm) or float(bpm) <= 0 or float(bpm) > 300:
        raise ValueError(f"Invalid BPM {bpm!r}: BPM must be a positive number between 1 and 300.")

    if not _is_valid_number(duration_s) or float(duration_s) <= 0:
        raise ValueError(f"Invalid duration_s {duration_s!r}: duration_s must be greater than 0.")

    if not isinstance(time_signature, str) or time_signature.strip() not in SUPPORTED_TIME_SIGNATURES:
        raise ValueError(
            f"Unsupported time_signature {time_signature!r}: must be one of {sorted(SUPPORTED_TIME_SIGNATURES.keys())}."
        )

    if not _is_valid_number(fps) or float(fps) <= 0 or float(fps) > 240:
        raise ValueError(f"Invalid fps {fps!r}: fps must be a positive number between 1 and 240.")

    if not isinstance(pattern, str) or pattern not in CUT_CADENCE_PATTERNS:
        raise ValueError(
            f"Unsupported cut pattern {pattern!r}: must be one of {sorted(CUT_CADENCE_PATTERNS.keys())}."
        )

    bpm_f = float(bpm)
    fps_f = float(fps)
    dur_f = float(duration_s)
    beats_per_bar, _ = SUPPORTED_TIME_SIGNATURES[time_signature.strip()]

    warnings: List[str] = []
    if fps_f not in STANDARD_FPS_VALUES:
        warnings.append(
            f"Non-standard fps ({fps_f:g}) supplied; standard broadcast rates are {sorted(STANDARD_FPS_VALUES)}."
        )
    if source == "estimated":
        warnings.append("Beat map source is 'estimated'; synchronization is approximate until verified against audio.")

    beat_seconds = 60.0 / bpm_f
    beat_frames = round(fps_f * 60.0 / bpm_f, 4)
    bar_seconds = beat_seconds * beats_per_bar

    # Generate beats_s and downbeats_s across [0, duration_s]
    beats_s: List[float] = []
    downbeats_s: List[float] = []
    beat_idx = 0
    while True:
        t = round(beat_idx * beat_seconds, 4)
        if t > dur_f + 1e-6:
            break
        beats_s.append(t)
        if beat_idx % beats_per_bar == 0:
            downbeats_s.append(t)
        beat_idx += 1

    # Generate cut_points_s using the selected cadence pattern (varying after 1 cycle per rule MQ2)
    base_steps = CUT_CADENCE_PATTERNS[pattern]
    alt_pattern = "call_response" if pattern != "call_response" else "steady"
    alt_steps = CUT_CADENCE_PATTERNS[alt_pattern]

    cut_points_s: List[float] = [0.0]
    current_beat_pos = 0.0
    step_idx = 0
    cycle_count = 0
    active_steps = base_steps

    while True:
        step_beats = active_steps[step_idx % len(active_steps)]
        current_beat_pos += step_beats
        t_cut = round(current_beat_pos * beat_seconds, 4)
        if t_cut >= dur_f - 1e-6:
            break
        cut_points_s.append(t_cut)
        step_idx += 1
        if step_idx % len(active_steps) == 0:
            cycle_count += 1
            active_steps = alt_steps if cycle_count % 2 == 1 else base_steps

    frame_indices: List[int] = [int(round(t * fps_f)) for t in cut_points_s]

    # Identify musical sections and drop points
    sections = _build_musical_sections(dur_f, downbeats_s, bar_seconds)
    drops_s = [sec["start_s"] for sec in sections if "drop" in sec["name"] or "chorus" in sec["name"]]
    if not drops_s and len(downbeats_s) >= 2:
        drops_s = [downbeats_s[min(1, len(downbeats_s) - 1)]]

    beat_map = {
        "bpm": bpm_f,
        "time_signature": time_signature.strip(),
        "fps": fps_f,
        "downbeats_s": downbeats_s,
        "beats_s": beats_s,
        "drops_s": drops_s,
        "sections": sections,
        "source": source,
        "confidence": round(float(confidence), 2),
    }

    return {
        "beat_seconds": round(beat_seconds, 4),
        "beat_frames": beat_frames,
        "bar_seconds": round(bar_seconds, 4),
        "snap_tolerance_ms": SNAP_TOLERANCE_MS,
        "beats_s": beats_s,
        "downbeats_s": downbeats_s,
        "drops_s": drops_s,
        "cut_points_s": cut_points_s,
        "frame_indices": frame_indices,
        "sections": sections,
        "beat_map": beat_map,
        "warnings": warnings,
    }


def _build_musical_sections(
    duration_s: float,
    downbeats_s: List[float],
    bar_seconds: float,
) -> List[Dict[str, Any]]:
    """Splits total duration into musical sections aligned to bar downbeats."""
    if duration_s <= 6.0 or len(downbeats_s) < 2:
        return [{"name": "hook_and_drop", "start_s": 0.0, "end_s": round(duration_s, 2), "energy": 9}]

    t1 = downbeats_s[min(1, len(downbeats_s) - 1)] if bar_seconds < duration_s * 0.5 else round(duration_s * 0.25, 2)
    t2 = (
        downbeats_s[min(len(downbeats_s) - 1, max(2, len(downbeats_s) // 2))]
        if len(downbeats_s) >= 3
        else round(duration_s * 0.65, 2)
    )
    if t2 <= t1:
        t2 = round(min(duration_s * 0.7, t1 + max(1.0, duration_s * 0.3)), 2)

    return [
        {"name": "verse_hook", "start_s": 0.0, "end_s": round(t1, 4), "energy": 7},
        {"name": "build_up_bridge", "start_s": round(t1, 4), "end_s": round(t2, 4), "energy": 8},
        {"name": "chorus_drop", "start_s": round(t2, 4), "end_s": round(duration_s, 4), "energy": 10},
    ]


def validate_cuts_against_beats(
    cut_points_s: List[float],
    beats_s: List[float],
    snap_tolerance_ms: float = SNAP_TOLERANCE_MS,
) -> Tuple[bool, List[str]]:
    """
    Checks MQ1: Every cut point must fall within `snap_tolerance_ms` (default 40ms) of a beat
    or half-beat subdivision. Returns (passed, errors).
    """
    if not beats_s:
        return False, ["beats_s is empty; cannot validate cut alignment."]

    # Include half-beat subdivisions for 0.5-beat build_up cuts
    valid_grid = set(beats_s)
    for idx in range(len(beats_s) - 1):
        mid = round((beats_s[idx] + beats_s[idx + 1]) / 2.0, 4)
        valid_grid.add(mid)
    sorted_grid = sorted(valid_grid)

    errors: List[str] = []
    for cut_t in cut_points_s:
        if not _is_valid_number(cut_t):
            errors.append(f"Invalid non-numeric cut point: {cut_t!r}")
            continue
        nearest = min(sorted_grid, key=lambda b, c=float(cut_t): abs(b - c))
        diff_ms = abs(float(cut_t) - nearest) * 1000.0
        if diff_ms > snap_tolerance_ms + 1e-3:
            errors.append(
                f"MQ1 violation: cut at {cut_t:.3f}s deviates by {diff_ms:.1f}ms from nearest beat "
                f"{nearest:.3f}s (max snap_tolerance_ms={snap_tolerance_ms:g}ms)."
            )
    return len(errors) == 0, errors


def build_project_montage(
    style: str,
    duration_s: float,
    bpm: float = 120.0,
    time_signature: str = "4/4",
    fps: float = 30.0,
    pattern: Optional[str] = None,
    source: str = "generated_with_music",
) -> Dict[str, Any]:
    """
    Constructs a complete `project.montage` object conforming to `new_json_fields`
    and passing MQ1..MQ7 + CR2 validation.
    """
    if style not in VALID_MONTAGE_STYLES:
        raise ValueError(f"Unsupported montage style {style!r}; must be one of {sorted(VALID_MONTAGE_STYLES)}")

    if style == "none":
        return {
            "style": "none",
            "beat_map": None,
            "cut_pattern": "none",
            "cut_points_s": [],
            "ramps": [],
            "sfx_cues": [],
        }

    default_bpm_map = {
        "montage_sequence": 100.0,
        "music_video": 120.0,
        "commercial_promo": 128.0,
        "short_form_edit": 140.0,
        "sizzle_reel": 124.0,
    }
    default_pattern_map = {
        "montage_sequence": "breathe",
        "music_video": "call_response",
        "commercial_promo": "build_up",
        "short_form_edit": "build_up",
        "sizzle_reel": "steady",
    }
    chosen_bpm = bpm if bpm > 0 else default_bpm_map.get(style, 120.0)
    chosen_pattern = pattern or default_pattern_map.get(style, "build_up")

    grid = compute_beat_grid(
        bpm=chosen_bpm,
        time_signature=time_signature,
        fps=fps,
        duration_s=duration_s,
        pattern=chosen_pattern,
        source=source,
    )
    beat_map = grid["beat_map"]
    drops_s = beat_map["drops_s"]
    drop_t = drops_s[0] if drops_s else round(duration_s * 0.5, 2)
    beat_sec = grid["beat_seconds"]

    # Build at most 1 speed ramp per clip, anchored to musical drop/build-up (MQ5)
    ramp_start = max(0.0, round(drop_t - beat_sec, 4))
    ramp_end = min(round(duration_s, 4), round(drop_t + beat_sec, 4))
    ramps = [
        {
            "clip_id": "1A",
            "start_s": ramp_start,
            "end_s": ramp_end,
            "from_speed": 2.0,
            "to_speed": 0.5,
            "curve": "ease_in_out",
            "musical_reason": f"Slow-motion emphasis into primary drop at {drop_t:g}s",
        }
    ]

    # Build beat-locked SFX cues respecting CR2 (<= 1 SFX per 2 beats)
    sfx_cues = [
        {
            "t_s": max(0.0, round(drop_t - 2 * beat_sec, 4)),
            "layer": "riser",
            "name": "2-beat tension riser before drop",
            "pre_roll_ms": 0,
        },
        {
            "t_s": round(drop_t, 4),
            "layer": "impact_hit",
            "name": "sub_drop + impact hit on chorus/drop downbeat",
            "pre_roll_ms": 0,
        },
    ]
    if len(grid["cut_points_s"]) > 2:
        sfx_cues.append(
            {
                "t_s": round(grid["cut_points_s"][1], 4),
                "layer": "whoosh_transition",
                "name": "whip-pan whoosh transition",
                "pre_roll_ms": 110,
            }
        )

    max_allowed_sfx = max(1, len(beat_map["beats_s"]) // 2)
    sfx_cues = sfx_cues[:max_allowed_sfx]

    return {
        "style": style,
        "beat_map": beat_map,
        "cut_pattern": chosen_pattern,
        "cut_points_s": grid["cut_points_s"],
        "ramps": ramps,
        "sfx_cues": sfx_cues,
    }


def validate_montage_section(montage: Any, total_runtime_s: float = 0.0) -> Tuple[List[str], List[str]]:
    """
    Validates `project.montage` against schema_and_validator_changes & MQ1..MQ6:
    - style in VALID_MONTAGE_STYLES
    - beat_map present when style != "none"
    - every cut in cut_points_s within snap_tolerance_ms (40ms) of beat_map.beats_s (MQ1)
    - speed ramps within [0.25x, 4.0x], max 1 ramp per clip_id, and has musical_reason (MQ5)
    - SFX count <= 1 per 2 beats in montage mode (CR2)
    """
    errs: List[str] = []
    warns: List[str] = []

    if not isinstance(montage, dict):
        return (["project.montage must be an object/dict"], [])

    style = montage.get("style", "none")
    if style not in VALID_MONTAGE_STYLES:
        errs.append(f"project.montage.style {style!r} not in {sorted(VALID_MONTAGE_STYLES)}")
        return errs, warns

    if style == "none":
        return errs, warns

    beat_map = montage.get("beat_map")
    if not isinstance(beat_map, dict):
        errs.append(f"project.montage.beat_map is required when style is '{style}'")
        return errs, warns

    bpm = beat_map.get("bpm")
    fps = beat_map.get("fps", 30.0)
    time_sig = beat_map.get("time_signature", "4/4")
    beats_s = beat_map.get("beats_s", [])

    if not _is_valid_number(bpm) or float(bpm) <= 0:
        errs.append(f"project.montage.beat_map.bpm must be > 0, got {bpm!r}")
    if not _is_valid_number(fps) or float(fps) <= 0:
        errs.append(f"project.montage.beat_map.fps must be > 0, got {fps!r}")
    if time_sig not in SUPPORTED_TIME_SIGNATURES:
        errs.append(f"project.montage.beat_map.time_signature {time_sig!r} unsupported")
    if not isinstance(beats_s, list) or not beats_s:
        errs.append("project.montage.beat_map.beats_s must be a non-empty list of beat timestamps")
        return errs, warns

    if beat_map.get("source") == "estimated":
        warns.append("project.montage.beat_map.source is 'estimated'; verify actual audio BPM before final cut")

    # MQ1: Check cut points against beat grid
    cut_points = montage.get("cut_points_s", [])
    if isinstance(cut_points, list) and cut_points:
        ok_cuts, cut_errs = validate_cuts_against_beats(cut_points, beats_s, SNAP_TOLERANCE_MS)
        if not ok_cuts:
            errs.extend(cut_errs)

    # MQ5: Validate speed ramps (0.25x..4.0x, max 1 per clip_id, musical justification)
    ramps = montage.get("ramps", [])
    if not isinstance(ramps, list):
        errs.append("project.montage.ramps must be a list")
    else:
        ramps_per_clip: Dict[str, int] = {}
        for idx, r in enumerate(ramps, start=1):
            if not isinstance(r, dict):
                errs.append(f"project.montage.ramps[{idx}] must be an object/dict")
                continue
            cid = str(r.get("clip_id") or f"clip_{idx}")
            ramps_per_clip[cid] = ramps_per_clip.get(cid, 0) + 1
            from_sp = r.get("from_speed")
            to_sp = r.get("to_speed")
            if not _is_valid_number(from_sp) or not _is_valid_number(to_sp):
                errs.append(f"ramp #{idx} ({cid}): from_speed and to_speed must be numbers")
            else:
                if not (MIN_RAMP_SPEED <= float(from_sp) <= MAX_RAMP_SPEED) or not (
                    MIN_RAMP_SPEED <= float(to_sp) <= MAX_RAMP_SPEED
                ):
                    errs.append(
                        f"ramp #{idx} ({cid}): speed ({from_sp}x -> {to_sp}x) outside allowed "
                        f"[{MIN_RAMP_SPEED}x..{MAX_RAMP_SPEED}x] range"
                    )
            st = r.get("start_s", 0.0)
            en = r.get("end_s", 0.0)
            if not _is_valid_number(st) or not _is_valid_number(en) or float(st) < 0 or float(st) >= float(en):
                errs.append(f"ramp #{idx} ({cid}): invalid start_s/end_s ({st}..{en})")
            elif total_runtime_s > 0 and float(en) > total_runtime_s + 0.5:
                errs.append(f"ramp #{idx} ({cid}): end_s={en} exceeds total_runtime_s={total_runtime_s}")
            if not str(r.get("musical_reason") or "").strip() and not str(r.get("curve") or "").strip():
                errs.append(f"ramp #{idx} ({cid}): missing musical justification or curve (MQ5)")

        for cid, count in ramps_per_clip.items():
            if count > MAX_RAMPS_PER_CLIP:
                errs.append(
                    f"clip '{cid}' has {count} speed ramps; maximum allowed is {MAX_RAMPS_PER_CLIP} ramp per clip"
                )

    # CR2: Validate SFX density in montage mode (<= 1 SFX per 2 beats)
    sfx_cues = montage.get("sfx_cues", [])
    if not isinstance(sfx_cues, list):
        errs.append("project.montage.sfx_cues must be a list")
    else:
        max_sfx = max(1, (len(beats_s) * MAX_SFX_PER_TWO_BEATS) // 2)
        if len(sfx_cues) > max_sfx:
            errs.append(
                f"CR2 violation: montage has {len(sfx_cues)} SFX cues across {len(beats_s)} beats "
                f"(max allowed is 1 SFX per 2 beats = {max_sfx})"
            )

    return errs, warns


def main() -> None:
    """CLI entrypoint for beat_grid.py."""
    parser = argparse.ArgumentParser(description="Calculate rhythmic montage beat grid and cut points.")
    parser.add_argument("--bpm", type=float, required=True, help="Tempo in Beats Per Minute (e.g. 120)")
    parser.add_argument("--time-signature", type=str, default="4/4", help="Time signature (e.g. 4/4, 3/4, 6/8)")
    parser.add_argument("--fps", type=float, default=30.0, help="Video frame rate (e.g. 30, 60)")
    parser.add_argument("--duration", dest="duration_s", type=float, default=15.0, help="Duration in seconds")
    parser.add_argument(
        "--pattern",
        type=str,
        default="build_up",
        help="Cut cadence pattern: steady, build_up, call_response, breathe",
    )
    parser.add_argument("--output", type=str, default="", help="Optional output JSON path")
    args = parser.parse_args()

    try:
        result = compute_beat_grid(
            bpm=args.bpm,
            time_signature=args.time_signature,
            fps=args.fps,
            duration_s=args.duration_s,
            pattern=args.pattern,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    out_json = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out_json)
        print(f"Wrote beat grid to {args.output}")
    else:
        print(out_json)


if __name__ == "__main__":
    main()
