#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CineFlow governance linter — CLI for the B Studio / Google Flow rule checkers.

Exposes the functions of `governance_and_omni.py` that had no command-line entry point,
so the deterministic pipeline in SKILL.md can actually enforce them.

Sub-commands:
    check      Lint a package JSON: Flow prompt continuity, SFX governor, window/face guard.
    sanitize   Apply the Google Flow / Omni 1.1 Flash prompt sanitizer to a prompt string.
    storyboard Build the contract-compliant storyboard contact-sheet prompt from a spec JSON.

Examples:
    python scripts/lint_package.py check studio/project/06_package.json
    python scripts/lint_package.py check pkg.json --surface flow --model omni-flash --handles @Kwame
    python scripts/lint_package.py check pkg.json --windows windows.json --word-timestamps words.json
    python scripts/lint_package.py sanitize "35mm f/1.4 portrait, no text"
    python scripts/lint_package.py storyboard spec.json

Exit code: 0 = clean, 1 = rule violations (or warnings with --strict), 2 = unreadable input.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arabic_helpers import (  # noqa: E402
    audit_cultural_and_dialect_authenticity,
    compile_multi_platform_tool_payload,
)
from governance_and_omni import (  # noqa: E402
    audit_sfx_governor,
    generate_contract_storyboard_prompt,
    lint_flow_continuity_and_platform_profile,
    sanitize_flow_video_prompt,
    validate_window_schedule_and_face_guard,
)
from validate_package import convert_scene_breakdown_to_package  # noqa: E402

# Package block modes (Google Flow UI names) -> machine mode names in FLOW_SURFACE_MODE_DURATIONS.
BLOCK_MODE_TO_FLOW_MODE: Dict[str, str] = {
    "ingredients": "references-to-video",
    "frames": "first-last-frame",
    "extend": "extend",
    "text": "text-to-video",
}

# Neutral combination that is valid in the platform matrix: used when --model is not given so that
# only the text rules (backward refs, token leaks, em dash, handles) run, without a platform verdict.
NEUTRAL_PROFILE: Tuple[str, str, str, int] = ("flow", "omni-flash", "text-to-video", 8)

_MMSS_RE = re.compile(r"^(\d{1,3}):(\d{2})(?:\.(\d+))?$")


