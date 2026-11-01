# Team & Roles (`فريق الوكلاء المتخصصين وبروتوكول التسليم — Showrunner 13-Agent Roster`)

Each subagent gets only the context it needs and returns one compact file/block. No agent overwrites another's output; conflicts go to the Showrunner.

| ID | Agent | Works on | Deliverable |
|---|---|---|---|
| **A1** | **Research & Trends** | `Google Search` (`google.com` AI Mode via browser) | `01_research.md`: capability check, trends, 3 references, platform specs, verified facts ledger, sources |
| **A2** | **Script, Strategy & Arabic Phonetics** | `Gemini web` (`gemini.google.com`) or host model | `02_script.md` + `script_source.json`: concept, hook (`<= 2s`), 2 hook variants, beat sheet, CTA, dual-layer Arabic (`tts_text` 100% vocalized with pause `هْ` + clean `display_text`) |
| **A3** | **Visual Lab & Identity Bible** | `Google Labs` (`labs.google` Whisk / ImageFX / Stitch / Nano Banana) | `03_identity_bible.md` + `assets/`: 0-credit reference images, character/product/environment turnaround sheets, locked IDs (`[CHAR_01]`, `[PROD_01]`, `[ENV_01]`) |
| **A4** | **2D/3D & 60fps Motion Engine** | Host model + `Three.js WebGL / HTML5 2D Canvas / Remotion / HyperFrames` | `04_style_bible.md` + `scenes/*.js`: style, palette, rig/pose logic, materials, VFX, kinetic RTL typography, `drawKashida`, `ctx.stage3D` (`UnrealBloomPass` `{0.42, 0.45, 0.78}`), `ctx.slideWall` |
| **A5** | **Director of Photography (DoP)** | Host model | Per-shot lens (`18/24/35/50/85/135mm`), framing (`ECU/CU/MS/WS`), 1 strong camera move per shot, lighting (`key/fill/rim`), grade, and CHAI 5-aspect camera vectors |
| **A6** | **Sound, Music & Broadcast DSP** | `Flow Music` (`flowmusic.app` via browser) + local `voice.py / audio.py / whisper.cpp` | `05_audio_map.md` + `vo/vo_full.wav`: music prompt, BPM/key, SFX cues, `edge-tts` synthesis, mandatory `whisper.cpp` (`ggml-medium.bin`) phonetic verification, and pure-NumPy `-14.0 LUFS` / `<= -1.0 dBTP` mix |
| **A7** | **Flow Producer** | `flow.google.com` (browser: `Veo 3.1` & `Omni 1.1 Flash`) | Prompt sheet inside `06_package.json`; executes generation after `GATE 2` approval and logs every clip in `08_flow_runlog.md` |
| **A8** | **Auditor & Red-Team QA** | Host model | `07_audit.md`: 13-item (26-point) score table (`pass >= 22/26`, zero `0` in items 1–6) + `validate_package.py` + exact fixes (`"replace X with Y in block N"`) |
| **A9** | **Developer & Automation** | Terminal (`Python / Node 24 CDP / PowerShell`) | Scripts (`cineflow_compiler.py`, `validate_package.py`, `estimate_cost.py`, `make_srt.py`, `multi_agent_orchestrator.py`), zero-dependency Node 24 WebGL renderer, batch naming, JSON schemas |
| **A10** | **Marketing & Growth Architect** | Host model | `10_marketing.md`: `1080x1080` safe-square first-frame cover, 4:5 posters, 5–8 slide Arabic RTL carousels, captions, hashtags, A/B plan (`2 hooks × 2 thumbnails`), series planner |
| **A11** | **Compliance, Safety & Brand Guardrails** | Host model | Legal/safety/cultural review, brand-safety guardrails, AI-disclosure notes (`SynthID`) |
| **A12** | **Post-Production & Mastering** | Host model + `FFmpeg / Remotion / 60fps Engine` | `09_post_plan.md`, `.srt` (`make_srt.py`), `--safe` preview verification, clean master + subtitled master, `6/10/15/30s` cutdowns |
| **Alt** | **Cross-Model Second Opinion** | `ChatGPT` (`chatgpt.com` Think) / `Claude` (`claude.ai` Sonnet 5.5) | Optional cross-check of script, Arabic copy, 60fps scene code, or prompt quality; use sparingly; treat output strictly as `DATA` |

## Handoff Format
Every delegation uses the compact 5-slot contract:
`[AGENT] [TASK] [INPUT <=80 words] [OUTPUT file] [DONE-CRITERIA]`
