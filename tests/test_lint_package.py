#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scripts/lint_package.py and for the Flow / package schemas and templates.

Compatible with `pytest -v tests/test_lint_package.py`.
"""

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, Optional, Type

import jsonschema
try:
    import pytest  # type: ignore
except ImportError:
    class _ExcInfo:  # pylint: disable=too-few-public-methods
        """Minimal exception wrapper mirroring `pytest.ExceptionInfo`."""

        def __init__(self, value: BaseException) -> None:
            self.value = value

    class _FallbackRaises:  # pylint: disable=too-few-public-methods
        """Context manager mirroring `pytest.raises` when pytest is absent."""

        def __init__(self, expected_exc: Type[BaseException]) -> None:
            self.expected_exc = expected_exc
            self.value: Optional[BaseException] = None
            self._info = _ExcInfo(Exception())

        def __enter__(self) -> _ExcInfo:
            self._info = _ExcInfo(Exception())
            return self._info

        def __exit__(self, exc_type: Any, exc_val: Any, _tb: Any) -> bool:
            if exc_type is not None and issubclass(exc_type, self.expected_exc):
                self._info.value = exc_val
                return True
            if exc_type is None:
                raise AssertionError(f"Expected {self.expected_exc.__name__} was not raised")
            return False

    class _PytestFallback:  # pylint: disable=too-few-public-methods
        """Lightweight stdlib fallback for `pytest` namespace."""

        CaptureFixture = object

        @staticmethod
        def raises(expected_exc: Type[BaseException]) -> _FallbackRaises:
            """Assert that `expected_exc` is raised within the `with` block."""
            return _FallbackRaises(expected_exc)

    pytest = _PytestFallback()  # type: ignore


ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "scripts"))

from cineflow_compiler import (  # noqa: E402
    ECOSYSTEM_22_TOOLS_REGISTRY,
    audit_cultural_and_dialect_authenticity,
    compile_cineflow_blueprint,
    compile_multi_platform_tool_payload,
)
from governance_and_omni import lint_flow_continuity_and_platform_profile  # noqa: E402
from lint_package import extract_sfx_events, lint_package_dict, main  # noqa: E402


def _blueprint() -> Dict[str, Any]:
    return compile_cineflow_blueprint(
        title="Lint Test",
        purpose="Commercials & TVCs",
        video_format="Live-Action",
        style_variant="Commercial Promo",
        aspect_ratio="9:16",
        total_runtime_seconds=20,
    )


def _load(rel: str) -> Any:
    return json.loads((ROOT_DIR / rel).read_text(encoding="utf-8"))


def test_compiler_output_is_clean_without_platform_profile() -> None:
    """Compiler output passes the text rules; platform profile is skipped without --model."""
    report = lint_package_dict(_blueprint())
    assert report["valid"], report["errors"]
    assert any("platform profile skipped" in note for note in report["notes"])


def test_platform_profile_only_runs_when_model_is_given() -> None:
    """With --model, an Extend block on omni-flash is reported as an unsupported combination."""
    package = _blueprint()
    assert any(block["mode"] == "Extend" for block in package["blocks"])
    strict = lint_package_dict(package, surface="flow", model="omni-flash")
    assert not strict["valid"]
    assert any("UNSUPPORTED_MODE_COMBO" in err for err in strict["errors"])


def test_backward_reference_and_bare_handle_are_flagged() -> None:
    """Backward references, token leaks and bare handles are all reported."""
    package = _blueprint()
    shot = package["blocks"][0]["shots"][0]
    shot["visual_prompt_en"] = "Kwame keeps walking as before, lit by 3500K light."
    report = lint_package_dict(package, handles=["@Kwame"])
    joined = " | ".join(report["errors"])
    assert "BACKWARD_REF" in joined
    assert "TOKEN_LEAK" in joined
    assert "BARE_HANDLE" in joined


def test_sfx_events_are_extracted_from_both_layouts() -> None:
    """SFX cues are normalized from project.montage and audio_map layouts."""
    montage_layout = {"project": {"montage": {"sfx_cues": [{"t_s": 2.0, "layer": "whoosh_transition", "name": "w", "pre_roll_ms": 110}]}}}
    events = extract_sfx_events(montage_layout)
    assert events == [{"time_s": 2.0, "name": "w", "category": "transition", "lead_s": 0.11}]

    audio_layout = {"audio_map": {"sfx_cues": [{"t": "00:10", "cue": "glass chime"}]}}
    events = extract_sfx_events(audio_layout)
    assert events[0]["time_s"] == 10.0 and events[0]["category"] == "semantic"


def test_sfx_governor_flags_tight_spacing() -> None:
    """Two SFX cues closer than 1.0s violate Rule 3."""
    package = _blueprint()
    package["project"]["montage"]["sfx_cues"] = [
        {"t_s": 5.0, "layer": "impact_hit", "name": "hit", "pre_roll_ms": 0},
        {"t_s": 5.4, "layer": "impact_hit", "name": "hit2", "pre_roll_ms": 0},
    ]
    report = lint_package_dict(package)
    assert any("Rule3_MinSpacing" in err for err in report["errors"])


def test_window_guard_flags_short_middle_window() -> None:
    """A 1.0s middle window violates the minimum window hold."""
    windows = [
        {"m": "FULL", "s": 0.0, "e": 5.0},
        {"m": "CARD", "s": 5.0, "e": 6.0},
        {"m": "FULL", "s": 6.0, "e": 15.0},
    ]
    report = lint_package_dict(_blueprint(), windows=windows)
    assert any("Rule79_MinWindowHold" in err for err in report["errors"])


def test_cli_check_exit_codes(tmp_path: Path) -> None:
    """CLI exits 0 when clean, 1 on violations and 2 on unreadable input."""
    good = tmp_path / "good.json"
    good.write_text(json.dumps(_blueprint(), ensure_ascii=False), encoding="utf-8")
    with pytest.raises(SystemExit) as ok:
        main(["check", str(good)])
    assert ok.value.code == 0

    bad_pkg = copy.deepcopy(_blueprint())
    bad_pkg["blocks"][0]["shots"][0]["visual_prompt_en"] = "Same trader, as before."
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(bad_pkg, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(SystemExit) as failed:
        main(["check", str(bad)])
    assert failed.value.code == 1

    with pytest.raises(SystemExit) as missing:
        main(["check", str(tmp_path / "missing.json")])
    assert missing.value.code == 2


def test_cli_sanitize_and_storyboard(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """The sanitize and storyboard sub-commands print valid JSON."""
    with pytest.raises(SystemExit):
        main(["sanitize", "85mm f/1.4 portrait, no text"])
    out = json.loads(capsys.readouterr().out)
    assert out["is_single_line"] and "replaced_numeric_lens_hud_tokens" in out["applied_fixes"]

    spec = tmp_path / "spec.json"
    spec.write_text(json.dumps({"duration_s": 8, "handles": ["@Kwame"]}), encoding="utf-8")
    with pytest.raises(SystemExit):
        main(["storyboard", str(spec)])
    board = json.loads(capsys.readouterr().out)
    assert board["panel_count"] == 3


def test_blueprint_schema_validates_compiler_output_and_examples() -> None:
    """Hard (non-skippable) JSON-schema validation of the blueprint format."""
    schema = _load("resources/blueprint_schema.json")
    validator = jsonschema.Draft7Validator(schema)
    assert not list(validator.iter_errors(_blueprint()))
    for name in (
        "example_01_commercial_promo.json",
        "example_02_explainer_and_story_script.json",
        "example_03_how_to_use_cineflow.json",
        "generated_perfume_ad.json",
    ):
        errors = list(validator.iter_errors(_load(f"examples/{name}")))
        assert not errors, f"{name}: {errors[0].message}"


def test_flow_pipeline_schema_is_valid_and_example_conforms() -> None:
    """The Flow pipeline schema is valid and the shipped example conforms and lints clean."""
    schema = _load("resources/flow_pipeline_schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    example = _load("examples/flow_pipeline.example.json")
    jsonschema.Draft202012Validator(schema).validate(example)

    handles = example["declared_handles"]
    for scene in example["scenes"]:
        result = lint_flow_continuity_and_platform_profile(
            scene["prompt"], "flow", "omni-flash", "references-to-video", 8, handles
        )
        assert result["valid"], result["errors"]


def test_flow_pipeline_schema_rejects_missing_scenes_and_bad_handle() -> None:
    """The Flow pipeline schema rejects missing scenes and non-PascalCase handles."""
    schema = _load("resources/flow_pipeline_schema.json")
    validator = jsonschema.Draft202012Validator(schema)
    assert list(validator.iter_errors({"project": "x"}))
    assert list(validator.iter_errors({"scenes": [{"id": "s1", "prompt": "p"}], "declared_handles": ["@bad-handle"]}))


def test_templates_are_well_formed() -> None:
    """Flow agent init and package templates keep their required top-level structure."""
    init = _load("templates/flow_agent_project_init.template.json")["flow_agent_init"]
    for key in ("version", "project_meta", "dialect_and_voice_engine", "visual_guardrails", "cast_registry", "scene_builder_workflow"):
        assert key in init, f"flow_agent_init missing '{key}'"
    raw = (ROOT_DIR / "templates" / "flow_agent_project_init.template.json").read_text(encoding="utf-8")
    for placeholder in ("{{PROJECT_TITLE}}", "{{PROJECT_SLUG}}", "{{DIALECT_NAME}}"):
        assert placeholder in raw

    package_template = _load("templates/package.template.json")
    for key in ("project", "identity_bible", "blocks", "outro"):
        assert key in package_template, f"package.template.json missing '{key}'"


def test_22_tool_ecosystem_payload_compiler_and_cli(capsys: pytest.CaptureFixture) -> None:
    """All 22 creative and generative tools are registered and compile valid payloads."""
    assert len(ECOSYSTEM_22_TOOLS_REGISTRY) == 22
    hailuo = compile_multi_platform_tool_payload(
        prompt="@Kwame lifts the @AmberFlacon in golden hour light.",
        tool_id="hailuo_minimax",
        camera_preset="orbit_arc",
    )
    assert hailuo["compiled_prompt"].startswith("[Truck left, Pan right]")

    seedance = compile_multi_platform_tool_payload(
        prompt="@Kwame walks through the market.",
        tool_id="seedance",
        duration_s=8,
        handles=["@Kwame"],
    )
    assert "@Image1 (@Kwame)" in seedance["compiled_prompt"]
    assert "Shot 1 (0s-4s):" in seedance["compiled_prompt"]

    higgs = compile_multi_platform_tool_payload(
        prompt="Subject stays centered while neon city spins.",
        tool_id="higgsfield",
        camera_preset="snorricam",
    )
    assert "DoP Preset: SnorriCam" in higgs["compiled_prompt"]

    with pytest.raises(SystemExit) as ok:
        main(["tool-payload", "davinci_resolve", "Apply 7-node DWG grade", "--camera", "push_in"])
    assert ok.value.code == 0
    cli_out = json.loads(capsys.readouterr().out)
    assert cli_out["tool_name"] == "DaVinci Resolve Studio"


def test_cultural_etiquette_and_dialect_authenticity_auditor() -> None:
    """Cultural auditor catches Majlis left-hand Finjan blunders and cross-dialect contamination."""
    clean = audit_cultural_and_dialect_authenticity(
        script_text="يا طويل العمر أبشر بالقهوة السعودية اللي تبيض الوجه",
        visual_prompt="Host holds brass Dallah in left hand and offers Finjan with right hand, filled to the bottom third.",
        target_dialect="SAUDI_NAJDI",
    )
    assert clean["valid"] is True
    assert not clean["violations"]

    bad = audit_cultural_and_dialect_authenticity(
        script_text="وش دعوة يا طويل العمر تعال دلوقتي نشرب القهوة كتير حلوة",
        visual_prompt="Host offers the finjan with his left hand, arabic coffee cup filled to the top, clinking glasses.",
        target_dialect="SAUDI_NAJDI",
    )
    assert bad["valid"] is False
    joined = " | ".join(bad["violations"])
    assert "CulturalEtiquette_MajlisHand" in joined
    assert "CulturalEtiquette_FinjanFill" in joined
    assert "CulturalEtiquette_Modesty" in joined
    assert "DialectContamination" in joined


class _SimpleCapsys:  # pylint: disable=too-few-public-methods
    """Stdlib stdout/stderr capture helper compatible with `pytest.CaptureFixture`."""

    def __init__(self) -> None:
        self.out_buf = io.StringIO()
        self.err_buf = io.StringIO()

    def readouterr(self) -> Any:
        """Read and reset captured stdout and stderr buffers."""
        out_v, err_v = self.out_buf.getvalue(), self.err_buf.getvalue()
        self.out_buf.seek(0)
        self.out_buf.truncate(0)
        self.err_buf.seek(0)
        self.err_buf.truncate(0)
        return type("CapResult", (), {"out": out_v, "err": err_v})()


class TestLintPackageUnittestBridge(unittest.TestCase):
    """Allows running all `test_lint_package.py` checks under standard `python3 -m unittest`."""

    def test_all_lint_and_schema_functions(self) -> None:
        """Execute every lint, schema, template, and CLI test under unittest."""
        test_compiler_output_is_clean_without_platform_profile()
        test_platform_profile_only_runs_when_model_is_given()
        test_backward_reference_and_bare_handle_are_flagged()
        test_sfx_events_are_extracted_from_both_layouts()
        test_sfx_governor_flags_tight_spacing()
        test_window_guard_flags_short_middle_window()
        test_blueprint_schema_validates_compiler_output_and_examples()
        test_flow_pipeline_schema_is_valid_and_example_conforms()
        test_flow_pipeline_schema_rejects_missing_scenes_and_bad_handle()
        test_templates_are_well_formed()
        test_cultural_etiquette_and_dialect_authenticity_auditor()
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            test_cli_check_exit_codes(tmp)
            cap = _SimpleCapsys()
            with redirect_stdout(cap.out_buf), redirect_stderr(cap.err_buf):
                test_cli_sanitize_and_storyboard(tmp, cap)
                test_22_tool_ecosystem_payload_compiler_and_cli(cap)
