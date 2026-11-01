#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CineFlow AI Studio — Multi-Agent Orchestrator & Broadcast Phonetic Validator
============================================================================
Coordinates the 7-Platform Execution Crew and 13 Showrunner Specialist Roles (A1..A12 + Alt).
Enforces the 4 Mandatory Arabic Broadcast Phonetic Laws using the unified threshold
`MIN_DIACRITIC_RATIO = 0.75` (counting vocalized Arabic base letters, never double-counting shaddah+haraka).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from studio_config import (  # noqa: E402
    MAX_LIPSYNC_WORDS_PER_PHRASE,
    MAX_TRUE_PEAK_DBTP,
    MIN_DIACRITIC_RATIO,
    TARGET_INTEGRATED_LUFS,
)

DAGGER_ALIF = "\u0670"
ARABIC_BASE_LETTER_RE = re.compile(r"[\u0621-\u063A\u0641-\u064A]")
VOCALIZED_BASE_LETTER_RE = re.compile(r"[\u0621-\u063A\u0641-\u064A][\u064B-\u0652\u0651]+")
CLAUSE_SPLIT_RE = re.compile(r"(?:[،.؛!؟…\n]+|\.\.+|\[[^\]]*\])")

BANNED_TRANSLITERATIONS = {
    "البرومبت",
    "برومبت",
    "تشاي",
    "كابشن",
    "موشن",
    "التايملاين",
    "تايملاين",
    "الفريم",
    "فريمات",
}

SEVEN_AGENT_REGISTRY: List[Dict[str, Any]] = [
    {
        "agent_id": "agent_1_master_orchestrator",
        "showrunner_roles": ["Showrunner", "A8", "A9", "A11"],
        "name_ar": "مدير المشروع والمايسترو",
        "name_en": "Master Orchestrator & Showrunner Agent",
        "endpoint": "local://cineflow-orchestrator",
        "phase": "All Phases (0 -> 9)",
        "deliverables": ["00_brief.md", "07_audit.md", "state.json", "decision_log.json"],
    },
    {
        "agent_id": "agent_2_gemini_multimodal",
        "showrunner_roles": ["A2", "A10"],
        "name_ar": "وكيل جيميناي متعدد الوسائط",
        "name_en": "Gemini Multimodal Script & Marketing Agent",
        "endpoint": "https://gemini.google.com/app",
        "phase": "Phase 2 & 9: Vocalized Scriptwriting & Marketing Expansion",
        "deliverables": ["02_script.md", "script_source.json", "10_marketing.md"],
    },
    {
        "agent_id": "agent_3_google_labs_creative",
        "showrunner_roles": ["A3"],
        "name_ar": "وكيل مختبرات جوجل للابتكار البصري",
        "name_en": "Google Labs Creative & Identity Bible Agent",
        "endpoint": "https://labs.google/",
        "phase": "Phase 3: 0-Credit Identity & Style Prototyping",
        "deliverables": ["03_identity_bible.md", "assets/character_anchor.png", "assets/product_anchor.png"],
    },
    {
        "agent_id": "agent_4_google_flow_director",
        "showrunner_roles": ["A5", "A7"],
        "name_ar": "وكيل جوجل فلو للإخراج السينمائي",
        "name_en": "Google Flow DoP & Video Producer Agent",
        "endpoint": "https://flow.google.com/",
        "phase": "Phase 4 & 7: 06_package.json & Veo 3.1 / Omni 1.1 Generation",
        "deliverables": ["06_package.json", "08_flow_runlog.md", "assets/scene_01..06.mp4"],
    },
    {
        "agent_id": "agent_5_flowmusic_audio_dsp",
        "showrunner_roles": ["A6", "A12"],
        "name_ar": "وكيل فلو ميوزك والهندسة الصوتية الإذاعية",
        "name_en": "FlowMusic, Broadcast TTS & -14 LUFS Mastering Agent",
        "endpoint": "https://www.flowmusic.app/session",
        "phase": "Phase 3 & 8: Musical Stems, Whisper-Verified TTS & -14 LUFS Master",
        "deliverables": ["05_audio_map.md", "09_post_plan.md", "vo_full.wav", "master.wav"],
    },
    {
        "agent_id": "agent_6_google_search_grounding",
        "showrunner_roles": ["A1"],
        "name_ar": "وكيل بحث جوجل للتوثيق المعرفي",
        "name_en": "Google Search Grounding & Capability Verification Agent",
        "endpoint": "https://www.google.com/",
        "phase": "Phase 1: 5-Batch Web Research & Verified Capabilities Ledger",
        "deliverables": ["01_research.md", "facts.md"],
    },
    {
        "agent_id": "agent_7_cross_model_critic_code",
        "showrunner_roles": ["A4", "Alt"],
        "name_ar": "وكيل المراجعة النقدية وهندسة التحريك العابر للنماذج",
        "name_en": "Cross-Model Critique & 60fps 3D/2D Motion Architect",
        "endpoint": "https://chatgpt.com/ + https://claude.ai/new",
        "phase": "Phase 3 & 5: 04_style_bible.md, 60fps 3D Stage & Second-Opinion QA",
        "deliverables": ["04_style_bible.md", "scenes/*.js", "renders/final.mp4"],
    },
]

