# CineFlow AI Studio — Multi-Agent Orchestrator Architecture (`منظومة الوكلاء السبعة للإنتاج السينمائي والإذاعي المتكامل`)

## 1. Executive Summary & Architectural Philosophy

**CineFlow AI Studio (`استوديو سينما فلو الذكي`)** operates as a **Hierarchical & Event-Driven Multi-Agent Video Production System**. Instead of relying on a single monolithic prompt or a single model's blind spots, a **7-Agent Specialized Crew** collaborates across real-time web research, multimodal scriptwriting, zero-credit visual prototyping, generative cinema direction, programmatic 60fps 3D/2D motion graphics, broadcast audio DSP, and cross-model quality critique.

### Core Architectural Principles
1. **Separation of Planning & GPU Render (`فصل التخطيط المنطقي عن التوليد الفعلي`)**: All research, scriptwriting, CHAI 5-aspect prompt compilation, slideshow-risk scoring, and code verification happen in text/JSON before spending a single video generation credit.
2. **3-Stage Credit Governance (`estimate ➔ reserve ➔ reconcile`)**:
   - **Stage 1 (`0 Credits` — `labs.google` / `Nano Banana 2 Lite` / `ImageFX` / `Whisk`)**: Character/product turnarounds (`@Character_01`, `@Product_01`) and scene-family keyframes.
   - **Stage 2 (`Low/Half Credit` — `flow.google.com` / `Omni 1.2 Flash`)**: `360p` motion test drafts with `0-credit 720p` upscaling and `10–15s` sample-first verification.
   - **Stage 3 (`Master Render` — `Veo 3.1 - Quality / Fast / Lite` / `Seedance 2.0 Standard` + `60fps 3D/2D Motion Engine`)**: Consolidated `8s–10s` master cinema shots interleaved with 60fps programmatic 3D WebGL (`Three.js`) + 2D Canvas motion stages.
3. **Deterministic State Handshake (`بروتوكول المصافحة البصرية والبيانية`)**: Agents never pass unstructured prose. Every handoff is validated against `blueprint_schema.json`, `facts.md` (Facts Ledger), `script.json` (100% vocalized broadcast phonetics), and frame-accurate `Scene Handshake` (`ffmpeg -sseof -0.04`).

---

## 2. System Topology & Orchestration Workflow

```mermaid
flowchart TD
    User(["User Command / Reference URL / Raw Recording"]) --> A1["1. Master Orchestrator Agent\n(مدير المشروع والمايسترو)"]

    subgraph Phase1 ["Phase 1: Grounding & Multimodal Blueprinting"]
        A1 -->|1. 5-Batch Query Dispatch| A6["6. Google Search Grounding Agent\n(https://www.google.com/ — AI Mode)"]
        A6 -->|Verified Facts Ledger & Cultural Pulse| A2["2. Gemini Multimodal Agent\n(https://gemini.google.com/ — Ultra / Argon / Task)"]
        A1 -->|2. Creative Direction & Dialect Lock| A2
    end

    subgraph Phase2 ["Phase 2: Cross-Model Audit & Zero-Credit Visual Lock"]
        A2 -->|Draft Blueprint + 60fps Stage Code| A7["7. Cross-Model Critique & Code Agent\n(https://chatgpt.com/ Think & https://claude.ai/ Sonnet 5.5)"]
        A7 -->|CHAI 3-Axis Audit + Slideshow Risk < 3.0| A3["3. Google Labs Creative Agent\n(https://labs.google/ — Whisk / Stitch / Nano Banana)"]
        A3 -->|0-Credit @Character_01 / @Product_01 Anchors| A4["4. Google Flow Video Director Agent\n(https://flow.google.com/ — Veo 3.1 & Omni 1.2 Flash)"]
    end

    subgraph Phase3 ["Phase 3: Parallel Cinema, 60fps 3D Motion & Audio DSP"]
        A4 -->|Veo 3.1 / Omni 1.2 Flash + Frames/Ingredients| MasterBus["60fps 3D WebGL + 2D Motion & Mastering Engine\n(Three.js + Remotion / HyperFrames + FFmpeg)"]
        A7 -->|Validated 60fps 3D Stage, SlideWall & RTL Kashida| MasterBus
        A2 -->|100% Vocalized Arabic Script (script.json)| A5["5. FlowMusic & Audio DSP Agent\n(https://www.flowmusic.app/session + 4-Bus DSP)"]
        A5 -->|BPM Stems + -14 LUFS Ducking + Whisper-Verified VO| MasterBus
    end

    MasterBus -->|Rendered 60fps MP4 + Contact Sheet| A1
    A1 -->|5-Point Post-Render Final Review| Output(["Master Broadcast Video + Social Publishing Pack"])
```

---

