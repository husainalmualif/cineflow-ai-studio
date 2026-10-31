"""Unit tests for CineFlow AI Studio Scriptwriter, Prompt Compiler, Kashida Engine, Lip-Sync Phraser, Slideshow Risk Scorer, and QA Validator."""

from scripts.cineflow_compiler import (
    apply_safe_arabic_kashida,
    build_taste_profile,
    check_scene_variation,
    compile_blueprint,
    detect_arabic_dialect,
    generate_keyword_variants,
    optimize_arabic_lip_sync,
    resolve_slash_macros,
    score_providers,
    score_slideshow_risk,
    select_pipeline_route,
    validate_delivery_promise,
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
    assert apply_safe_arabic_kashida("دار", count=3) == "دار"
    assert apply_safe_arabic_kashida("لا", count=3) == "لا"
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


def test_openmontage_governance_scorers() -> None:
    """Verify Taste Profile, 12-Route Pipeline Selector, Slideshow Risk Scorer, Variation Checker, and Provider Scorer."""
    assert select_pipeline_route("Documentaries", "Live-Action", "Montage Sequence") == "route_7_documentary_montage"
    assert select_pipeline_route("Entertainment Videos", "Animation (2D / 3D)", "Short-Form Edits / AMV") == "route_8_character_animation_ink_theater"
    assert select_pipeline_route("Explainer Videos", "360 & Interactive", "Commercial Promo") == "route_9_3d_world_generation"

    taste = build_taste_profile("Commercials & TVCs", "Commercial Promo", "gold")
    assert 1 <= taste["visual_variance"] <= 10
    assert 1 <= taste["motion_intensity"] <= 10
    assert 1 <= taste["information_density"] <= 10

    providers = score_providers("Commercials & TVCs", "Live-Action")
    assert providers["selected_primary"] == "google_flow_veo_3_1"
    assert providers["selected_score"] > 9.0


def test_compile_blueprint_commercial_and_explainer() -> None:
    """Verify full blueprint compilation including programmatic editing timeline, OpenMontage governance, and social publish pack."""
    bp = compile_blueprint(
        idea="إعلان قهوة مختصة /dollyin /macro /goldenhour /4k /ar 9:16",
        purpose="Commercials & TVCs",
        video_format="Live-Action",
        style_variant="Commercial Promo",
        dialogue="ويش سر القهوة اللي تعدل المزاج من أول رشفة؟",
        total_runtime_seconds=15,
    )
    assert bp["production_profile"]["aspect_ratio"] == "9:16"
    assert bp["production_profile"]["pipeline_type"] == "route_1_generative_cinema"
    assert bp["global_parameters"]["total_runtime_seconds"] == 15
    assert "script_and_content" in bp
    assert "post_production_timeline" in bp
    assert "production_governance" in bp
    assert bp["post_production_timeline"]["render_runtime"] == "remotion"
    assert bp["post_production_timeline"]["composition_mode"] == "atelier"
    assert bp["post_production_timeline"]["audio_mastering_spec"]["target_lufs"] == -14.0
    assert bp["post_production_timeline"]["rtl_caption_config"]["post_word_hold_sec"] == 0.45
    assert len(bp["scene_breakdown"]) == 3
    assert bp["scene_breakdown"][0]["layout_mode"] == "R_FULL"
    assert bp["scene_breakdown"][1]["layout_mode"] == "R_LOWER"
    assert bp["scene_breakdown"][1]["hero_moment"] is True
    assert "chai_5_aspect_breakdown" in bp["scene_breakdown"][0]
    assert all(s["duration_seconds"] <= 10 for s in bp["scene_breakdown"])

    risk = score_slideshow_risk(bp["scene_breakdown"])
    assert risk["verdict"] == "strong"
    var_rep = check_scene_variation(bp["scene_breakdown"])
    assert var_rep["verdict"] == "strong"
    prom = validate_delivery_promise(bp["scene_breakdown"])
    assert prom["valid"] is True

    assert bp["qa_audit"]["kashida_and_rtl_caption_verified"] is True
    assert bp["qa_audit"]["calmness_and_hold_laws_verified"] is True
    assert bp["qa_audit"]["slideshow_risk_passed"] is True
    assert bp["qa_audit"]["scene_variation_passed"] is True
    assert bp["qa_audit"]["delivery_promise_verified"] is True
    assert bp["qa_audit"]["chai_critique_and_decision_log_verified"] is True
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
        render_runtime="hyperframes",
    )
    assert explainer_bp["production_profile"]["purpose"] == "Explainer Videos"
    assert explainer_bp["production_profile"]["pipeline_type"] == "route_3_motion_stage_60fps"
    assert explainer_bp["post_production_timeline"]["render_runtime"] == "hyperframes"
    assert explainer_bp["post_production_timeline"]["visual_design_style"] == "glassUI+explainer"
    assert "exploded-view" in explainer_bp["scene_breakdown"][0]["visual_prompt"]
