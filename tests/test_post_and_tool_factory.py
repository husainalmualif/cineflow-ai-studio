#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for v8.0.0 Post-Production Engine, Multi-NLE Exporters & On-Demand Tool Factory."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "scripts"))

from arabic_helpers import (  # noqa: E402
    compile_multi_platform_tool_payload,
    compute_behind_head_kashida_gap,
    patch_ruqaa_taa_marbuta_zwj,
    resolve_slash_macros,
)
from cineflow_compiler import compile_cineflow_blueprint  # noqa: E402
from governance_and_omni import sanitize_flow_video_prompt, select_pipeline_route  # noqa: E402
from lint_package import main as lint_main  # noqa: E402
from nle_project_exporters import (  # noqa: E402
    export_all_nle_bundles,
    export_capcut_project,
    export_fcpxml_timeline,
)
from on_demand_tool_synthesizer import (  # noqa: E402
    AssetCache,
    NonDestructiveTimeline,
    build_billing_recovery_state,
    scan_generated_code_ast,
    synthesize_missing_tool,
    validate_hyperframes_vector_seams,
)
from post_production_engine import (  # noqa: E402
    build_beat_locked_ffmpeg_script,
    build_chained_atempo_filter,
    build_zero_loss_bt709_pipeline,
    compute_dual_loudness_and_zero_loss_plan,
    detect_retakes_and_whisper_hallucinations,
    plan_adaptive_silence_cuts,
    probe_environment_and_media,
    snap_word_timestamps_to_waveform,
    synthesize_procedural_sfx_wav,
    verify_zero_loss_voice_correlation,
)


