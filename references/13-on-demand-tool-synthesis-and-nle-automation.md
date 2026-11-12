# 13 — On-Demand Montage Tool Synthesis, Non-Destructive Spine NLE, HyperFrames Seam Gate & Executable Post-Production (`v8.0.0`)

This reference documents the executable post-production engines, multi-NLE timeline exporters, on-the-fly montage tool factory, non-destructive spine operations, HyperFrames v2 seam/check contracts, and `ManimCE` AST security gates integrated into **`cineflow-ai-studio v8.0.0`**.

---

## 1. Rule Zero Capability Probe & 4-Tier On-Demand Tool Synthesis (`صناعة أدوات المونتاج الفورية عند عدم توفرها`)

Before planning edits or rendering (`A0_Probe`), execute **`scripts/post_production_engine.py probe`** (or **`scripts/on_demand_tool_synthesizer.py probe-gaps`**) to inspect available binaries (`ffmpeg`, `ffprobe`, `whisper`, `node`, `npx`, `blender`, `manim`, `aerender`) and fingerprint source media (`SHA-256`, HDR `HLG/PQ`, rotation `90°/270°`, `bt601`/`pc` full-range streams).

Whenever an external editing suite, plugin, or runtime is unavailable, **never block delivery**—immediately synthesize a verified replacement tool via **`scripts/on_demand_tool_synthesizer.py`**:

| Missing Software / Capability | On-Demand Synthesis Command (`synthesize <kind>`) | What CineFlow Builds & Verifies Instantly |
| :--- | :--- | :--- |
| **Desktop NLE Missing (`Premiere`, `Resolve`, `CapCut` unavailable)** | `python scripts/on_demand_tool_synthesizer.py synthesize browser_nle_studio --output-dir studio/nle --package 06_package.json` | Single-file zero-dependency **HTML5 Canvas + WebAudio Non-Destructive NLE Studio (`cineflow_studio_editor.html`)** + `render_master.sh` (`Blade`, `4-Window FULL/CARD/SIDE/NONE`, `J/L-Cut`, RTL captions, `9:16` safe-zone overlay, 1-click JSON export). |
| **Motion Runtime Missing (`Node`, `Remotion`, `HyperFrames` unavailable)** | `python scripts/on_demand_tool_synthesizer.py synthesize standalone_ffmpeg_cutter --output-dir studio/tools` | Self-contained Python CLI (`auto_montage_cli.py`, AST-verified) for adaptive silence cutting, `9:16` face-centered reframing (`crop + lanczos`), and linear `bt709/tv` LUFS mastering. |
| **External SFX Library Missing** | `python scripts/on_demand_tool_synthesizer.py synthesize procedural_sfx_pack --output-dir studio/sfx` | Zero-sample `48 kHz` broadcast `.wav` pack (`whoosh_up`, `whoosh_down` `< 3 kHz`, `pop`, `tick`, `thud`, `riser`, `phone_top_pluck`) + `sfx_manifest.json` with measured acoustic `_lead_s`. |
| **Scientific / Math / Engineering Diagram Needed (`Tool #23: ManimCE`)** | `python scripts/on_demand_tool_synthesizer.py synthesize manim_scientific_scene --output-dir studio/manim` | AST-scanned `ManimCE` scene (`manim_scene.py`, blocking 25 dangerous modules & 15 builtins) ready for `--transparent` ProRes 4444 / WebM alpha compositing. |
| **Bespoke 60fps HTML/GSAP `Atelier` Stage Needed** | `python scripts/on_demand_tool_synthesizer.py synthesize hyperframes_atelier_bundle --output-dir studio/atelier` | Full `HyperFrames` bundle (`index.html` with opaque `#root` White-Flash Guard + `<template>` scene + `*.motion.json` expectations + `ledger.json` Vector-Law seam manifest). |

---

## 2. Multi-NLE Final Timeline & Desktop Motion Exporters (`scripts/nle_project_exporters.py`)

Deliver editable project timelines alongside `.mp4` masters so human editors can fine-tune cuts, color, and Arabic typography inside their preferred suite:

```bash
# Export all 6 professional post-production formats in one command:
python scripts/nle_project_exporters.py export-all studio/project/06_package.json --output studio/project/nle_exports

# Or target a specific NLE / 3D / Compositing suite:
python scripts/nle_project_exporters.py capcut studio/project/06_package.json --output studio/project/capcut_draft
python scripts/nle_project_exporters.py fcpxml studio/project/06_package.json --output studio/project/timeline.fcpxml
python scripts/nle_project_exporters.py edl studio/project/06_package.json --output studio/project/timeline.edl
python scripts/nle_project_exporters.py resolve studio/project/06_package.json --output studio/project/resolve_setup.py
python scripts/nle_project_exporters.py after-effects studio/project/06_package.json --output studio/project/ae_comp.jsx
python scripts/nle_project_exporters.py blender studio/project/06_package.json --output studio/project/blender_rig.py
```

1. **CapCut Desktop (`draft_content.json` `v183+`)**: Microsecond (`1,000,000 µs`) timeline tracks (`Video Spine`, `ProRes 4444 Alpha Overlays`, `RTL Cairo Captions` with semantic word anchors `"S1:كلمة-0.1"`, `Voiceover + Music + SFX`).
2. **Premiere Pro / Final Cut Pro / DaVinci Resolve (`FCPXML v1.10` & `CMX 3600 EDL`)**: Rational frame-accurate timecodes, `beat_grid.py` sequence markers, J/L-cut audio roles, and RTL title lanes.
3. **DaVinci Resolve Studio (`DaVinciResolveScript`)**: Automates timeline setup, beat/semantic markers, **7-Node DaVinci Wide Gamut (`CST_IN -> Exposure -> Pivot 0.435 -> Skin Magic Mask protecting 123° Vectorscope I-Line -> Vignette -> Halation/Grain -> CST_OUT Rec.709`)**, and Fairlight `-9.5 dB` sidechain ducking.
4. **Adobe After Effects (`.jsx`) & Blender (`bpy`)**: Self-sizing `sourceRectAtTime` RTL Arabic pills + `AgX` `TRACK_TO` dolly camera rigs.

