"""Unit tests for CineFlow AI Studio Scriptwriter, Prompt Compiler, Dialect Detector, Lip-Sync Phraser, and QA Engine."""

from scripts.cineflow_compiler import (
    compile_blueprint,
    detect_arabic_dialect,
    optimize_arabic_lip_sync,
    resolve_slash_macros,
)


def test_detect_arabic_dialect() -> None:
    """Verify automatic detection across Bahraini, Saudi, Iraqi, Kuwaiti, and MSA dialects."""
    assert "BAHRAINI_KHALEEJI" in detect_arabic_dialect("ويش فيك اليوم يا خويي شحالك")
    assert "SAUDI_KHALEEJI" in detect_arabic_dialect("وش رايك نروح الحين يا طويل العمر")
    assert "IRAQI" in detect_arabic_dialect("شلونك يا خويه گلب وچبد")
    assert "KUWAITI_GULF" in detect_arabic_dialect("شنو هذا صج وايد حلو")
    assert "MSA" in detect_arabic_dialect("إن الجودة الأصيلة تصنع الفارق دائماً")


def test_optimize_arabic_lip_sync_word_limit_and_pauses() -> None:
    """Verify Audio-Math Law (Words <= Duration * 2.5) and breath pause insertion."""
    raw = "كلمة١ كلمة٢ كلمة٣ كلمة٤ كلمة٥ كلمة٦ كلمة٧ كلمة٨ كلمة٩ كلمة١٠ كلمة١١ كلمة١٢"
    # For a 4-second clip, max words = floor(4 * 2.5) = 10 words
    synced = optimize_arabic_lip_sync(raw, duration_seconds=4)
    assert "كلمة١٠" in synced
    assert "كلمة١١" not in synced
    assert ".. [0.3s breath pause]" in synced


def test_resolve_slash_macros() -> None:
    """Verify slash macros expand into physical camera and lighting directives."""
    macros = resolve_slash_macros("مشهد سيارة تسرع /dollyin /neon /4k /ar 9:16")
    joined = " ".join(macros)
    assert "dolly push-in" in joined
    assert "neon" in joined
    assert "4K" in joined
    assert "9:16" in joined


def test_compile_blueprint_commercial_and_explainer() -> None:
    """Verify full blueprint compilation for both Commercial and Explainer video modes."""
    bp = compile_blueprint(
        idea="إعلان قهوة مختصة /dollyin /macro /goldenhour /4k /ar 9:16",
        purpose="Commercials & TVCs",
        video_format="Live-Action",
        style_variant="Commercial Promo",
        dialogue="ويش سر القهوة اللي تعدل المزاج من أول رشفة؟",
        total_runtime_seconds=15,
    )
    assert bp["production_profile"]["aspect_ratio"] == "9:16"
    assert bp["global_parameters"]["total_runtime_seconds"] == 15
    assert "script_and_content" in bp
    assert "full_spoken_script" in bp["script_and_content"]
    assert len(bp["scene_breakdown"]) == 3
    assert all(s["duration_seconds"] <= 10 for s in bp["scene_breakdown"])
    assert bp["qa_audit"]["audio_math_passed"] is True
    assert bp["qa_audit"]["anti_cgi_guardrails_injected"] is True
    assert len(bp["marketing_expansion"]["carousel_arabic_copy"]) == 7

    explainer_bp = compile_blueprint(
        idea="شرح تطبيق ذكي لإدارة الوقت والمهام /exploded_view /orbit_360 /4k /ar 9:16",
        purpose="Explainer Videos",
        video_format="Motion Graphics",
        style_variant="Short-Form Edits / AMV",
        dialogue="تعبت من زحمة المهام اليومية؟ هذا التطبيق يرتب يومك في ثلاث ثواني",
        total_runtime_seconds=15,
    )
    assert explainer_bp["production_profile"]["purpose"] == "Explainer Videos"
    assert "Problem Identification" in explainer_bp["script_and_content"]["narrative_framework"]
    assert "exploded-view" in explainer_bp["scene_breakdown"][0]["visual_prompt"]
