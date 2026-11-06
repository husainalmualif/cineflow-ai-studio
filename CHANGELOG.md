# Changelog — CineFlow AI Studio

All notable changes to `cineflow-ai-studio` are documented in this file.

## [7.0.0] — 2026-11-06
### Added & Upgraded (Pure Gemini Omni 1.2 Flash Native Edition — `google-flow-director v3.0.0`)
- **Gemini Omni 1.2 Flash Native Architecture (`scripts/studio_config.py`, `scripts/governance_and_omni.py`, `scripts/arabic_helpers.py`, `SKILL.md`, `references/09-google-flow-agent-scenes-and-tools-mastery.md`)**:
  - Upgraded default Google Flow and Interactions API model to **`Gemini Omni 1.2 Flash`** (`flow.google.com` UI: `Omni 1.2 Flash`, internal RPC codename: `macaron_cookie`, Gemini API ID: `gemini-omni-1.2-flash`, Vertex AI slug: `omni-1-2-flash`, released `2026-11-05` at **`$0.07/second` for `720p`** — **30% lower** than Omni 1.1).
  - **Purged 3 Obsolete Legacy Rules (`purged_legacy_rules`)**:
    1. Purged *Single-Speaker Shot Lock / Gender-Morphing Workaround* — replaced by native **Multi-Speaker Conditioning** routing distinct `1-second` voice references to `4+` characters in a single `15s` clip with expressive lip-sync and zero identity/gender drift.
    2. Purged *Avoid Multi-Angle Front-and-Back References in One Shot* — replaced by native **Multi-Modal Reference Adherence** combining model photos, front-and-back garment/product shots, `3-second` motion reference clips, and `1-second` voice cues across `360°` turns and match cuts.
    3. Purged *Mandatory Full Clip Re-Generation on Background/Lighting/Aspect Changes* — replaced by **`0-credit` Multi-Turn Conversational Editing & Motion Transfer** (`macaron_cookie_edit` / `macaron_cookie_edit_360p`) across full `15s` clips.
  - **Integrated the 6 Core Pillars (`core_pillars_v3`) & 3 Native Prompt Templates (`prompt_templates_v3` / `compile_omni_1_2_native_prompt`)**:
    - **Pillar 1**: `360p/720p` Fast Draft (`1 credit/s` at `360p` for `3..10s`, `3 credits/s` at `720p`) ➔ `0-credit` Multi-Turn Conversational Edit & Motion Transfer ➔ `0-credit` `1080p` / `50-credit` `4K` Master Upscale.
    - **Pillar 2**: Native **`3s` to `15s` in `1-second` increments** (`ALLOWED_CLIP_DURATIONS = (3..15)`, `MAX_SINGLE_SHOT_SECONDS = 15`, `Length` slider on `flow.google.com` for `t2v/i2v/r2v`, `3..10s` for `Frames` First-to-Last Keyframe Interpolation & `Extend`).
    - **Pillar 3**: Multi-Modal Reference Adherence (Front/Back Images + `3s` Motion Clips + `1s` Voice Cues).
    - **Pillar 4**: Native Multi-Speaker Conditioning & Direct Arabic Dialect Prefix Law (`يتحدث باللهجة البحرينية: "<النص>"` directly before quoted dialogue).
    - **Pillar 5**: Unbroken Cinematic Camera Control (continuous FPV drone flythroughs guided by architectural reference photos, unbroken crash zoom-outs, and `360°` orbits).
    - **Pillar 6**: Clean `Scenebuilder` Timeline Assembly (approved `1080p/4K` upscaled masters only, `Shot 1 -> Shot N`) + Full-Bleed Borderless Frame Sanitizer (stripping `Kodak Vision3 500T` / film-stock rebate tokens).
- **Updated Schemas & Templates (`resources/blueprint_schema.json`, `resources/flow_pipeline_schema.json`, `templates/flow_agent_project_init.template.json`)**:
  - Expanded `allowed_clip_seconds` to `[3..15]` and `flow_pipeline_schema.json` `duration` enum to `["3s".."15s"]` with `"Omni 1.2 Flash"` as default model.