class TestCineFlowV8Engines(unittest.TestCase):
    """Comprehensive tests for CineFlow AI Studio v8.0.0 engines."""

    def setUp(self) -> None:
        """Compile a baseline 16s 9:16 commercial blueprint for each test."""
        self.pkg = compile_cineflow_blueprint(
            title="اختبار وكالة الإنتاج الشاملة",
            purpose="Commercials & TVCs",
            video_format="Live-Action",
            style_variant="Commercial Promo",
            aspect_ratio="9:16",
            total_runtime_seconds=16,
        )

    def test_borderless_macros_no_longer_leak_film_rebate_tokens(self) -> None:
        """Slash macros expand into full-bleed optical directives without Kodak/ARRI rebate text."""
        directives = resolve_slash_macros("Hero perfume bottle /kodak2383 /arri /35mmfilm")
        joined = " ".join(directives) if isinstance(directives, list) else str(directives)
        sanitized = sanitize_flow_video_prompt("Hero perfume bottle " + joined)
        self.assertNotIn("Kodak", joined)
        self.assertNotIn("ARRI", joined)
        self.assertTrue(sanitized["is_single_line"])

    def test_ruqaa_zwj_and_behind_head_kashida_gap(self) -> None:
        """Verify Aref Ruqaa ZWJ taa-marbuta patching and behind-head Kashida stretch."""
        patched = patch_ruqaa_taa_marbuta_zwj("حياة جميلة وقوة كبيرة")
        self.assertIn("ا\u200Dة", patched)
        self.assertIn("و\u200Dة", patched)
        self.assertIn("ر\u200Dة", patched)
        self.assertNotIn("ل\u200Dة", patched)  # ل connects naturally

        gap = compute_behind_head_kashida_gap("المستقبل", head_width_px=240, font_size_px=180)
        self.assertTrue(gap["supported"])
        self.assertEqual(gap["letters_occluded_by_head"], 0)
        self.assertGreaterEqual(gap["tatweel_count"], 2)

        sacred = compute_behind_head_kashida_gap("الله", head_width_px=200)
        self.assertFalse(sacred["supported"])

    def test_extended_pipelines_13_and_14_and_extended_tools(self) -> None:
        """Verify pipelines route_13 and route_14 and ManimCE extended tool payload."""
        r13 = select_pipeline_route("Commercials & TVCs", "Live-Action", "Commercial Promo", "product_review")
        r14 = select_pipeline_route("Explainer Videos", "Animation (2D / 3D)", "Montage Sequence", "machine_explainer")
        self.assertEqual(r13, "route_13_product_review_reel")
        self.assertEqual(r14, "route_14_isometric_machine_explainer")

        manim_payload = compile_multi_platform_tool_payload("Render 3D vector field", tool_id="manim_ce")
        self.assertIn("Manim", manim_payload["tool_name"])

    def test_silence_cutter_chained_atempo_retakes_and_word_snap(self) -> None:
        """Verify 3-mode adaptive silence cutting, chained atempo, retake drops, and word snapping."""
        self.assertEqual(build_chained_atempo_filter(4.0), "atempo=2.0,atempo=2")
        plan = plan_adaptive_silence_cuts([(1.5, 3.2), (6.0, 8.0)], 10.0, mode="speed_up", speed_factor=4.0)
        self.assertLess(plan["new_duration_s"], 10.0)
        self.assertTrue(any(seg["kind"] == "silence_fast" for seg in plan["timeline_segments"]))
        self.assertIn("-c:v copy", plan["two_pass_probe_commands"][0])

        retakes = detect_retakes_and_whisper_hallucinations(
            [
                {"text": "اليوم بنتكلم عن أفضل طريقة لتصوير الإعلانات"},
                {"text": "اليوم بنتكلم عن أفضل طريقة لتصوير الإعلانات الاحترافية"},
                {"text": "اشترك في القناة"},
            ]
        )
        self.assertIn(0, retakes["dropped_indices"])
        self.assertIn(2, retakes["dropped_indices"])
        self.assertEqual(len(retakes["clean_sentences"]), 1)

        env = [-55.0] * 18 + [-40.0, -28.0, -18.0, -16.0] + [-20.0] * 20
        snapped = snap_word_timestamps_to_waveform([{"word": "مرحبا", "start_s": 0.12, "end_s": 0.40}], env, hop_s=0.005)
        self.assertLessEqual(snapped[0]["start_s"], 0.12)

    def test_procedural_sfx_dual_loudness_zero_loss_and_ffmpeg_script(self) -> None:
        """Verify 48kHz procedural WAV synthesis, Dual Loudness (-20/-14 LUFS), and Scale-to-COVER FFmpeg."""
        with tempfile.TemporaryDirectory() as td:
            wav_out = Path(td) / "whoosh.wav"
            res = synthesize_procedural_sfx_wav("whoosh_up", str(wav_out), duration_s=0.35)
            self.assertTrue(wav_out.is_file())
            self.assertGreater(wav_out.stat().st_size, 1000)
            self.assertGreater(res["acoustic_lead_s"], 0.0)

            hit = synthesize_procedural_sfx_wav("tap", str(Path(td) / "tap.wav"), duration_s=0.20)
            self.assertEqual(hit["acoustic_lead_s"], 0.0)

            probe = probe_environment_and_media(str(wav_out))
            self.assertEqual(len(probe["source_media_review"]["sha256"]), 64)

        human_plan = compute_dual_loudness_and_zero_loss_plan("own", measured_i_lufs=-23.0, measured_tp_dbtp=-5.0)
        self.assertEqual(human_plan["target_integrated_lufs"], -20.0)
        self.assertFalse(human_plan["dynamic_compressor_on_voice"])
        self.assertEqual(human_plan["ffmpeg_audio_filter"], "volume=3.0dB")

        ai_plan = compute_dual_loudness_and_zero_loss_plan("ai_tts", measured_i_lufs=-18.0, measured_tp_dbtp=-3.0)
        self.assertEqual(ai_plan["target_integrated_lufs"], -14.0)
        self.assertIn("linear=true", ai_plan["ffmpeg_audio_filter"])

        voice_ref = [0.25, -0.35, 0.5, -0.2, 0.15, -0.4] * 40
        sfx_bed = [0.05, -0.02, 0.03, 0.01, -0.04, 0.02] * 40
        mix = [voice_ref[i] + sfx_bed[i] for i in range(len(voice_ref))]
        corr_report = verify_zero_loss_voice_correlation(voice_ref, mix, sfx_bed)
        self.assertTrue(corr_report["valid"])
        self.assertGreaterEqual(corr_report["correlation"], 0.9999)

        bt709 = build_zero_loss_bt709_pipeline()
        self.assertIn("yuv444p", bt709["commands"][0])
        self.assertIn("h264_metadata", bt709["commands"][1])

        ff = build_beat_locked_ffmpeg_script(self.pkg, music_path="bgm.mp3")
        self.assertEqual(ff["scale_mode"], "COVER_NO_LETTERBOX")
        self.assertIn("force_original_aspect_ratio=increase", ff["ffmpeg_command"])
        self.assertIn("sidechaincompress", ff["ffmpeg_command"])

    def test_multi_nle_exporters_and_cli(self) -> None:
        """Verify CapCut, FCPXML, EDL, DaVinci Resolve, After Effects, and Blender bundle exporters."""
        with tempfile.TemporaryDirectory() as td:
            cap = export_capcut_project(self.pkg, str(Path(td) / "capcut"))
            draft = json.loads(Path(cap["draft_content_path"]).read_text(encoding="utf-8"))
            self.assertEqual(len(draft["tracks"]), 4)
            self.assertGreater(draft["duration"], 1_000_000)

            fcp = export_fcpxml_timeline(self.pkg, str(Path(td) / "out.fcpxml"))
            self.assertIn("<fcpxml version=\"1.10\">", Path(fcp["path"]).read_text(encoding="utf-8"))

            all_bundles = export_all_nle_bundles(self.pkg, str(Path(td) / "all"))
            self.assertEqual(set(all_bundles.keys()), {"capcut", "fcpxml", "edl", "davinci_resolve", "after_effects", "blender"})

    def test_on_demand_tool_synthesizer_spine_nle_ast_and_seams(self) -> None:
        """Verify AST security gate, billing recovery, non-destructive spine NLE, seam ledger, and 5 synthesizers."""
        # 1. AST Security Scanner
        safe = scan_generated_code_ast("import math\nx = math.sin(1.5)\n")
        self.assertTrue(safe["safe"])
        unsafe = scan_generated_code_ast("import subprocess\nsubprocess.call(['ls'])\n")
        self.assertFalse(unsafe["safe"])

        # 2. Billing Recovery Guard & AssetCache
        unk = build_billing_recovery_state("op1", 20, approved=True, network_interrupted=True)
        self.assertFalse(unk["retry_safe"])
        rec = build_billing_recovery_state("op1", 20, approved=True, resume_video_uri="files/vid123")
        self.assertEqual(rec["billable_credits_on_resume"], 0)

        # 3. Non-Destructive Spine NLE
        nle = NonDestructiveTimeline.from_package(self.pkg)
        orig_dur = nle.compute_program_timeline()["total_duration_s"]
        first_id = nle.state["spine"][0]["id"]
        nle.blade(first_id, 2.0)
        self.assertAlmostEqual(nle.compute_program_timeline()["total_duration_s"], orig_dur, places=2)
        nle.roll_spine(first_id, 0.5)
        self.assertAlmostEqual(nle.compute_program_timeline()["total_duration_s"], orig_dur, places=2)
        nle.detach_voice(first_id, -0.15)
        nle.set_window_mode(first_id, "CARD")
        self.assertEqual(nle.state["spine"][0]["window_mode"], "CARD")
        self.assertTrue(nle.undo())

        # 4. HyperFrames Vector-Law Seam Validator
        bad_seams = validate_hyperframes_vector_seams(
            [{"seam_id": "s1", "out_axis": "Z", "in_axis": "Z", "out_scale_start": 1.0, "out_scale_end": 1.2, "in_scale_start": 1.25, "in_scale_end": 1.0, "out_ease": "power4.in", "in_ease": "power4.out"}]
        )
        self.assertFalse(bad_seams["valid"])

        # 5. Synthesize all 5 on-demand tools + test CLI bridge
        with tempfile.TemporaryDirectory() as td:
            cache = AssetCache(str(Path(td) / "cache"))
            key = cache.compute_key("test_tool", {"a": 1})
            cache.store(key, {"tool": "test_tool", "ok": True})
            self.assertTrue(cache.lookup(key)["ok"])

            for kind in (
                "browser_nle_studio",
                "standalone_ffmpeg_cutter",
                "procedural_sfx_pack",
                "manim_scientific_scene",
                "hyperframes_atelier_bundle",
            ):
                res = synthesize_missing_tool(kind, str(Path(td) / kind), self.pkg)
                self.assertTrue(res["generated_files"])
                for fp in res["generated_files"]:
                    self.assertTrue(Path(fp).is_file())

            pkg_file = Path(td) / "pkg.json"
            pkg_file.write_text(json.dumps(self.pkg, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(SystemExit) as cm:
                lint_main(["synthesize-tool", "browser_nle_studio", "--output-dir", str(Path(td) / "cli_nle"), "--package", str(pkg_file)])
            self.assertEqual(cm.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