## 3. Specification of the 7 Specialized Agents

### Agent 1: Master Orchestrator Agent (`مدير المشروع والمايسترو`)
- **Primary Role**: Autonomous Executive Producer, Pipeline Router, State Manager, Budget Governor, and Final Quality Gatekeeper.
- **Core Responsibilities**:
  1. **Intent Classification & Pipeline Routing**: Classifies incoming requests into one of the **8 Video Purposes**, **5 Artistic Formats**, and **14 Autonomous Production Pipelines (`route_1` through `route_14`)**.
  2. **Taste Profile Initialization (`taste_profile`)**: Locks the visual direction (`design_read`), 3 integer dials (`visual_variance: 1..10`, `motion_intensity: 1..10`, `information_density: 1..10`), color palette (`midnight`, `ocean`, `gold`, `emerald`, etc.), and `17 Visual Styles`.
  3. **Append-Only Decision Logging (`decision_log`)**: Records provider selection scores across 7 dimensions (motion fidelity, Arabic typography safety, lip-sync accuracy, identity retention, aspect-ratio support, cost efficiency, latency).
  4. **Final Post-Render Gate (`final_review`)**: Executes the 5 mandatory post-render checks (`technical_probe`, `visual_spotcheck >= 4 frames`, `audio_spotcheck`, `promise_preservation`, `subtitle_check`) before approving delivery.

---

### Agent 2: Gemini Multimodal Agent (`وكيل جيميناي متعدد الوسائط`)
- **Target Endpoint**: `https://gemini.google.com/app` (Google AI **Ultra** tier; Mode Picker: **Argon**; **Chat** & **Task** modes; **Notebooks**) + Gemini API (`gemini-3.1-pro` / `gemini-omni-1.2-flash`)
- **Primary Role**: Chief Multimodal Analyst, Arabic Broadcast Scriptwriter, Phonetic Linguist, and CHAI 5-Aspect Prompt Architect.
- **Core Responsibilities**:
  1. **Reference Video Deconstruction (`route_10`)**: Analyzes reference videos frame-by-frame to extract `motion_type` (`motion_clip / animated_still / static_image`), optical flow variance, pacing cadence, and hook mechanics.
  2. **100% Phonetically Vocalized Broadcast Scriptwriting (`script.json`)**:
     - Enforces **100% full Arabic diacritics (`التشكيل الكامل لكل حرف`)** in `tts_text`.
     - Converts every pause-final or sentence-final `تاء مربوطة` (`ة`) into `هْ` (`هاء ساكنة`) in `tts_text` (`وَاحِدَهْ`, `الْمُتَكَامِلَهْ`, `لَقْطَهْ`, `الثَّانِيَهْ`, `الْجَاهِزَهْ`) so neural TTS (`edge-tts`) pronounces a natural `-ah` pause instead of broken `-tu/-ta`.
     - Eliminates all superscript dagger alifs (`ٰ`) and replaces broken English transliterations (`البرومبت`, `تشاي`, `كابشن`, `موشن`) with pure eloquent Arabic in `tts_text`, while preserving clean orthographic Arabic in `display_text`.
     - Enforces the **Lip-Sync Audio-Math Law** (`Words <= Duration_Seconds * 2.5`).
  3. **CMU/Harvard CHAI 5-Aspect Scene Prompting**: Populates `[1. Subject]`, `[2. Subject Motion]`, `[3. Scene]`, `[4. Spatial Framing]`, and `[5. Camera]` for every scene.
  4. **Multi-Format Marketing Expansion**: Generates the `first_frame_cover`, `poster_layout_prompt`, `carousel_arabic_copy`, and platform-distinct `social_publish_pack`.

---

### Agent 3: Google Labs Creative Agent (`وكيل مختبرات جوجل للابتكار البصري`)
- **Target Endpoint**: `https://labs.google/` (`Whisk`, `ImageFX`, `Stitch` at `https://stitch.withgoogle.com/`, `Nano Banana Pro`, `Nano Banana 2 Lite`)
- **Primary Role**: Zero-Credit Visual Concept Designer, Character/Product Identity Anchor Architect, and UI/Style Prototype Specialist.
- **Core Responsibilities**:
  1. **Stage 1 Zero-Credit Prototyping (`0 Credits`)**: Generates high-consistency character turnaround sheets (`@Character_01`), diegetic packaging/product anchors (`@Product_01`), and environment DNA plates (`@Setting_DNA`) using `Nano Banana 2 Lite`.
  2. **Whisk Style & Structure Fusion**: Blends subject, scene, and style reference images to lock visual consistency before video generation begins.
  3. **Stitch UI Prototyping (`stitch.withgoogle.com`)**: Generates clean application UI screens for `route_6_3d_device_explainer` (`31_device3d.js` Three.js iPhone/MacBook mockups).
  4. **Anti-AI Sheen Texture Injection**: Enforces `35mm film grain ISO 800, subtle optical halation, microscopic skin pores and authentic fabric texture --no CGI, no plastic skin, no garbled Arabic text`.