## [6.6.0] — 2026-11-03
### Added (22-Tool Creative & Generative Video Ecosystem + Human-Level Cultural, Dialect & Media Psychology Mastery)
- **Complete 22-Tool Creative & AI Video Ecosystem (`references/11-22-tool-video-ecosystem-and-nle-mastery.md` & `ECOSYSTEM_22_TOOLS_REGISTRY`)**:
  - Added actionable CLI/API hooks, prompt grammars, camera command tokens, and post-production interchange rules for all **22 tools**:
    - **3D & Motion Graphics (`4`)**: `Blender` (`bpy` headless CLI, AgX/ACEScg, Geometry Nodes), `Cinema 4D` (`c4d` Python SDK, MoGraph Fields Spring, Redshift Cryptomatte AOVs, Cineware), `Adobe After Effects` (`aerender`, JS Expressions `sourceRectAtTime` RTL pills, `.mogrt`), `Apple Motion` (`.motn` Behaviors, FCP Rig publishing).
    - **Professional NLEs (`4`)**: `DaVinci Resolve Studio` (`DaVinciResolveScript`, 7-Node DaVinci Wide Gamut CST pipeline, Magic Mask skin protection, Fairlight `-14.0 LUFS`), `Adobe Premiere Pro` (`FCPXML`/`EDL` beat markers, Essential Sound ducking), `CapCut` (`draft_content.json` microsecond generator), `Wondershare Filmora` (`.wfp`, Silence Detection `-32dB`, AI Audio Stretch).
    - **AI Avatar, Long-Form Storyboard & Cloud Repurposing (`5`)**: `HeyGen` (`Avatar IV` API v2 + vocalized Arabic visemes), `Synthesia` (`Express-2 Avatars`), `MagicLight.AI` (5-stage Character Bible Asset Store + Nano Storyboard 30–50m long-form workflow), `Veed.io` (`Eye Contact` + `Clean Audio`), `OpusClip` (`ClipAnything` virality scoring + `9:16` active-speaker face-tracking).
    - **Frontier Generative Video Models (`9`)**: `Google Veo 3.1`, `Google Flow` (`Omni 1.1 Flash` + `Nano Banana Pro`), `Runway Gen-4` (`Act-One`), `Kling AI 2.1/3.0` (`Elements` + 6-axis Camera Control), `Hailuo AI / MiniMax` (`I2V-01-Director` bracketed camera commands `[Push in, Pan right]` + `S2V-01`), `Wan 2.1/3.0` (`VACE` + `FLF2V`), `Dreamina` (`Seedream 3.0`), `Seedance 2.0` (`@Image1`/`@Video1`/`@Audio1` multi-shot syntax), and `Higgsfield AI Studio` (`Soul ID` + `DoP` presets `SnorriCam`, `Crash Zoom`, `Bullet Time`).
- **Human-Level Arabic Dialectology, Cultural Etiquette & Media Psychology (`references/12-human-cultural-dialects-and-media-psychology.md`)**:
  - Documented the **12-Dialect Sociolinguistic Matrix**, **6 Cultural & Majlis Etiquette Laws** (`Dallah` in left hand, `Finjan` offered with right hand filled one-third, regional `Thobe/Kandura/Dishdasha/Shemagh/Ghutra/Kuma` precision, intergenerational respect), and **Behavioral Media/Advertising Psychology** (Schwartz's 5 awareness stages, Kahneman System 1/2 cognitive ease, Cialdini's triggers, Binet & Field dual-engine law, and 2026 short-form retention gates).
- **Programmable Compilers & CLI Subcommands (`scripts/arabic_helpers.py` & `scripts/lint_package.py`)**:
  - Added `compile_multi_platform_tool_payload` (`lint_package.py tool-payload`) and `audit_cultural_and_dialect_authenticity` (`lint_package.py cultural-audit`), and unified model registry verification dates (`2026-11-03`) across `studio_config.py`, `references/model-registry.md`, and `references/08-model-registry-and-benchmarks.md`.

