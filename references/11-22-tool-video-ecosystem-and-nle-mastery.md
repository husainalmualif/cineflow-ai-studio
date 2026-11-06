# 11 — Complete 22-Tool Creative Video, 3D, NLE & Generative AI Ecosystem Mastery

This reference provides exact, zero-error operational workflows, CLI/API automation hooks, prompt grammars, camera command tokens, and post-production interchange rules across all **22 industry-standard tools** in the CineFlow AI Studio ecosystem.

---

## Category A — 3D & Motion Graphics Engines (`4 Tools`)

### 1. Blender (`bpy` Headless Python 4.x/5.x & Cycles / EEVEE Next)
- **Headless CLI Render Command (Zero GUI Overhead)**:
  ```bash
  blender -b scene.blend -P scripts/setup_render.py -E CYCLES -o //renders/frame_#### -F OPEN_EXR_MULTILAYER -a
  ```
- **Color Management & Compositing Law**:
  - Set View Transform to **`AgX`** (Look: `AgX - Medium High Contrast` or `Punchy`) for direct MP4 delivery, or export **16-bit half-float `OpenEXR MultiLayer`** in **`ACEScg`** when compositing in DaVinci Resolve Fusion / After Effects.
- **Programmatic `bpy` Camera Rig & Dolly Automation**:
  - Parent the camera (`bpy.data.objects["Camera"]`) to an `Empty` focus target with a `TRACK_TO` constraint (`track_axis='TRACK_NEGATIVE_Z'`, `up_axis='UP_Y'`), keyframe focal length (`35mm -> 85mm`) and `dof.aperture_fstop = 1.8`, and set interpolation to `BEZIER` (`handle_left_type = 'AUTO_CLAMPED'`).
- **Geometry Nodes & Grease Pencil 3.0**:
  - Drive procedural mograph instances via `Scene Time -> Seconds` or baked audio f-curves (`Sound to Samples`), and use Grease Pencil `LineArt` modifier for 2D/3D hybrid editorial outlines.

### 2. Cinema 4D (`c4d` Python SDK, MoGraph & Redshift)
- **MoGraph Procedural Hierarchy**:
  - `Cloner` (Grid / Radial / Object mode) -> driven by **`Plain` + `Shader` + `Random` Effectors** -> attenuated by **Fields** (`Linear Field` + `Delay Layer` in **`Spring`** mode at `35%–55%` strength for organic physical overshoot).
- **Redshift Multi-Pass AOV Pipeline**:
  - Always enable: `Beauty`, `DiffuseFilter`, `Reflections`, `SpecLighting`, `Emission`, `Z-Depth` (unfiltered), `MotionVectors`, and **`Cryptomatte`** (Material + Object ID) for instant matte isolation in After Effects / Nuke / Fusion.
- **Cineware Live Bridge**:
  - Import `.c4d` scenes directly into Adobe After Effects via **Cineware**, extract the C4D 3D Camera and Nulls (`Extract`), and pin 2D Arabic HUD callouts to 3D Null coordinates in screen space.

### 3. Adobe After Effects (`ExtendScript .jsx`, `aerender` & Expressions)
- **Headless CLI Render (`aerender`)**:
  ```bash
  aerender -project project.aep -comp "Main_9x16_Master" -RStemplate "Best Settings" -OMtemplate "Lossless with Alpha" -output out/master.mov
  ```
- **Modern JavaScript Expression Engine Rules**:
  - **Dynamic Self-Sizing RTL Arabic Text Pill (`sourceRectAtTime`)**:
    ```javascript
    const s = thisComp.layer("AR_Caption").sourceRectAtTime(time, false);
    const padX = 48, padY = 28;
    [s.width + padX * 2, s.height + padY * 2];
    ```
  - **Inertial Overshoot Bounce (Keyframed Entry)**:
    ```javascript
    const amp = 0.05, freq = 2.8, decay = 5.0;
    let n = 0;
    if (numKeys > 0) {
      n = nearestKey(time).index;
      if (key(n).time > time) n--;
    }
    if (n === 0) value;
    else {
      const t = time - key(n).time;
      const v = velocityAtTime(key(n).time - thisComp.frameDuration / 10);
      value + v * amp * Math.sin(freq * t * 2 * Math.PI) / Math.exp(decay * t);
    }
    ```
  - **Posterized Editorial Collage Motion (`Vox` Style)**: `posterizeTime(15); wiggle(2, 6);`