---

### Agent 4: Google Flow Video Director Agent (`وكيل جوجل فلو للإخراج السينمائي`)
- **Target Endpoint**: `https://flow.google.com/` (`/project/<uuid>`, `/tools`, `/create-tool`, `Flow TV`)
- **Primary Role**: Generative Director of Photography (DoP), Motion Continuity Controller, and Scene Handshake Executor.
- **Live Studio Capabilities & Controls**:
  - **Project Asset Libraries**: `All media`, `Images`, `Videos`, `Characters`, `Scenes`, `Uploads`, `Library` collections, and `Tools`.
  - **Prompt Bar & Agent Mode**: Multiline prompt box + `Add ingredients` + `Agent` mode + `Settings trigger`:
    - **Modality**: `Image` | `Video`
    - **Conditioning Mode**: `Frames` (First/Last keyframe interpolation) | `Ingredients` (Consistent character/object reference conditioning)
    - **Aspect Ratio**: `16:9` | `9:16`
    - **Model Family**: `Omni 1.2 Flash`, `Veo 3.1 - Lite`, `Veo 3.1 - Fast`, `Veo 3.1 - Quality`
    - **Resolution & Duration**: `360p` (fast preview) | `720p`; `4s`, `6s`, `8s`, `10s`; batch `x1..x4`.
- **Core Responsibilities**:
  1. **Ingredients & Identity Lock**: Attaches Agent 3's reference plates via `Add ingredients` (`Lock [Character ID: @Character_01]`, `Lock [Product ID: @Product_01]`).
  2. **Stage 2 Draft-First Motion Testing**: Tests camera vectors in `Omni 1.2 Flash` (`360p` -> `720p`) before master rendering.
  3. **Stage 3 Master Cinema Rendering**: Executes `Veo 3.1 - Quality` (`8s–10s` consolidated clips in `9:16` or `16:9`).
  4. **Frame-Accurate Scene Handshake (`المصافحة البصرية`)**: Extracts the final frame of `Scene N` (`ffmpeg -sseof -0.04`) and feeds it into `Frames` mode as the start frame of `Scene N+1`.

---

### Agent 5: FlowMusic & Audio DSP Agent (`وكيل فلو ميوزك والهندسة الصوتية الإذاعية`)
- **Target Endpoint**: `https://www.flowmusic.app/` & `https://www.flowmusic.app/session` + Local Broadcast DSP (`voice.py` + `timeline.py` + `audio.py` + `whisper.cpp`)
- **Primary Role**: AI Music Composer, Broadcast Voiceover Synthesizer, Whisper Phonetic Auditor, Beat-Grid Extractor, and `-14.0 LUFS` Audio Mastering Engineer.
- **Live Studio Capabilities (`flowmusic.app/session`)**:
  - **AI Producer Chat**: Slash commands `/brainstormLyrics`, `/createSongTogether`, `/remixMyMusic`, multimodal audio/image attachment, and voice mode.
  - **Compose Studio**: `Lyrics`, `Instrumental` toggle, `Sound description` (Genre + Time Signature + Instrumentation + Mood + Reverb + BPM + Key), `Advanced` mode, `Turntable`, and `Spaces`.
- **Core Responsibilities**:
  1. **Custom Score & Procedural Beat Bed Generation**: Generates royalty-free cinematic scores in `FlowMusic` or mathematical beat-synced multi-bus beds (`kick`, `clap`, `hat`, `bass`, `pad`, `arp`, and `top` phone speaker layer `400Hz–10kHz`) via `audio.py`.
  2. **100% Vocalized Broadcast TTS + Mandatory Whisper Verification**:
     - Synthesizes `script.json` (`tts_text` with full harakat and pause `هْ`) via `edge-tts` (`ar-SA-HamedNeural`), maps exact word timestamps onto clean orthographic `display_text` words, and runs `whisper.cpp` (`ggml-medium.bin`) to verify zero pronunciation errors before video rendering.
  3. **14 Procedural SFX & `-14.0 LUFS` Mastering**: Places frame-accurate SFX (`riser`, `swoosh-pass`, `impact`, `pop`, `shimmer`, `typing`, `tick`) anchored to scenes/words/beats, sidechain ducks the music bed under speech (`40ms` lookahead), applies a lookahead peak limiter, and normalizes to **`-14.0 LUFS` (`-1.5 dBTP`)**.

---

