#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate a production package (06_package.json or compiled blueprint JSON).
Usage: python scripts/validate_package.py <package.json>

Checks:
1. Top-level JSON type (must be an object/dict) & required sections (project, identity_bible, blocks, outro).
   Automatically converts legacy `scene_breakdown`-only blueprints if `blocks` is absent.
2. Verified platform capabilities & hard-bounded per-clip durations (strictly within {4, 6, 8, 10}s).
3. Unique block_id & shot_id, shot density (1..3 shots/block), valid shot `t_range` within block duration.
4. Identity Bible ID declarations and prompt-level `[ID]` / `@ID` reference integrity.
5. `Extend` chain integrity: `extend_from_block` must reference an earlier block, cumulative chain <= 40s.
6. Prompt concision (<= 120 words/block), mandatory negatives, and anti-uncanny-valley rules.
7. Lip-sync clause length (<= 8 words per breath clause) on BOTH `dialogue_ar` and `dialogue_tts_ar`,
   plus consistency between `dialogue_ar` and `dialogue_tts_ar`.
8. Broadcast Arabic phonetic validation on `dialogue_tts_ar` (>= 75% vocalized base letters,
   clause-final `هْ` instead of `ة`, zero `\u0670` dagger alifs, zero banned transliterations).
9. Overlay timing bounds (`0 <= start_s < end_s <= total_runtime_s`) and word count (<= 6 words).
"""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Any, Dict, List, Set, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from beat_grid import validate_montage_section  # noqa: E402
from multi_agent_orchestrator import CLAUSE_SPLIT_RE, validate_arabic_phonetics  # noqa: E402
from studio_config import (  # noqa: E402
    ALLOWED_CLIP_DURATIONS,
    HARD_ALLOWED_CLIP_DURATIONS,
    MAX_EXTEND_CHAIN_SECONDS,
    MAX_LIPSYNC_WORDS_PER_PHRASE,
    MAX_OVERLAY_WORDS,
    MAX_PROMPT_WORDS_PER_BLOCK,
    MAX_SHOTS_PER_BLOCK,
    MIN_DIACRITIC_RATIO,
)

ID_TOKEN_RE = re.compile(r"\[([A-Z]+_\d+)\]|@([A-Z]+_\d+)")
T_RANGE_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*s?\s*$")


def is_number(val: Any) -> bool:
    """Returns True if val is an int or float (and not a bool)."""
    return isinstance(val, (int, float)) and not isinstance(val, bool)


def words(text: Any) -> int:
    """Counts whitespace-delimited words."""
    return len(str(text or "").split())


def split_clauses(text: str) -> List[str]:
    """Splits dialogue into breath clauses on punctuation, '..', or '[...]' pause markers."""
    return [c.strip() for c in CLAUSE_SPLIT_RE.split(str(text or "")) if c.strip()]


def convert_scene_breakdown_to_package(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts a `scene_breakdown` blueprint into a canonical Showrunner package dict
    (`project`, `identity_bible`, `blocks`, `overlays`, `outro`) if `blocks` is not already present.
    """
    if not isinstance(data, dict) or "blocks" in data:
        return data
    if "scene_breakdown" not in data or not isinstance(data.get("scene_breakdown"), list):
        return data

    meta = data.get("project_metadata", {})
    scenes = data["scene_breakdown"]
    identity_bible = [
        {
            "id": "CHAR_01",
            "type": "character",
            "description": "Primary hero presenter/subject locked across all shots",
        },
        {
            "id": "PROD_01",
            "type": "product",
            "description": "Hero product/brand artifact with consistent geometry and material finish",
        },
        {
            "id": "ENV_01",
            "type": "environment",
            "description": "Primary architectural studio/location environment with locked lighting",
        },
    ]

    blocks: List[Dict[str, Any]] = []
    overlays: List[Dict[str, Any]] = []
    elapsed = 0.0

    for idx, sc in enumerate(scenes, start=1):
        raw_dur = sc.get("duration_seconds", 6)
        dur = int(raw_dur) if is_number(raw_dur) and int(raw_dur) in HARD_ALLOWED_CLIP_DURATIONS else 6
        shot_id = f"{idx}A"
        dl_ar = str(sc.get("dialogue_lip_sync") or "").strip()
        dl_tts = str(sc.get("dialogue_tts_ar") or "").strip()
        if dl_ar.startswith("[") and dl_ar.endswith("]"):
            dl_ar = ""
        if dl_ar and not dl_tts:
            dl_ar = " ".join(w for w in dl_ar.replace("[0.3s pause]", "").split() if not w.startswith("["))
        blocks.append(
            {
                "block_id": idx,
                "duration_s": dur,
                "mode": "Ingredients" if idx == 1 else "Extend",
                "extend_from_block": None if idx == 1 else idx - 1,
                "ids_used": ["CHAR_01", "PROD_01", "ENV_01"],
                "shots": [
                    {
                        "shot_id": shot_id,
                        "t_range": f"0-{dur}",
                        "visual_prompt_en": str(sc.get("visual_prompt") or "Cinematic shot of [CHAR_01] with [PROD_01] in [ENV_01].")[:380],
                        "camera": str(sc.get("camera_movement") or "50mm lens, MS, smooth dolly-in"),
                        "lighting_grade": "motivated key/rim lighting, natural Rec.709 grade",
                        "audio_sync": str(sc.get("audio_sfx_sync") or "clean studio room tone and subtle foley"),
                        "dialogue_ar": dl_ar,
                        "dialogue_tts_ar": dl_tts,
                        "dialogue_gloss_en": "Spoken Arabic marketing line" if dl_ar else "",
                        "negatives": str(
                            sc.get("negative_guardrails")
                            or "no extra fingers, no distorted text, no logo morphing, no static-photo mouth cutout"
                        ),
                    }
                ],
            }
        )
        overlay_text = " ".join(str(sc.get("text_overlay") or "سينما فلو").split()[:MAX_OVERLAY_WORDS])
        overlays.append(
            {
                "start_s": round(elapsed, 2),
                "end_s": round(elapsed + dur, 2),
                "text_ar": overlay_text,
                "position": "bottom-safe",
            }
        )
        elapsed += dur

    converted = dict(data)
    converted["project"] = {
        "title": meta.get("idea_summary", "CineFlow Compiled Project"),
        "purpose": meta.get("purpose", "Commercials & TVCs"),
        "format": meta.get("video_format", "Live-Action"),
        "edit_style": meta.get("style_variant", "Commercial Promo"),
        "aspect_ratio": meta.get("aspect_ratio", "9:16"),
        "total_runtime_s": int(elapsed),
        "verified_capabilities": {
            "status": "VERIFIED",
            "per_clip_s_options": list(ALLOWED_CLIP_DURATIONS),
            "extend_max_s": MAX_EXTEND_CHAIN_SECONDS,
            "max_ref_images": 7,
        },
    }
    converted["identity_bible"] = identity_bible
    converted["blocks"] = blocks
    converted["overlays"] = overlays
    converted["outro"] = {
        "safe_zone_note": "9:16 central 80% safe zone; top 8% and bottom 20% clear for platform UI",
        "cta_ar": "ابدأ الآن",
    }
    return converted