- **Roto Brush 3.0 & 3D Camera Tracker**:
  - Freeze Roto Brush 3.0 propagation before final render to lock alpha mattes (`Feather: 3px`, `Shift Edge: -15%`, `Decontaminate Edge Colors: ON`).

### 4. Apple Motion (`.motn` XML, Behaviors & Final Cut Pro Rigs)
- **Keyframe-Free Behavior Architecture**:
  - Prefer **Behaviors** over manual keyframes: **`Overshoot`** (for springy title/card reveals), **`Logarithmic`** (for smooth deceleration), **`Ramp`**, and **`Sequence Text`** (`Animate: Word` or `Character` with `Direction: Right to Left` for Arabic).
- **Publishing `.moti` / `.motr` Templates to Final Cut Pro**:
  - Bind layout switches (`9:16` vs `16:9`), brand colors, and text fields to a **Rig** (`Pop-up` or `Slider` widget) and check `Publish` so editors can customize inside Final Cut Pro without opening Motion.

---

## Category B — Professional NLEs & Post-Production Suites (`4 Tools`)

### 5. DaVinci Resolve Studio (`DaVinciResolveScript`, Color & Fairlight)
- **Fixed 7-Node Color Pipeline (`DaVinci Wide Gamut / Intermediate`)**:
  1. **Node 01 (`CST_IN`)**: Color Space Transform from Camera/Generator Input (`Rec.709` / `sRGB`) -> `DaVinci Wide Gamut` / `DaVinci Intermediate`.
  2. **Node 02 (`EXPOSURE_WB`)**: Offset exposure & Printer Lights white balance.
  3. **Node 03 (`CONTRAST_PIVOT`)**: Contrast (`1.08–1.15`) with Pivot (`0.435`).
  4. **Node 04 (`SKIN_MAGIC_MASK`)**: Qualifier / Magic Mask on speaker skin -> lock on skin-tone line, protect saturation, and apply subtle Midtone Detail (`+10`).
  5. **Node 05 (`RELIGHT_VIGNETTE`)**: Power Window soft radial gradient behind subject (`Outside` -0.35 stops).
  6. **Node 06 (`HALATION_GRAIN`)**: ResolveFX `Halation` (subtle warm edge bloom) + `Film Grain` (`35mm 250D`, `Intensity: 0.18`).
  7. **Node 07 (`CST_OUT`)**: `DaVinci Wide Gamut` / `DaVinci Intermediate` -> `Rec.709` / `Gamma 2.4` (with `Tone Mapping: DaVinci` and `Gamut Mapping: Saturation Compression`).
- **Fairlight Broadcast Audio Mastering**:
  - Dialogue Track: High-pass filter at `80 Hz` (`18 dB/oct`), De-Esser at `6.5 kHz`, Compressor (`3:1`, `-18 dB` threshold, `+3 dB` makeup).
  - Music Bus: Sidechain Compressor keyed from Dialogue Bus (`-9.5 dB` ducking, `15 ms` attack, `450 ms` release).
  - Master Bus: Loudness Meter locked to **`-14.0 LUFS` integrated** and **`-1.5 dBTP` True Peak** for social/web delivery.

### 6. Adobe Premiere Pro (`ExtendScript`, FCPXML & Essential Sound)
- **Timeline Interchange (`FCPXML` / `EDL`)**:
  - Import beat markers generated by `scripts/beat_grid.py` as sequence markers, use **Scene Edit Detection** on pre-rendered AI compilation reels, and enable **Optical Flow** time interpolation on speed ramps (`0.25x..4.0x`).
- **Lumetri & Essential Sound Order**:
  - Tag dialogue clips as `Dialogue` (Clarity: `Dynamic`, `DeNoise: 25%`) and music bed as `Music` (`Duck against Dialogue: Sensitivity 6, Duck Amount -9.5 dB, Fades 450 ms`).

### 7. CapCut (`draft_content.json` Programmatic Project Generator)
- **Programmatic Draft Folder Anatomy**:
  - A CapCut project directory requires `draft_content.json` and `draft_meta_info.json`.
  - All timeline positions (`start`, `duration`) inside `draft_content.json` are stored in **microseconds (`1 second = 1,000,000 µs`)**:
    - `tracks[0]`: Main video spine (`type: "video"`).
    - `tracks[1]`: Overlay / B-Roll / PIP (`type: "video"`).
    - `tracks[2]`: RTL Arabic captions (`type: "text"`, `font_title: "Cairo"`, `check_flag: 7` for fill + stroke + background pill).
    - `tracks[3..4]`: Voiceover + ducked music + SFX (`type: "audio"`).

