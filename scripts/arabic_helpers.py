#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arabic Broadcast Linguistics, Kashida Engine, Remotion v4.0.539 ZWJ Letter Splitter,
Video-First Layout Validator, Lip-Sync Phraser, and Slash Macro Resolver for CineFlow AI Studio.
"""

from __future__ import annotations

import math
import os
import re
import sys
from typing import Any, Dict, List, Set

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from studio_config import (  # noqa: E402
    DIALECT_LEXICON,
    KASHIDA_PROTECTED_WORDS,
    MACRO_DICTIONARY,
    MAX_WORDS_PER_SECOND_AR,
    NON_CONNECTING_ARABIC_LETTERS,
    VIDEO_LAYOUT_MAX_FOCAL_POINTS_PER_SCENE,
    VIDEO_LAYOUT_MIN_HEADLINE_PX,
    VIDEO_LAYOUT_MIN_SUPPORTING_PX,
    VIDEO_LAYOUT_SAFE_MARGIN_X_PX,
    VIDEO_LAYOUT_SAFE_MARGIN_Y_PX,
)

HARAKAT_CHARS: Set[str] = set("\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0670")
ARABIC_BASE_RE = re.compile(r"[\u0621-\u063A\u0641-\u064A]")
_RTL_WORD_RE = re.compile(r"[\u0591-\u07FF\uFB1D-\uFDFD\uFE70-\uFEFC]")
_HARAKAT_EXT_RE = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]")
_ARABIC_EXT_BASE_RE = re.compile(r"[\u0621-\u064A\u066E-\u066F\u0671-\u06D3\u06F0-\u06FC]")
_RIGHT_JOIN_ONLY_SET: Set[str] = set("اأإآدذرزوؤةءٱ")
_ALEF_WITH_LAM_SET: Set[str] = set("اأإآٱ")
_ZWJ: str = "\u200D"


def detect_arabic_dialect_with_confidence(text: str) -> Dict[str, Any]:
    """
    Detects the Arabic or regional dialect with confidence score and matched markers.
    Returns dialect='UNKNOWN (غير معروف)' and confidence=0.0 when text is empty, non-Arabic, or unmatched.
    """
    raw = str(text or "").strip()
    if not raw or not ARABIC_BASE_RE.search(raw):
        return {"dialect": "UNKNOWN (غير معروف)", "confidence": 0.0, "matched_markers": []}

    label_map = {
        "BAHRAIN_URBAN": "BAHRAINI_KHALEEJI (اللهجة البحرينية الأصيلة)",
        "SAUDI_HIJAZI": "SAUDI_HIJAZI (اللهجة الحجازية السعودية)",
        "SAUDI_NAJDI": "SAUDI_KHALEEJI (اللهجة السعودية الخليجية)",
        "IRAQI": "IRAQI (اللهجة العراقية)",
        "KUWAITI": "KUWAITI_GULF (اللهجة الكويتية / الخليجية)",
        "EMIRATI": "EMIRATI_GULF (اللهجة الإماراتية)",
        "LEVANTINE": "LEVANTINE (اللهجة الشامية)",
        "EGYPTIAN": "EGYPTIAN (اللهجة المصرية)",
        "MSA": "MSA (العربية الفصحى العصرية)",
    }

    best_code = ""
    best_matches: List[str] = []
    for code in (
        "BAHRAIN_URBAN",
        "SAUDI_HIJAZI",
        "SAUDI_NAJDI",
        "IRAQI",
        "KUWAITI",
        "EMIRATI",
        "LEVANTINE",
        "EGYPTIAN",
    ):
        matches = [m for m in DIALECT_LEXICON[code] if re.search(rf"(?<!\w){re.escape(m)}(?!\w)", raw)]
        if len(matches) > len(best_matches):
            best_code = code
            best_matches = matches

    if best_code:
        conf = min(0.98, round(0.65 + 0.12 * len(best_matches), 2))
        return {
            "dialect": label_map[best_code],
            "confidence": conf,
            "matched_markers": best_matches,
        }

    if re.search(r"(?<!\w)(الحين|تبي|عشان|اللي)(?!\w)", raw):
        return {
            "dialect": "KHALEEJI_GENERAL (اللهجة الخليجية البيضاء)",
            "confidence": 0.72,
            "matched_markers": ["خليجي عام"],
        }

    msa_matches = [m for m in DIALECT_LEXICON["MSA"] if re.search(rf"(?<!\w){re.escape(m)}(?!\w)", raw)]
    if msa_matches or re.search(r"[\u064B-\u0650]", raw):
        conf = min(0.95, round(0.60 + 0.10 * max(1, len(msa_matches)), 2))
        return {
            "dialect": label_map["MSA"],
            "confidence": conf,
            "matched_markers": msa_matches or ["تشكيل فصيح"],
        }

    return {"dialect": "UNKNOWN (غير معروف)", "confidence": 0.0, "matched_markers": []}


def detect_arabic_dialect(text: str) -> str:
    """Detect the specific Arabic or regional dialect from natural text or dialogue."""
    return str(detect_arabic_dialect_with_confidence(text)["dialect"])


def apply_safe_arabic_kashida(word: str, count: int = 3) -> str:
    """
    Insert Kashida (ـ) safely after the last valid connecting Arabic base letter,
    respecting Harakat/Tashkeel, protecting sacred/frozen words ('الله', 'لا', etc.),
    and never breaking non-connecting letters.
    """
    clean = str(word or "").strip()
    if len(clean) < 2:
        return clean

    stripped_unvocalized = re.sub(r"[\u064B-\u0652\u0670ـ]", "", clean)
    if stripped_unvocalized in KASHIDA_PROTECTED_WORDS:
        return clean

    clusters: List[str] = []
    for ch in clean:
        if ch in HARAKAT_CHARS and clusters:
            clusters[-1] += ch
        else:
            clusters.append(ch)

    if len(clusters) < 2:
        return clean

    valid_idx = -1
    for i in range(len(clusters) - 1):
        base_char = clusters[i][0]
        next_base = clusters[i + 1][0]
        if base_char == "ل" and next_base in {"ا", "أ", "إ", "آ"}:
            continue
        if base_char == "ل" and next_base == "ل" and i + 2 < len(clusters) and clusters[i + 2][0] == "ه":
            continue
        if base_char not in NON_CONNECTING_ARABIC_LETTERS and "\u0621" <= base_char <= "\u064a":
            valid_idx = i

    if valid_idx == -1:
        return clean

    kashida_bar = "ـ" * max(1, count)
    clusters[valid_idx] = clusters[valid_idx] + kashida_bar
    return "".join(clusters)


def is_rtl_text(text: str) -> bool:
    """
    Detect whether a string should use dir='rtl' by checking whether the majority
    of whitespace-delimited words contain RTL characters (remotion-markup/arabic-text.md).
    """
    words = [w for w in str(text or "").strip().split() if w]
    if not words:
        return True
    rtl_count = sum(1 for w in words if _RTL_WORD_RE.search(w))
    return rtl_count > (len(words) / 2.0)


def split_arabic_letters_zwj(word: str) -> List[str]:
    """
    Official Remotion v4.0.539 per-letter Arabic splitter (`remotion-markup/arabic-text.md`):
    - Attaches Harakat/Tashkeel marks to their base letter
    - Keeps Lam-Alef ligatures (لا، لأ، لإ، لآ، لٱ) as a single indivisible unit
    - Keeps consecutive non-Arabic characters (digits/Latin runs like '2026', 'iOS') together
    - Injects U+200D Zero-Width Joiners (ZWJ) before/after connected Arabic letters so
      isolated <span> elements preserve initial/medial/final contextual shaping.
    """
    clusters: List[Dict[str, str]] = []
    for ch in str(word or ""):
        if _HARAKAT_EXT_RE.match(ch) and clusters:
            clusters[-1]["marks"] += ch
        else:
            clusters.append({"base": ch, "marks": ""})

    units: List[Dict[str, Any]] = []
    i = 0
    while i < len(clusters):
        c = clusters[i]
        if c["base"] == "ل" and (i + 1) < len(clusters) and clusters[i + 1]["base"] in _ALEF_WITH_LAM_SET:
            nxt = clusters[i + 1]
            units.append({
                "text": c["base"] + c["marks"] + nxt["base"] + nxt["marks"],
                "first_base": c["base"],
                "last_base": nxt["base"],
                "is_arabic": True,
            })
            i += 2
            continue
        if _ARABIC_EXT_BASE_RE.match(c["base"]):
            units.append({
                "text": c["base"] + c["marks"],
                "first_base": c["base"],
                "last_base": c["base"],
                "is_arabic": True,
            })
        elif units and not units[-1]["is_arabic"]:
            units[-1]["text"] += c["base"] + c["marks"]
        else:
            units.append({
                "text": c["base"] + c["marks"],
                "first_base": c["base"],
                "last_base": c["base"],
                "is_arabic": False,
            })
        i += 1

    def _joins_right(unit: Dict[str, Any]) -> bool:
        return bool(unit["is_arabic"] and unit["first_base"] != "ء")

    def _joins_left(unit: Dict[str, Any]) -> bool:
        return bool(unit["is_arabic"] and unit["last_base"] not in _RIGHT_JOIN_ONLY_SET)

    result: List[str] = []
    for idx, unit in enumerate(units):
        prev_u = units[idx - 1] if idx > 0 else None
        next_u = units[idx + 1] if (idx + 1) < len(units) else None
        prefix = _ZWJ if (prev_u and _joins_left(prev_u) and _joins_right(unit)) else ""
        suffix = _ZWJ if (next_u and _joins_left(unit) and _joins_right(next_u)) else ""
        result.append(f"{prefix}{unit['text']}{suffix}")
    return result


def validate_video_first_layout(
    headline_px: int,
    supporting_px: int,
    margin_x_px: int = VIDEO_LAYOUT_SAFE_MARGIN_X_PX,
    margin_y_px: int = VIDEO_LAYOUT_SAFE_MARGIN_Y_PX,
    focal_points_per_scene: int = VIDEO_LAYOUT_MAX_FOCAL_POINTS_PER_SCENE,
    width: int = 1080,
) -> Dict[str, Any]:
    """
    Validate scene typography & layout against Remotion v4.0.539 `remotion-create/video-layout.md`:
    - 'You are designing a video, not a webpage.'
    - One primary focal point per scene (`focal_points_per_scene <= 1`).
    - Minimum font sizes scaled to composition width (for 1080px: Headline >= 84px, Supporting >= 44px).
    - Safe area margins >= 80px horizontal and >= 100px vertical (scaled to width).
    """
    scale = max(0.5, float(width) / 1080.0)
    min_headline = round(VIDEO_LAYOUT_MIN_HEADLINE_PX * scale)
    min_support = round(VIDEO_LAYOUT_MIN_SUPPORTING_PX * scale)
    min_margin_x = round(VIDEO_LAYOUT_SAFE_MARGIN_X_PX * scale)
    min_margin_y = round(VIDEO_LAYOUT_SAFE_MARGIN_Y_PX * scale)

    errors: List[str] = []
    if headline_px < min_headline:
        errors.append(
            f"Video-First Layout violation: Main headline ({headline_px}px) is below minimum "
            f"{min_headline}px for {width}px-wide video."
        )
    if supporting_px < min_support:
        errors.append(
            f"Video-First Layout violation: Supporting text ({supporting_px}px) is below minimum "
            f"{min_support}px for {width}px-wide video."
        )
    if margin_x_px < min_margin_x:
        errors.append(
            f"Video-First Layout violation: Horizontal safe margin ({margin_x_px}px) is below minimum {min_margin_x}px."
        )
    if margin_y_px < min_margin_y:
        errors.append(
            f"Video-First Layout violation: Vertical safe margin ({margin_y_px}px) is below minimum {min_margin_y}px."
        )
    if focal_points_per_scene > VIDEO_LAYOUT_MAX_FOCAL_POINTS_PER_SCENE:
        errors.append(
            f"Video-First Layout violation: Scene has {focal_points_per_scene} competing focal points "
            "(must be 1 primary focal point, not a webpage dashboard)."
        )
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "thresholds": {
            "min_headline_px": min_headline,
            "min_supporting_px": min_support,
            "min_margin_x_px": min_margin_x,
            "min_margin_y_px": min_margin_y,
            "max_focal_points_per_scene": VIDEO_LAYOUT_MAX_FOCAL_POINTS_PER_SCENE,
        },
    }


def generate_keyword_variants(keyword: str) -> List[str]:
    """
    Generate comprehensive Arabic orthographic variants for comment-keyword DM matching:
    - Initial/medial hamza (أ/إ/آ <-> ا)
    - Carrier hamza (ؤ -> و, ئ -> ي)
    - Final taa marbuta (ة <-> ه)
    - Final alef maqsura / yaa (ى <-> ي)
    """
    base = str(keyword or "").strip()
    if not base:
        return ["تفاصيل"]

    seeds: Set[str] = {base}
    for item in list(seeds):
        seeds.add(item.replace("ؤ", "و"))
        seeds.add(item.replace("ئ", "ي"))
        seeds.add(item.replace("ؤ", "و").replace("ئ", "ي"))

    for item in list(seeds):
        seeds.add(re.sub(r"[أإآ]", "ا", item))

    for item in list(seeds):
        if item.endswith("ة"):
            seeds.add(item[:-1] + "ه")
        elif item.endswith("ه"):
            seeds.add(item[:-1] + "ة")

    for item in list(seeds):
        if item.endswith("ى"):
            seeds.add(item[:-1] + "ي")
        elif item.endswith("ي"):
            seeds.add(item[:-1] + "ى")

    return sorted(seeds)


def optimize_arabic_lip_sync(raw_dialogue: str, duration_seconds: int) -> str:
    """
    Enforce the Audio-Math Law (Words <= Duration * 2.5 per shot) and split Arabic dialogue
    into crisp 4-word breath clauses separated by `.. [0.3s breath pause]`.
    """
    if not isinstance(duration_seconds, (int, float)) or isinstance(duration_seconds, bool) or duration_seconds <= 0:
        raise ValueError(f"duration_seconds must be > 0, got {duration_seconds!r}")

    if not raw_dialogue or not raw_dialogue.strip():
        return "[No Spoken Dialogue - Visual & SFX Driven]"

    all_words = [w for w in raw_dialogue.strip().split() if w]
    max_words_per_shot = max(1, math.floor(duration_seconds * MAX_WORDS_PER_SECOND_AR))

    shot_strings: List[str] = []
    for shot_start in range(0, len(all_words), max_words_per_shot):
        shot_slice = all_words[shot_start : shot_start + max_words_per_shot]
        clauses: List[str] = []
        for idx in range(0, len(shot_slice), 4):
            clauses.append(" ".join(shot_slice[idx : idx + 4]))
        shot_strings.append(" .. [0.3s breath pause] ".join(clauses))

    return " || [SHOT_SPLIT] || ".join(shot_strings)


def auto_vocalize_arabic_for_tts(text: str) -> str:
    """
    Deterministically vocalizes an Arabic dialogue string for broadcast TTS (`dialogue_tts_ar`)
    so that >= 80% of Arabic base letters carry explicit harakat, pause-final `ة` becomes `هْ`,
    and superscript dagger alif (`\\u0670`) is replaced with standard fatha.
    """
    clean = str(text or "").replace("\u0670", "\u064e").strip()
    if not clean or clean.startswith("["):
        return ""

    clean = clean.replace("|| [SHOT_SPLIT] ||", " ، ").replace("[0.3s breath pause]", "").replace("..", "،")
    tokens = [t for t in clean.split() if t]
    vocalized_tokens: List[str] = []

    for tok in tokens:
        if re.fullmatch(r"[،.؛!؟…\"'()\[\]:-]+", tok):
            vocalized_tokens.append(tok)
            continue

        m_punc = re.match(r"^(.*?)([،.؛!؟…\"')\]»]*)$", tok)
        core = m_punc.group(1) if m_punc else tok
        trail = m_punc.group(2) if m_punc else ""

        core = re.sub(r"ة[\u064B-\u0652\u0651]*$", "هْ", core)

        out_chars: List[str] = []
        chars = list(core)
        for i, ch in enumerate(chars):
            out_chars.append(ch)
            if not ARABIC_BASE_RE.match(ch):
                continue
            next_ch = chars[i + 1] if i + 1 < len(chars) else ""
            if next_ch in HARAKAT_CHARS:
                continue
            if i == 0 and ch == "ا" and len(chars) >= 2 and chars[1] == "ل":
                continue
            if i == len(chars) - 1:
                out_chars.append("\u0652")
            else:
                out_chars.append("\u064e")
        vocalized_tokens.append("".join(out_chars) + trail)

    return " ".join(vocalized_tokens)


def resolve_slash_macros(idea: str) -> List[str]:
    """Extract and expand all slash macros found in the user's idea string."""
    lowered = str(idea or "").lower()
    expanded: List[str] = []
    for macro, description in MACRO_DICTIONARY.items():
        if macro in lowered:
            expanded.append(description)
    if not expanded:
        expanded.append(
            "smooth physical camera dolly push-in, 35mm anamorphic prime lens, volumetric cinematic lighting"
        )
    return expanded


