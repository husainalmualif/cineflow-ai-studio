#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Production Governance, Slideshow Risk Scorer, Scene Variation Auditor,
7-Dimension Provider Selector, Runtime Partitioner & Omni Flash Stateful Payload Builder.
"""

from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter
from typing import Any, Dict, FrozenSet, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from studio_config import (  # noqa: E402
    MAX_TOTAL_RUNTIME_SECONDS,
    MIN_TOTAL_RUNTIME_SECONDS,
    OMNI_FLASH_MODEL_DEFAULT,
    OMNI_INLINE_MAX_MB,
    VALID_FORMATS,
    VALID_PURPOSES,
    VALID_STYLE_VARIANTS,
)

GENERIC_SLOP_PHRASES: FrozenSet[str] = frozenset({
    "a person",
    "a beautiful",
    "in today's world",
    "cutting-edge",
    "state-of-the-art",
    "next-generation",
    "revolutionary",
    "amazing",
    "incredible",
    "seamless",
    "elegant solution",
})


def build_omni_interaction_payload(
    task: str,
    prompt: str,
    aspect_ratio: Optional[str] = "16:9",
    delivery: str = "inline",
    previous_interaction_id: Optional[str] = None,
    images_b64: Optional[List[Dict[str, str]]] = None,
    video_file_uri: Optional[str] = None,
    estimated_size_mb: float = 2.0,
    model: str = OMNI_FLASH_MODEL_DEFAULT,
) -> Dict[str, Any]:
    """
    Build a validated stateful Gemini Interactions API payload (`client.interactions.create(...)`)
    following the `omni-skill-agy` FastMCP Video Agent rules (`references/gemini-interactions-api.md`):
    - Sets `store=True`, `background=False`, `stream=False` so every turn returns a chainable `interaction.id`.
    - Enforces Aspect Ratio Inheritance Law: `aspect_ratio` ('16:9' or '9:16') is allowed ONLY on initial
      `generate_video`; stateful `edit_video` calls inherit aspect ratio and must NOT re-send `aspect_ratio`.
    - Enforces Delivery Mode Ceiling: upgrades `delivery` to `'uri'` automatically if `estimated_size_mb >= 4.0`.
    """
    valid_tasks = {
        "generate_video",
        "edit_video",
        "animate_image",
        "interpolate_images",
        "generate_with_subjects",
        "edit_user_video",
    }
    if task not in valid_tasks:
        raise ValueError(f"Unsupported Omni task '{task}'. Must be one of {sorted(valid_tasks)}.")
    if not prompt or not str(prompt).strip():
        raise ValueError("Omni interaction prompt must be a non-empty string.")

    effective_delivery = "uri" if (delivery == "uri" or estimated_size_mb >= OMNI_INLINE_MAX_MB) else "inline"
    response_format: Dict[str, Any] = {"type": "video"}
    if effective_delivery == "uri":
        response_format["delivery"] = "uri"

    payload: Dict[str, Any] = {
        "model": model,
        "response_format": response_format,
        "background": False,
        "store": True,
        "stream": False,
    }

    if task == "generate_video":
        if aspect_ratio in ("16:9", "9:16"):
            response_format["aspect_ratio"] = aspect_ratio
        payload["input"] = str(prompt).strip()
    elif task == "edit_video":
        if not previous_interaction_id or not str(previous_interaction_id).strip():
            raise ValueError("edit_video requires a non-empty latest previous_interaction_id.")
        payload["previous_interaction_id"] = str(previous_interaction_id).strip()
        payload["input"] = str(prompt).strip()
    elif task in ("animate_image", "interpolate_images", "generate_with_subjects"):
        if not images_b64:
            raise ValueError(f"{task} requires at least one image dict in images_b64.")
        if task == "interpolate_images" and len(images_b64) != 2:
            raise ValueError("interpolate_images requires exactly 2 keyframe images (start and end).")
        payload["input"] = [*images_b64, {"type": "text", "text": str(prompt).strip()}]
    elif task == "edit_user_video":
        if not video_file_uri or not str(video_file_uri).strip():
            raise ValueError("edit_user_video requires a File API video_file_uri.")
        payload["input"] = [
            {"type": "document", "uri": str(video_file_uri).strip()},
            {"type": "text", "text": str(prompt).strip()},
        ]

    return payload


def validate_taxonomy_inputs(purpose: str, video_format: str, style_variant: str) -> None:
    """Validates purpose, video_format, and style_variant against canonical sets (fixes H3)."""
    if purpose not in VALID_PURPOSES:
        raise ValueError(f"Unsupported purpose {purpose!r}. Must be one of {sorted(VALID_PURPOSES)}")
    if video_format not in VALID_FORMATS:
        raise ValueError(f"Unsupported video_format {video_format!r}. Must be one of {sorted(VALID_FORMATS)}")
    if style_variant not in VALID_STYLE_VARIANTS:
        raise ValueError(
            f"Unsupported style_variant {style_variant!r}. Must be one of {sorted(VALID_STYLE_VARIANTS)}"
        )


def select_pipeline_route(purpose: str, video_format: str, style_variant: str) -> str:
    """Map validated production parameters to one of the 12 autonomous CineFlow execution pipelines."""
    validate_taxonomy_inputs(purpose, video_format, style_variant)
    if purpose == "Documentaries":
        return "route_7_documentary_montage"
    if video_format in ("Animation", "Animation (2D / 3D)"):
        return "route_8_character_animation_ink_theater"
    if video_format == "360 & Interactive":
        return "route_9_3d_world_generation"
    if video_format == "Motion Graphics":
        return "route_3_motion_stage_60fps"
    if purpose == "Explainer Videos":
        return "route_6_3d_device_explainer"
    if purpose == "Testimonial Videos":
        return "route_2_talking_head_reel"
    if style_variant in ("Sizzle Reel", "Sizzle Reel / Recap", "Montage Sequence"):
        return "route_4_silent_broll_montage"
    return "route_1_generative_cinema"


def partition_runtime_into_allowed_blocks(total_runtime_seconds: int) -> List[int]:
    """
    Partitions `total_runtime_seconds` into a list of block durations strictly from `{4, 6, 8, 10}`.
    """
    if (
        not isinstance(total_runtime_seconds, (int, float))
        or isinstance(total_runtime_seconds, bool)
        or total_runtime_seconds < MIN_TOTAL_RUNTIME_SECONDS
        or total_runtime_seconds > MAX_TOTAL_RUNTIME_SECONDS
    ):
        raise ValueError(
            f"total_runtime_seconds must be between {MIN_TOTAL_RUNTIME_SECONDS} and "
            f"{MAX_TOTAL_RUNTIME_SECONDS}, got {total_runtime_seconds!r}"
        )

    target = int(round(total_runtime_seconds))
    if target % 2 == 1:
        target += 1

    if target == 4:
        return [4]
    if target == 6:
        return [6]
    if target == 8:
        return [4, 4]
    if target == 10:
        return [6, 4]

    min_blocks = max(3, math.ceil(target / 10))
    max_blocks = target // 4
    n_blocks = max(min_blocks, min(max_blocks, max(3, round(target / 8))))
    blocks = [4] * n_blocks
    rem = target - sum(blocks)

    idx = 1 if n_blocks >= 3 else 0
    while rem >= 2:
        if blocks[idx] < 10:
            blocks[idx] += 2
            rem -= 2
        idx = (idx + 1) % n_blocks
        if all(b == 10 for b in blocks) and rem >= 4:
            blocks.append(4)
            n_blocks += 1
            rem -= 4

    return blocks


def build_taste_profile(purpose: str, style_variant: str, color_palette: str) -> Dict[str, Any]:
    """Construct the Taste Direction Profile with 3 integer dials (1-10)."""
    validate_taxonomy_inputs(purpose, "Live-Action", style_variant)
    motion_intensity = (
        8
        if style_variant in (
            "Commercial Promo",
            "Short-Form Edits / AMV",
            "Edits / AMV",
            "Sizzle Reel",
            "Sizzle Reel / Recap",
        )
        else 6
    )
    info_density = 7 if purpose in ("Educational & Training", "Explainer Videos") else 4
    visual_variance = 6
    return {
        "design_read": (
            f"High-craft {purpose} ({style_variant}): tactile physical realism paired with disciplined "
            f"'{color_palette}' palette typography and purposeful camera momentum; zero generic AI templates."
        ),
        "visual_variance": visual_variance,
        "motion_intensity": motion_intensity,
        "information_density": info_density,
        "palette_discipline": f"Curated '{color_palette}' palette with strict presenter skin-tone protection (grade: false on faces).",
        "layout_variation": "Alternating R_FULL hero framing with R_LOWER + Headout Action-Verb Stage and clean safe-zone outro.",
        "reference_strategy": "Zero-credit Nano Banana 2 Lite reference keyframes per scene family before Veo 3.1 / Seedance 2.0 motion generation.",
        "anti_patterns": [
            "generic AI-purple gradient backgrounds",
            "same camera shot size across 3 consecutive scenes",
            "caption duplicating on-screen SerifLine headline verbatim",
            "reusing the same hero-component spine across every beat",
        ],
        "quality_gates": [
            "Every scene carries an explicit shot_intent and CHAI 5-aspect breakdown.",
            "Signature depth device appears in at most 1-2 climactic beats.",
        ],
    }


def score_slideshow_risk(
    scenes: List[Dict[str, Any]],
    renderer_family: str = "cinematic-commercial",
    render_runtime: str = "remotion",
) -> Dict[str, Any]:
    """Score slideshow risk across 6 dimensions (0.0-5.0, lower is better)."""
    if not scenes or not isinstance(scenes, list):
        return {"average": 5.0, "verdict": "fail", "dimensions": {}, "render_runtime": render_runtime}

    n = len(scenes)
    static_types = {"image", "still", "static_image", "slide", "text_card", "stat_card", "kpi_grid"}
    static_type_count = sum(
        1 for s in scenes
        if str(s.get("type", "video")).lower() in static_types
        or str(s.get("motion_type", "")).lower() in ("static_image", "still", "none")
    )

    prompts = [
        str(s.get("visual_prompt") or s.get("visual_prompt_en") or json.dumps(s, sort_keys=True)).strip()
        for s in scenes
    ]
    unique_prompts = len(set(prompts))
    duplicate_ratio = (n - unique_prompts) / n if n > 1 else 0.0

    sizes = [str(s.get("shot_language", {}).get("shot_size", "none")) for s in scenes]
    most_common_size, most_common_size_count = Counter(sizes).most_common(1)[0]
    size_ratio = most_common_size_count / n

    rep_score = 0.0
    if duplicate_ratio > 0:
        rep_score += duplicate_ratio * 5.0
    if n >= 2 and (most_common_size in ("none", "unspecified") or size_ratio >= 0.67):
        rep_score += 3.5
    if static_type_count / n >= 0.4:
        rep_score += 4.0
    rep_score = min(5.0, rep_score)

    decorative_count = sum(
        1 for s in scenes
        if not (s.get("information_role") or s.get("narrative_role") or s.get("shot_intent"))
    )
    dec_score = (decorative_count / n) * 5.0
    if duplicate_ratio >= 0.5 or static_type_count / n >= 0.5:
        dec_score = max(dec_score, 4.2)
    dec_score = min(5.0, dec_score)

    moving_shots = [
        s for s in scenes
        if str(s.get("type", "video")).lower() not in static_types
        and str(s.get("motion_type", "motion_clip")).lower() not in ("static_image", "still", "none")
        and str(s.get("shot_language", {}).get("camera_movement", "static")).lower()
        not in ("static", "unspecified", "none", "locked", "")
    ]
    if not moving_shots or len(moving_shots) < n * 0.5 or duplicate_ratio >= 0.5:
        motion_score = 4.8
    else:
        purposeless_moving = sum(1 for s in moving_shots if not s.get("shot_intent"))
        motion_score = min(5.0, (purposeless_moving / len(moving_shots)) * 4.0)

    intents = [str(s.get("shot_intent") or "").strip() for s in scenes if str(s.get("shot_intent") or "").strip()]
    unique_intents = len(set(intents))
    if not intents or (n >= 2 and unique_intents <= max(1, n // 3)):
        intent_score = 4.5
    else:
        intent_score = min(5.0, (1.0 - (len(intents) / n)) * 5.0)

    text_ratio = static_type_count / n
    typo_score = 4.5 if text_ratio >= 0.5 else (2.5 if text_ratio > 0.3 else 0.0)

    cin_issues = 0
    if "cinematic" in renderer_family.lower():
        if not any(s.get("hero_moment") for s in scenes):
            cin_issues += 1
        if len(moving_shots) < n * 0.5:
            cin_issues += 1
        has_lighting = sum(1 for s in scenes if s.get("shot_language", {}).get("lighting_key"))
        if has_lighting < n * 0.5:
            cin_issues += 1
        if duplicate_ratio >= 0.4:
            cin_issues += 2
    cin_score = min(5.0, cin_issues * 1.6)

    dimensions = {
        "repetition": {"score": round(rep_score, 2), "reason": "Checks prompt, shot_size, and visual type diversity"},
        "decorative_visuals": {"score": round(dec_score, 2), "reason": "Checks narrative role and non-static substance"},
        "weak_motion": {"score": round(motion_score, 2), "reason": "Checks real camera/subject motion vs static stills"},
        "weak_shot_intent": {"score": round(intent_score, 2), "reason": f"{unique_intents}/{n} unique shot intents"},
        "typography_overreliance": {"score": round(typo_score, 2), "reason": "Checks static slide/card ratio"},
        "unsupported_cinematic_claims": {"score": round(cin_score, 2), "reason": "Checks hero_moment, lighting, and motion"},
    }
    avg = round(sum(d["score"] for d in dimensions.values()) / len(dimensions), 2)
    verdict = "strong" if avg < 2.0 else ("acceptable" if avg < 3.0 else ("revise" if avg < 3.8 else "fail"))
    return {
        "average": avg,
        "score": avg,
        "total_score": avg,
        "verdict": verdict,
        "dimensions": dimensions,
        "render_runtime": render_runtime,
    }


def check_scene_variation(scenes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Run the 8-point scene variation and anti-slop check before asset generation."""
    if not scenes or not isinstance(scenes, list):
        return {"score": 5.0, "verdict": "fail", "violations": ["No scenes provided"], "suggestions": []}

    n = len(scenes)
    violations: List[str] = []
    suggestions: List[str] = []
    penalty = 0.0

    prompts = [
        str(s.get("visual_prompt") or s.get("visual_prompt_en") or json.dumps(s, sort_keys=True)).strip()
        for s in scenes
    ]
    unique_prompts = len(set(prompts))
    if unique_prompts < n:
        dup_count = n - unique_prompts
        violations.append(f"{dup_count} duplicate/identical scenes or visual prompts detected.")
        suggestions.append("Give every scene a distinct visual_prompt, subject action, and spatial framing.")
        penalty += 3.5

    shot_sizes = [str(s.get("shot_language", {}).get("shot_size", "unspecified")) for s in scenes]
    unspecified_count = sum(1 for sz in shot_sizes if sz in ("unspecified", "none", ""))
    if unspecified_count > 0:
        violations.append(f"{unspecified_count}/{n} scenes are missing explicit shot_language.shot_size.")
        penalty += 2.2

    longest_run = 1
    current_run = 1
    for idx in range(1, n):
        if shot_sizes[idx] == shot_sizes[idx - 1]:
            current_run += 1
            longest_run = max(longest_run, current_run)
        else:
            current_run = 1
    if n >= 3 and longest_run >= 2:
        violations.append(f"{longest_run} consecutive same-size shots detected ({shot_sizes[0]}).")
        suggestions.append("Alternate shot sizes across consecutive scenes (e.g. MCU -> ECU -> MW).")
        penalty += 2.0

    static_types = {"image", "still", "static_image", "slide", "text_card", "stat_card"}
    static_scenes = sum(
        1 for s in scenes
        if str(s.get("type", "video")).lower() in static_types
        or str(s.get("motion_type", "")).lower() in ("static_image", "still", "none")
    )
    if static_scenes > 0:
        violations.append(f"{static_scenes}/{n} scenes are static images/slides instead of real motion.")
        penalty += 3.2

    cam_moves = [str(s.get("shot_language", {}).get("camera_movement", "static")) for s in scenes]
    if n >= 2 and len(set(cam_moves)) == 1:
        violations.append(f"All {n} scenes use the exact same camera_movement ('{cam_moves[0]}').")
        penalty += 2.0

    if not any(s.get("hero_moment") for s in scenes):
        violations.append("No hero_moment flagged across scene_breakdown.")
        suggestions.append("Mark the climax or primary showcase scene with hero_moment=True.")
        penalty += 1.2

    generic_hits = sum(
        1 for s in scenes
        if any(phrase in str(s.get("visual_prompt", "")).lower() for phrase in GENERIC_SLOP_PHRASES)
    )
    if generic_hits >= max(1, math.ceil(n * 0.34)):
        violations.append(f"{generic_hits}/{n} scenes contain generic AI slop phrasing.")
        penalty += 1.5

    textured = sum(1 for s in scenes if s.get("texture_keywords"))
    if textured < n * 0.3:
        violations.append("Insufficient texture_keywords coverage across scenes.")
        penalty += 1.2

    score = round(min(5.0, penalty), 2)
    verdict = "strong" if score < 2.0 else ("acceptable" if score < 3.0 else ("revise" if score < 3.8 else "fail"))
    return {
        "score": score,
        "verdict": verdict,
        "violations": violations,
        "suggestions": suggestions,
    }


