"""Unit tests for CineFlow AI Studio Scriptwriter, Prompt Compiler, Kashida Engine, Lip-Sync Phraser, and QA Validator."""

from scripts.cineflow_compiler import (
    apply_safe_arabic_kashida,
    compile_blueprint,
    detect_arabic_dialect,
    generate_keyword_variants,
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


def test_apply_safe_arabic_kashida() -> None:
    """Verify Kashida is placed only after connecting letters, after Harakat, and never breaks 'لا' or 'دار'."""
    stretched = apply_safe_arabic_kashida("الفخامة", count=3)
    assert "ـــ" in stretched
    # Non-connecting word 'دار' or 'لا' must not have Kashida inserted
    assert apply_safe_arabic_kashida("دار", count=3) == "دار"
    assert apply_safe_arabic_kashida("لا", count=3) == "لا"
    # Word with Shadda on 'رّ' ('تتحرّك') must place Kashida after 'ح', never after non-connecting 'رّ'
    tashkeel_word = apply_safe_arabic_kashida("تتحرّك", count=2)
    assert "حــرّك" in tashkeel_word


def test_generate_keyword_variants() -> None:
    """Verify Arabic orthographic variants for comment-keyword DM automation."""
    variants = generate_keyword_variants("إبداع")
    assert "إبداع" in variants
    assert "ابداع" in variants


def test_optimize_arabic_lip_sync_word_limit_and_pauses() -> None:
    """Verify Audio-Math Law (Words <= Duration * 2.5) and breath pause insertion."""
    raw = "كلمة١ كلمة٢ كلمة٣ كلمة٤ كلمة٥ كلمة٦ كلمة٧ كلمة٨ كلمة٩ كلمة١٠ كلمة١١ كلمة١٢"
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
    """Verify full blueprint compilation including programmatic editing timeline and social publish pack."""
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
    assert "post_production_timeline" in bp
    assert bp["post_production_timeline"]["audio_mastering_spec"]["target_lufs"] == -14.0
    assert bp["post_production_timeline"]["rtl_caption_config"]["post_word_hold_sec"] == 0.45
    assert len(bp["scene_breakdown"]) == 3
    assert bp["scene_breakdown"][0]["layout_mode"] == "R_FULL"
    assert bp["scene_breakdown"][1]["layout_mode"] == "R_LOWER"
    assert all(s["duration_seconds"] <= 10 for s in bp["scene_breakdown"])
    assert bp["qa_audit"]["kashida_and_rtl_caption_verified"] is True
    assert bp["qa_audit"]["calmness_and_hold_laws_verified"] is True
    assert "first_frame_cover" in bp["marketing_expansion"]
    assert "social_publish_pack" in bp["marketing_expansion"]
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
    assert explainer_bp["post_production_timeline"]["visual_design_style"] == "glassUI+explainer"
    assert "exploded-view" in explainer_bp["scene_breakdown"][0]["visual_prompt"]
