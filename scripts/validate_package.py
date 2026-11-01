#!/usr/bin/env python3
"""Validate a production package (06_package.json).
Usage: python scripts/validate_package.py <package.json>

Checks:
1. Required top-level sections (project, identity_bible, blocks, outro).
2. Verified platform capabilities & allowed per-clip durations (4, 6, 8, 10s).
3. Shot density (1..3 shots per block), Identity Bible ID references, and Extend chain links.
4. Prompt concision (<= 120 words per block) and mandatory negative prompts.
5. Lip-sync phrase length (<= 8 words per sentence), English gloss, and anti-uncanny-valley rules.
6. Optional Arabic broadcast phonetic validation on dialogue_tts_ar (>= 70% diacritic ratio, pause هْ, zero dagger alif ٰ).
"""
import json
import re
import sys

ARABIC_BASE_RE = re.compile(r"[\u0621-\u063A\u0641-\u064A]")
ARABIC_DIACRITIC_RE = re.compile(r"[\u064B-\u0652\u0651]")


def words(s):
    return len(str(s).split())


def check_tts_phonetics(tts_str, context_label, errs, warns):
    if not tts_str or not str(tts_str).strip():
        return
    txt = str(tts_str).strip()
    if "\u0670" in txt:
        errs.append(f"{context_label}: contains forbidden superscript dagger alif (\\u0670)")
    base_letters = len(ARABIC_BASE_RE.findall(txt))
    diacritics = len(ARABIC_DIACRITIC_RE.findall(txt))
    if base_letters > 0:
        ratio = diacritics / base_letters
        if ratio < 0.70:
            warns.append(
                f"{context_label}: dialogue_tts_ar diacritic ratio is {ratio:.2f} (target >= 0.75 for broadcast TTS)"
            )
    tokens = [t.strip("،.؟!,:;\"'()[]") for t in txt.split() if t.strip("،.؟!,:;\"'()[]")]
    if tokens and "ة" in tokens[-1]:
        warns.append(
            f"{context_label}: pause-final word '{tokens[-1]}' in dialogue_tts_ar contains 'ة' (replace with 'هْ' for natural TTS pause)"
        )


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:
        print(f"FAIL: cannot read JSON: {e}")
        sys.exit(1)

    errs, warns = [], []
    for k in ("project", "identity_bible", "blocks", "outro"):
        if k not in d:
            errs.append(f"missing key: {k}")

    p = d.get("project", {})
    caps = p.get("verified_capabilities", {})
    allowed = set(caps.get("per_clip_s_options", [4, 6, 8, 10]))
    if caps.get("status") != "VERIFIED":
        warns.append("capabilities are UNVERIFIED: run Phase 1 research")

    motion_cfg = p.get("motion_engine_60fps", {})
    if motion_cfg.get("enabled"):
        bloom = motion_cfg.get("bloom", {})
        if bloom.get("strength", 0.42) > 0.75:
            warns.append("motion_engine_60fps.bloom.strength > 0.75 risks washing out 3D cards (recommended 0.42)")

    ids = {i.get("id") for i in d.get("identity_bible", [])}
    total = 0

    for b in d.get("blocks", []):
        bid = b.get("block_id")
        dur = b.get("duration_s")
        total += dur or 0
        if dur not in allowed:
            errs.append(f"block {bid}: duration {dur}s not in {sorted(allowed)}")
        shots = b.get("shots", [])
        if not shots:
            errs.append(f"block {bid}: no shots")
        if len(shots) > 3:
            errs.append(f"block {bid}: {len(shots)} shots (max 3)")
        for u in b.get("ids_used", []):
            if u not in ids:
                errs.append(f"block {bid}: unknown id {u}")
        if b.get("mode") == "Extend" and not b.get("extend_from_block"):
            errs.append(f"block {bid}: Extend needs extend_from_block")

        prompt_words = sum(
            words(s.get("visual_prompt_en", ""))
            + words(s.get("audio_sync", ""))
            + words(s.get("camera", ""))
            + words(s.get("lighting_grade", ""))
            for s in shots
        )
        if prompt_words > 120:
            warns.append(f"block {bid}: prompt ~{prompt_words} words (target <=120)")

        for s in shots:
            sid = s.get("shot_id")
            vp = str(s.get("visual_prompt_en", "")).lower()
            if "static jpeg mouth" in vp or "mouth patch" in vp:
                errs.append(f"shot {sid}: static-photo mouth-patch animation is HARD_BANNED")
            dl = s.get("dialogue_ar", "")
            for line in [x for x in str(dl).replace("؟", ".").replace("!", ".").split(".") if x.strip()]:
                if words(line) > 8:
                    warns.append(f"shot {sid}: dialogue phrase >8 words")
            if dl and not s.get("dialogue_gloss_en"):
                warns.append(f"shot {sid}: missing English gloss")
            if not s.get("negatives"):
                warns.append(f"shot {sid}: no negatives")
            if s.get("dialogue_tts_ar"):
                check_tts_phonetics(s.get("dialogue_tts_ar"), f"shot {sid}", errs, warns)

    for o in d.get("overlays", []):
        if words(o.get("text_ar", "")) > 6:
            warns.append("overlay text >6 words")

    if p.get("total_runtime_s") and total and abs(total - p["total_runtime_s"]) > 2:
        warns.append(f"sum of blocks {total}s differs from total_runtime_s {p['total_runtime_s']}s")

    for e in errs:
        print("ERROR:", e)
    for w in warns:
        print("WARN:", w)
    print("PASS" if not errs else "FAIL", f"({len(errs)} errors, {len(warns)} warnings)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