---

## 3. Dual Loudness Law, Zero-Loss Voice/Color & Waveform Word Snapping (`scripts/post_production_engine.py`)

1. **Dual Loudness Calibration Law (`compute_dual_loudness_and_zero_loss_plan`)**:
   - **Real Human Presenter (`source_type = "own"`)**: Default `0 dB` untouched dynamics, or a **single linear fixed gain (`volume=<diff>dB`)** targeting **`-20.0 LUFS`** clamped by **`-1.0 dBTP`**. Never apply dynamic normalizers (`dynaudnorm` / `acompressor`) to real human speech.
   - **AI TTS & Commercial Mixes (`source_type = "ai_tts"`)**: Lookahead-limited linear loudnorm (`loudnorm=linear=true`) targeting **`-14.0 LUFS`** (`<= -1.5 dBTP`) with `-9.5 dB` sidechain music ducking and a **Phone-Speaker Translation Layer (`phone_top_pluck`: `420–3200 Hz` FM pluck + `5.2–10 kHz` crisp hat)**.
2. **Zero-Loss Post-Render Gates**:
   - **Voice Subtraction Gate (`verify_zero_loss_voice_correlation`)**: `corr(voice_ref, mix - sfx) >= 0.999` and `|ΔRMS| < 0.15 dB`.
   - **Color & Bitstream Gate (`build_zero_loss_bt709_pipeline`)**: `yuv444p` `bt709 / tv` intermediate + `-bsf:v h264_metadata` tags (`|ΔY| <= 0.6`, `|ΔU|, |ΔV| <= 0.4`, `|ΔR - ΔB| <= 0.8`).
3. **Container-Safe Silence Cutting & Waveform Word Snapping**:
   - Always probe with `ffmpeg -i src.mov -c:v copy -sn -dn -af silencedetect=...` (copying video instead of `-vn` prevents MOV/MPEG-TS audio timestamp drift), never use raw `-f concat -c copy` on variable-framerate phone clips, chain `atempo` stages (`build_chained_atempo_filter`) when speeding up silence `> 2.0x`, snap word starts via `120 Hz` HPF energy onset (`-20ms` pre-lead), and strip duplicate retakes (`SequenceMatcher >= 0.60`).

---

## 4. HyperFrames Unified `check` Gate & Motion Doctrine Vector Law

1. **Unified Pre-Render Gate (`npx hyperframes validate` is Deprecated)**:
   - Replace legacy `validate` / `inspect` / `layout` calls with the unified single-Chrome gate:
     ```bash
     npx hyperframes lint --json
     npx hyperframes check --json --snapshots --caption-zone
     npx hyperframes snapshot --review --json
     ```
2. **12-Rule Render Contract & White-Flash Guard**:
   - Wrap sub-compositions in `<template>`, match `#root` / host / `window.__timelines["<id>"]` IDs verbatim, use `gsap.fromTo()` (never `gsap.from()` or `tl.add()` across sub-comps), paint `#root` with an explicit opaque background (`#050811`) + ping-pong `data-track-index="0|1"`, ship Arabic fonts locally in `assets/fonts/` via `@font-face`, and pass `--model small --language ar` to `npx hyperframes transcribe`.
   - Compute beat frames from index `Math.round(index * fps * 60 / BPM)` (never cumulative rounded addition) and place SFX peaks **+1 frame after** the visual cut (light leads sound).
3. **Vector Law & Seam Ledger (`validate_hyperframes_vector_seams`)**:
   - Exit of Scene `A` dictates entry of Scene `B`: matching axis (`X/Y/Z`), matching Z-scale derivative sign (`1->1.2` pairs with `0.75->1`), symmetric peak-velocity curves (`power4.in` -> `power4.out` `Cut the Curve` `±230px`), and `Nudge Curve` 3-stage settle tail (`tail >= 3x launch`).

---

## 5. Pipelines 13 & 14 + Advanced Arabic Depth Typography (`headGap` & Ruqaa `ZWJ`)

- **`route_13_product_review_reel` (`مراجعات المنتجات المتتبعة`)**: Combines non-linear focus time-mapping (`tmap`), `PyrLK + RANSAC Homography` label tracking (`DEPTH.box`), `DeepFilterNet` voice isolation, animated spec/discount cards, and a mandatory pricing/facts `qa.jpg` audit sheet.
- **`route_14_isometric_machine_explainer` (`شرح الآلات الإيزومتري المقصوص`)**: Locks `facts.md` first, then builds 3-layer (`back / mid / front`) cutaway machine cross-sections drawn via ink-wave reveal over `2.4s` before physical mechanical actuation.
- **4-Layer Depth Relighting (`BiRefNet + pymatting + depth.js`) & `headGap` (`arabic_helpers.py`)**:
  - Parallax ratios `{room: 0.72, back: 0.86, person: 1.0, front: 1.55}`; background glow words illuminate the wall and hair/shoulder rim **without** tinting presenter skin.
  - `compute_behind_head_kashida_gap()` stretches only the connecting Kashida bar across the speaker's head width so 100% of Arabic base letters and dots remain visible to the right and left of the head, and `patch_ruqaa_taa_marbuta_zwj()` injects `\u200D` before isolated `ة` in `Aref Ruqaa` fonts so its two dots never vanish.
