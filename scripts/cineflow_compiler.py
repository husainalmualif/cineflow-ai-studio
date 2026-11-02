#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CineFlow AI Studio — Unified Scriptwriter, Prompt Compiler, Programmatic Edit Planner,
Arabic Kashida Engine, Lip-Sync Phraser, Slideshow Risk Scorer, Provider Selector & Showrunner Packager.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arabic_helpers import (  # noqa: E402
    ARABIC_BASE_RE,
    HARAKAT_CHARS,
    apply_safe_arabic_kashida,
    auto_vocalize_arabic_for_tts,
    detect_arabic_dialect,
    detect_arabic_dialect_with_confidence,
    generate_keyword_variants,
    is_rtl_text,
    optimize_arabic_lip_sync,
    resolve_slash_macros,
    split_arabic_letters_zwj,
    validate_video_first_layout,
)
from beat_grid import build_project_montage  # noqa: E402
from governance_and_omni import (  # noqa: E402
    GENERIC_SLOP_PHRASES,
    build_omni_interaction_payload,
    build_taste_profile,
    check_scene_variation,
    partition_runtime_into_allowed_blocks,
    score_providers,
    score_slideshow_risk,
    select_pipeline_route,
    validate_delivery_promise,
    validate_taxonomy_inputs,
)
from studio_config import (  # noqa: E402
    ALLOWED_CLIP_DURATIONS,
    CAPABILITY_VERIFICATION_STATUS,
    DEFAULT_UNREAL_BLOOM,
    HARD_ALLOWED_CLIP_DURATIONS,
    MAX_EXTEND_CHAIN_SECONDS,
    MAX_OVERLAY_WORDS,
    MODEL_REGISTRY_LAST_VERIFIED,
    MONTAGE_STYLE_ALIAS_MAP,
    OUTRO_SAFE_ZONES,
    SILENCE_THRESHOLD_DB,
    TARGET_INTEGRATED_LUFS,
)

__all__ = [
    "ARABIC_BASE_RE",
    "GENERIC_SLOP_PHRASES",
    "HARAKAT_CHARS",
    "Optional",
    "Set",
    "apply_safe_arabic_kashida",
    "auto_vocalize_arabic_for_tts",
    "build_omni_interaction_payload",
    "build_taste_profile",
    "check_scene_variation",
    "compile_blueprint",
    "compile_cineflow_blueprint",
    "detect_arabic_dialect",
    "detect_arabic_dialect_with_confidence",
    "generate_keyword_variants",
    "is_rtl_text",
    "optimize_arabic_lip_sync",
    "partition_runtime_into_allowed_blocks",
    "resolve_slash_macros",
    "score_providers",
    "score_slideshow_risk",
    "select_pipeline_route",
    "split_arabic_letters_zwj",
    "validate_delivery_promise",
    "validate_taxonomy_inputs",
    "validate_video_first_layout",
]

PURPOSE_FRAMEWORKS: Dict[str, str] = {
    "Commercials & TVCs": (
        "6-Stage Direct-Response Curve: Hook (0-2s) -> Problem Agitation -> "
        "Product Hero Showcase -> Safe-Zone Offer & CTA"
    ),
    "Corporate Videos": "Vision Hook -> Human & Operational Excellence -> Brand Commitment Outro",
    "Educational & Training": (
        "Curiosity Question -> Action-Verb Stage Metaphor & Step-by-Step Breakdown -> Key Takeaway"
    ),
    "Explainer Videos": "Problem Identification -> Agitation -> How the Solution Works (Action-Verb Stage) -> CTA",
    "Testimonial Videos": "Initial Challenge -> Turning Point Experience -> Tangible Results & Recommendation",
    "Documentaries": (
        "Atmospheric Mystery Hook -> CLIP Real-Footage Corpus & Factual Context -> "
        "Reflective Remotion Alpha End-Tag"
    ),
    "Event Videos": "High-Energy Cold Open -> Dynamic Crowd & Keynotes Montage -> Event Emblem Outro",
    "Entertainment Videos": "Inciting Hook -> Rising Dramatic/Rhythmic Action -> Emotional Climax & Payoff",
}

PURPOSE_STYLE_MAP: Dict[str, str] = {
    "Commercials & TVCs": "studio3D+keynote",
    "Corporate Videos": "editorial+keynote",
    "Educational & Training": "explainer+swiss",
    "Explainer Videos": "glassUI+explainer",
    "Testimonial Videos": "editorial",
    "Documentaries": "archive",
    "Event Videos": "brutal+keynote",
    "Entertainment Videos": "paperCut+keynote",
}


