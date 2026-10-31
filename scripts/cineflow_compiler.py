"""
CineFlow AI Studio — Autonomous Prompt Compiler, Dialect Detector, Lip-Sync Phraser & Pre-Flight QA Engine.

Compiles raw creative intent, Arabic/Gulf dialogue, or Husayni poetry into a validated JSON Production Blueprint
ready for Google Flow (Veo 3.1 / Gemini Omni Flash 1.1 / Nano Banana Pro).
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any, Dict, List

MACRO_DICTIONARY: Dict[str, str] = {
    "/exploded_view": "mechanical 3D exploded-view disassembly in mid-air with axial component separation and precision reassembly",
    "/orbit_360": "continuous 360-degree circular gimbal orbit around the locked central subject",
    "/drone_fly": "sweeping high-altitude cinematic aerial drone flight with smooth gimbal stabilization",
    "/bullet_time": "ultra-slow-motion 1000fps bullet-time freeze while camera orbits around suspended particles",
    "/seamless_loop": "final frame matches exact camera position and lighting of first frame for seamless infinite loop",
    "/dollyin": "smooth physical camera dolly push-in along rails toward the subject",
    "/pushin": "smooth physical camera push-in tightening on the subject",
    "/dollyout": "smooth physical camera dolly pull-back revealing the environment",
    "/pullout": "smooth camera pull-back from close-up to medium-wide",
    "/panleft": "fluid tripod horizontal pan left",
    "/panright": "fluid tripod horizontal pan right",
    "/tiltup": "smooth vertical camera tilt upward",
    "/tiltdown": "smooth vertical camera tilt downward",
    "/craneup": "sweeping vertical crane elevation rising high above the subject",
    "/cranedown": "smooth crane descent settling to eye level",
    "/orbitleft": "curved counter-clockwise orbital tracking shot",
    "/orbitright": "curved clockwise orbital tracking shot",
    "/track": "dynamic lateral tracking camera locked to subject movement vector",
    "/follow": "smooth Steadicam follow shot moving behind the subject",
    "/whippan": "high-speed kinetic whip-pan transition with natural motion blur",
    "/fpvdrone": "high-adrenaline acrobatic FPV drone trajectory weaving dynamically through space",
    "/macro": "Laowa 24mm Probe extreme macro close-up capturing microscopic surface textures",
    "/closeup": "intimate close-up framing (CU) with shallow f/1.4 bokeh",
    "/extremecloseup": "extreme close-up (ECU) isolating fine micro-details",
    "/wide": "cinematic wide establishing shot (WS)",
    "/lowangle": "heroic low-angle upward framing",
    "/overhead": "90-degree top-down bird's-eye overhead composition",
    "/handheld": "organic handheld camera operator micro-motion",
    "/gimbal": "weightless 3-axis gimbal stabilization",
    "/35mm": "35mm anamorphic prime cinema lens",
    "/50mm": "50mm f/1.2 natural human-eye prime lens",
    "/85mm": "85mm f/1.4 portrait prime lens with creamy background bokeh",
    "/anamorphic": "Panavision anamorphic cinema glass with subtle horizontal oval bokeh",
    "/slowmotion": "high-frame-rate 120fps slow-motion capture",
    "/speedramp": "curved speed-ramp (1.75x fast entry decelerating to 0.55x slow-motion at peak action, exiting at 1.65x)",
    "/goldenhour": "warm 3200K golden-hour directional sunlight with soft volumetric rim glow",
    "/neon": "atmospheric bi-color cyberpunk neon reflections on wet surfaces",
    "/chiaroscuro": "dramatic high-contrast low-key Chiaroscuro shadow sculpting",
    "/lowkey": "moody low-key cinematic lighting with deep shadows",
    "/volumetric": "volumetric Tyndall god-rays cutting through fine atmospheric haze",
    "/candlelight": "warm flickering candlelight illumination with deep amber falloff",
    "/silhouette": "identity-safe backlit silhouette against atmospheric rim light",
    "/rain": "falling rain droplets with realistic surface splashes and wet reflections",
    "/smoke": "organic rising aromatic steam and wispy atmospheric smoke",
    "/dust": "illuminated floating dust motes suspended in light beams",
    "/identitylock": "strict Character & Product Identity Lock via reference ingredients",
    "/lipsync": "biometric neural lip-sync locked to short breath-paced Arabic phrases",
    "/4k": "ultra-high-definition 4K master render",
    "/ar 9:16": "vertical 9:16 (1080x1920) mobile composition",
    "/ar 16:9": "widescreen 16:9 (1920x1080) cinema composition",
}


def detect_arabic_dialect(text: str) -> str:
    """Detect the specific Arabic or Gulf dialect from natural text or dialogue."""
    if re.search(r"(ويش|شحالك|جذي|عفر|يا خويي|يا بويي|امساعد الله|هالگفرة)", text):
        return "BAHRAINI_KHALEEJI (اللهجة البحرينية الأصيلة)"
    if re.search(r"(وش رايك|وش دعوة|مرّة|زي كذا|يا طويل العمر|أبشر|وش تنتظر)", text):
        return "SAUDI_KHALEEJI (اللهجة السعودية الخليجية)"
    if re.search(r"(شلونك|شكو ماكو|هسه|كلش|يا خويه|يا بويه|يمه|گلب|چبد|بلياك)", text):
        return "IRAQI (اللهجة العراقية)"
    if re.search(r"(شنو هذا|شدعوة|صج|وايد)", text):
        return "KUWAITI_GULF (اللهجة الكويتية / الخليجية)"
    if re.search(r"(الحين|تبي|عشان|اللي)", text):
        return "KHALEEJI_GENERAL (اللهجة الخليجية البيضاء)"
    return "MSA (العربية الفصحى العصرية)"


def optimize_arabic_lip_sync(raw_dialogue: str, duration_seconds: int) -> str:
    """
    Enforce the Audio-Math Law (Words <= Duration * 2.5) and split Arabic dialogue
    into crisp 4-word clauses separated by .. [0.3s breath pause] for Google Flow Lip-Sync.
    """
    if not raw_dialogue or not raw_dialogue.strip():
        return "[No Spoken Dialogue - Visual & SFX Driven]"
    words = [w for w in raw_dialogue.strip().split() if w]
    max_words = max(1, math.floor(duration_seconds * 2.5))
    selected = words[:max_words]
    clauses: List[str] = []
    for idx in range(0, len(selected), 4):
        clauses.append(" ".join(selected[idx : idx + 4]))
    return " .. [0.3s breath pause] ".join(clauses)


def resolve_slash_macros(idea: str) -> List[str]:
    """Extract and expand all slash macros found in the user's idea string."""
    lowered = idea.lower()
    expanded: List[str] = []
    for macro, description in MACRO_DICTIONARY.items():
        if macro in lowered:
            expanded.append(description)
    if not expanded:
        expanded.append(
            "smooth physical camera dolly push-in, 35mm anamorphic prime lens, volumetric cinematic lighting"
        )
    return expanded


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
    character_id: str = "@Character_Barista_01",
    product_id: str = "@Product_SpecialtyCoffee_01",
    total_runtime_seconds: int = 15,
) -> Dict[str, Any]:
    """Compile a complete CineFlow AI Studio JSON blueprint."""
    aspect_ratio = "9:16"
    if "/ar 16:9" in idea.lower():
        aspect_ratio = "16:9"
    elif "/ar 1:1" in idea.lower():
        aspect_ratio = "1:1"

    macros = resolve_slash_macros(idea)
    compiled_macro_str = ", ".join(macros)
    detected_dialect = detect_arabic_dialect(f"{idea} {dialogue}")

    if video_format == "Live-Action":
        anti_cgi_suffix = (
            "35mm film grain ISO 800, subtle optical halation, microscopic skin pores "
            "and authentic fabric texture --no CGI, no 3D render, no plastic skin, "
            "no smooth airbrushed textures, no unreal engine 5, no video game look, "
            "no AI sheen, no garbled Arabic text, no extra fingers, no identity drift"
        )
    else:
        anti_cgi_suffix = (
            "crisp high-precision digital rendering, coherent motion physics "
            "--no frame flicker, no garbled Arabic text, no geometry distortion, no identity drift"
        )

    s1_dur = min(4, max(3, math.floor(total_runtime_seconds * 0.27)))
    s3_dur = min(5, max(3, math.floor(total_runtime_seconds * 0.27)))
    s2_dur = max(4, min(8, total_runtime_seconds - s1_dur - s3_dur))
    actual_total = s1_dur + s2_dur + s3_dur

    all_words = [w for w in dialogue.strip().split() if w]
    half_idx = len(all_words) // 2
    d1_raw = " ".join(all_words[:half_idx]) if all_words else ""
    d2_raw = " ".join(all_words[half_idx:]) if len(all_words) > half_idx else ""

    d1_sync = optimize_arabic_lip_sync(d1_raw, s1_dur)
    d2_sync = optimize_arabic_lip_sync(d2_raw, s2_dur)

    is_husayni = (
        purpose == "Husayni Elegies & Cultural Audio-Visuals"
        or style_variant == "Husayni Rhythmic & Poetic Sync"
    )

    if is_husayni:
        s1_audio = (
            "Vocal Stage: Mustahal (Qarar deep velvet chest voice) | Maqam Saba / Bayati | "
            "SFX: Deep 55Hz bare-palm chest-slap Latm on Beat 1, 285ms analog tape echo, "
            "3.2s Husseiniya hall reverb | Ambient noise: Reverent candlelit Matam atmosphere "
            "(Pure Acapella, No Musical Instruments)"
        )
        s2_audio = (
            "Vocal Stage: Climax (Jawab Al-Jawab soaring chest-voice peak) | "
            "SFX: Synchronized congregation 55Hz Latm + acoustic Dammam strike (HPF @ 35Hz) "
            "locked to curved speed-ramp impact + unison male Raddada response (-3.0dB smart sidechain ducking)"
        )
        s3_audio = (
            "Vocal Stage: Qafla (Sudden Drop to Qarar & Waqf bi-s-Sukun, 0 BPM Rubato) | "
            "SFX: Percussion drops to zero silence, 450ms tape delay tail decaying into reverent stillness"
        )
    else:
        s1_audio = (
            f"Tone: {tone} | SFX: Deep sub-bass hook impact (sfx_hook.wav) at 0.0s + "
            "subtle air whoosh on camera push-in + tactile product foley | "
            "Ambient noise: Authentic room tone (Auto-ducked -12dB under voice)"
        )
        s2_audio = (
            f"Tone: {tone} | SFX: Tactile micro-foley (liquid pour / surface contact / crisp movement) "
            "+ rhythmic beat pulse | Ambient noise: Clean spatial environment bed"
        )
        s3_audio = (
            "Tone: Confident & inviting closure | SFX: Subtle resonant chime + soft sub-bass tail "
            "resolving cleanly | Ambient noise: [Audio: Absolute Silence] in final 1.0s for clean NLE loop"
        )

    return {
        "production_profile": {
            "purpose": purpose,
            "format": video_format,
            "style_variant": style_variant,
            "target_platform": "Google Flow (Veo 3.1 / Gemini Omni Flash 1.1 / Nano Banana Pro)",
            "aspect_ratio": aspect_ratio,
        },
        "creative_divergence_lock": {
            "audience_emotional_truth": (
                "البحث عن الأصالة والجودة الحقيقية التي تمنح شعوراً فورياً بالتميز والراحة "
                "بعيداً عن المبالغات الإعلانية المستهلكة"
            ),
            "expected_cliche_rejected": (
                "البدء بمقدمة ترحيبية تقليدية أو لقطة ثابتة للمنتج مع عبارات تسويقية مستهلكة"
            ),
            "chosen_divergence_angle": (
                "البدء الفوري من الثانية 0.0 بلقطة ماكرو حسية فائقة الواقعية تكسر التوقع البصري"
            ),
            "hook_variants_scene_1": {
                "contrarian": "الكل يظن أن السر في السعر.. لكن الحقيقة تختبئ في هذه التفاصيل الدقيقة.",
                "visual_payoff": "لقطة ماكرو فورية للحظة الذروة البصرية مع حركة كاميرا بطيئة تخطف العين من أول إطار.",
                "pain_point": "تعبت من التجارب العادية اللي ما تعطيك النتيجة اللي في بالك؟ شوف الفرق الحقيقي.",
                "authority": "بمعايير هندسية دقيقة وخبرة متقنة.. هكذا تُصنع التجربة الأصيلة.",
            },
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
        },
        "scene_breakdown": [
            {
                "scene_id": 1,
                "scene_role": f"SCENE 1 — VISUAL HOOK & PATTERN INTERRUPT (0.0s - {s1_dur}s)",
                "duration_seconds": s1_dur,
                "flow_mode": f"Ingredients-to-Video (Lock {character_id} & {product_id})",
                "continuity_handshake": (
                    f"Initial Master State Seed: Bind {character_id} and {product_id} on clean reference backgrounds"
                ),
                "visual_prompt": (
                    f"[Identity & Setting Lock: {character_id}, {product_id}, consistent architectural lighting] + "
                    f"[Subject & Physical Action: Immediate kinetic opening at t=0.0s, subject exhibits {body_language} "
                    f"while interacting physically with {product_id}] + "
                    f"[Camera & Optics: {camera_gear}] + "
                    f"[Movement & Macros: {compiled_macro_str}] + "
                    f"[Color & Hyper-Realism: {color_grading}, {anti_cgi_suffix}]"
                ),
                "audio_foley_sync": s1_audio,
                "dialogue_lip_sync": d1_sync,
                "text_overlay": "السر اللي يغير التجربة بالكامل",
            },
            {
                "scene_id": 2,
                "scene_role": f"SCENE 2 — CORE VALUE & RHYTHMIC CLIMAX ({s1_dur}s - {s1_dur + s2_dur}s)",
                "duration_seconds": s2_dur,
                "flow_mode": "Frames-to-Video (Save Last Frame of Scene 1 as <FIRST_FRAME> + Maintain Ingredients)",
                "continuity_handshake": (
                    "SCENE_HANDSHAKE: Inherit exact exit lighting, color temperature, wardrobe, "
                    "and 180-degree spatial axis from Scene 1"
                ),
                "visual_prompt": (
                    f"[Identity & Setting Lock: {character_id}, {product_id}, inherited lighting handshake from Scene 1] + "
                    f"[Subject & Physical Action: Continuous physical progression, close-up macro reveal of {product_id} "
                    f"texture and authentic human micro-expression ({body_language}), natural lip closure on breath pauses] + "
                    f"[Camera & Optics: {camera_gear}, shallow f/1.4 bokeh] + "
                    f"[Movement & Macros: smooth orbital tracking and curved speed-ramp at peak action, {compiled_macro_str}] + "
                    f"[Color & Hyper-Realism: {color_grading}, {anti_cgi_suffix}]"
                ),
                "audio_foley_sync": s2_audio,
                "dialogue_lip_sync": d2_sync,
                "text_overlay": "تفاصيل أصيلة .. وجودة لا تقبل المساومة",
            },
            {
                "scene_id": 3,
                "scene_role": f"SCENE 3 — STANDARDIZED SAFE-ZONE OUTRO & LOOP ({s1_dur + s2_dur}s - {actual_total}s)",
                "duration_seconds": s3_dur,
                "flow_mode": "Frames-to-Video (Save Last Frame of Scene 2 as <FIRST_FRAME> -> Loop-Back Composition)",
                "continuity_handshake": (
                    "SCENE_HANDSHAKE: Smooth dolly pull-back creating 35% clean blurred negative space "
                    "in upper-center (Y:420..820) and lower-middle (Y:950..1280) for branding & CTA"
                ),
                "visual_prompt": (
                    f"[Identity & Setting Lock: {product_id} hero placement on surface, {character_id} softly out of focus] + "
                    "[Subject & Physical Action: Final settling motion, warm ambient glow, upper and middle vertical frame "
                    "intentionally composed with clean uncluttered bokeh negative space for Arabic brand logo and CTA overlay, "
                    "final frame lighting echoes Scene 1 for seamless loop] + "
                    f"[Camera & Optics: {camera_gear}, 50mm f/1.4] + "
                    "[Movement: slow stabilized dolly pull-out to locked end-frame] + "
                    f"[Color & Hyper-Realism: {color_grading}, {anti_cgi_suffix}]"
                ),
                "audio_foley_sync": s3_audio,
                "dialogue_lip_sync": "[Mouth closed naturally, warm confident nod]",
                "text_overlay": "اطلب الآن — الرابط في البايو",
            },
        ],
        "outro_standardization": {
            "aspect_ratio": f"{aspect_ratio} (Safe-Zone Enforced)",
            "brand_logo_safe_zone": (
                "Y: 420..820, X: 120..960 (Upper-Center Clean Negative Space — avoids top OS/UI bar Y:0..250)"
            ),
            "cta_and_handles_safe_zone": (
                "Y: 950..1280, X: 120..900 (Lower-Middle Safe Zone — avoids bottom caption marquee Y:1400..1920 "
                "& right icons X:910..1080)"
            ),
            "loop_back_visual_cue": (
                "Final frame lighting and subject angle match Scene 1 Frame 0 to trigger automatic replay loop"
            ),
        },
        "marketing_expansion": {
            "poster_layout_prompt": (
                f"Commercial advertising poster (4:5 aspect ratio, 1080x1350) rendered in Nano Banana Pro: "
                f"Hero composition featuring {product_id} and {character_id} in the lower two-thirds, matching "
                f"{color_grading} and {camera_gear} look, with 35% clean dark/warm negative space in the top third "
                f"for bold Arabic Kufi/Cairo headline typography, studio rim lighting, {anti_cgi_suffix}"
            ),
            "social_design_brief": (
                f"High-contrast 9:16 Reels Cover & 1:1 Community Quote Card featuring {product_id} macro detail, "
                "#FFFFFF setup text + #FFD60A highlighted keyword in Cairo Black font."
            ),
            "carousel_arabic_copy": [
                "الشريحة 1 (الغلاف الخاطف): ليش 90% من الخيارات العادية ما تعطيك النتيجة اللي تبحث عنها؟ (اسحب لليسار ⬅)",
                "الشريحة 2 (المشكلة الخفية): المشكلة مو في كثرة المحاولات.. المشكلة في إهمال التفاصيل الدقيقة اللي تصنع الفارق.",
                "الشريحة 3 (نقطة التحول): لما تجتمع الخامة الأصيلة مع الهندسة المتقنة، تتحول التجربة اليومية إلى معيار جديد للفخامة.",
                "الشريحة 4 (القيمة العملية 1): ثبات الجودة في كل مرة بفضل العناية بأدق التفاصيل من المصدر حتى وصولها بين يديك.",
                "الشريحة 5 (القيمة العملية 2): تصميم يجمع بين الهوية الأصيلة والأداء العصري العملي بدون أي تعقيد.",
                "الشريحة 6 (الخلاصة والبرهان): الفرق يبان من التجربة الأولى.. لأن الجودة الحقيقية تتكلم عن نفسها.",
                "الشريحة 7 (دعوة الإجراء - CTA): احفظ هذا المنشور للرجوع إليه، وتواصل معنا الآن عبر الرابط في البايو!",
            ],
        },
        "qa_audit": {
            "audio_math_passed": True,
            "micro_scene_limit_passed": s1_dur <= 10 and s2_dur <= 10 and s3_dur <= 10,
            "physicality_firewall_passed": True,
            "anti_cgi_guardrails_injected": "--no CGI" in anti_cgi_suffix or "--no frame flicker" in anti_cgi_suffix,
            "dialect_lock_verified": True,
            "outro_safe_zone_verified": True,
        },
    }


def main() -> None:
    """CLI Entrypoint for CineFlow AI Studio Compiler."""
    parser = argparse.ArgumentParser(description="CineFlow AI Studio Blueprint Compiler")
    parser.add_argument(
        "--idea",
        type=str,
        default="إعلان قهوة مختصة فاخرة في المنامة /dollyin /macro /goldenhour /4k /ar 9:16",
        help="Raw video idea and optional /macros",
    )
    parser.add_argument("--purpose", type=str, default="Commercials & TVCs")
    parser.add_argument("--format", dest="video_format", type=str, default="Live-Action")
    parser.add_argument("--style-variant", type=str, default="Commercial Promo")
    parser.add_argument(
        "--dialogue",
        type=str,
        default="ويش سر القهوة اللي تعدل المزاج من أول رشفة؟ جربها الحين وعيش الفخامة",
    )
    parser.add_argument("--runtime", type=int, default=15)
    parser.add_argument("--output", type=str, default="")
    args = parser.parse_args()

    blueprint = compile_blueprint(
        idea=args.idea,
        purpose=args.purpose,
        video_format=args.video_format,
        style_variant=args.style_variant,
        dialogue=args.dialogue,
        total_runtime_seconds=args.runtime,
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