SHOWRUNNER_13_ROLES: List[str] = [
    "A1_Research_and_Trends",
    "A2_Script_and_Strategy",
    "A3_Visual_Lab_and_Identity_Bible",
    "A4_2D_3D_60fps_Motion_Engine",
    "A5_Director_of_Photography",
    "A6_Sound_Music_and_Broadcast_DSP",
    "A7_Flow_Producer",
    "A8_Auditor_and_Red_Team_QA",
    "A9_Developer_and_Automation",
    "A10_Marketing_and_Growth",
    "A11_Compliance_and_Brand_Safety",
    "A12_Post_Production_and_Mastering",
    "Alt_Cross_Model_Second_Opinion",
]


def compute_vocalized_letter_ratio(tts_text: str) -> float:
    """
    Computes the fraction of Arabic base letters (excluding tatweel) that carry
    at least one diacritic mark. Always bounded in [0.0, 1.0].
    Fixes H5: shaddah + fatha on a single letter counts as 1 vocalized letter, not 2.
    """
    base_letters = ARABIC_BASE_LETTER_RE.findall(tts_text)
    if not base_letters:
        return 0.0
    vocalized_letters = VOCALIZED_BASE_LETTER_RE.findall(tts_text)
    return min(1.0, len(vocalized_letters) / len(base_letters))


def validate_arabic_phonetics(
    tts_text: str,
    min_ratio: float = MIN_DIACRITIC_RATIO,
    check_lip_sync_clauses: bool = False,
) -> Dict[str, Any]:
    """
    Validates an Arabic TTS string against the 4 Mandatory Broadcast Phonetic Laws:
    1. Vocalized base-letter ratio >= MIN_DIACRITIC_RATIO (0.75).
    2. Pause-final / clause-final تاء مربوطة (`ة`) in EVERY clause MUST be written as `هْ`.
    3. Zero superscript dagger alifs (`ٰ` U+0670).
    4. Zero banned broken English tech transliterations.
    5. Optional lip-sync clause length check (<= 8 words per breath clause).
    """
    issues: List[str] = []
    text = str(tts_text or "").strip()
    if not text:
        return {
            "valid": False,
            "diacritic_ratio": 0.0,
            "threshold": min_ratio,
            "issues": ["Empty TTS text."],
        }

    if DAGGER_ALIF in text:
        issues.append("Contains superscript dagger alif (U+0670); replace with standard fatha.")

    ratio = compute_vocalized_letter_ratio(text)
    if ratio < min_ratio:
        issues.append(
            f"Insufficient vocalized letter ratio ({ratio:.2f} < {min_ratio:.2f}); "
            "vocalize at least 75% of Arabic base letters."
        )

    # Check pause-final تاء مربوطة at the end of EVERY clause/sentence
    clauses = [c.strip() for c in CLAUSE_SPLIT_RE.split(text) if c.strip()]
    pause_taa_words: List[str] = []
    for clause in clauses:
        words_in_clause = [
            w.strip("\"'()[]«»-—:")
            for w in clause.split()
            if w.strip("\"'()[]«»-—:")
        ]
        if not words_in_clause:
            continue
        last_word = words_in_clause[-1]
        if re.search(r"ة[\u064B-\u0652\u0651]*$", last_word):
            pause_taa_words.append(last_word)
        if check_lip_sync_clauses and len(words_in_clause) > MAX_LIPSYNC_WORDS_PER_PHRASE:
            issues.append(
                f"TTS clause exceeds {MAX_LIPSYNC_WORDS_PER_PHRASE} words "
                f"({len(words_in_clause)} words): '{clause[:40]}...'"
            )

    if pause_taa_words:
        issues.append(
            f"Pause-final تاء مربوطة found at clause boundary ({pause_taa_words}); "
            "rewrite trailing ة as هْ for natural broadcast pause."
        )

    clean_tokens = [re.sub(r"[^\u0621-\u063A\u0641-\u064A]", "", tok) for tok in text.split()]
    for banned in sorted(BANNED_TRANSLITERATIONS):
        if banned in clean_tokens:
            issues.append(f"Banned English transliteration '{banned}' in TTS text; use pure eloquent Arabic.")

    return {
        "valid": len(issues) == 0,
        "passed": len(issues) == 0,
        "diacritic_ratio": round(ratio, 3),
        "threshold": min_ratio,
        "issues": issues,
    }