## [6.5.1] — 2026-11-03
### Added
- **`scripts/lint_package.py`**: CLI for the governance functions that had no entry point (`audit_sfx_governor`, `validate_window_schedule_and_face_guard`, `lint_flow_continuity_and_platform_profile`, `sanitize_flow_video_prompt`, `generate_contract_storyboard_prompt`) with `check` / `sanitize` / `storyboard` sub-commands; wired into SKILL.md Section 4, README and CI.
- `tests/test_lint_package.py` (12 tests): linter behaviour, CLI exit codes, hard JSON-schema validation of blueprint examples, `flow_pipeline_schema.json` validity, template structure.
- `examples/flow_pipeline.example.json`: a schema-valid Flow pipeline sample.
### Changed
- CI runs on a Python `3.9 / 3.11 / 3.12` matrix (MCP dependencies are installed only on Python >= 3.11) and now also runs `--verify-plan` and the new linter.
- `jsonschema` is a hard dev dependency; the schema test no longer skips silently when it is missing.

## [6.5.0] — 2026-11-03
### Added (Google Flow CLI, Scripting `v1.6.0`, Omni Flash UGC & Browser Automation Mastery)
- **Unified Reference & Declarative Pipeline Schema (`references/10-google-flow-cli-scripting-and-automation-mastery.md` & `resources/flow_pipeline_schema.json`)**:
  - Synthesized `google-flow-scripting-skill` (`v1.6.0`), `google-flow-cli`, `google-flow-api` (`omni-flash-video` & `ugc-product-video`), and `Google-Flow-Automation`:
    1. **Surface × Model × Mode × Duration Matrix (`FLOW_SURFACE_MODE_DURATIONS`)** across `flow` and `gemini-api` (`veo-3.1-lite`, `veo-3.1-fast`, `veo-3.1-quality`, `omni-flash`).
    2. **8-Point Continuity & Mechanical Script Linter**: forbids backward references (`"from segment 1"`, `"the same trader"`, `"as before"`, `"still wet"`), token-bleed numbers/hex codes/bracketed set names (`3500K`, `#FFAA00`, `(Market Lane)`), and non-canonical or bare `@PascalCase` handles.
    3. **Contract-Compliant Storyboard Contact-Sheet Generator**: maps `4s -> 2x1`, `6s/8s -> 3x1`, `10s -> 2x2`, opens copy-paste prompt with `GENERATE THE STORYBOARD IMAGE NOW.`, and separates Operator Notes and Approval Checklist.
    4. **Zero-Bot-Flag Chrome CDP (`port 9222`), 5-Stage Agent State Machine & Angular CDK/ProseMirror Selector Map**: documents `aisandbox-root > flow-project-shell`, `.cdk-overlay-pane` mediaType-first switching, `Escape` backdrop dismissal, virtualized `flow-video-tile` hover-to-mount, signed CDN URLs, and declarative `flow.json` chained-keyframe pipelines.
    5. **Exact Credit Table & 6-Step Checkpointed UGC Product Video Pipeline (`ugc_state.json`)**: documents `Omni 1.1 Flash` (`4s=7/4`, `6s=10/5`, `8s=12/6`, `10s=15/7`, `edit=20/10` at `720p/360p`), free `1080p` upscales, `0-credit` `Nano Banana` reference sheets, shared `startImage = endImage` unified anchor stills for seamless loop cuts, and React native prototype value/file setters + `Policy Error` vs `Server Busy` queue classification.
- **Programmable Validators & Generators (`scripts/governance_and_omni.py` & `scripts/cineflow_compiler.py`)**:
  - Added `lint_flow_continuity_and_platform_profile` and `generate_contract_storyboard_prompt` with full unit test coverage in `tests/test_montage.py`.

