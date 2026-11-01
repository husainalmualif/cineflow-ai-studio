#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comprehensive Unit, Negative, Schema & Interoperability Tests for CineFlow AI Studio.

Compatible with both `pytest -v tests/test_cineflow_compiler.py` and direct CLI execution:
`python tests/test_cineflow_compiler.py`.
"""

from __future__ import annotations

import contextlib
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterator, Optional, Type

try:
    import pytest  # type: ignore
except ImportError:  # pragma: no cover
    pytest = None  # type: ignore

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from cineflow_compiler import (  # noqa: E402
    apply_safe_arabic_kashida,
    check_scene_variation,
    compile_blueprint,
    compile_cineflow_blueprint,
    detect_arabic_dialect,
    generate_keyword_variants,
    optimize_arabic_lip_sync,
    partition_runtime_into_allowed_blocks,
    resolve_slash_macros,
    score_providers,
    score_slideshow_risk,
    validate_delivery_promise,
    validate_taxonomy_inputs,
)
from estimate_cost import estimate_package_cost  # noqa: E402
from make_srt import build_srt_string, extract_validated_cues  # noqa: E402
from multi_agent_orchestrator import (  # noqa: E402
    SEVEN_AGENT_REGISTRY,
    SHOWRUNNER_13_ROLES,
    build_execution_plan,
    compute_vocalized_letter_ratio,
    validate_arabic_phonetics,
)
from studio_config import (  # noqa: E402
    HARD_ALLOWED_CLIP_DURATIONS,
    MACRO_DICTIONARY,
    MIN_DIACRITIC_RATIO,
)
from validate_package import (  # noqa: E402
    convert_scene_breakdown_to_package,
    validate_package_dict,
)


@contextlib.contextmanager
def assert_raises(exc_type: Type[BaseException], match: Optional[str] = None) -> Iterator[None]:
    """Portable replacement for pytest.raises supporting optional regex match."""
    try:
        yield
    except exc_type as exc:
        if match and not re.search(match, str(exc)):
            raise AssertionError(f"Exception '{exc}' did not match pattern '{match}'") from exc
        return
    raise AssertionError(f"Expected {exc_type.__name__} to be raised, but no exception was raised.")


def test_c1_compiler_to_validator_cost_srt_interoperability() -> None:
    """Fixes C1: Output of compile_blueprint passes validate_package, estimate_cost, and make_srt directly."""
    bp = compile_blueprint(
        idea="إعلان قهوة مختصة فاخرة /anamorphic /dollyin /ar 9:16",
        purpose="Commercials & TVCs",
        video_format="Live-Action",
        style_variant="Commercial Promo",
        dialogue="هلا والله، تبي الصدق؟ قهوة المجلس تجمع الأصالة والفخامة في كل فنجان.",
        total_runtime_seconds=20,
    )
    errs, _ = validate_package_dict(bp)
    assert errs == [], f"Compiler output failed validate_package_dict: {errs}"

    cost = estimate_package_cost(bp, credits_per_generation=10.0, expected_rerolls_per_block=1.0)
    assert cost["blocks"] == 3
    assert cost["base_blocks"] == 1
    assert cost["extend_blocks"] == 2
    assert cost["stage1_reference_credits"] == 0.0
    assert cost["expected"] == 60.0

    cues = extract_validated_cues(bp)
    assert len(cues) >= 1
    srt_text = build_srt_string(bp)
    assert "-->" in srt_text
    assert "قهوة" in srt_text


def test_c1_legacy_scene_breakdown_auto_conversion() -> None:
    """Legacy scene_breakdown-only payloads convert cleanly and pass validation."""
    bp = compile_blueprint(
        idea="Legacy Blueprint Test /dollyin",
        purpose="Explainer Videos",
        video_format="Motion Graphics",
        style_variant="Commercial Promo",
        dialogue="ابدأ رحلتك اليوم واصنع مستقبلك بيدك الآن.",
        total_runtime_seconds=16,
    )
    legacy_only: dict[str, Any] = {
        "production_profile": bp["production_profile"],
        "global_parameters": bp["global_parameters"],
        "scene_breakdown": bp["scene_breakdown"],
        "outro_standardization": bp["outro_standardization"],
    }
    converted = convert_scene_breakdown_to_package(legacy_only)
    assert "blocks" in converted
    assert "project" in converted
    errs, _ = validate_package_dict(legacy_only)
    assert errs == []


def test_c2_slideshow_risk_and_scene_variation_reject_bad_inputs() -> None:
    """Fixes C2: 6 identical scenes or static-image scenes fail slideshow & variation checks."""
    identical_scenes = [
        {
            "scene_id": i,
            "duration_seconds": 6,
            "layout_mode": "R_FULL",
            "type": "static_image",
            "motion_type": "static_image",
            "hero_moment": False,
            "shot_language": {"shot_size": "medium_shot", "camera_movement": "static"},
            "visual_prompt": "Montage of stunning visuals in a futuristic digital network",
            "texture_keywords": [],
        }
        for i in range(1, 7)
    ]
    risk = score_slideshow_risk(identical_scenes)
    var = check_scene_variation(identical_scenes)
    promise = validate_delivery_promise(identical_scenes, promise_type="motion_led", motion_required=True)

    assert risk["verdict"] == "fail"
    assert risk["total_score"] >= 3.8
    assert var["verdict"] == "fail"
    assert len(var["violations"]) >= 3
    assert promise["valid"] is False


def test_c3_provider_scoring_selects_different_winners_by_context() -> None:
    """Fixes C3: Provider selector dynamically chooses distinct optimal engines per task/budget."""
    p_comm = score_providers("Commercials & TVCs", "Live-Action", "Commercial Promo", "standard")
    p_doc = score_providers("Documentaries", "Live-Action", "Montage Sequence", "standard")
    p_anim = score_providers("Explainer Videos", "Animation (2D / 3D)", "Commercial Promo", "standard")
    p_motion = score_providers("Explainer Videos", "Motion Graphics", "Commercial Promo", "standard")
    p_music = score_providers("Entertainment Videos", "Live-Action", "Music Videos", "standard")
    p_draft = score_providers("Commercials & TVCs", "Live-Action", "Commercial Promo", "draft")

    assert p_comm["selected_primary"] == "google_flow_veo_3_1"
    assert p_doc["selected_primary"] == "clip_archival_remotion_hybrid"
    assert p_anim["selected_primary"] == "ink_theater_cmu_mocap"
    assert p_motion["selected_primary"] == "hyperframes_remotion_60fps"
    assert p_music["selected_primary"] == "seedance_2_0"
    assert p_draft["selected_primary"] == "gemini_omni_flash_1_1"


def test_h1_h3_runtime_partitioning_and_extend_chain_cap() -> None:
    """Fixes H1 & H3: Runtimes (15, 20, 45, 90s) partition strictly into {4, 6, 8, 10}s with <= 40s chains."""
    for target in (15, 20, 45, 90):
        blocks = partition_runtime_into_allowed_blocks(target)
        assert all(b in HARD_ALLOWED_CLIP_DURATIONS for b in blocks)
        assert abs(sum(blocks) - target) <= 2

    with assert_raises(ValueError):
        partition_runtime_into_allowed_blocks(0)
    with assert_raises(ValueError):
        partition_runtime_into_allowed_blocks(-10)
    with assert_raises(ValueError):
        partition_runtime_into_allowed_blocks(999)

    bp_90 = compile_blueprint(
        idea="وثائقي طويل /dollyin",
        purpose="Documentaries",
        video_format="Live-Action",
        style_variant="Montage Sequence",
        dialogue="تاريخ طويل من الإبداع والتميز في صناعة المحتوى المرئي الحديث.",
        total_runtime_seconds=90,
    )
    errs, _ = validate_package_dict(bp_90)
    assert errs == [], f"90s blueprint failed Extend chain cap validation: {errs}"
    ingredients_blocks = [b for b in bp_90["blocks"] if b["mode"] == "Ingredients"]
    assert len(ingredients_blocks) >= 3  # 90s requires at least 3 chains of <= 40s


def test_h2_taxonomy_validation_rejects_unknown_inputs() -> None:
    """Fixes H2: Unknown purpose, video_format, or style_variant raises ValueError."""
    with assert_raises(ValueError, match="Unsupported purpose"):
        validate_taxonomy_inputs("Invalid Purpose", "Live-Action", "Commercial Promo")
    with assert_raises(ValueError, match="Unsupported video_format"):
        validate_taxonomy_inputs("Commercials & TVCs", "Hologram Telepathy", "Commercial Promo")
    with assert_raises(ValueError, match="Unsupported style_variant"):
        validate_taxonomy_inputs("Commercials & TVCs", "Live-Action", "Random TikTok Filter")


def test_h4_lip_sync_preserves_all_words_and_rejects_nonpositive_duration() -> None:
    """Fixes H4: optimize_arabic_lip_sync never drops words and rejects duration <= 0."""
    with assert_raises(ValueError):
        optimize_arabic_lip_sync("مرحبا بكم", 0)
    with assert_raises(ValueError):
        optimize_arabic_lip_sync("مرحبا بكم", -5)

    long_line = "هذا النص الطويل يحتوي على كلمات كثيرة جدا لاختبار عدم حذف أي كلمة أثناء تقسيم المشاهد الصوتية"
    result = optimize_arabic_lip_sync(long_line, 6)
    for word in long_line.split():
        assert word in result, f"Word '{word}' was dropped from lip-sync output!"
    assert "[SHOT_SPLIT]" in result


def test_h5_h6_vocalized_letter_ratio_and_clause_final_taa_marbuta() -> None:
    """Fixes H5 & H6: Ratio counts vocalized base letters in [0, 1] and checks mid-sentence pause ة."""
    assert MIN_DIACRITIC_RATIO == 0.75
    text_good = "قَهْوَهْ مُخْتَصَّهْ ، تَبْدَأُ مِنْ أَوَّلِ قَطْرَهْ."
    ratio = compute_vocalized_letter_ratio(text_good)
    assert 0.75 <= ratio <= 1.0
    res_good = validate_arabic_phonetics(text_good)
    assert res_good["passed"] is True

    text_mid_taa = "قَهْوَةٌ مُخْتَصَّةٌ ، تَبْدَأُ مِنْ أَوَّلِ قَطْرَهْ."
    res_bad = validate_arabic_phonetics(text_mid_taa)
    assert res_bad["passed"] is False
    assert any("تاء مربوطة" in issue for issue in res_bad["issues"])


def test_medium_validator_gaps_all_10_negative_cases() -> None:
    """Tests all 10 medium_validator_gaps reported in the engineering audit."""
    errs_list, _ = validate_package_dict(["not", "a", "dict"])
    assert any("top-level JSON must be an object/dict" in e for e in errs_list)

    base = json.loads(
        (ROOT_DIR / "examples" / "example_03_showrunner_package.json").read_text(encoding="utf-8")
    )
    errs_clean, _ = validate_package_dict(base)
    assert errs_clean == []

    bad_caps = copy.deepcopy(base)
    bad_caps["project"]["verified_capabilities"]["per_clip_s_options"] = [60]
    errs, _ = validate_package_dict(bad_caps)
    assert any("hard ceiling" in e for e in errs)

    bad_dur = copy.deepcopy(base)
    bad_dur["blocks"][0]["duration_s"] = "10"
    errs, _ = validate_package_dict(bad_dur)
    assert any("duration_s must be a number" in e for e in errs)

    dup_ids = copy.deepcopy(base)
    dup_ids["blocks"][1]["block_id"] = 1
    dup_ids["blocks"][1]["shots"][0]["shot_id"] = "1A"
    errs, _ = validate_package_dict(dup_ids)
    assert any("duplicate block_id" in e for e in errs)
    assert any("duplicate shot_id" in e for e in errs)

    bad_ext = copy.deepcopy(base)
    bad_ext["blocks"][1]["extend_from_block"] = 99
    errs, _ = validate_package_dict(bad_ext)
    assert any("extend_from_block" in e for e in errs)

    bad_ref = copy.deepcopy(base)
    bad_ref["blocks"][0]["shots"][0]["visual_prompt_en"] += " alongside [CHAR_09]"
    errs, _ = validate_package_dict(bad_ref)
    assert any("CHAR_09" in e for e in errs)

    bad_trange = copy.deepcopy(base)
    bad_trange["blocks"][0]["shots"][0]["t_range"] = "0-25"
    errs, _ = validate_package_dict(bad_trange)
    assert any("t_range" in e for e in errs)

    bad_ov = copy.deepcopy(base)
    bad_ov["overlays"][0]["start_s"] = 15.0
    bad_ov["overlays"][0]["end_s"] = 10.0
    errs, _ = validate_package_dict(bad_ov)
    assert any("overlay #1: invalid timing" in e for e in errs)

    bad_align = copy.deepcopy(base)
    bad_align["blocks"][0]["shots"][0]["dialogue_tts_ar"] = (
        "نَكْهَهْ الصَّبَاحِ تَبْدَأُ مِنْ أَوَّلِ قَطْرَهْ فِي كُلِّ يَوْمٍ جَدِيدٍ وَمُمَيَّزْ."
    )
    errs, _ = validate_package_dict(bad_align)
    assert any("word count" in e or "exceeds" in e for e in errs)


def test_fragile_tools_estimate_cost_and_make_srt_validation() -> None:
    """Tests negative input guards on estimate_cost.py and make_srt.py."""
    base = json.loads(
        (ROOT_DIR / "examples" / "example_03_showrunner_package.json").read_text(encoding="utf-8")
    )
    with assert_raises(ValueError, match="credits_per_generation must be > 0"):
        estimate_package_cost(base, credits_per_generation=0, expected_rerolls_per_block=1)
    with assert_raises(ValueError, match="expected_rerolls_per_block must be >= 0"):
        estimate_package_cost(base, credits_per_generation=10, expected_rerolls_per_block=-1)

    cost_high = estimate_package_cost(base, credits_per_generation=10, expected_rerolls_per_block=3.0)
    assert cost_high["worst_case"] > cost_high["expected"]

    no_dlg = {"blocks": [], "overlays": [{"start_s": 8.0, "end_s": 3.0, "text_ar": "نص تجريبي"}]}
    with assert_raises(ValueError, match="invalid timing"):
        extract_validated_cues(no_dlg)


def test_dialect_kashida_macros_and_keyword_variants() -> None:
    """Tests dialect detection (9 dialects + UNKNOWN), sacred Kashida protection, and 190+ macros."""
    assert detect_arabic_dialect("Build the future with AI today") == "UNKNOWN (غير معروف)"
    assert detect_arabic_dialect("") == "UNKNOWN (غير معروف)"
    assert "BAHRAINI" in detect_arabic_dialect("هلا بوي شخبارك يبه في المنامة")
    assert "IRAQI" in detect_arabic_dialect("شلونك عيني شكو ماكو في بغداد")
    assert "EGYPTIAN" in detect_arabic_dialect("ازيك يا باشا عامل ايه النهارده")
    assert "LEVANTINE" in detect_arabic_dialect("شو أخبارك هلق يا زلمة")

    for sacred in ("الله", "لله", "اللهم", "بسم", "الرحمن", "الرحيم", "محمد", "لا"):
        assert apply_safe_arabic_kashida(sacred, count=3) == sacred

    variants = generate_keyword_variants("مؤسسة")
    assert "موسسة" in variants
    assert "مؤسسه" in variants

    assert len(MACRO_DICTIONARY) >= 185
    resolved = resolve_slash_macros("/anamorphic /dollyin /goldenhour")
    assert len(resolved) == 3


def test_orchestrator_7_agents_and_13_showrunner_roles() -> None:
    """Verifies alignment between the 7 platform agents and 13 Showrunner roles."""
    assert len(SEVEN_AGENT_REGISTRY) == 7
    assert len(SHOWRUNNER_13_ROLES) == 13
    plan = build_execution_plan("Test Project", "route_3_motion_stage_60fps", 20.0)
    assert len(plan["agents"]) == 7
    assert len(plan["showrunner_roles"]) == 13


def test_jsonschema_and_evals_suite() -> None:
    """Validates compiled blueprints against resources/blueprint_schema.json and checks evals.json."""
    schema = json.loads((ROOT_DIR / "resources" / "blueprint_schema.json").read_text(encoding="utf-8"))
    bp = compile_cineflow_blueprint(
        title="Schema Validation Test",
        purpose="Commercials & TVCs",
        video_format="Live-Action",
        style_variant="Commercial Promo",
        aspect_ratio="9:16",
        total_runtime_seconds=20,
    )
    for req_key in schema["required"]:
        assert req_key in bp, f"Missing required schema key: {req_key}"

    try:
        import jsonschema  # type: ignore

        jsonschema.validate(instance=bp, schema=schema)
        for ex_name in ("example_01_commercial_promo.json", "example_02_explainer_and_story_script.json"):
            ex_data = json.loads((ROOT_DIR / "examples" / ex_name).read_text(encoding="utf-8"))
            jsonschema.validate(instance=ex_data, schema=schema)
    except ImportError:
        pass

    evals = json.loads((ROOT_DIR / "resources" / "evals.json").read_text(encoding="utf-8"))
    assert len(evals["cases"]) >= 20
    pos = [c for c in evals["cases"] if c["category"] == "positive_trigger"]
    neg = [c for c in evals["cases"] if c["category"] == "negative_non_trigger"]
    edge = [c for c in evals["cases"] if c["category"] == "edge_case"]
    assert len(pos) >= 12
    assert len(neg) >= 4
    assert len(edge) >= 4


if __name__ == "__main__":
    test_funcs = [obj for name, obj in list(globals().items()) if name.startswith("test_") and callable(obj)]
    for fn in test_funcs:
        fn()
        print(f"PASS: {fn.__name__}")
    print(f"\nALL {len(test_funcs)} TEST SUITES PASSED SUCCESSFULLY!")