def build_execution_plan(
    topic: str,
    pipeline_type: str = "route_3_motion_stage_60fps",
    duration_seconds: float = 30.0,
) -> Dict[str, Any]:
    """Builds a structured 7-Agent & 13-Role execution plan for a CineFlow AI Studio project."""
    return {
        "topic": topic,
        "pipeline_type": pipeline_type,
        "duration_seconds": duration_seconds,
        "agent_count": len(SEVEN_AGENT_REGISTRY),
        "showrunner_role_count": len(SHOWRUNNER_13_ROLES),
        "showrunner_roles": SHOWRUNNER_13_ROLES,
        "agents": SEVEN_AGENT_REGISTRY,
        "quality_gates": {
            "phonetic_tts_validation": (
                f">= {int(MIN_DIACRITIC_RATIO * 100)}% vocalized base letters + "
                "clause-final هْ + zero dagger alifs + Whisper medium check"
            ),
            "min_diacritic_ratio": MIN_DIACRITIC_RATIO,
            "slideshow_risk_threshold": "< 3.0",
            "motion_fps": 60,
            "audio_loudness_target_lufs": TARGET_INTEGRATED_LUFS,
            "true_peak_dbtp": MAX_TRUE_PEAK_DBTP,
        },
    }


def main() -> int:
    """CLI entry point for the 7-Agent Orchestrator & Broadcast Phonetic Validator."""
    parser = argparse.ArgumentParser(
        description="CineFlow AI Studio — 7-Agent Orchestrator & Arabic Phonetic Validator"
    )
    parser.add_argument("--topic", "--brief", dest="topic", default="CineFlow AI Studio Showcase")
    parser.add_argument("--pipeline", default="route_3_motion_stage_60fps", help="Pipeline route ID")
    parser.add_argument("--duration", type=float, default=30.0, help="Target duration in seconds")
    parser.add_argument("--validate-script", type=Path, help="Path to script.json to validate phonetically")
    parser.add_argument(
        "--output-plan", "--output", dest="output_plan", type=Path, help="Path to write execution plan JSON"
    )
    args = parser.parse_args()

    if args.validate_script:
        data = json.loads(args.validate_script.read_text(encoding="utf-8"))
        items = data.get("scenes", data) if isinstance(data, dict) else data
        all_valid = True
        for idx, item in enumerate(items, start=1):
            tts_text = item.get("tts_text") or item.get("dialogue_tts_ar") or item.get("text") or ""
            res = validate_arabic_phonetics(tts_text)
            status = "PASS" if res["valid"] else "FAIL"
            print(f"[Line {idx}] {status} (diacritic_ratio={res['diacritic_ratio']})")
            for issue in res["issues"]:
                print(f"  - {issue}")
            if not res["valid"]:
                all_valid = False
        if not all_valid:
            return 1

    plan = build_execution_plan(args.topic, args.pipeline, args.duration)
    if args.output_plan:
        args.output_plan.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote 7-Agent execution plan to {args.output_plan}")
    elif not args.validate_script:
        print(json.dumps(plan, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