def _load_json(path: str) -> Any:
    """Load a JSON file or raise SystemExit(2) with a readable message."""
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError) as exc:
        print(f"FAIL: cannot read JSON '{path}': {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


def _parse_time_s(raw: Any) -> Optional[float]:
    """Parse seconds from a number or an 'MM:SS' string; return None when unusable."""
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        return float(raw)
    if isinstance(raw, str):
        match = _MMSS_RE.match(raw.strip())
        if match:
            frac = float(f"0.{match.group(3)}") if match.group(3) else 0.0
            return int(match.group(1)) * 60 + int(match.group(2)) + frac
        try:
            return float(raw)
        except ValueError:
            return None
    return None


def extract_sfx_events(package: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Normalize SFX cues from either package layout into the governor's event shape.

    Supported layouts:
      * `project.montage.sfx_cues`: {t_s, layer, name, pre_roll_ms}
      * `audio_map.sfx_cues`:       {t: "MM:SS", cue}
    """
    raw_cues: List[Any] = []
    project = package.get("project")
    montage = project.get("montage") if isinstance(project, dict) else None
    if isinstance(montage, dict) and isinstance(montage.get("sfx_cues"), list):
        raw_cues = montage["sfx_cues"]
    audio_map = package.get("audio_map")
    if not raw_cues and isinstance(audio_map, dict) and isinstance(audio_map.get("sfx_cues"), list):
        raw_cues = audio_map["sfx_cues"]

    events: List[Dict[str, Any]] = []
    for cue in raw_cues:
        if not isinstance(cue, dict):
            continue
        time_s = _parse_time_s(cue.get("t_s", cue.get("t", cue.get("time_s"))))
        if time_s is None:
            continue
        layer = str(cue.get("layer", "")).lower()
        name = str(cue.get("name", cue.get("cue", "sfx"))).strip() or "sfx"
        events.append(
            {
                "time_s": time_s,
                "name": name,
                "category": "transition" if "transition" in layer or "whoosh" in layer else "semantic",
                "lead_s": float(cue.get("pre_roll_ms", 0) or 0) / 1000.0,
            }
        )
    return events


def package_duration_s(package: Dict[str, Any], default: float = 60.0) -> float:
    """Return the package runtime in seconds (project.total_runtime_s) or a default."""
    project = package.get("project")
    if isinstance(project, dict):
        try:
            value = float(project.get("total_runtime_s", 0) or 0)
        except (TypeError, ValueError):
            value = 0.0
        if value > 0:
            return value
    return default


def iter_shot_prompts(package: Dict[str, Any]) -> List[Tuple[int, str, str, int, str]]:
    """Return (block_id, shot_id, flow_mode, duration_s, prompt) for every shot with a prompt."""
    rows: List[Tuple[int, str, str, int, str]] = []
    for index, block in enumerate(package.get("blocks") or [], start=1):
        if not isinstance(block, dict):
            continue
        block_id = block.get("block_id", index)
        flow_mode = BLOCK_MODE_TO_FLOW_MODE.get(str(block.get("mode", "")).strip().lower(), "text-to-video")
        try:
            duration_s = int(block.get("duration_s", 8))
        except (TypeError, ValueError):
            duration_s = 8
        for shot in block.get("shots") or []:
            if isinstance(shot, dict) and shot.get("visual_prompt_en"):
                rows.append((int(block_id), str(shot.get("shot_id", "?")), flow_mode, duration_s, str(shot["visual_prompt_en"])))
    return rows


def lint_package_dict(
    package: Dict[str, Any],
    *,
    surface: Optional[str] = None,
    model: Optional[str] = None,
    handles: Optional[List[str]] = None,
    windows: Optional[List[Dict[str, Any]]] = None,
    word_timestamps: Optional[List[float]] = None,
    face_top_y: int = 578,
) -> Dict[str, Any]:
    """Run every applicable governance check and return a structured report."""
    data = convert_scene_breakdown_to_package(package) if isinstance(package, dict) else {}
    errors: List[str] = []
    warnings: List[str] = []
    notes: List[str] = []

    # 1) Flow prompt continuity & platform profile (per shot).
    platform_enabled = model is not None
    if not platform_enabled:
        notes.append("platform profile skipped (pass --model to verify surface/model/mode/duration)")
    prompts = iter_shot_prompts(data)
    for block_id, shot_id, flow_mode, duration_s, prompt in prompts:
        if platform_enabled:
            result = lint_flow_continuity_and_platform_profile(
                prompt, surface or "flow", str(model), flow_mode, duration_s, handles or []
            )
        else:
            n_surface, n_model, n_mode, n_duration = NEUTRAL_PROFILE
            result = lint_flow_continuity_and_platform_profile(
                prompt, n_surface, n_model, n_mode, n_duration, handles or []
            )
        for err in result["errors"]:
            errors.append(f"block {block_id} shot {shot_id}: {err['code']}: {err['message']}")
        for warn in result["warnings"]:
            warnings.append(f"block {block_id} shot {shot_id}: {warn['code']}: {warn['message']}")
    if not prompts:
        notes.append("no shots with visual_prompt_en found; continuity lint skipped")

    # 2) SFX governor.
    sfx_events = extract_sfx_events(data)
    duration_s = package_duration_s(data)
    if sfx_events:
        sfx_report = audit_sfx_governor(sfx_events, word_timestamps, duration_s)
        errors.extend(f"sfx: {violation}" for violation in sfx_report["violations"])
    else:
        notes.append("no SFX cues found; SFX governor skipped")

    # 3) Window schedule & face guard (needs explicit stage windows).
    stage_windows = windows
    if stage_windows is None and isinstance(data.get("stage_windows"), list):
        stage_windows = data["stage_windows"]
    if stage_windows:
        window_report = validate_window_schedule_and_face_guard(stage_windows, duration_s, face_top_y)
        errors.extend(f"window: {violation}" for violation in window_report["violations"])
    else:
        notes.append("no stage windows provided (--windows or package.stage_windows); window guard skipped")

    return {"valid": not errors, "errors": errors, "warnings": warnings, "notes": notes}


def _cmd_check(args: argparse.Namespace) -> int:
    package = _load_json(args.package)
    if not isinstance(package, dict):
        print("FAIL: top-level package JSON must be an object", file=sys.stderr)
        return 2
    windows = _load_json(args.windows) if args.windows else None
    if isinstance(windows, dict):
        windows = windows.get("windows") or windows.get("stage_windows")
    words = _load_json(args.word_timestamps) if args.word_timestamps else None
    if isinstance(words, dict):
        words = words.get("word_timestamps") or words.get("words")

    report = lint_package_dict(
        package,
        surface=args.surface,
        model=args.model,
        handles=args.handles,
        windows=windows,
        word_timestamps=[float(w) for w in words] if words else None,
        face_top_y=args.face_top_y,
    )
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for line in report["errors"]:
            print("ERROR:", line)
        for line in report["warnings"]:
            print("WARN:", line)
        for line in report["notes"]:
            print("NOTE:", line)
        print("PASS" if report["valid"] else "FAIL", f"({len(report['errors'])} errors, {len(report['warnings'])} warnings)")
    failed = bool(report["errors"]) or (args.strict and bool(report["warnings"]))
    return 1 if failed else 0


def _cmd_sanitize(args: argparse.Namespace) -> int:
    text = sys.stdin.read() if args.prompt == "-" else args.prompt
    print(json.dumps(sanitize_flow_video_prompt(text), ensure_ascii=False, indent=2))
    return 0


def _cmd_storyboard(args: argparse.Namespace) -> int:
    spec = _load_json(args.spec)
    if not isinstance(spec, dict):
        print("FAIL: storyboard spec must be a JSON object", file=sys.stderr)
        return 2
    print(json.dumps(generate_contract_storyboard_prompt(spec), ensure_ascii=False, indent=2))
    return 0


def _cmd_tool_payload(args: argparse.Namespace) -> int:
    try:
        res = compile_multi_platform_tool_payload(
            prompt=args.prompt,
            tool_id=args.tool,
            camera_preset=args.camera,
            duration_s=args.duration,
            handles=args.handles,
        )
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


def _cmd_cultural_audit(args: argparse.Namespace) -> int:
    res = audit_cultural_and_dialect_authenticity(
        script_text=args.script,
        visual_prompt=args.visual_prompt,
        target_dialect=args.dialect,
    )
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res["valid"] else 1


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(description="CineFlow governance linter (SFX governor, window guard, Flow continuity, 22-tool payloads & cultural audit).")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="lint a package JSON file")
    check.add_argument("package", help="path to the package/blueprint JSON")
    check.add_argument("--surface", default=None, help="flow | gemini-api (used only with --model)")
    check.add_argument("--model", default=None, help="e.g. omni-flash, veo-3.1-lite; enables the platform-profile check")
    check.add_argument("--handles", nargs="*", default=None, help="declared @PascalCase handles")
    check.add_argument("--windows", default=None, help="JSON list of stage windows (m/s/e or mode/start_s/end_s)")
    check.add_argument("--word-timestamps", default=None, help="JSON list of spoken-word timestamps in seconds")
    check.add_argument("--face-top-y", type=int, default=578, help="face top Y in px for 9:16 (default 578)")
    check.add_argument("--strict", action="store_true", help="treat warnings as failures")
    check.add_argument("--json", action="store_true", help="print the report as JSON")
    check.set_defaults(func=_cmd_check)

    sanitize = sub.add_parser("sanitize", help="sanitize a Google Flow video prompt")
    sanitize.add_argument("prompt", help="prompt text, or '-' to read stdin")
    sanitize.set_defaults(func=_cmd_sanitize)

    storyboard = sub.add_parser("storyboard", help="build the storyboard contact-sheet prompt")
    storyboard.add_argument("spec", help="path to the storyboard spec JSON")
    storyboard.set_defaults(func=_cmd_storyboard)

    tool_p = sub.add_parser("tool-payload", help="compile a prompt for any of the 22 creative/AI video tools")
    tool_p.add_argument("tool", help="tool_id from ECOSYSTEM_22_TOOLS_REGISTRY (e.g. hailuo_minimax, higgsfield, seedance, davinci_resolve)")
    tool_p.add_argument("prompt", help="visual action prompt")
    tool_p.add_argument("--camera", default="push_in", help="camera move preset (default: push_in)")
    tool_p.add_argument("--duration", type=int, default=8, help="duration in seconds (default: 8)")
    tool_p.add_argument("--handles", nargs="*", default=None, help="optional @PascalCase handles")
    tool_p.set_defaults(func=_cmd_tool_payload)

    cult = sub.add_parser("cultural-audit", help="audit Arabic dialect and Majlis/cultural etiquette")
    cult.add_argument("script", help="spoken Arabic script")
    cult.add_argument("visual_prompt", help="English visual prompt")
    cult.add_argument("--dialect", default="AUTO", help="target dialect code (default: AUTO)")
    cult.set_defaults(func=_cmd_cultural_audit)
    return parser


def main(argv: Optional[List[str]] = None) -> None:
    """CLI entry point."""
    args = build_parser().parse_args(argv)
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