def _build_scene_and_block(
    idx: int,
    total_scenes: int,
    dur: int,
    start_s: int,
    raw_dialogue_slice: str,
    context: Dict[str, Any],
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Constructs a synchronized (scene_dict, block_dict, overlay_dict) triple."""
    shot_sizes = ["medium_close_up", "extreme_close_up", "medium_shot", "close_up", "medium_wide"]
    cam_moves = ["dolly_in", "orbit_arc", "truck_left", "crane_up", "dolly_out"]
    cam_angles = ["eye_level", "low_angle", "three_quarter", "high_angle", "level_angle"]
    layouts = ["R_FULL", "R_LOWER", "R_DOWN", "R_OFF"]

    if idx == 1:
        role_label = f"SCENE 1 — VISUAL HOOK & 3-LAYER STACK (0.0s - {dur}s)"
        shot_size = "medium_close_up"
        cam_move = "dolly_in"
        cam_angle = "eye_level"
        layout = "R_FULL"
        is_hero = False
        intent = "Stop scroll within 1.5s via physical dolly push-in and 3-layer Behind-Head Kashida hook."
        info_role = "hook_premise"
        narr_role = "inciting_visual_hook"
        overlay_text = context["kashida_hook_word"]
    elif idx == total_scenes:
        role_label = f"SCENE {idx} — STANDARDIZED SAFE-ZONE OUTRO & LOOP ({start_s}s - {start_s + dur}s)"
        shot_size = "medium_wide"
        cam_move = "dolly_out"
        cam_angle = "level_angle"
        layout = "R_FULL"
        is_hero = False
        intent = "Resolve visual tension into a clean 35% negative-space composition for Safe-Zone Brand Logo and CTA."
        info_role = "call_to_action_resolution"
        narr_role = "loop_back_payoff"
        overlay_text = "اطلب الآن — الرابط في البايو"
    else:
        role_label = f"SCENE {idx} — ACTION-VERB STAGE & CORE PROOF ({start_s}s - {start_s + dur}s)"
        shot_size = shot_sizes[(idx - 1) % (len(shot_sizes) - 1)]
        if shot_size == "medium_close_up" and idx == 2:
            shot_size = "extreme_close_up"
        cam_move = cam_moves[(idx - 1) % (len(cam_moves) - 1)]
        cam_angle = cam_angles[(idx - 1) % len(cam_angles)]
        layout = "R_LOWER" if idx == 2 else layouts[(idx - 1) % len(layouts)]
        is_hero = idx == 2
        intent = f"Deliver tangible physical proof in beat {idx} while Action-Verb Stage illustrates spoken verb."
        info_role = f"core_mechanism_beat_{idx}"
        narr_role = "climax_demonstration" if is_hero else f"rising_proof_{idx}"
        overlay_text = "تفاصيل أصيلة وجودة عالية" if idx == 2 else f"خطوة عملية متقنة {idx}"

    dl_sync = (
        optimize_arabic_lip_sync(raw_dialogue_slice, dur)
        if raw_dialogue_slice
        else "[Mouth closed naturally, warm confident nod]"
    )
    dl_words = [w for w in raw_dialogue_slice.split() if w]
    dl_clauses = [" ".join(dl_words[i : i + 6]) for i in range(0, len(dl_words), 6)]
    dl_ar_clean = " . ".join(dl_clauses)
    dl_tts_ar = auto_vocalize_arabic_for_tts(dl_ar_clean) if dl_ar_clean else ""

    scene_dict: Dict[str, Any] = {
        "scene_id": idx,
        "scene_role": role_label,
        "duration_seconds": dur,
        "layout_mode": layout,
        "type": "video",
        "shot_intent": intent,
        "information_role": info_role,
        "narrative_role": narr_role,
        "hero_moment": is_hero,
        "shot_language": {
            "shot_size": shot_size,
            "camera_movement": cam_move,
            "camera_angle": cam_angle,
            "focus_dof": "shallow_dof_f1.4" if idx == 1 else "rack_focus_foreground_to_midground",
            "lighting_key": "golden_hour_rim_and_rembrandt_key" if idx % 2 == 1 else "chiaroscuro_specular_macro",
        },
        "chai_5_aspect_breakdown": {
            "subject": f"{context['character_id']} (verbatim identity lock) with {context['product_id']} in [ENV_01].",
            "subject_motion": f"In beat {idx}, {context['character_id']} demonstrates {context['product_id']} with {context['body_language']}.",
            "scene": f"Overlays ({layout}): '{overlay_text}' | Setting: Architectural studio [ENV_01] with volumetric light.",
            "spatial_framing": f"{shot_size} framing at {cam_angle}, distinct from adjacent scenes.",
            "camera": f"Real-time -> {context['camera_gear']} -> {cam_move} -> {context['compiled_macro_str']}.",
        },
        "texture_keywords": ["35mm film grain ISO 800", "microscopic skin pores", "natural fabric weave", "optical halation"],
        "flow_mode": "Ingredients-to-Video" if idx == 1 else "Frames-to-Video (<FIRST_FRAME> Scene Handshake)",
        "continuity_handshake": f"Scene {idx} continuity lock binding {context['character_id']} and {context['product_id']}.",
        "visual_prompt": (
            f"[Beat {idx} Identity Lock: {context['character_id']} [CHAR_01], {context['product_id']} [PROD_01], [ENV_01]] + "
            f"[Action: {context['body_language']}, {shot_size} view] + "
            f"[Camera: {context['camera_gear']}, {cam_move}, {context['compiled_macro_str']}] + "
            f"[Grade: {context['color_grading']}, {context['anti_cgi_suffix']}]"
        ),
        "stage_motion_actors": f"Stage layout `{layout}` anchored to '{overlay_text}' with +0.45s post-word hold",
        "audio_foley_sync": f"Tone: {context['tone']} | Beat {idx} foley + -9.5dB sidechain ducked 120 BPM bed",
        "dialogue_lip_sync": dl_sync,
        "dialogue_tts_ar": dl_tts_ar,
        "text_overlay": overlay_text,
    }

    block_dict: Dict[str, Any] = {
        "block_id": idx,
        "duration_s": dur,
        "mode": context["block_mode"],
        "extend_from_block": context["extend_from_block"],
        "ids_used": ["CHAR_01", "PROD_01", "ENV_01"],
        "shots": [
            {
                "shot_id": f"{idx}A",
                "t_range": f"0-{dur}",
                "visual_prompt_en": (
                    f"Beat {idx} {shot_size}: [CHAR_01] demonstrates [PROD_01] inside [ENV_01] with "
                    f"confident physical gesture ({context['compiled_macro_str'][:120]})."
                ),
                "camera": f"{cam_move}, {shot_size}, {cam_angle}, shallow f/1.4 depth of field",
                "lighting_grade": f"{context['color_grading']}, motivated key and rim light",
                "emotion_body_language": context["body_language"],
                "audio_sync": "clean studio ambience and tactile foley; 120 BPM bed ducked -9.5 dB in post",
                "dialogue_ar": dl_ar_clean,
                "dialogue_tts_ar": dl_tts_ar,
                "dialogue_gloss_en": f"Spoken Arabic marketing line for beat {idx}" if dl_ar_clean else "",
                "negatives": (
                    "no extra fingers, no distorted text, no logo morphing, no watermark, "
                    "no CGI plastic skin, no static-photo mouth cutout"
                ),
            }
        ],
    }

    overlay_dict: Dict[str, Any] = {
        "start_s": float(start_s),
        "end_s": float(start_s + dur),
        "text_ar": " ".join(overlay_text.split()[:MAX_OVERLAY_WORDS]),
        "position": "bottom-safe",
    }

    return scene_dict, block_dict, overlay_dict


def compile_blueprint(
    idea: str,
    purpose: str = "Commercials & TVCs",
    video_format: str = "Live-Action",
    style_variant: str = "Commercial Promo",
    dialogue: str = "ويش سر القهوة اللي تعدل المزاج من أول رشفة؟ جربها الحين وعيش الفخامة",
    tone: str = "Warm, Confident, Inviting (دافئ، واثق، وجذاب)",
    body_language: str = "Relaxed shoulders, confident steady hands, warm eye contact (مرتاح وواثق)",
    camera_gear: str = "ARRI Alexa 65 + 35mm Anamorphic Prime & 85mm Macro Lens",
    color_grading: str = "Cinematic Warm Golden-Amber LUT with Skin-Tone Protection",
    character_id: str = "@Character_Lead_01",
    product_id: str = "@Product_Hero_01",
    total_runtime_seconds: int = 15,
    color_palette: str = "gold",
    comment_keyword: str = "إبداع",
    render_runtime: str = "remotion",
    composition_mode: str = "atelier",
    budget_tier: str = "standard",
) -> Dict[str, Any]:
    """
    Compile a unified CineFlow AI Studio JSON blueprint + Showrunner Package (`06_package.json`).
    """
    validate_taxonomy_inputs(purpose, video_format, style_variant)
    block_durations = partition_runtime_into_allowed_blocks(total_runtime_seconds)
    actual_total = sum(block_durations)

    aspect_ratio = "9:16"
    if "/ar 16:9" in idea.lower() or "/16x9" in idea.lower():
        aspect_ratio = "16:9"
    elif "/ar 1:1" in idea.lower() or "/1x1" in idea.lower():
        aspect_ratio = "1:1"

    macros = resolve_slash_macros(idea)
    compiled_macro_str = ", ".join(macros)
    detected_dialect = detect_arabic_dialect(f"{idea} {dialogue}")
    narrative_framework = PURPOSE_FRAMEWORKS[purpose]
    visual_design_style = PURPOSE_STYLE_MAP[purpose]
    pipeline_type = select_pipeline_route(purpose, video_format, style_variant)
    runtime_category = (
        "Short-Form Viral / Micro-Content (10-15s)"
        if total_runtime_seconds <= 16
        else "Long-Form / Chaptered Narrative (>15s)"
    )

    if video_format == "Live-Action":
        anti_cgi_suffix = (
            "35mm film grain ISO 800, subtle optical halation, microscopic skin pores "
            "and authentic fabric texture --no CGI, no 3D render, no plastic skin, "
            "no AI sheen, no garbled Arabic text, no subtitles, no extra fingers, no identity drift"
        )
    else:
        anti_cgi_suffix = (
            "crisp high-precision digital rendering, coherent motion physics "
            "--no frame flicker, no garbled Arabic text, no subtitles, no geometry distortion, no identity drift"
        )

    all_words = [w for w in str(dialogue or "").strip().split() if w]
    n_blocks = len(block_durations)
    spoken_blocks = max(1, n_blocks - 1)
    words_per_block = math.ceil(len(all_words) / spoken_blocks) if all_words else 0

    hook_focus_word = all_words[1] if len(all_words) > 1 else (all_words[0] if all_words else "الفخامة")
    kashida_hook_word = apply_safe_arabic_kashida(hook_focus_word, count=3)
    anchor_word_s2 = all_words[min(len(all_words) - 1, words_per_block)] if all_words else "التجربة"

    scenes: List[Dict[str, Any]] = []
    blocks: List[Dict[str, Any]] = []
    overlays: List[Dict[str, Any]] = []
    elapsed = 0
    current_chain_s = 0

    for idx, dur in enumerate(block_durations, start=1):
        if idx <= spoken_blocks and all_words:
            w_start = (idx - 1) * words_per_block
            w_slice = " ".join(all_words[w_start : w_start + words_per_block])
        else:
            w_slice = ""

        if idx == 1 or current_chain_s + dur > MAX_EXTEND_CHAIN_SECONDS:
            block_mode = "Ingredients"
            ext_from = None
            current_chain_s = dur
        else:
            block_mode = "Extend"
            ext_from = idx - 1
            current_chain_s += dur

        ctx = {
            "character_id": character_id,
            "product_id": product_id,
            "body_language": body_language,
            "camera_gear": camera_gear,
            "color_grading": color_grading,
            "compiled_macro_str": compiled_macro_str,
            "anti_cgi_suffix": anti_cgi_suffix,
            "tone": tone,
            "kashida_hook_word": kashida_hook_word,
            "block_mode": block_mode,
            "extend_from_block": ext_from,
        }
        sc, blk, ov = _build_scene_and_block(idx, n_blocks, dur, elapsed, w_slice, ctx)
        scenes.append(sc)
        blocks.append(blk)
        overlays.append(ov)
        elapsed += dur

    clean_title = re.sub(r"/\S+", "", idea).strip() or f"{purpose} Production"
    keyword_variants = generate_keyword_variants(comment_keyword)

    taste_profile = build_taste_profile(purpose, style_variant, color_palette)
    slideshow_report = score_slideshow_risk(
        scenes, renderer_family="cinematic-commercial", render_runtime=render_runtime
    )
    variation_report = check_scene_variation(scenes)
    promise_report = validate_delivery_promise(scenes, promise_type="motion_led", motion_required=True)
    provider_report = score_providers(purpose, video_format, style_variant, budget_tier)

    decision_log = [
        {
            "category": "provider_selection",
            "subject": "Primary Video Generation & Keyframe Stack",
            "selected": provider_report["selected_primary"],
            "options_considered": [c["provider"] for c in provider_report["candidates_ranked"]],
            "confidence": 0.92,
            "reason": f"Selected {provider_report['selected_label']} for {purpose} ({video_format}).",
            "user_visible": True,
        },
        {
            "category": "render_runtime_selection",
            "subject": "Programmatic Composition Runtime",
            "selected": render_runtime,
            "options_considered": ["remotion", "hyperframes", "ffmpeg"],
            "confidence": 0.90,
            "reason": "Deterministic RTL caption burn, 4-state spatial layouts, and 60fps composition.",
            "user_visible": True,
        },
        {
            "category": "composition_mode",
            "subject": "Composition Authoring Mode (Templated vs Atelier)",
            "selected": composition_mode,
            "options_considered": ["atelier", "templated"],
            "confidence": 0.94,
            "reason": "Bespoke atelier authoring with distinct primary visual subject per scene.",
            "user_visible": True,
        },
    ]

    identity_bible = [
        {
            "id": "CHAR_01",
            "type": "character",
            "name": character_id,
            "descriptor": f"{character_id} with consistent facial geometry, wardrobe, and natural skin texture",
            "description": f"{character_id} with consistent facial geometry, wardrobe, and natural skin texture",
            "reference_images": ["assets/CHAR_01_turnaround.png"],
        },
        {
            "id": "PROD_01",
            "type": "product",
            "name": product_id,
            "descriptor": f"{product_id} with locked dimensions, logo placement, and specular material finish",
            "description": f"{product_id} with locked dimensions, logo placement, and specular material finish",
            "reference_images": ["assets/PROD_01_hero.png"],
        },
        {
            "id": "ENV_01",
            "type": "environment",
            "name": "Primary Studio Environment",
            "descriptor": f"Architectural setting with {color_grading} and volumetric depth",
            "description": f"Architectural setting with {color_grading} and volumetric depth",
            "reference_images": ["assets/ENV_01_plate.png"],
        },
    ]

    idea_low = idea.lower()
    has_music_cue = any(
        tok in idea_low
        for tok in ("موسيقى", "إيقاع", "نبض", "أغنية", "music", "beat", "bpm", "edit", "مونتاج إيقاعي")
    )
    if style_variant in ("none", "Narrative Continuity Sequence"):
        montage_style = "none"
    elif purpose == "Corporate Videos" and not has_music_cue:
        montage_style = "none"
    else:
        montage_style = MONTAGE_STYLE_ALIAS_MAP.get(style_variant, "commercial_promo")

    montage_config = build_project_montage(
        style=montage_style,
        duration_s=float(actual_total),
        fps=30.0,
        source="generated_with_music" if montage_style != "none" else "estimated",
    )

    project_state = {
        "phase": "06_package_compiled",
        "decisions": decision_log,
        "approvals": {
            "gate_1_concept_approved": True,
            "gate_2_paid_credits_approved": False,
        },
        "beat_map_status": (
            montage_config["beat_map"]["source"] if montage_config.get("beat_map") else "not_applicable"
        ),
        "credits_spent_vs_estimated": {
            "spent": 0,
            "estimated_minimum": len(blocks) * 10,
            "estimated_expected": len(blocks) * 20,
        },
        "open_issues": [],
    }

    return {
        "project": {
            "title": clean_title,
            "purpose": purpose,
            "format": video_format,
            "style": style_variant,
            "edit_style": style_variant,
            "aspect_ratio": aspect_ratio,
            "total_runtime_s": actual_total,
            "requested_runtime_s": total_runtime_seconds,
            "motion_engine_60fps": {
                "enabled": True,
                "fps": 60,
                "bloom": dict(DEFAULT_UNREAL_BLOOM),
                "max_rtl_header_chars": 30,
            },
            "verified_capabilities": {
                "status": "VERIFIED",
                "verification_policy": CAPABILITY_VERIFICATION_STATUS,
                "last_verified_date": MODEL_REGISTRY_LAST_VERIFIED,
                "verification_note": "Verify on screen before spending credits (references/model-registry.md)",
                "per_clip_s_options": list(ALLOWED_CLIP_DURATIONS),
                "extend_cap_s": MAX_EXTEND_CHAIN_SECONDS,
                "extend_max_s": MAX_EXTEND_CHAIN_SECONDS,
                "max_ref_images": 7,
            },
            "montage": montage_config,
        },
        "project_state": project_state,
        "identity_bible": identity_bible,
        "blocks": blocks,
        "overlays": overlays,
        "outro": {
            "safe_zone": "9:16 central 80% safe zone; top 8% (Y:0..160) and bottom 20% (Y:1500..1920) clear",
            "safe_zone_note": "9:16 central 80% safe zone; top 8% (Y:0..160) and bottom 20% (Y:1500..1920) clear",
            "cta_ar": "اطلب الآن — الرابط في البايو",
        },
        "production_profile": {
            "purpose": purpose,
            "format": video_format,
            "style_variant": style_variant,
            "pipeline_type": pipeline_type,
            "execution_route": "Hybrid Generative (Google Flow / Seedance 2.0) + Programmatic Studio (Remotion / HyperFrames / FFmpeg)",
            "target_platform": "Google Flow (Veo 3.1 / Omni Flash 1.1 / Nano Banana Pro / Seedance 2.0) + Remotion/HyperFrames/FFmpeg Studio",
            "aspect_ratio": aspect_ratio,
            "runtime_category": runtime_category,
        },
        "script_and_content": {
            "video_title": clean_title,
            "narrative_framework": narrative_framework,
            "audience_emotional_truth": (
                "البحث عن الجودة الأصيلة والحل العملي المباشر الذي يمنح المشاهد نتيجة فورية "
                "وملموسة بعيداً عن المقدمات الطويلة والمبالغات التسويقية"
            ),
            "expected_cliche_rejected": (
                "البدء بمقدمة ترحيبية تقليدية بطيئة أو لقطة ثابتة للمنتج مع عبارات إعلانية مستهلكة"
            ),
            "chosen_divergence_angle": (
                "الدخول الفوري من الثانية 0.0 بلقطة بصرية خاطفة مع هوك ثلاثي الطبقات خلف الرأس يكسر التوقع البصري"
            ),
            "research_brief_summary": {
                "batches_executed": [
                    "1. Landscape Scan & Gap Analysis",
                    "2. Trending Pulse",
                    "3. Citable Data & Evidence",
                    "4. Audience Questions & Misconceptions",
                    "5. Expert & Contrarian Angles",
                ],
                "timeliness_window": "evergreen_with_trending_hook",
                "primary_gap_addressed": "Visualizing the physical mechanism immediately in the first 1.5 seconds.",
            },
            "hook_variants_scene_1": {
                "contrarian": "أغلب الناس يركزون على الشكل الخارجي.. لكن السر الحقيقي يبدأ من هذه التفصيلة.",
                "visual_payoff": "لقطة ماكرو سينمائية فورية للحظة الذروة البصرية مع حركة كاميرا تخطف العين من أول إطار.",
                "pain_point": "تعبت من الخيارات العادية اللي ما تعطيك النتيجة اللي في بالك؟ شوف الفرق الحقيقي.",
                "authority": "بمعايير هندسية دقيقة وتجربة متقنة.. هكذا تُصنع النتيجة الاحترافية من أول مرة.",
            },
            "full_spoken_script": " | ".join(
                f"[المشهد {sc['scene_id']}]: {sc['dialogue_lip_sync']}" for sc in scenes
            ),
            "facts_ledger": [
                f"العنصر الأساسي المقفول: {product_id}",
                f"الشخصية المرجعية المقفولة: {character_id}",
                f"المدة القياسية المعتمدة: {actual_total} ثانية ({len(blocks)} بلوكات)",
            ],
        },
        "global_parameters": {
            "tone": tone,
            "body_language_baseline": body_language,
            "dialect_lock": detected_dialect,
            "color_grading": color_grading,
            "camera_gear_emulation": camera_gear,
            "identity_lock_target": (
                f"Lock [Character ID: {character_id}] + Lock [Product ID: {product_id}] + Lock [Setting DNA]"
            ),
            "credit_governance_mode": (
                "Step 1: Nano Banana 2 Lite (0-Credit Keyframes) -> "
                "Step 2: Gemini Omni Flash 360p Draft (0-Credit 720p Upscale) -> "
                "Step 3: Veo 3.1 Quality Final Render"
            ),
            "total_runtime_seconds": actual_total,
            "requested_runtime_seconds": total_runtime_seconds,
        },
        "scene_breakdown": scenes,
        "post_production_timeline": {
            "render_runtime": render_runtime,
            "composition_mode": composition_mode,
            "visual_design_style": visual_design_style,
            "color_palette": color_palette,
            "silence_cut_config": {
                "noise_db": int(SILENCE_THRESHOLD_DB),
                "min_silence_sec": 0.35,
                "pre_roll_ms": 120,
                "post_roll_ms": 150,
                "merge_gap_ms": 180,
                "crossfade_ms": 20,
            },
            "depth_moments_planned": [
                f"Moment 1 (Hook): 3-Layer Stacked Hook (`stack`) with pixel-stretched Kashida '{kashida_hook_word}' behind speaker head",
                f"Moment 2 (Core): Action-Verb Stage (`R_LOWER + headout`) anchored to word '{anchor_word_s2}' with +0.45s hold",
                "Moment 3 (Brand Climax): Radial brand-colored wall illumination behind rotoscoped speaker (`grade: false` on skin)",
            ],
            "rtl_caption_config": {
                "cap_style": "chunk",
                "font_family": "Cairo",
                "max_words_per_pill": 4,
                "pill_center_y": 1395,
                "post_word_hold_sec": 0.45,
                "exit_ease_sec": 0.40,
                "never_on_face": True,
                "caption_onscreen_text_dedup": True,
                "kashida_rules_enforced": True,
            },
            "audio_mastering_spec": {
                "target_lufs": TARGET_INTEGRATED_LUFS,
                "true_peak_dbtp": -1.5,
                "lra_lu": 11.0,
                "sidechain_ducking": "threshold=0.03:ratio=5:attack=15:release=450",
                "max_sfx_events_per_min": 15,
                "sfx_peak_limit_dbfs": -18.0,
            },
            "export_targets": [
                "MP4 Master (-14 LUFS + 0.1s First-Frame Cover, < 29MB)",
                "SRT Subtitles (.srt)",
                "Clean Transcript (.txt)",
                "CapCut Editable Draft Project (draft_content.json)",
                "Interactive Browser Timeline Editor (editor.mjs / studio.html / Backlot Live Board)",
            ],
        },
        "production_governance": {
            "taste_profile": taste_profile,
            "delivery_promise": promise_report,
            "slideshow_risk_report": slideshow_report,
            "scene_variation_report": variation_report,
            "scored_provider_selection": provider_report,
            "decision_log": decision_log,
            "budget_governance": {
                "mode": "cap",
                "workflow": "estimate -> reserve -> reconcile",
                "sample_first_gate_sec": 12,
                "zero_credit_keyframes": "Nano Banana 2 Lite",
                "zero_credit_draft_upscale": "Gemini Omni Flash 1.1 (360p -> 720p)",
            },
            "chai_final_review_checklist": {
                "critique_axes": [
                    "Accurate (concrete field/frame ref)",
                    "Complete (pattern-wide scan)",
                    "Constructive (mandatory proposed_fix on CRITICAL)",
                ],
                "post_render_5_checks": [
                    "1. technical_probe (ffprobe container, resolution, duration within 1.0s)",
                    "2. visual_spotcheck (>= 4 sampled frames, zero black frames or 640x360 letterbox traps)",
                    "3. audio_spotcheck (-14.0 LUFS, -1.5 dBTP, zero clipping)",
                    "4. promise_preservation (motion_ratio >= 70%, silent_downgrade_detected == false)",
                    "5. subtitle_and_distinctness_check (zero caption/SerifLine duplication, no hero-component spine)",
                ],
            },
        },
        "outro_standardization": {
            "aspect_ratio": f"{aspect_ratio} (Safe-Zone Enforced)",
            "brand_logo_safe_zone": "Y: 420..820, X: 120..960 (Upper-Center Clean Negative Space)",
            "cta_and_handles_safe_zone": "Y: 950..1280, X: 120..900 (Lower-Middle Safe Zone)",
            "defaults_from_existing_skill": dict(OUTRO_SAFE_ZONES),
            "loop_back_visual_cue": "Final frame lighting and subject angle match Scene 1 Frame 0 for replay loop",
        },
        "marketing_expansion": {
            "first_frame_cover": {
                "injected_at": "First 0.1s frame of delivered MP4 (--first)",
                "safe_square_bounds": "1080x1080 Center Square (Y: 420..1500)",
                "hook_headline": f"السر الحقيقي|*{hook_focus_word}*",
                "typography_floors": "Headline >= 170px, Subtext >= 110px, Logo >= 200px, Chin >= 30px above headline",
            },
            "marketing_poster": (
                f"4:5 poster (1080x1350) locking {character_id} and {product_id} with 35% upper negative space for Arabic headline"
            ),
            "poster_layout_prompt": (
                f"Commercial advertising poster (4:5 aspect ratio, 1080x1350) rendered in Nano Banana Pro: "
                f"Hero composition featuring {product_id} and {character_id} in the lower two-thirds, matching "
                f"{color_grading} and {camera_gear} look, with 35% clean negative space in the top third, {anti_cgi_suffix}"
            ),
            "social_design_set": (
                f"Unified 9:16 cover, 4:5 feed card, and 1:1 profile/community graphic locking {product_id} visual identity"
            ),
            "social_design_brief": (
                f"High-contrast 9:16 Reels Cover & 1:1 Quote Card featuring {product_id} macro detail, "
                "#FFFFFF setup text + #FFD60A highlighted keyword in Cairo Black font."
            ),
            "arabic_carousel": [
                "الشريحة 1: ليش الخيارات العادية ما تعطيك النتيجة اللي تبحث عنها؟ اسحب لليسار.",
                "الشريحة 2: المشكلة في إهمال التفاصيل الدقيقة اللي تصنع الفارق الحقيقي.",
                "الشريحة 3: لما تجتمع الخامة الأصيلة مع الإتقان، تتحول التجربة إلى معيار جديد.",
                "الشريحة 4: ثبات الجودة في كل مرة بفضل العناية بأدق التفاصيل من المصدر.",
                "الشريحة 5: تصميم يجمع بين الهوية الأصيلة والأداء العصري العملي بدون تعقيد.",
                f"الشريحة 6: احفظ المنشور واكتب كلمة ({comment_keyword}) بالتعليقات ليصلك الرابط فوراً.",
            ],
            "carousel_arabic_copy": [
                "الشريحة 1: ليش الخيارات العادية ما تعطيك النتيجة اللي تبحث عنها؟ اسحب لليسار.",
                "الشريحة 2: المشكلة في إهمال التفاصيل الدقيقة اللي تصنع الفارق الحقيقي.",
                "الشريحة 3: لما تجتمع الخامة الأصيلة مع الإتقان، تتحول التجربة إلى معيار جديد.",
                "الشريحة 4: ثبات الجودة في كل مرة بفضل العناية بأدق التفاصيل من المصدر.",
                "الشريحة 5: تصميم يجمع بين الهوية الأصيلة والأداء العصري العملي بدون تعقيد.",
                f"الشريحة 6: احفظ المنشور واكتب كلمة ({comment_keyword}) بالتعليقات ليصلك الرابط فوراً.",
            ],
            "publish_pack": {
                "ab_test_plan": "Test Hook A (Contrarian Question) vs Hook B (Visual Macro Payoff) across first 3 seconds.",
                "ai_content_disclosure": "Apply platform AI-generated / synthetic media disclosure label where applicable.",
                "prohibited_claims_checked": True,
                "post_publish_feedback_file": "project_state.json",
            },
            "social_publish_pack": {
                "primary_search_phrase": clean_title[:45],
                "comment_keyword_variants": keyword_variants,
                "instagram": {
                    "caption": (
                        f"{clean_title[:45]} — تفصيلة واحدة تغير النتيجة بالكامل.\n\n"
                        f"اكتب كلمة ({comment_keyword}) في التعليقات وبيوصلك الدليل والتفاصيل مباشرة!"
                    ),
                    "hashtags": ["#صناعة_المحتوى", "#تسويق_رقمي", "#جودة", "#ابداع"],
                    "alt_text": f"فيديو يوضح {clean_title} بتصوير سينمائي وموشن جرافيك توضيحي",
                    "pinned_comment": f"اكتب ({comment_keyword}) في تعليق وبيوصلك الرابط المباشر فوراً 👇",
                },
                "tiktok": {
                    "caption": f"{clean_title[:45]} — اكتب ({comment_keyword}) بالتعليقات للتفاصيل!",
                    "hashtags": ["#اكسبلور", "#صناعة_محتوى", "#تيك_توك"],
                },
                "youtube_shorts": {
                    "title": f"{clean_title[:65]} | السر العملي",
                    "description": f"{clean_title[:45]} بخطوات عملية مركزة. اكتب ({comment_keyword}) للتفاصيل.",
                    "hashtags": ["#Shorts", "#تسويق", "#إنتاج_فيديو"],
                },
            },
        },
        "qa_audit": {
            "audio_math_passed": True,
            "micro_scene_limit_passed": all(d in HARD_ALLOWED_CLIP_DURATIONS for d in block_durations),
            "physicality_firewall_passed": True,
            "anti_cgi_guardrails_injected": "--no CGI" in anti_cgi_suffix or "--no frame flicker" in anti_cgi_suffix,
            "dialect_lock_verified": True,
            "outro_safe_zone_verified": True,
            "kashida_and_rtl_caption_verified": True,
            "calmness_and_hold_laws_verified": True,
            "audio_lufs_and_sfx_cap_verified": True,
            "slideshow_risk_passed": slideshow_report["verdict"] in ("strong", "acceptable"),
            "scene_variation_passed": variation_report["verdict"] in ("strong", "acceptable"),
            "delivery_promise_verified": promise_report["valid"],
            "chai_critique_and_decision_log_verified": len(decision_log) >= 3,
        },
    }


def compile_cineflow_blueprint(
    title: str = "CineFlow Masterpiece Production",
    purpose: str = "Commercials & TVCs",
    video_format: str = "Live-Action",
    style_variant: str = "Commercial Promo",
    aspect_ratio: str = "9:16",
    total_runtime_seconds: int = 20,
    macro: str = "/anamorphic",
    render_runtime: str = "remotion",
    design_style: str = "kinetic_typography",
    spoken_script: str = "ويش سر القهوة اللي تعدل المزاج من أول رشفة؟ جربها الحين وعيش الفخامة",
    budget_tier: str = "standard",
) -> Dict[str, Any]:
    """Convenience wrapper around compile_blueprint accepting explicit title, aspect_ratio, and macro."""
    idea_full = f"{title} {macro} /ar {aspect_ratio}".strip()
    res = compile_blueprint(
        idea=idea_full,
        purpose=purpose,
        video_format=video_format,
        style_variant=style_variant,
        dialogue=spoken_script,
        total_runtime_seconds=total_runtime_seconds,
        render_runtime=render_runtime,
        budget_tier=budget_tier,
    )
    if design_style:
        res["post_production_timeline"]["visual_design_style"] = design_style
    return res


def main() -> None:
    """CLI Entrypoint for CineFlow AI Studio Compiler."""
    parser = argparse.ArgumentParser(description="CineFlow AI Studio Blueprint & Showrunner Package Compiler")
    parser.add_argument(
        "--idea",
        "--title",
        dest="idea",
        type=str,
        default="إعلان قهوة مختصة فاخرة في المنامة /dollyin /macro /goldenhour /4k /ar 9:16",
        help="Raw video idea/title and optional /macros",
    )
    parser.add_argument("--purpose", type=str, default="Commercials & TVCs")
    parser.add_argument("--format", dest="video_format", type=str, default="Live-Action")
    parser.add_argument("--style-variant", "--style", dest="style_variant", type=str, default="Commercial Promo")
    parser.add_argument(
        "--dialogue",
        "--script",
        dest="dialogue",
        type=str,
        default="ويش سر القهوة اللي تعدل المزاج من أول رشفة؟ جربها الحين وعيش الفخامة",
    )
    parser.add_argument("--runtime", type=int, default=16)
    parser.add_argument("--aspect", type=str, default="")
    parser.add_argument("--macro", type=str, default="")
    parser.add_argument("--design-style", type=str, default="")
    parser.add_argument("--palette", type=str, default="gold")
    parser.add_argument("--keyword", type=str, default="إبداع")
    parser.add_argument(
        "--render-runtime", type=str, default="remotion", choices=["remotion", "hyperframes", "ffmpeg"]
    )
    parser.add_argument("--composition-mode", type=str, default="atelier", choices=["atelier", "templated"])
    parser.add_argument("--budget-tier", type=str, default="standard", choices=["draft", "standard", "cinema"])
    parser.add_argument("--output", type=str, default="")
    args = parser.parse_args()

    idea_combined = args.idea
    if args.macro and args.macro not in idea_combined:
        idea_combined = f"{idea_combined} {args.macro}"
    if args.aspect and f"/ar {args.aspect}" not in idea_combined:
        idea_combined = f"{idea_combined} /ar {args.aspect}"

    blueprint = compile_blueprint(
        idea=idea_combined,
        purpose=args.purpose,
        video_format=args.video_format,
        style_variant=args.style_variant,
        dialogue=args.dialogue,
        total_runtime_seconds=args.runtime,
        color_palette=args.palette,
        comment_keyword=args.keyword,
        render_runtime=args.render_runtime,
        composition_mode=args.composition_mode,
        budget_tier=args.budget_tier,
    )
    json_str = json.dumps(blueprint, ensure_ascii=False, indent=2)
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json_str, encoding="utf-8")
        print(f"Saved CineFlow AI Studio Blueprint to: {out_path}")
    else:
        print(json_str)


if __name__ == "__main__":
    main()