## [6.4.0] — 2026-11-02
### Added (Google Flow Complete Ecosystem Mastery, Native Dialect Law & Anti-Hallucination Prompt Sanitizer)
- **Google Flow Agent, Voices/Characters/Avatars, Scene Builder & `Mondo Sónico` (`references/09-google-flow-agent-scenes-and-tools-mastery.md` & `templates/flow_agent_project_init.template.json`)**:
  - Added the structured **JSON Project Initialization Brief** (`flow_agent_init` v2.0) for `Flow Agent` (`Agent instructions` + `Agent settings`), locking `@Character` tags, `@Voice` profiles, dialect phonetic lexicons (`باجر -> Baa-gir` with hard `G`, `تقول / دقايق / عقب / قبل` with hard Gulf `G`), and `Scenes` (`Add to scene`, `+ New scene`, `Add clip`, `Extend Veo 3.1 - Lite`) + `Mondo Sónico` multi-track sound design.
  - Updated `references/02-flow-rules.md` and `references/07-field-tested-production-lessons.md` with the **Omni 1.1 Flash Native Dialect Law** (natural dialect orthography + English phonetic brackets without textbook MSA tanween), **Visual-Audio Conditioning Wardrobe Lock** (preventing South-Asian/foreign accent drift), and **Anti-Lens-HUD / Anti-Text-Hallucination Laws**.
- **Programmable Helpers & Sanitizer (`scripts/arabic_helpers.py` & `scripts/governance_and_omni.py`)**:
  - Added `format_omni_flash_dialect_dialogue` to strip textbook MSA tanween/harakat for `Omni 1.1 Flash` native multimodal speech and generate English phonetic brackets.
  - Added `sanitize_flow_video_prompt` to strip numeric lens specs (`85mm f/1.8 Anamorphic`), replace negative text phrases (`no text`, `no subtitles`) with positive optical framing, replace handwritten paper note props, and flatten multi-line prompts into single-line strings for Google Flow's Slate.js editor.

## [6.3.0] — 2026-11-02
### Added (B Studio `v1.0.10` & Video-Edit `v1.1` Mastery Integration)
- **Reference Constitution (`references/b-studio-and-video-edit-mastery.md`)**:
  - Documented the **Zero-Loss Voice & Color Preservation Pipeline** (`48kHz` 24-bit stereo `pcm_s24le` `voice.wav` separate from `16kHz` Whisper `a.wav`, `corr >= 0.999`, `|gain| < 0.15 dB`, `yuv444p` `bt709/tv` intermediate, silent PNG Remotion render, `|ΔY| <= 0.6`, `|ΔR - ΔB| <= 0.8`).
  - Documented **Balanced Two-Line Word-Reveal Captions** (Rule 76 `even(ws, n)` balanced word partitioning with `visibility: 'hidden'` pre-spoken layout lock and `CAPMOVE` collision avoidance).
  - Documented the **4 Window States (`FULL`, `CARD`, `SIDE`, `NONE`)** for `9:16` (`1080×1920`) and `16:9` (`1920×1080`), hair-safe ceiling `fullFloor = face_top_y - 158`, and `baked_faces` guard.
  - Documented the **10 Visual Metaphor Mechanisms** (`odometer`, `dotGrid`, `donutSplit`, `flipCard`, `stackBlocks`, `growBars`, `iconStrip`, `windingPath`, `rings`, `gauge`), the **Vox Paper-Collage Kit** (`15fps` `step(t)` posterized time, `PushPin`, `Yarn`/`yarnPath`, `HandStamp`, `Highlight` with `isolation: 'isolate'`), **Gaze-Raise Cuts**, **Source-Cut Alignment**, and **Interactive NLE Operations (`rollSpine`, `slideSpine`, `slip`, `cutWords`, `capPauses`, `detachVoice`, 5+1 Inspiration Session & Clip Dissection)**.
- **Programmable Validators & Helpers**:
  - Added `split_caption_cards_balanced` in `scripts/arabic_helpers.py`.
  - Added `audit_sfx_governor` and `validate_window_schedule_and_face_guard` in `scripts/governance_and_omni.py` (re-exported in `scripts/cineflow_compiler.py`) with full unit test coverage in `tests/test_montage.py`.

