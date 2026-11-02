#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Positive and Negative Acceptance Tests for Rhythmic Montage & Beat Grid (tests/test_montage.py).

Compatible with both `pytest -v tests/test_montage.py` and direct CLI execution:
`python tests/test_montage.py`.
"""

from __future__ import annotations

import contextlib
import copy
import sys
from pathlib import Path
from typing import Iterator, Optional, Type

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from beat_grid import (  # noqa: E402
    build_project_montage,
    compute_beat_grid,
    validate_cuts_against_beats,
    validate_montage_section,
)
from cineflow_compiler import (  # noqa: E402
    audit_sfx_governor,
    build_omni_interaction_payload,
    compile_blueprint,
    is_rtl_text,
    optimize_arabic_lip_sync,
    partition_runtime_into_allowed_blocks,
    split_arabic_letters_zwj,
    split_caption_cards_balanced,
    validate_video_first_layout,
    validate_window_schedule_and_face_guard,
)
from validate_package import validate_package_dict  # noqa: E402


@contextlib.contextmanager
def assert_raises(exc_type: Type[BaseException], match: Optional[str] = None) -> Iterator[None]:
    """Portable replacement for pytest.raises."""
    try:
        yield
    except exc_type as exc:
        if match and match.lower() not in str(exc).lower():
            raise AssertionError(f"Exception '{exc}' did not contain '{match}'") from exc
        return
    raise AssertionError(f"Expected {exc_type.__name__} to be raised, but no exception was raised.")


def test_beat_math_120bpm_30fps_equals_15_frames() -> None:
    """At 120 BPM and 30 fps, beat_seconds is 0.5s and beat_frames is 15 frames."""
    grid = compute_beat_grid(bpm=120, time_signature="4/4", fps=30, duration_s=15, pattern="build_up")
    assert grid["beat_seconds"] == 0.5
    assert grid["beat_frames"] == 15.0
    assert grid["bar_seconds"] == 2.0
    assert grid["beats_s"][:4] == [0.0, 0.5, 1.0, 1.5]
    assert len(grid["cut_points_s"]) == len(grid["frame_indices"])


def test_positive_sports_commercial_15s_produces_commercial_promo_montage() -> None:
    """Positive 1: 15s sports commercial produces commercial_promo montage with beat_map, cut_pattern, and ramps."""
    bp = compile_blueprint(
        idea="إعلان سريع الإيقاع لمنتج رياضي احترافي /dollyin /ar 9:16",
        purpose="Commercials & TVCs",
        video_format="Live-Action",
        style_variant="Commercial Promo",
        dialogue="انطلق بأقصى سرعة وحقق هدفك اليوم.",
        total_runtime_seconds=15,
    )
    montage = bp["project"]["montage"]
    assert montage["style"] == "commercial_promo"
    assert isinstance(montage["beat_map"], dict)
    assert montage["beat_map"]["bpm"] > 0
    assert montage["cut_pattern"] in ("steady", "build_up", "call_response", "breathe")
    assert len(montage["ramps"]) >= 1
    errs, _ = validate_package_dict(bp)
    assert not errs, f"Sports commercial blueprint failed validation: {errs}"


def test_positive_music_video_links_cuts_to_song_structure() -> None:
    """Positive 2: Music video request links cuts and sections to song structure (verse, build, chorus_drop)."""
    bp = compile_blueprint(
        idea="فيديو كليب أغنية مصورة بإيقاع حماسي /orbit /ar 16:9",
        purpose="Entertainment Videos",
        video_format="Live-Action",
        style_variant="Music Videos",
        dialogue="نغني للحياة ونصنع الفرح في كل خطوة.",
        total_runtime_seconds=20,
    )
    montage = bp["project"]["montage"]
    assert montage["style"] == "music_video"
    section_names = [s["name"] for s in montage["beat_map"]["sections"]]
    assert any("verse" in n for n in section_names)
    assert any("chorus" in n or "drop" in n for n in section_names)
    errs, _ = validate_package_dict(bp)
    assert not errs


def test_positive_corporate_video_without_music_disables_rhythmic_montage() -> None:
    """Positive 3: Corporate video without music does not activate rhythmic montage (style == 'none')."""
    bp = compile_blueprint(
        idea="فيديو مؤسسي رسمي يستعرض قيم الشركة والتقرير السنوي",
        purpose="Corporate Videos",
        video_format="Live-Action",
        style_variant="Commercial Promo",
        dialogue="نلتزم بأعلى معايير الجودة والشفافية في خدمة عملائنا.",
        total_runtime_seconds=16,
    )
    montage = bp["project"]["montage"]
    assert montage["style"] == "none"
    assert montage["beat_map"] is None
    errs, _ = validate_package_dict(bp)
    assert not errs


def test_negative_cut_deviating_120ms_from_beat_is_rejected() -> None:
    """Negative 1: Cut deviating 120ms (> 40ms snap_tolerance_ms) from a beat is rejected (MQ1)."""
    grid = compute_beat_grid(bpm=120, time_signature="4/4", fps=30, duration_s=10, pattern="steady")
    bad_cuts = [0.0, 0.5, 1.12, 2.0]  # 1.12s is 120ms off the 1.0s beat
    ok, errs = validate_cuts_against_beats(bad_cuts, grid["beats_s"], snap_tolerance_ms=40.0)
    assert ok is False
    assert any("120.0ms" in e or "MQ1 violation" in e for e in errs)

    # Also verify via full validate_package_dict
    bp = compile_blueprint(
        idea="إعلان حركي /dollyin",
        purpose="Commercials & TVCs",
        video_format="Live-Action",
        style_variant="Commercial Promo",
        total_runtime_seconds=16,
    )
    bp_bad = copy.deepcopy(bp)
    bp_bad["project"]["montage"]["cut_points_s"] = [0.0, 1.12]
    pkg_errs, _ = validate_package_dict(bp_bad)
    assert any("MQ1 violation" in e for e in pkg_errs)


def test_negative_eight_ramps_in_single_clip_and_invalid_speed_rejected() -> None:
    """Negative 2: 8 speed ramps in a single clip (or speed outside 0.25x..4.0x) is rejected."""
    montage = build_project_montage("commercial_promo", duration_s=16.0, bpm=120.0)
    montage_8_ramps = copy.deepcopy(montage)
    montage_8_ramps["ramps"] = [
        {
            "clip_id": "1A",
            "start_s": float(i),
            "end_s": float(i + 0.8),
            "from_speed": 2.0,
            "to_speed": 0.5,
            "curve": "ease_in_out",
            "musical_reason": f"Beat hit {i}",
        }
        for i in range(8)
    ]
    errs, _ = validate_montage_section(montage_8_ramps, total_runtime_s=16.0)
    assert any("has 8 speed ramps" in e for e in errs)

    # Speed outside 0.25x..4.0x
    montage_bad_speed = copy.deepcopy(montage)
    montage_bad_speed["ramps"][0]["from_speed"] = 8.0
    errs_sp, _ = validate_montage_section(montage_bad_speed, total_runtime_s=16.0)
    assert any("outside allowed" in e for e in errs_sp)


def test_negative_cr2_sfx_density_and_missing_beat_map_rejected() -> None:
    """Negative 3: Missing beat_map when style != 'none' or excessive SFX (> 1 per 2 beats) is rejected."""
    errs_no_bm, _ = validate_montage_section({"style": "commercial_promo", "beat_map": None})
    assert any("beat_map is required" in e for e in errs_no_bm)

    montage = build_project_montage("short_form_edit", duration_s=10.0, bpm=120.0)
    # 10s at 120 BPM = 21 beats -> max 10 SFX cues. Inject 25 SFX cues:
    montage["sfx_cues"] = [
        {"t_s": round(i * 0.3, 2), "layer": "impact_hit", "name": f"hit_{i}", "pre_roll_ms": 0}
        for i in range(25)
    ]
    errs_sfx, _ = validate_montage_section(montage, total_runtime_s=10.0)
    assert any("CR2 violation" in e for e in errs_sfx)


def test_negative_beat_grid_invalid_inputs_raise_clear_errors() -> None:
    """Negative 4: beat_grid handles invalid/negative BPM, zero duration, bad time_signature, fps, and pattern."""
    with assert_raises(ValueError, match="Invalid BPM"):
        compute_beat_grid(bpm=-120, time_signature="4/4", fps=30, duration_s=15, pattern="steady")
    with assert_raises(ValueError, match="Invalid BPM"):
        compute_beat_grid(bpm=0, time_signature="4/4", fps=30, duration_s=15, pattern="steady")
    with assert_raises(ValueError, match="Invalid duration_s"):
        compute_beat_grid(bpm=120, time_signature="4/4", fps=30, duration_s=0, pattern="steady")
    with assert_raises(ValueError, match="Unsupported time_signature"):
        compute_beat_grid(bpm=120, time_signature="7/13", fps=30, duration_s=15, pattern="steady")
    with assert_raises(ValueError, match="Invalid fps"):
        compute_beat_grid(bpm=120, time_signature="4/4", fps=-30, duration_s=15, pattern="steady")
    with assert_raises(ValueError, match="Unsupported cut pattern"):
        compute_beat_grid(bpm=120, time_signature="4/4", fps=30, duration_s=15, pattern="random_chaos")

    # Non-standard positive FPS returns a warning without crashing
    grid_odd_fps = compute_beat_grid(bpm=120, time_signature="4/4", fps=48, duration_s=10, pattern="steady")
    assert any("Non-standard fps" in w for w in grid_odd_fps["warnings"])


def test_negative_runtime_45s_not_truncated_and_long_dialogue_split() -> None:
    """Negative 5: 45s runtime is never silently shortened to 17s; long dialogue is split, never truncated."""
    blocks_45 = partition_runtime_into_allowed_blocks(45)
    assert sum(blocks_45) >= 45

    long_ar = "هذا الحوار الإعلاني الطويل جدا مصمم لاختبار تقسيم الجمل الطويلة على عدة لقطات متتالية دون حذف أي كلمة"
    synced = optimize_arabic_lip_sync(long_ar, duration_seconds=4)
    for w in long_ar.split():
        assert w in synced
    assert "[SHOT_SPLIT]" in synced


def test_remotion_v4_arabic_zwj_splitter_and_video_first_layout() -> None:
    """Verify Remotion v4.0.539 split_arabic_letters_zwj (ZWJ + harakat + لا ligature + LTR runs) and video-layout.md rules."""
    # 1. RTL word-majority detection
    assert is_rtl_text("مَرْحَباً بِكُمْ في Remotion") is True
    assert is_rtl_text("Welcome to Remotion Studio 2026") is False

    # 2. ZWJ letter splitting preserves harakat, لا ligature, and LTR runs
    units = split_arabic_letters_zwj("سَلَامٌ2026")
    # 'سَ' joins left -> ends with ZWJ
    assert units[0] == "سَ\u200D"
    # 'لَا' ligature kept together, joins right (with س) -> starts with ZWJ, ends without ZWJ because ا is right-join-only
    assert units[1] == "\u200Dلَا"
    # 'مٌ' after ا does not join right, and is followed by non-Arabic '2026' so no ZWJ
    assert units[2] == "مٌ"
    # '2026' kept intact as single LTR run
    assert units[3] == "2026"

    # 3. Video-First Layout validation (Headline >= 84px, Supporting >= 44px, Margins >= 80/100, 1 focal point)
    ok_layout = validate_video_first_layout(headline_px=92, supporting_px=48, margin_x_px=80, margin_y_px=120, focal_points_per_scene=1)
    assert ok_layout["valid"] is True
    assert not ok_layout["errors"]

    bad_webpage_layout = validate_video_first_layout(headline_px=32, supporting_px=18, margin_x_px=24, margin_y_px=40, focal_points_per_scene=4)
    assert bad_webpage_layout["valid"] is False
    assert len(bad_webpage_layout["errors"]) == 5


def test_omni_flash_stateful_interactions_payload_builder() -> None:
    """Verify stateful Gemini Interactions API payload builder (store=True, aspect_ratio inheritance, 4MB URI upgrade)."""
    # 1. Initial generation sets aspect_ratio and store=True
    gen = build_omni_interaction_payload(
        task="generate_video",
        prompt="A tracking shot of a red fox running through fresh snow at golden hour",
        aspect_ratio="9:16",
        estimated_size_mb=2.5,
    )
    assert gen["store"] is True
    assert gen["response_format"] == {"type": "video", "aspect_ratio": "9:16"}

    # 2. Stateful edit chains previous_interaction_id, omits aspect_ratio, and upgrades >=4MB to delivery='uri'
    edit = build_omni_interaction_payload(
        task="edit_video",
        prompt="make it nighttime with heavy snowfall",
        previous_interaction_id="v1_Chdja1JpYXFyVkVkcWVq",
        aspect_ratio="9:16",
        estimated_size_mb=5.2,
    )
    assert edit["previous_interaction_id"] == "v1_Chdja1JpYXFyVkVkcWVq"
    assert "aspect_ratio" not in edit["response_format"]
    assert edit["response_format"]["delivery"] == "uri"

    # 3. Missing previous_interaction_id on edit_video is rejected
    with assert_raises(ValueError, match="previous_interaction_id"):
        build_omni_interaction_payload(task="edit_video", prompt="make it rain")


def test_b_studio_balanced_caption_cards() -> None:
    """Verify Rule 76 balanced 2-line word-reveal caption splitting with no orphan single-word cards."""
    words = [
        {"t": "هذا", "s": 0.0, "e": 0.3},
        {"t": "النظام", "s": 0.3, "e": 0.7},
        {"t": "الهندسي", "s": 0.7, "e": 1.1},
        {"t": "يحافظ", "s": 1.1, "e": 1.5},
        {"t": "على", "s": 1.5, "e": 1.7},
        {"t": "نقاء", "s": 1.7, "e": 2.1},
        {"t": "الصوت", "s": 2.1, "e": 2.5},
        {"t": "والصورة", "s": 2.5, "e": 3.0},
        {"t": "بالكامل", "s": 3.0, "e": 3.5},
    ]
    cards = split_caption_cards_balanced(words, max_chars_per_line=18, max_lines=2)
    assert len(cards) >= 2
    for card in cards:
        assert card["line_count"] <= 2
        assert card["pre_spoken_css"] == "visibility:hidden"
        assert card["has_orphan_word_card"] is False
        assert len(card["w"]) >= 2


def test_b_studio_sfx_governor() -> None:
    """Verify `05b_sfx_audit.py` 5-rule SFX governor (word lock, onset lead, >=1.0s spacing, spectral budget, density)."""
    word_ts = [1.0, 2.5, 4.2, 6.0, 8.5]
    clean_events = [
        {"name": "whoosh_soft", "time_s": 1.04, "category": "transition", "centroid_hz": 1400.0, "lead_s": 0.08, "measured_onset_s": 0.96},
        {"name": "paper_slide", "time_s": 2.48, "category": "semantic", "centroid_hz": 2100.0, "lead_s": 0.0, "measured_onset_s": 2.49},
        {"name": "stamp_hit", "time_s": 4.22, "category": "semantic", "centroid_hz": 1850.0, "lead_s": 0.05, "measured_onset_s": 4.18},
    ]
    ok_res = audit_sfx_governor(clean_events, word_timestamps=word_ts, duration_s=60.0)
    assert ok_res["valid"] is True
    assert not ok_res["violations"]

    bad_events = [
        {"name": "sharp_ding", "time_s": 1.0, "category": "semantic", "centroid_hz": 5200.0},
        {"name": "sharp_ding", "time_s": 1.4, "category": "semantic", "centroid_hz": 5200.0},  # < 1.0s gap & > 120ms from word 2.5
        {"name": "sharp_ding", "time_s": 2.5, "category": "semantic", "centroid_hz": 5200.0},  # 3rd >4kHz in 1 min (> 2.0/min)
        {"name": "sharp_ding", "time_s": 4.2, "category": "semantic", "centroid_hz": 5200.0},  # 4th repeat (> 3)
    ]
    bad_res = audit_sfx_governor(bad_events, word_timestamps=word_ts, duration_s=60.0)
    assert bad_res["valid"] is False
    assert any("Rule3_MinSpacing" in v for v in bad_res["violations"])
    assert any("Rule4_SpectralBudget" in v for v in bad_res["violations"])
    assert any("Rule55_SemanticRepeat" in v for v in bad_res["violations"])


def test_b_studio_window_schedule_and_face_guard() -> None:
    """Verify Rules 77-82 window schedule hold times, face return >= 2.5s, NONE cap, and fullFloor hair guard."""
    valid_stage = [
        {"m": "FULL", "s": 0.0, "e": 4.0},
        {"m": "CARD", "s": 4.0, "e": 8.5},
        {"m": "FULL", "s": 8.5, "e": 12.0},
        {"m": "SIDE", "s": 12.0, "e": 17.0},
        {"m": "NONE", "s": 17.0, "e": 21.0},
        {"m": "FULL", "s": 21.0, "e": 30.0},
    ]
    valid_boxes = [{"mode": "FULL", "top": 210, "height": 180}]  # 390 <= fullFloor (578 - 158 = 420)
    ok = validate_window_schedule_and_face_guard(valid_stage, duration_s=30.0, face_top_y=578, graphics_boxes=valid_boxes)
    assert ok["valid"] is True
    assert ok["full_floor_px"] == 420

    bad_stage = [
        {"m": "FULL", "s": 0.0, "e": 3.5},
        {"m": "CARD", "s": 3.5, "e": 4.8},   # < 2.0s window hold
        {"m": "FULL", "s": 4.8, "e": 7.0},   # 2.2s: >= 2.0s hold, but < 2.5s speaker return between graphics
        {"m": "NONE", "s": 7.0, "e": 9.5},
        {"m": "NONE", "s": 10.0, "e": 13.0},
        {"m": "NONE", "s": 14.0, "e": 17.0},  # 3rd NONE after hook (> 2 per 120s)
    ]
    bad_boxes = [{"mode": "FULL", "top": 260, "height": 220}]  # 480 > fullFloor (420)
    bad = validate_window_schedule_and_face_guard(bad_stage, duration_s=30.0, face_top_y=578, graphics_boxes=bad_boxes)
    assert bad["valid"] is False
    assert len(bad["violations"]) == 4


if __name__ == "__main__":
    test_funcs = [obj for name, obj in list(globals().items()) if name.startswith("test_") and callable(obj)]
    for fn in test_funcs:
        fn()
        print(f"PASS: {fn.__name__}")
    print(f"\nALL {len(test_funcs)} MONTAGE TEST SUITES PASSED SUCCESSFULLY!")