### Agent 6: Google Search Grounding Agent (`وكيل بحث جوجل للتوثيق المعرفي`)
- **Target Endpoint**: `https://www.google.com/` (`AI Mode`, multimodal file/model search bar)
- **Primary Role**: Deep Web Researcher, Fact-Checker, Cultural/Trending Pulse Analyst, and Archival Corpus Retriever.
- **Core Responsibilities**:
  1. **5-Batch Deep Web Research (`research_brief`)**: Executes Landscape Scan, Trending Pulse, Citable Data, Audience Pain Mining, and Contrarian Expert Angles.
  2. **Facts Ledger Locking (`facts.md`)**: Compiles an immutable ledger of verified statistics, proper nouns, and product claims. No on-screen number or spoken claim can appear in the video unless present in `facts.md`.
  3. **Retrieval-First Documentary Corpus (`route_7`)**: Queries public-domain and CC0 repositories (`Archive.org`, `NASA`, `Wikimedia Commons`, `Pexels`, `Unsplash`) to build a CLIP-searchable visual corpus (`>= 8x` candidate clips per slot).

---

### Agent 7: Cross-Model Critique & Code Agent (`وكيل المراجعة النقدية وهندسة التحريك العابر للنماذج`)
- **Target Endpoints**: `https://chatgpt.com/` (`Think` mode, `Projects`) & `https://claude.ai/new` (**Sonnet 5.5 Medium**, `Chat` & `Cowork` modes, `Artifacts`, `Code`)
- **Primary Role**: Independent Red-Team Critic, Slideshow Risk Auditor, 60fps 3D/2D Motion Engine Architect (`Three.js` + `engine.js` / `Remotion` / `HyperFrames`), and Arabic Typography/Kashida Validator.
- **Core Responsibilities**:
  1. **CHAI 3-Axis Pre-Render Critique**: Audits Agent 2's blueprint so every finding is **Accurate** (cites exact `scene_id` and field), **Complete** (scans all scenes for systemic issues), and **Constructive** (provides a drop-in replacement fix).
  2. **6-Dimension Slideshow Risk Scorer (`score_slideshow_risk`)**: Rejects any plan scoring `>= 3.0` or failing `motion_ratio >= 70%`, replacing static/comical photo cutouts with true 60fps 3D/2D procedural choreography.
  3. **60fps 3D + 2D Motion Engine Architecture (`video-ad-editor/motion/`)**: Writes deterministic 60fps scenes combining `MOTION.stage`, `ctx.slideWall` (3D 6×5 card wall with motion blur and match-cut landing), `ctx.stage3D` (Three.js PBR meshes + `UnrealBloomPass`), `ctx.text.drawKashida` (smooth pixel-accurate Arabic tatweel), and word-by-word highlighted Arabic captions.

---

## 4. Inter-Agent Data Contract & Execution Sequence (`بروتوكول تتابع المهام وتبادل البيانات`)

| Step | Source Agent | Target Agent | Payload / Artifact | Validation Gate |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Agent 1 (Orchestrator)** | **Agent 6 (Google Search)** | `research_queries.json` (5 batches) | All 5 research batches populated; zero unverified claims. |
| **2** | **Agent 6 (Google Search)** | **Agent 2 (Gemini Ultra)** | `research_brief.json` + `facts.md` | Every statistic linked to a primary source in `facts.md`. |
| **3** | **Agent 2 (Gemini Ultra)** | **Agent 7 (ChatGPT/Claude)** | `script.json` + `draft_blueprint.json` | 100% vocalized `tts_text`, pause `هْ`, zero `ٰ`, CHAI 5-aspect slots full. |
| **4** | **Agent 7 (ChatGPT/Claude)** | **Agent 3 (Google Labs)** | Approved `blueprint.json` + 60fps `scenes/*.js` | `score_slideshow_risk < 3.0`, `motion_ratio >= 70%`, zero lint errors. |
| **5** | **Agent 3 (Google Labs)** | **Agent 4 (Google Flow)** | `0-Credit` `@Character_01` & `@Product_01` PNGs | Identity consistency verified across front/3-quarter angles. |
| **6** | **Agent 4 (Google Flow)** | **Master Compositor** | `scene_01..06.mp4` (`Veo 3.1` / `Omni 1.1`) | `Scene Handshake` (`-sseof -0.04`) continuity & anti-AI sheen verified. |
| **7** | **Agent 5 (FlowMusic/DSP)** | **Master Compositor** | `vo_full.wav` + `timeline.json` + `-14 LUFS` Mix | Whisper medium verification passed; `-14.0 LUFS`, `<= -1.5 dBTP`. |
| **8** | **Master Compositor** | **Agent 1 (Orchestrator)** | `final.mp4` (60fps) + `contact.png` | Passes 5-point `final_review` + Safe-Zone (`--safe`) check. |