## [6.2.0] — 2026-11-02
### Fixed & Improved (Repository Audit & Code Review Hardening)
- **Modularized Compiler & Pylint Cleanliness**:
  - Split `scripts/cineflow_compiler.py` (previously 1,764 lines) into three focused modules under the 1,000-line limit:
    - `scripts/arabic_helpers.py` (Arabic dialect detection, safe Kashida/Tatweel, lip-sync splitting, ZWJ letter splitter, video-first layout validator).
    - `scripts/governance_and_omni.py` (delivery promise validator, scene variation & anti-slideshow auditor, Gemini Omni Flash stateful payload builder).
    - `scripts/cineflow_compiler.py` (core blueprint compiler and CLI).
  - Fixed missing `Optional, Set` typing imports and `text_ratio` naming in `cineflow_compiler.py` / `governance_and_omni.py`.
  - Removed unused variables/imports in `scripts/beat_grid.py` (`tol_s`, loop cell variable binding), `scripts/make_srt.py` (`Dict`), and `tests/test_cineflow_compiler.py` (`pytest`).
  - Updated empty list assertions (`not errs`) in `tests/test_montage.py`.
- **Unified Naming & Centralized Model Registry**:
  - Unified skill name (`cineflow-ai-studio`) and MCP server name (`cineflow-omni-agent`) in `mcp/project-setup.sh`.
  - Centralized `MODEL_REGISTRY`, `MODEL_REGISTRY_LAST_VERIFIED = "2026-11-02"`, and `OMNI_FLASH_MODEL_DEFAULT` in `scripts/studio_config.py`, read directly by `mcp/server.py` and `mcp/project-setup.sh`.
- **MCP Server Security & Lazy Initialization (`mcp/server.py`)**:
  - Replaced `pickle.load` / `token.pickle` in `upload_to_youtube` with safe JSON serialization (`token.json` via `Credentials.from_authorized_user_file` and `creds.to_json()`).
  - Replaced import-time `genai.Client()` initialization with lazy `_get_client()` initialization that raises a clear error if `GEMINI_API_KEY` / `GOOGLE_API_KEY` is missing.
  - Added `.gitignore` to protect `client_secrets.json`, `token.*`, `.mcp.json`, `.env`, and `*gemini.key`.
- **CI Coverage & Dynamic Reference Verification**:
  - Added `pyproject.toml`, `requirements-dev.txt`, and `scripts/verify_skill_references.py` (automatically checks every file referenced in `SKILL.md` and `README.md` and ensures `evals/evals.json` and `resources/evals.json` stay in sync).
  - Added `mcp/server.py` and `tests/test_omni_agent.py` to `.github/workflows/ci.yml` (`pylint` and `pytest`).
- **Documentation & Attribution**:
  - Streamlined `README.md` as a concise entry point and moved deep architectural documentation to `references/architecture-and-pipelines.md`.
  - Added sample generated files (`examples/generated_perfume_ad.json`, `examples/multi_agent_plan.json`, `examples/script_source.json`) so every command in `README.md` runs out of the box.
  - Documented external source, version (`v4.0.539`), and license attribution for `references/remotion_skills_official/` and added `scripts/sync_remotion_skills.py`.

## [6.1.0] — 2026-11-02
### Added
- Integrated official **Remotion v4.0.539** rules (`references/remotion-v4-mastery.md` and `references/remotion_skills_official/`), including Arabic ZWJ per-letter animation (`split_arabic_letters_zwj`) and video-first layout validation (`validate_video_first_layout`).
- Integrated **Gemini Omni Flash Stateful Interactions API** (`references/gemini-interactions-api.md`, `mcp/server.py`, `mcp/project-setup.sh`, `tests/test_omni_agent.py`).

## [6.0.0] — 2026-11-01
### Added
- Initial unified release combining CineFlow AI Studio, Rhythmic Beat-Locked Montage (`scripts/beat_grid.py`), 7-Agent Orchestrator (`scripts/multi_agent_orchestrator.py`), Showrunner validators (`scripts/validate_package.py`, `scripts/estimate_cost.py`, `scripts/make_srt.py`), and 4 golden examples.