### 8. Wondershare Filmora (`.wfp` & Smart Editing Workflow)
- **Rapid Social Assembly**:
  - Use **Silence Detection** (`Threshold: -32 dB`, `Minimum Duration: 0.35s`, `Buffer: 0.12s`), **AI Audio Stretch** to re-time music beds to exact `15s` / `30s` / `60s` cuts while preserving musical outro cadences, and **Auto Beat Sync** for fast B-roll placement.

---

## Category C — AI Avatar, Long-Form Storyboard & Cloud Repurposing (`5 Tools`)

### 9. HeyGen (`Avatar IV` & Video Agent API v2)
- **Avatar IV Realism & Arabic Lip-Sync Contract**:
  - Supply fully vocalized Arabic text (`dialogue_tts_ar` with pause-final `ة -> هْ` or pre-mastered `48 kHz` WAV audio) so visemes match pharyngeal and emphatic Arabic consonants (`ع، ح، ق، ص، ض، ط، ظ`).
  - Insert `<break time="0.3s"/>` between clauses (`<= 8 words`) to prevent robotic continuous mouth movement, and enable micro-head nods and eye-blink naturalism.

### 10. Synthesia (`Express-2 Avatars` & API v2)
- **Enterprise & Multi-Avatar Training Videos**:
  - Use **Express-2 full-body avatars** with explicit script markers for camera framing (`Close-up` on key takeaways, `Medium` on explanations, `Two-shot` for conversational Q&A) and export SCORM / `.srt` localized tracks.

### 11. MagicLight.AI (`magiclight.ai` Long-Form Story-to-Video Pipeline)
- **5-Stage Long-Form Narrative Workflow (Up to 30–50 Minutes)**:
  1. **Phase 1 — Character Bible (`Asset Store`)**: Pre-build and save recurring characters (`up to 1,000 chars` visual DNA + reference portraits) and lock one of the **20+ global visual styles** (`3D Animation`, `Cinematic Realism`, `Anime`, `Pixar-style`, `Cyberpunk`, `Watercolor`).
  2. **Phase 2 — Script-to-Storyboard Parsing (`up to 12,000 chars` per chapter)**: Paste or upload `.txt`/`.docx` script; MagicLight segments it into sequential **Nano Storyboard (`Nano Banana 2`) Cards** with **50+ preset poses**.
  3. **Phase 3 — Panel Pose & Angle Refinement**: Verify cast assignment in every card, adjust camera angle/expression presets, and fix individual panel prompts before spending video credits.
  4. **Phase 4 — Multi-Model Video Animation**: Route approved storyboard cards to the integrated video engine (`Veo 3`, `Kling 3.0`, `Seedance 2.5 / 2.0`, `Wan 3.0`, `MiniMax Hailuo H3`, or `Sora 2`) while maintaining locked character embeddings across 100+ shots.
  5. **Phase 5 — Voice Casting & Subtitle Compilation**: Assign character-matched voices, background music, and synchronized captions.

### 12. Veed.io (Cloud NLE, Eye Contact & Clean Audio)
- **Talking-Head Polish Pipeline**:
  - Apply **Clean Audio** (`75%–85%` strength so voice warmth is preserved without metallic artifacts), **Eye Contact Correction** for teleprompter reads, and **Magic Cut** to remove bad takes before exporting burned-in or `.srt` captions.

### 13. OpusClip (`ClipAnything` Multimodal Virality Engine)
- **Virality Score (`0–100`) & `9:16` Auto-Reframe Contract**:
  - Use `ClipAnything` visual + audio + sentiment prompts (e.g., `"Extract 30-45s segments with a strong contrarian hook, high vocal energy, or a concrete product demonstration"`).
  - Lock **Active Speaker Face-Tracking (`9:16` Center-Cut)** with `Split-Screen` fallback for two-speaker podcast turns, enable **AI B-Roll** only on non-hero explanatory beats, and export XML to Premiere Pro / DaVinci Resolve for final color and `-14 LUFS` audio polish.

---

## Category D — Frontier Generative Video Foundation Models (`9 Tools`)