def _validate_shot(
    shot: Any,
    block_id: Any,
    block_dur: float,
    declared_ids: Set[str],
    block_ids_used: Set[str],
    seen_shot_ids: Set[str],
    errs: List[str],
    warns: List[str],
) -> int:
    """Validates a single shot inside a block and returns its prompt word count."""
    if not isinstance(shot, dict):
        errs.append(f"block {block_id}: shot entry must be an object/dict")
        return 0

    sid = shot.get("shot_id")
    if not sid or not isinstance(sid, str):
        errs.append(f"block {block_id}: missing or non-string shot_id")
        sid = f"{block_id}_unknown"
    elif sid in seen_shot_ids:
        errs.append(f"duplicate shot_id: {sid}")
    else:
        seen_shot_ids.add(sid)

    # Validate t_range against block_dur
    t_range = str(shot.get("t_range") or "")
    m_range = T_RANGE_RE.match(t_range)
    if not m_range:
        errs.append(f"shot {sid}: invalid or missing t_range '{t_range}' (expected '0-{block_dur}')")
    else:
        t_start, t_end = float(m_range.group(1)), float(m_range.group(2))
        if t_start < 0 or t_start >= t_end or t_end > block_dur:
            errs.append(
                f"shot {sid}: t_range '{t_range}' out of bounds for block {block_id} duration {block_dur}s"
            )

    vp = str(shot.get("visual_prompt_en") or "")
    cam = str(shot.get("camera") or "")
    lg = str(shot.get("lighting_grade") or "")
    aud = str(shot.get("audio_sync") or "")

    if "static jpeg mouth" in vp.lower() or "mouth patch" in vp.lower():
        errs.append(f"shot {sid}: static-photo mouth-patch animation is HARD_BANNED")

    # Check ID references in prompt fields
    combined_prompt = f"{vp} {cam} {lg} {aud}"
    for m_id in ID_TOKEN_RE.finditer(combined_prompt):
        ref_id = m_id.group(1) or m_id.group(2)
        if ref_id not in declared_ids:
            errs.append(f"shot {sid}: prompt references undefined ID '{ref_id}' not in identity_bible")
        elif ref_id not in block_ids_used:
            errs.append(f"shot {sid}: prompt references ID '{ref_id}' not listed in block {block_id} ids_used")

    # Validate dialogue_ar & dialogue_tts_ar lip-sync and consistency
    dl_ar = str(shot.get("dialogue_ar") or "").strip()
    dl_tts = str(shot.get("dialogue_tts_ar") or "").strip()
    dl_gloss = str(shot.get("dialogue_gloss_en") or "").strip()

    for clause in split_clauses(dl_ar):
        if words(clause) > MAX_LIPSYNC_WORDS_PER_PHRASE:
            errs.append(
                f"shot {sid}: dialogue_ar clause exceeds {MAX_LIPSYNC_WORDS_PER_PHRASE} words ({words(clause)} words)"
            )

    if dl_ar and not dl_gloss:
        warns.append(f"shot {sid}: missing English gloss (dialogue_gloss_en)")
    if dl_gloss and not dl_ar and not dl_tts:
        errs.append(f"shot {sid}: dialogue_gloss_en provided without spoken/display Arabic dialogue")
    if (dl_ar and not dl_tts) or (dl_tts and not dl_ar):
        errs.append(f"shot {sid}: dialogue_ar and dialogue_tts_ar must both be populated when dialogue is present")

    if not str(shot.get("negatives") or "").strip():
        errs.append(f"shot {sid}: missing mandatory negative prompts (negatives)")

    if dl_tts:
        phon = validate_arabic_phonetics(dl_tts, min_ratio=MIN_DIACRITIC_RATIO, check_lip_sync_clauses=True)
        if not phon["valid"]:
            for issue in phon["issues"]:
                errs.append(f"shot {sid} dialogue_tts_ar: {issue}")

        # Verify spoken text (dialogue_tts_ar) matches display text (dialogue_ar) word count
        if dl_ar:
            ar_clauses = split_clauses(dl_ar)
            tts_clauses = split_clauses(dl_tts)
            ar_wc = sum(words(c) for c in ar_clauses)
            tts_wc = sum(words(c) for c in tts_clauses)
            if abs(ar_wc - tts_wc) > 2:
                errs.append(
                    f"shot {sid}: dialogue_tts_ar word count ({tts_wc}) diverges from dialogue_ar ({ar_wc})"
                )

    return words(vp) + words(aud) + words(cam) + words(lg)


