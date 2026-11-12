# Changelog — CineFlow AI Studio

All notable changes to `cineflow-ai-studio` are documented in this file.

## [8.0.0] — 2026-11-11
### Added & Upgraded (Comprehensive Video Production Agent, Google Flow Omni 1.2 Unification, Multi-NLE Exporters & On-Demand Tool Factory)
- **Executable Post-Production & Zero-Loss Signal Engine (`scripts/post_production_engine.py`)**:
  - Added Rule Zero capability & source media fingerprinter (`probe_environment_and_media`: `SHA-256`, HDR `HLG/PQ`, mobile rotation `90°/270°`, `bt601`/`pc` full-range stream checks).
  - Added 3-mode adaptive silence cutter (`plan_adaptive_silence_cuts`: `remove`, `speed_up` with chained `atempo` filters for `> 2.0x`, `mark`; container-safe `-c:v copy` detection commands and `120ms/150ms` Arabic breath/consonant padding).
  - Added `120 Hz` HPF waveform word-onset snapper (`snap_word_timestamps_to_waveform` with `-20ms` visual pre-lead) and duplicate retake + Whisper hallucination loop detector (`detect_retakes_and_whisper_hallucinations`).
  - Added zero-sample `48 kHz` procedural broadcast WAV synthesizer (`synthesize_procedural_sfx_wav`: `18` sounds including `< 3 kHz` warm `whoosh_up/down`, Shepard `riser`, Doppler `swoosh_pass`, and `phone_top_pluck` `420–3200 Hz` mobile beat translation with automatic acoustic `_lead_s` calculation).
  - Enforced the **Dual Loudness & Zero-Loss Voice/Color Law**: `-20.0 LUFS` linear fixed-gain (`<= -1.0 dBTP`, zero dynamic compressor pumping) for real human voice (`own`) verified via waveform subtraction (`corr >= 0.999`, `|ΔRMS| < 0.15 dB`), `-14.0 LUFS` lookahead-limited linear loudnorm (`<= -1.5 dBTP`) for synthetic/commercial mixes, `bt709/tv` `yuv444p` intermediates, and Scale-to-COVER beat-locked FFmpeg filtergraph generation.
- **Multi-NLE Final Timeline & Desktop Motion Exporters (`scripts/nle_project_exporters.py`)**:
  - Added frame-accurate project exporters from `06_package.json` for **CapCut Desktop** (`draft_content.json` + `draft_meta_info.json` in microseconds with semantic word anchors `"S1:كلمة-0.1"` and ProRes 4444 overlay tracks), **Premiere Pro / Final Cut Pro / DaVinci Resolve (`FCPXML v1.10`)**, **Universal `CMX 3600 EDL`**, **DaVinci Resolve Studio (`DaVinciResolveScript` with 7-Node DaVinci Wide Gamut CST protecting the `123°` skin I-line + Fairlight `-9.5 dB` ducking)**, **Adobe After Effects (`.jsx` ExtendScript)**, and **Blender 4.x/5.x (`bpy` `AgX` `TRACK_TO` camera rigs)**.
- **On-Demand Montage & Editing Tool Synthesizer (`scripts/on_demand_tool_synthesizer.py` & `references/13-on-demand-tool-synthesis-and-nle-automation.md`)**:
  - Built 5 instant fallback tool generators (`browser_nle_studio` single-file HTML5 Canvas + WebAudio non-destructive timeline editor, `standalone_ffmpeg_cutter`, `procedural_sfx_pack`, `manim_scientific_scene` with 25-module / 15-builtin `AST Security Gate`, and `hyperframes_atelier_bundle` with opaque `#root` White-Flash Guard, `*.motion.json`, and Vector-Law `ledger.json`).
  - Added `NonDestructiveTimeline` (`Source-Time Anchoring` with undoable `blade`, `roll_spine`, `slip`, `detach_voice` J/L-cut, and `4-Window FULL/CARD/SIDE/NONE`), `AssetCache` (`SHA-256` + `events.jsonl`), and `build_billing_recovery_state` (`retry_safe=False` & free `GET` `resume_video_uri` recovery).
- **Google Flow (`flow.google.com`) & HyperFrames Harmonization (`scripts/studio_config.py`, `scripts/arabic_helpers.py`, `scripts/governance_and_omni.py`, `scripts/lint_package.py`)**:
  - Purged remaining `Omni 1.1` legacy durations/references and replaced rebate-triggering film-stock/camera slash macros (`/kodak2383`, `/35mmfilm`, `/arri`) with borderless optical descriptions.
  - Upgraded HyperFrames pre-render gate from deprecated `npx hyperframes validate` to `npx hyperframes check --json --snapshots --caption-zone` + `validate_hyperframes_vector_seams`.
  - Added `route_13_product_review_reel` and `route_14_isometric_machine_explainer`, `patch_ruqaa_taa_marbuta_zwj` (`\u200D` for `Aref Ruqaa`), and `compute_behind_head_kashida_gap` (`headGap`).

## [7.0.0] — 2026-11-06
### Added & Upgraded (Pure Gemini Omni 1.2 Flash Native Edition — `google-flow-director v3.0.0`)
- Upgraded default Google Flow and Interactions API model to **`Gemini Omni 1.2 Flash`** (`macaron_cookie`, `gemini-omni-1.2-flash`, `3–15s` in `1s` steps, `0-credit` conversational edits, multi-speaker dialect routing).

## [6.6.0] — 2026-11-03
### Added
- Complete 22-Tool Creative & Generative Video Ecosystem + 12-Dialect Cultural & Media Psychology Mastery.
