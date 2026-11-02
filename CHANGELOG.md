# Changelog — CineFlow AI Studio

All notable changes to `cineflow-ai-studio` are documented in this file.

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