def validate_package_dict(raw_data: Any) -> Tuple[List[str], List[str]]:
    """Validates a package dictionary and returns (errors, warnings)."""
    errs: List[str] = []
    warns: List[str] = []

    if not isinstance(raw_data, dict):
        return (["top-level JSON must be an object/dict, got " + type(raw_data).__name__], [])

    d = convert_scene_breakdown_to_package(raw_data)

    for req_key in ("project", "identity_bible", "blocks", "outro"):
        if req_key not in d:
            errs.append(f"missing key: {req_key}")

    if errs:
        return errs, warns

    p = d.get("project")
    if not isinstance(p, dict):
        errs.append("project must be an object/dict")
        return errs, warns

    caps = p.get("verified_capabilities", {})
    if not isinstance(caps, dict):
        errs.append("project.verified_capabilities must be an object/dict")
        caps = {}

    raw_opts = caps.get("per_clip_s_options", list(ALLOWED_CLIP_DURATIONS))
    if not isinstance(raw_opts, list) or not raw_opts or not all(is_number(x) for x in raw_opts):
        errs.append("verified_capabilities.per_clip_s_options must be a non-empty list of numbers")
        allowed: Set[int] = set(HARD_ALLOWED_CLIP_DURATIONS)
    else:
        invalid_opts = [x for x in raw_opts if x not in HARD_ALLOWED_CLIP_DURATIONS]
        if invalid_opts:
            errs.append(
                f"per_clip_s_options contains unsupported durations {invalid_opts}; "
                f"hard ceiling allows only {sorted(HARD_ALLOWED_CLIP_DURATIONS)}"
            )
        allowed = set(int(x) for x in raw_opts if x in HARD_ALLOWED_CLIP_DURATIONS)

    if caps.get("status") != "VERIFIED":
        warns.append("capabilities are UNVERIFIED: run Phase 1 research")

    motion_cfg = p.get("motion_engine_60fps", {})
    if isinstance(motion_cfg, dict) and motion_cfg.get("enabled"):
        bloom = motion_cfg.get("bloom", {})
        if isinstance(bloom, dict) and is_number(bloom.get("strength")) and bloom["strength"] > 0.75:
            warns.append("motion_engine_60fps.bloom.strength > 0.75 risks washing out 3D cards (recommended 0.42)")

    ib = d.get("identity_bible")
    if not isinstance(ib, list) or not ib:
        errs.append("identity_bible must be a non-empty list")
        declared_ids: Set[str] = set()
    else:
        declared_ids = {
            str(item.get("id"))
            for item in ib
            if isinstance(item, dict) and item.get("id")
        }

    blocks = d.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        errs.append("blocks must be a non-empty list")
        return errs, warns

    total_dur = 0.0
    seen_block_ids: Set[Any] = set()
    seen_shot_ids: Set[str] = set()
    chain_durations: Dict[Any, float] = {}

    for b in blocks:
        if not isinstance(b, dict):
            errs.append("each block in blocks must be an object/dict")
            continue

        bid = b.get("block_id")
        if bid is None or isinstance(bid, bool) or not isinstance(bid, (int, str)):
            errs.append(f"invalid block_id: {bid!r}")
        elif bid in seen_block_ids:
            errs.append(f"duplicate block_id: {bid}")

        dur = b.get("duration_s")
        if not is_number(dur):
            errs.append(
                f"block {bid}: duration_s must be a number in {sorted(HARD_ALLOWED_CLIP_DURATIONS)}, "
                f"got {type(dur).__name__}"
            )
            dur_val = 0.0
        else:
            dur_val = float(dur)
            total_dur += dur_val
            if dur_val not in allowed or dur_val not in HARD_ALLOWED_CLIP_DURATIONS:
                errs.append(f"block {bid}: duration {dur_val:g}s not in allowed {sorted(allowed)}")

        # Check Extend chain references and 40s cumulative ceiling
        mode = b.get("mode")
        ext_from = b.get("extend_from_block")
        if mode == "Extend":
            if ext_from is None:
                errs.append(f"block {bid}: mode 'Extend' requires extend_from_block")
            elif ext_from not in seen_block_ids:
                errs.append(
                    f"block {bid}: extend_from_block '{ext_from}' must reference an earlier existing block_id"
                )
            else:
                chain_durations[bid] = chain_durations.get(ext_from, 0.0) + dur_val
                if chain_durations[bid] > MAX_EXTEND_CHAIN_SECONDS:
                    errs.append(
                        f"block {bid}: cumulative Extend chain duration {chain_durations[bid]:g}s "
                        f"exceeds {MAX_EXTEND_CHAIN_SECONDS}s cap"
                    )
        else:
            chain_durations[bid] = dur_val

        if bid is not None and not isinstance(bid, bool):
            seen_block_ids.add(bid)

        ids_used_raw = b.get("ids_used", [])
        if not isinstance(ids_used_raw, list):
            errs.append(f"block {bid}: ids_used must be a list")
            block_ids_used: Set[str] = set()
        else:
            block_ids_used = {str(u) for u in ids_used_raw}
            for u in block_ids_used:
                if u not in declared_ids:
                    errs.append(f"block {bid}: unknown id '{u}' in ids_used")

        shots = b.get("shots", [])
        if not isinstance(shots, list) or not shots:
            errs.append(f"block {bid}: no shots")
            continue
        if len(shots) > MAX_SHOTS_PER_BLOCK:
            errs.append(f"block {bid}: {len(shots)} shots (max {MAX_SHOTS_PER_BLOCK})")

        prompt_words = 0
        for s in shots:
            prompt_words += _validate_shot(
                s, bid, dur_val if dur_val > 0 else 10.0, declared_ids, block_ids_used, seen_shot_ids, errs, warns
            )

        if prompt_words > MAX_PROMPT_WORDS_PER_BLOCK:
            errs.append(
                f"block {bid}: prompt {prompt_words} words exceeds max {MAX_PROMPT_WORDS_PER_BLOCK} words"
            )

    declared_runtime = p.get("total_runtime_s")
    if declared_runtime is not None:
        if not is_number(declared_runtime) or declared_runtime <= 0:
            errs.append(f"project.total_runtime_s must be a positive number, got {declared_runtime!r}")
        elif total_dur and abs(total_dur - float(declared_runtime)) > 2:
            errs.append(
                f"sum of blocks {total_dur:g}s differs from project.total_runtime_s {declared_runtime}s"
            )

    max_valid_time = float(declared_runtime) if is_number(declared_runtime) and declared_runtime > 0 else total_dur
    overlays = d.get("overlays", [])
    if not isinstance(overlays, list):
        errs.append("overlays must be a list")
    else:
        for idx, o in enumerate(overlays, start=1):
            if not isinstance(o, dict):
                errs.append(f"overlay #{idx}: must be an object/dict")
                continue
            st = o.get("start_s")
            en = o.get("end_s")
            if not is_number(st) or not is_number(en):
                errs.append(f"overlay #{idx}: start_s and end_s must be numbers")
            elif st < 0 or st >= en or (max_valid_time > 0 and en > max_valid_time + 0.5):
                errs.append(
                    f"overlay #{idx}: invalid timing {st}..{en}s (must satisfy 0 <= start_s < end_s <= {max_valid_time:g}s)"
                )
            if words(o.get("text_ar", "")) > MAX_OVERLAY_WORDS:
                errs.append(f"overlay #{idx}: text_ar exceeds {MAX_OVERLAY_WORDS} words")

    if "montage" in p and p["montage"] is not None:
        m_errs, m_warns = validate_montage_section(p["montage"], max_valid_time)
        errs.extend(m_errs)
        warns.extend(m_warns)

    return errs, warns


# Backwards-compatible alias
validate = validate_package_dict


def main() -> None:
    """CLI entry point for validating a package JSON file."""
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            raw_data = json.load(f)
    except (OSError, ValueError, TypeError) as exc:
        print(f"FAIL: cannot read JSON: {exc}")
        sys.exit(1)

    errs, warns = validate_package_dict(raw_data)
    for e in errs:
        print("ERROR:", e)
    for w in warns:
        print("WARN:", w)
    print("PASS" if not errs else "FAIL", f"({len(errs)} errors, {len(warns)} warnings)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
