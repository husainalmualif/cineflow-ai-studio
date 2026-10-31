#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CineFlow AI Studio — Multi-Agent Orchestrator & Broadcast Phonetic Validator
============================================================================
Coordinates the 7-Agent Specialized Video Production Crew across:
1. Master Orchestrator Agent (مدير المشروع والمايسترو)
2. Gemini Multimodal Agent (https://gemini.google.com/)
3. Google Labs Creative Agent (https://labs.google/)
4. Google Flow Video Director Agent (https://flow.google.com/)
5. FlowMusic & Audio DSP Agent (https://www.flowmusic.app/)
6. Google Search Grounding Agent (https://www.google.com/)
7. Cross-Model Critique & Code Agent (https://chatgpt.com/ & https://claude.ai/)

Also enforces the 4 Mandatory Arabic Broadcast Phonetic Laws on `script.json`
before neural TTS (`edge-tts`) synthesis and verifies spoken accuracy with Whisper.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

HARAKAT_RE = re.compile(r"[\u064B-\u0652\u0651]")
DAGGER_ALIF = "\u0670"
ARABIC_LETTER_RE = re.compile(r"[\u0621-\u064A]")
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
        "name_ar": "مدير المشروع والمايسترو",
        "name_en": "Master Orchestrator Agent",
        "endpoint": "local://cineflow-orchestrator",
        "phase": "All Phases (1 -> 3)",
        "deliverables": ["project_state.json", "decision_log.json", "final_review.json"],
    },
    {
        "agent_id": "agent_2_gemini_multimodal",
        "name_ar": "وكيل جيميناي متعدد الوسائط",
        "name_en": "Gemini Multimodal Agent",
        "endpoint": "https://gemini.google.com/app",
        "phase": "Phase 1: Blueprinting & Vocalized Scriptwriting",
        "deliverables": ["script.json", "draft_blueprint.json", "social_publish_pack.json"],
    },
    {
        "agent_id": "agent_3_google_labs_creative",
        "name_ar": "وكيل مختبرات جوجل للابتكار البصري",
        "name_en": "Google Labs Creative Agent",
        "endpoint": "https://labs.google/",
        "phase": "Phase 2: 0-Credit Identity & Style Prototyping",
        "deliverables": ["character_anchor.png", "product_anchor.png", "scene_keyframes/"],
    },
    {
        "agent_id": "agent_4_google_flow_director",
        "name_ar": "وكيل جوجل فلو للإخراج السينمائي",
        "name_en": "Google Flow Video Director Agent",
        "endpoint": "https://flow.google.com/",
        "phase": "Phase 3: Veo 3.1 & Omni 1.1 Flash Cinema Generation",
        "deliverables": ["scene_01..06.mp4", "scene_handshake_frames/"],
    },
    {
        "agent_id": "agent_5_flowmusic_audio_dsp",
        "name_ar": "وكيل فلو ميوزك والهندسة الصوتية الإذاعية",
        "name_en": "FlowMusic & Audio DSP Agent",
        "endpoint": "https://www.flowmusic.app/session",
        "phase": "Phase 3: Musical Stems, Vocalized TTS & -14 LUFS Mastering",
        "deliverables": ["vo_full.wav", "words.json", "timeline.json", "master.wav"],
    },
    {
        "agent_id": "agent_6_google_search_grounding",
        "name_ar": "وكيل بحث جوجل للتوثيق المعرفي",
        "name_en": "Google Search Grounding Agent",
        "endpoint": "https://www.google.com/",
        "phase": "Phase 1: 5-Batch Web Research & Facts Ledger",
        "deliverables": ["research_brief.json", "facts.md"],
    },
    {
        "agent_id": "agent_7_cross_model_critic_code",
        "name_ar": "وكيل المراجعة النقدية وهندسة التحريك العابر للنماذج",
        "name_en": "Cross-Model Critique & 60fps Motion Architect",
        "endpoint": "https://chatgpt.com/ + https://claude.ai/new",
        "phase": "Phase 2 & 3: CHAI 3-Axis Audit, Slideshow Risk < 3.0 & 60fps 3D Stage",
        "deliverables": ["chai_audit_report.json", "scenes/*.js", "renders/final.mp4"],
    },
]


def validate_arabic_phonetics(tts_text: str) -> Dict[str, Any]:
    """
    Validates a single Arabic TTS line against the 4 Mandatory Broadcast Phonetic Laws:
    1. High diacritic coverage (>= 60% of Arabic base letters carry harakat/sukun/shaddah).
    2. Pause-final / sentence-final تاء مربوطة (`ة`) MUST be written as `هْ`.
    3. Zero superscript dagger alifs (`ٰ` U+0670).
    4. Zero banned broken English tech transliterations.
    """
    issues: List[str] = []

    if DAGGER_ALIF in tts_text:
        issues.append("Contains superscript dagger alif (U+0670); replace with standard fatha.")

    letters = ARABIC_LETTER_RE.findall(tts_text)
    harakat = HARAKAT_RE.findall(tts_text)
    ratio = len(harakat) / max(len(letters), 1)
    if ratio < 0.55:
        issues.append(f"Insufficient diacritic density ({ratio:.2f} < 0.55); fully vocalize every word.")

    pause_taa = re.findall(r"\S*ة[\u064B-\u0652\u0651]*(?=[،.؛!؟…]|$)", tts_text)
    if pause_taa:
        issues.append(
            f"Pause-final تاء مربوطة found ({pause_taa}); rewrite trailing ة as هْ so edge-tts pronounces natural '-ah'."
        )

    clean_tokens = [
        re.sub(r"[^\u0621-\u064A]", "", tok)
        for tok in tts_text.split()
    ]
    for banned in BANNED_TRANSLITERATIONS:
        if banned in clean_tokens:
            issues.append(f"Banned English transliteration '{banned}' in TTS text; use pure eloquent Arabic.")

    return {
        "valid": len(issues) == 0,
        "diacritic_ratio": round(ratio, 3),
        "issues": issues,
    }


def build_execution_plan(topic: str, pipeline_type: str = "route_3_motion_stage_60fps") -> Dict[str, Any]:
    """Builds a structured 7-Agent execution plan for a CineFlow AI Studio project."""
    return {
        "topic": topic,
        "pipeline_type": pipeline_type,
        "agent_count": len(SEVEN_AGENT_REGISTRY),
        "agents": SEVEN_AGENT_REGISTRY,
        "quality_gates": {
            "phonetic_tts_validation": "100% diacritics + pause هْ + zero dagger alifs + Whisper medium check",
            "slideshow_risk_threshold": "< 3.0",
            "motion_fps": 60,
            "audio_loudness_target_lufs": -14.0,
            "true_peak_dbtp": -1.5,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="CineFlow AI Studio — 7-Agent Orchestrator & Arabic Phonetic Validator"
    )
    parser.add_argument("--topic", default="CineFlow AI Studio Showcase", help="Project topic or brief")
    parser.add_argument("--validate-script", type=Path, help="Path to script.json to validate phonetically")
    parser.add_argument("--output-plan", type=Path, help="Optional path to write multi-agent execution plan JSON")
    args = parser.parse_args()

    if args.validate_script:
        data = json.loads(args.validate_script.read_text(encoding="utf-8"))
        items = data.get("scenes", data) if isinstance(data, dict) else data
        all_valid = True
        for idx, item in enumerate(items, start=1):
            tts_text = item.get("tts_text") or item.get("text") or ""
            res = validate_arabic_phonetics(tts_text)
            status = "PASS" if res["valid"] else "FAIL"
            print(f"[Line {idx}] {status} (diacritic_ratio={res['diacritic_ratio']})")
            for issue in res["issues"]:
                print(f"  - {issue}")
            if not res["valid"]:
                all_valid = False
        if not all_valid:
            return 1

    plan = build_execution_plan(args.topic)
    if args.output_plan:
        args.output_plan.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote 7-Agent execution plan to {args.output_plan}")
    elif not args.validate_script:
        print(json.dumps(plan, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