### 14. Google Veo (`Veo 3.1` Lite / Fast / Quality)
- **Allowed Durations & Modes (`FLOW_SURFACE_MODE_DURATIONS`)**:
  - `veo-3.1-lite` & `veo-3.1-fast`: `4s, 6s, 8s` (`text-to-video`, `first-frame`, `first-last-frame`) and `8s` (`references-to-video`, up to 3 ingredients).
  - `veo-3.1-quality`: `8s` (`text-to-video`, `first-frame`, `first-last-frame`) — highest photorealistic texture and physics.
  - `Extend`: Routes through `veo-3.1-lite` (`+8s` on Flow, `+7s` on Gemini API).

### 15. Google Flow (`flow.google.com` + `Gemini Omni 1.2 Flash` + `Nano Banana Pro`)
- **Multimodal Production Rules (`google-flow-director v3.0.0 — Pure Gemini Omni 1.2 Flash Native Edition`)**:
  - `Gemini Omni 1.2 Flash` (`macaron_cookie` / `gemini-omni-1.2-flash`): **`3s` to `15s` in `1-second` increments** on Flow (`3..15s` slider for `t2v/i2v/r2v`, `3..10s` for `Frames` First-to-Last Interpolation & `Extend`), combining **front-and-back garment/product photos + `3s` motion reference clips + `1s` voice cues** and routing distinct voices across **`4+` speakers** in a single `15s` clip with `يتحدث باللهجة البحرينية: "<النص>"`.
  - **Credit Optimization (Pillar 1)**: Generate character/product sheets in `Nano Banana Pro` (`0 credits`), draft motion at `360p` (`1 credit/s` for `3..10s`) or `720p` (`$0.07/s` on API, `30%` cheaper than Omni 1.1), refine turn-by-turn via **`0-credit` Multi-Turn Conversational Editing & Motion Transfer**, and run the **`1080p` upscale for `0 credits`** (`4K` upscale = `50 credits`).

### 16. Runway (`Gen-4` / `Gen-4 Turbo` / `Act-One` / `Frames`)
- **Gen-4 Prompt Grammar (Motion-Delta Only & No Negative Prompts)**:
  - When animating a `Frames` keyframe image in `Gen-4` / `Gen-4 Turbo`, describe **only the motion delta** (`[Camera Framing & Movement] + [Subject Physical Action] + [Environmental Motion]`) — never re-describe static clothing/background details already visible in the reference image.
  - **Never** include negative clauses (`no blur, no distortion`) in Runway prompts — they cause positive token bleed.
  - **`Act-One`**: Transfer subtle human facial micro-expressions and eye darts from a smartphone driving video onto any generated character still or video (keep both driving video and target portrait within **`<= 30°` off-axis head rotation** with clean frontal lighting).

### 17. Kling AI (`Kling 2.0 / 2.1 / 3.0 Master`)
- **`Elements` Multi-Subject Consistency & 6-Axis Camera Control**:
  - **`Elements` Mode**: Upload up to **4 cropped subject/object cutouts** (`@CharA`, `@ProductB`, `@PropC`, `@EnvD`) and describe their exact spatial interaction in a `5s` or `10s` shot.
  - **6-Axis Camera Control**: Explicitly set `Horizontal (-10..+10)`, `Vertical (-10..+10)`, `Pan (-10..+10)`, `Tilt (-10..+10)`, `Roll (-10..+10)`, and `Zoom (-10..+10)` sliders, or use **Motion Brush** (up to 6 regions) + **Static Mask** to lock architectural backgrounds against warping.

### 18. Hailuo AI / MiniMax (`I2V-01-Director` / `T2V-01-Director` / `S2V-01`)
- **Mandatory Bracketed Camera Command Grammar (`[Command]`)**:
  - `I2V-01-Director` and `T2V-01-Director` execute exact camera trajectories when placed inside square brackets at the exact timestamp/position in the prompt:
    - **Horizontal / Lateral**: `[Truck left]`, `[Truck right]`, `[Pan left]`, `[Pan right]`
    - **Depth / Focal**: `[Push in]`, `[Pull out]`, `[Zoom in]`, `[Zoom out]`
    - **Vertical**: `[Pedestal up]`, `[Pedestal down]`, `[Tilt up]`, `[Tilt down]`
    - **Dynamic / Cinema**: `[Tracking shot]`, `[Shake]`, `[Static shot]`
  - **Combination Rule**: Combine at most **2–3 compatible commands inside one bracket** (e.g., `[Push in, Pan right]` or `[Truck left, Tilt up]`) at the start of the shot description:
    > `[Push in, Pan right] @Kwame lifts the @AmberFlacon toward the warm golden-hour window light, condensation glistening on the glass.`
  - **`S2V-01` (Subject Reference)**: Locks a single human face identity from 1 reference photo across arbitrary new angles and lighting setups.