def validate_delivery_promise(
    scenes: List[Dict[str, Any]],
    promise_type: str = "motion_led",
    motion_required: bool = True,
) -> Dict[str, Any]:
    """Validate that a motion-led promise has >= 70% real motion cuts and zero unapproved still fallback."""
    if not scenes:
        return {"valid": False, "violations": ["No scenes to validate"], "motion_ratio": 0.0}

    real_motion_types = {"video", "animation", "avatar"}
    motion_cuts = sum(
        1 for s in scenes
        if str(s.get("type", "video")).lower() in real_motion_types
        and str(s.get("motion_type", "motion_clip")).lower() not in ("static_image", "still", "none")
    )
    motion_ratio = round(motion_cuts / len(scenes), 2)
    violations: List[str] = []
    if motion_required and promise_type == "motion_led" and motion_ratio < 0.7:
        violations.append(f"Motion ratio {motion_ratio:.0%} is below 70% floor for motion_led delivery promise.")
    return {
        "promise_type": promise_type,
        "motion_required": motion_required,
        "motion_ratio": motion_ratio,
        "motion_cuts": motion_cuts,
        "total_cuts": len(scenes),
        "valid": len(violations) == 0,
        "violations": violations,
    }


def score_providers(
    purpose: str,
    video_format: str,
    style_variant: str = "Commercial Promo",
    budget_tier: str = "standard",
) -> Dict[str, Any]:
    """Score providers dynamically across 7 weighted dimensions based on purpose, format, style_variant, and budget_tier."""
    weights = {
        "task_fit": 0.30,
        "output_quality": 0.20,
        "control_features": 0.15,
        "reliability": 0.15,
        "cost_efficiency": 0.10,
        "latency": 0.05,
        "continuity": 0.05,
    }

    is_doc = purpose == "Documentaries"
    is_anim = video_format in ("Animation", "Animation (2D / 3D)")
    is_motion = video_format == "Motion Graphics" or purpose in ("Explainer Videos", "Educational & Training")
    is_music_ent = purpose == "Entertainment Videos" or style_variant == "Music Videos"
    is_draft = budget_tier in ("draft", "low", "preview")

    candidates = [
        {
            "provider": "google_flow_veo_3_1",
            "label": "Google Flow (Veo 3.1 Quality + Nano Banana 2 Lite + Scene Handshake)",
            "metrics": {
                "task_fit": 9.7 if (video_format == "Live-Action" and not is_doc and not is_music_ent) else 7.4,
                "output_quality": 9.7,
                "control_features": 9.5,
                "reliability": 9.3,
                "cost_efficiency": 7.8 if not is_draft else 5.5,
                "latency": 8.2,
                "continuity": 9.6,
            },
        },
        {
            "provider": "clip_archival_remotion_hybrid",
            "label": "CLIP Real-Footage Archival Corpus + Remotion ProRes 4444 Alpha End-Tag",
            "metrics": {
                "task_fit": 9.8 if is_doc else 6.2,
                "output_quality": 9.5 if is_doc else 7.5,
                "control_features": 9.6,
                "reliability": 9.7,
                "cost_efficiency": 9.8,
                "latency": 9.2,
                "continuity": 9.4,
            },
        },
        {
            "provider": "ink_theater_cmu_mocap",
            "label": "HyperFrames Ink Theater (Rigged SVG + 12 CMU Mocap Clips + Three.js 3D)",
            "metrics": {
                "task_fit": 9.8 if is_anim else 6.5,
                "output_quality": 9.4 if is_anim else 7.8,
                "control_features": 9.7,
                "reliability": 9.6,
                "cost_efficiency": 9.7,
                "latency": 9.1,
                "continuity": 9.5,
            },
        },
        {
            "provider": "hyperframes_remotion_60fps",
            "label": "60fps Three.js WebGL + Remotion/HyperFrames Atelier Motion Engine",
            "metrics": {
                "task_fit": 9.8 if (is_motion and not is_anim) else 7.5,
                "output_quality": 9.6,
                "control_features": 9.8,
                "reliability": 9.7,
                "cost_efficiency": 9.6,
                "latency": 9.3,
                "continuity": 9.7,
            },
        },
        {
            "provider": "seedance_2_0",
            "label": "Seedance 2.0 (Multi-Shot Beat Sync + Native Quoted Lip-Sync)",
            "metrics": {
                "task_fit": 9.8 if (is_music_ent and not is_anim) else 8.4,
                "output_quality": 9.6,
                "control_features": 9.4,
                "reliability": 9.1,
                "cost_efficiency": 8.2,
                "latency": 8.5,
                "continuity": 9.4,
            },
        },
        {
            "provider": "gemini_omni_flash_1_1",
            "label": "Gemini Omni Flash 1.1 (360p Fast Draft -> 0-Credit 720p Upscale)",
            "metrics": {
                "task_fit": 9.8 if is_draft else 8.0,
                "output_quality": 8.6,
                "control_features": 8.9,
                "reliability": 9.5,
                "cost_efficiency": 9.9,
                "latency": 9.8,
                "continuity": 8.8,
            },
        },
    ]

    ranked: List[Dict[str, Any]] = []
    for item in candidates:
        total = sum(item["metrics"][k] * weights[k] for k in weights)
        ranked.append({
            "provider": item["provider"],
            "label": item["label"],
            "weighted_score": round(total, 2),
            "dimensions": item["metrics"],
        })
    ranked.sort(key=lambda x: x["weighted_score"], reverse=True)
    return {
        "scoring_weights": weights,
        "selected_primary": ranked[0]["provider"],
        "selected_label": ranked[0]["label"],
        "selected_score": ranked[0]["weighted_score"],
        "candidates_ranked": ranked,
        "purpose_context": purpose,
        "format_context": video_format,
        "budget_tier": budget_tier,
    }