def _partition_even(items: List[Any], parts: int) -> List[List[Any]]:
    """
    Balanced word partitioning (`even(ws, n)` from B Studio `Captions.tsx` Rule 76).
    Splits `items` into `parts` contiguous slices of nearly equal size so no single
    orphan word is left alone on a line or caption card.
    """
    total = len(items)
    if parts <= 1 or total <= 1:
        return [items] if items else []
    parts = min(parts, total)
    out: List[List[Any]] = []
    for idx in range(parts):
        start_i = int(round(idx * total / parts))
        end_i = int(round((idx + 1) * total / parts))
        if end_i > start_i:
            out.append(items[start_i:end_i])
    return out


def split_caption_cards_balanced(
    words: List[Dict[str, Any]],
    max_chars_per_line: int = 24,
    max_lines: int = 2,
) -> List[Dict[str, Any]]:
    """
    Implements B Studio Rule 76 (`Captions.tsx`):
    - Maximum `max_lines` (default 2) lines per caption card.
    - If a sentence wraps to > `max_lines`, splits it into `ceil(lines / max_lines)` cards
      with balanced word counts (`_partition_even`) so no orphan single-word card is produced.
    - Inside each card, balances words across at most 2 lines and enforces
      `pre_spoken_css = "visibility:hidden"` so the card bounding box never jumps as words reveal.
    """
    if not words:
        return []

    normalized: List[Dict[str, Any]] = []
    for idx, item in enumerate(words):
        if isinstance(item, dict):
            text = str(item.get("t", item.get("word", ""))).strip()
            start_s = float(item.get("s", item.get("start", idx * 0.35)))
            end_s = float(item.get("e", item.get("end", start_s + 0.32)))
            hi = bool(item.get("hi", False))
        else:
            text = str(item).strip()
            start_s = round(idx * 0.35, 3)
            end_s = round(start_s + 0.32, 3)
            hi = False
        if text:
            normalized.append({"t": text, "s": start_s, "e": end_s, "hi": hi})

    if not normalized:
        return []

    total_chars = sum(len(w["t"]) + 1 for w in normalized) - 1
    estimated_lines = max(1, (total_chars + max_chars_per_line - 1) // max(1, max_chars_per_line))
    num_cards = max(1, (estimated_lines + max_lines - 1) // max(1, max_lines))

    card_slices = _partition_even(normalized, num_cards)
    cards: List[Dict[str, Any]] = []
    for card_words in card_slices:
        card_chars = sum(len(w["t"]) + 1 for w in card_words) - 1
        line_count = 2 if (card_chars > max_chars_per_line and len(card_words) >= 2) else 1
        lines = _partition_even(card_words, line_count)
        cards.append(
            {
                "s": card_words[0]["s"],
                "e": card_words[-1]["e"],
                "w": card_words,
                "lines": [[w["t"] for w in ln] for ln in lines],
                "line_count": len(lines),
                "max_lines_enforced": max_lines,
                "pre_spoken_css": "visibility:hidden",
                "has_orphan_word_card": len(card_words) == 1 and len(normalized) > 1,
            }
        )
    return cards