### 19. Wan (`Wan 2.1 / 2.6 / 3.0` & `VACE` All-in-One Video Creation & Editing)
- **`VACE` Video Condition Unit (`VCU`) & First-Last-Frame (`FLF2V`)**:
  - **`VCU` 4-Tuple Architecture**: `V = [T, F_c, M_c, I_r]` unifying `T` (text prompt), `F_c` (active/inactive context frames), `M_c` (binary spatiotemporal mask where `1` = regenerate and `0` = preserve), and `I_r` (reference subject/object cutouts).
  - **`FLF2V` (`First-Last-Frame-to-Video`)**: Supply both `start_frame.png` and `end_frame.png` with an explicit motion bridge prompt (`720p` / `1080p`).
  - **Task Composition**: Combines **Reference-to-Video (`R2V`)**, **Video-to-Video (`V2V`)**, **Masked Video Inpainting**, and **Video Outpainting** (`16:9 <-> 9:16`) in a single pass.

### 20. Dreamina (`Jimeng AI` by ByteDance — `Seedream 3.0` & `Seedance 2.0 / 2.5`)
- **Native Bilingual Typography & Micro-Acting**:
  - `Seedream 3.0` renders crisp poster/title typography and high-fashion editorial keyframes; `Seedance 2.0 / 2.5` animates them with nuanced micro-expressions (subtle eyebrow lifts, natural breathing chest motion, and tear/sweat specular physics).

### 21. Seedance (`Seedance 2.0 / 2.5` Multimodal `@` Tag & Multi-Shot Engine)
- **Multimodal `@Image1..@Image9` / `@Video1..@Video3` / `@Audio1..@Audio3` (`<= 12` Files Total) + Multi-Shot Syntax**:
  - In **All Reference Mode**, upload up to **12 multimodal files** (`@Image1..@Image9` for cast/props, `@Video1..@Video3` for camera/choreography transfer, `@Audio1..@Audio3` for beat/lip-sync) and script **2 to 4 sequential cuts** inside a single generation:
    ```text
    Use @Image1 for the main presenter's appearance, @Image2 for the hero perfume bottle, @Video1 for camera tracking energy, and @Audio1 for beat rhythm.
    Shot 1 (0s-3s): Medium close-up. @Image1 reaches across the walnut table and lifts @Image2 into warm key light as the camera pushes in.
    Shot 2 (3s-6s): Hard cut to extreme macro close-up of @Image2 spraying a fine golden mist in slow motion, matching the motion rhythm of @Video1.
    Shot 3 (6s-10s): Cut to medium wide shot as @Image1 smiles confidently on the final beat drop of @Audio1.
    ```

### 22. Higgsfield AI Studio (`Cinema Studio 4.0` / `Soul 2.0` / `DoP I2V-01` & MCP)
- **Two-Stage `Soul` -> `DoP` Workflow + Inline `#` Camera Hashtag Stacking**:
  1. Lock character identity using **`Soul ID`** (`Higgsfield Soul 2.0` photorealistic fashion/lifestyle image model) and color grade via **`Soul HEX`** (palette lock) or **Era Regrading (`1960..2020`)**.
  2. Animate with **`Higgsfield DoP` (`Director of Photography`)** by selecting one of the physical cinema-rig presets (`Crash Zoom In`, `Crash Zoom Out`, `Bullet Time`, `SnorriCam`, `RoboArm`, `FPV Drone`, `Whip Pan`, `Dutch Angle`, `Arc Left`, `Arc Right`, `Super Dolly`, `Lazy Susan`, `Handheld`) or stacking up to **2 inline `#` camera hashtags** (`#snorricam`, `#crash_zoom`, `#bullet_time`, `#roboarm`, `#fpv_drone`, `#whip_pan`, `#dutch_angle`, `#handheld`), and describe **only the subject's internal physical action**.
  3. **Programmatic / Agentic Integration**: Supports the official Higgsfield MCP server (`https://mcp.higgsfield.ai/mcp`) for automated image-to-video generation.
