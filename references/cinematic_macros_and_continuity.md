# Cinematic Macro Dictionary, Master State Engine & Scene Handshake Reference

This reference manual documents the internal continuity, camera optics, slash-macro compilation, and quality assurance engine of **CineFlow AI Studio**.

---

## 1. Master State Engine & Continuity Protection (`إدارة الحالة المركزية ومنع الانحراف`)

### 1.1 The 23 State Domains (`MASTER_STATE`)
`MASTER_STATE` is the single source of continuity truth across the entire video sequence:
1. `PROJECT_STATE`: Project ID, Purpose, Format, Style Variant, Target Platform (`Google Flow`).
2. `CAMPAIGN_STATE`: Strategic Intent, Audience Emotional Truth, Chosen Divergence Angle.
3. `STYLE_STATE`: Visual Style, Rendering Profile, Genre Profile, Anti-AI Sheen Lock.
4. `CHARACTER_STATE`: `Character_ID`, `@CHARACTER_REF`, Facial Structure, Wardrobe, Hair, Accessories, Body Proportions, Behavioral Profile.
5. `PRODUCT_STATE`: `Product_ID`, `@PRODUCT_REF`, Geometry, Dimensions, Packaging, Logo, Materials, Typography, Brand Colors (`CMYK/Pantone`).
6. `ENVIRONMENT_STATE`: `Environment_ID`, `@ENVIRONMENT_REF`, Location, Architecture, Time of Day, Weather, Spatial Layout, Background Elements.
7. `CAMERA_STATE`: Camera Hardware Profile, Lens Focal Length, Framing, Position, Trajectory, Focus, Depth of Field (`DOF`).
8. `LIGHTING_STATE`: Key Light, Fill Light, Rim Light, Practical Lights, Color Temperature (`Kelvin`), Contrast Ratio, Exposure, Volumetric Atmosphere.
9. `COLOR_STATE`: LUT / Color Grading Theme, White Balance, Saturation, Skin-Tone Protection Baseline, Shadow/Highlight Tint.
10. `LANGUAGE_STATE`: `ARABIC | ENGLISH | MIXED | AUTO`.
11. `DIALECT_STATE`: `BAHRAINI_KHALEEJI | SAUDI_KHALEEJI | KUWAITI_GULF | EMIRATI | OMANI | IRAQI | LEVANTINE | EGYPTIAN | MSA`.
12. `SPEAKER_STATE`: `Speaker_ID`, `Voice_ID`, Gender, Age Profile, Pitch, Speech Rhythm.
13. `VOICE_STATE`: Vocal Tone, Timbre, Pace, Accent, Breathing Profile.
14. `SCRIPT_STATE`: `Exact_User_Text` (`Verbatim_Script_Lock = TRUE`).
15. `PERFORMANCE_STATE`: Tone of Voice (`Emotion`), Body Language (`Micro-Cues`), Intensity, Subtext, Pause Timing, Gaze Direction (`Eyeline_Match`).
16. `AUDIO_STATE`: Dialogue Timing, Foley SFX, Ambient Room Tone, Auto-Ducking, Silence Tags (`[Audio: Absolute Silence]`).
17. `MUSIC_STATE`: Genre, Tempo, Musical Key, BPM, Beat Grid Markers, Rhythmic Sync Mode.
18. `PHYSICS_STATE`: Gravity, Collision, Momentum, Cloth Dynamics, Fluid Dynamics, Smoke/Particle Behavior (`MOTION_LOCK`).
19. `TEMPORAL_STATE`: Scene Duration, Shot Duration (`3–10s`), Time Elapsed, Pacing Curve.
20. `SPATIAL_STATE`: `180_Degree_Rule_Lock`, Entry/Exit Vectors, Subject Coordinates, Safe-Zone Grid.
21. `EMOTIONAL_STATE`: Emotional Arc Curve, Tension Level, Audience Empathy Target.
22. `CONTINUITY_STATE`: `Previous_Approved_Shot`, `Current_Shot`, `Next_Shot`, `First_Last_Frame_Seed`.
23. `EVOLUTION_STATE`: Tracks authorized narrative changes vs. unauthorized generative drift.

### 1.2 State Status Tags (`STATE_STATUS`)
Every variable in `MASTER_STATE` carries one of six statuses:
- **`LOCKED`**: Immutable unless explicitly overridden by the Director (`Character_ID`, `Product_ID`, `Brand_Logo`, `Dialect_State`, `Verbatim_Script`).
- **`INHERITED`**: Automatically carried forward from `LAST_APPROVED_STATE`.
- **`EVOLVING`**: Intentionally progressing due to narrative, temporal, emotional, or environmental logic.
- **`MUTATED`**: Explicitly changed by the Director for the current shot (e.g., `"خله يدخل المطبخ"` mutates `ENVIRONMENT_STATE = Kitchen` while inheriting `CHARACTER_STATE`, `WARDROBE`, and `DIALECT_STATE`).
- **`RESET`**: Reinitialized for a new unrelated scene or flashback.
- **`AUTO`**: Safely inferred by the studio when unspecified by the user.

> [!IMPORTANT]
> **Last Approved State Protection**: A failed generation (`HARD_FAIL` or visible identity drift) **MUST NEVER** update `MASTER_STATE`. Subsequent shots always inherit strictly from `LAST_APPROVED_STATE`.

---

## 2. Scene Handshake & Seamless Extension Protocol (`المصافحة البصرية والامتداد السلس`)

To prevent visual jumps between shots in Google Flow (`Scenebuilder` / `Frames to Video` / `Ingredients to Video`), every transition between `Scene_N` and `Scene_N+1` executes the **Scene Handshake Protocol**:

```text
SCENE_N_APPROVED_EXIT_STATE
  ├── VISUAL_HANDSHAKE: Character Pose, Gaze Direction (Eyeline Match), Movement Vector, Lens Continuity
  ├── SPATIAL_HANDSHAKE: Room/Location, Entry/Exit Vector, 180-Degree Axis Lock
  ├── LIGHTING & COLOR HANDSHAKE: SCENE_[N]_EXIT_LIGHTING >>> INHERIT EXACTLY >>> SCENE_[N+1]_ENTRY_LIGHTING
  ├── AUDIO & DIALOGUE HANDSHAKE: Room Tone continuity, J-Cut / L-Cut overlap (0.15s–0.25s), Breath continuity
  └── FIRST/LAST FRAME SEED: Save Last Frame of Scene_N and feed as + Add start frame (<FIRST_FRAME>) of Scene_N+1
```

### Runtime Partitioning Law
- **Viral Short-Form / Micro-Content (`10–15s` total)**: Decompose into **2 to 3 tight micro-scenes (`3–5s` or `4–7s` each)** so visual energy stays high and zero AI degradation occurs.
- **Unbroken Single-Shot Scenes (`<= 10s`)**: Prompt explicitly with `"Continuous, unbroken shot, no scene cuts"`.
- **Extended Narrative Scenes (`> 10s`)**: Split into sequential generation chunks (`Chunk A: 0–8s` + `Chunk B: 8–15s`), instructing Google Flow to use the **Saved Last Frame of Chunk A** as `<FIRST_FRAME>` while maintaining `@Character_01` and `@Product_01` ingredients.

---

## 3. Complete AI Cinematic Macro Dictionary (`180+ Slash Macros`)

When the user includes any `/macro` or `[BRACKETED_OVERRIDE]`, the compiler enforces the exact physical definition below as a **Hard Constraint**:

### A. Smart Macros (One-Click Complex Sequences)
| Slash Macro | Compiled Physical & Cinematic Directive for Google Flow / Veo |
| :--- | :--- |
| `/exploded_view` | Mechanical 3D exploded-view disassembly in mid-air, internal components separating smoothly along axial vectors with studio rim lighting, then reassembling with precision |
| `/orbit_360` | Continuous 360-degree circular gimbal orbit around the locked central subject, maintaining constant distance and focal lock |
| `/drone_fly` | Sweeping high-altitude cinematic aerial drone flight with smooth gimbal stabilization over the environment |
| `/3d_construction_timelapse` | Accelerated time-lapse progression showing structural assembly from foundation to finished form with locked camera tripod framing |
| `/bullet_time` | Frozen ultra-slow-motion matrix bullet-time moment (1000fps simulation) while the camera orbits smoothly around suspended particles and droplets |
| `/morph` | Seamless geometric and material transformation between the starting form and target form with continuous lighting |
| `/cinemagraph` | Completely static locked-off composition where only one subtle environmental element (e.g., steam, fabric edge, or rain) moves in a loop |
| `/seamless_loop` | Match the final frame's exact camera position, subject pose, and lighting to the opening frame (`<FIRST_FRAME>` = `<LAST_FRAME>`) for an infinite loop |

### B. Camera Movement (`CAMERA_MOVEMENT`)
- `/dollyin` / `/pushin`: Smooth physical camera dolly push-in along rails toward the subject, gradually tightening framing.
- `/dollyout` / `/pullout`: Smooth physical camera dolly pull-back away from the subject, revealing surrounding environment.
- `/truckleft` / `/truckright`: Lateral camera trucking parallel to the subject's horizontal plane (`left` or `right`).
- `/panleft` / `/panright`: Tripod-mounted horizontal camera rotation (`left` or `right`) from a fixed nodal point.
- `/tiltup` / `/tiltdown`: Tripod-mounted vertical camera rotation (`upward` or `downward`).
- `/craneup` / `/cranedown`: Sweeping vertical jib/crane elevation (`rising high` or `descending low`) while maintaining subject framing.
- `/orbitleft` / `/orbitright` / `/arcshot`: Curved semi-circular camera arc around the subject (`counter-clockwise` or `clockwise`).
- `/track` / `/follow`: Dynamic tracking camera moving at the exact speed and vector of the moving subject.
- `/pedestalup` / `/pedestaldown`: Vertical camera column lift/drop keeping the optical axis strictly horizontal.
- `/z-axis-move`: Rapid depth-axis camera movement pushing straight through foreground elements toward the subject.

### C. Zoom, Focus & Optics (`ZOOM_AND_FOCUS` & `LENS_OPTICS`)
- `/zoomin`, `/zoomout`, `/crashzoom`: Optical focal-length zoom (`smooth zoom-in`, `zoom-out`, or `high-speed whip crash-zoom`).
- `/rackfocus`, `/pullfocus`: Deliberate focus shift from foreground object to background subject (or vice versa) with creamy bokeh transition.
- `/focusface`, `/focuseyes`, `/focusobject`: Razor-sharp tack focus locked strictly on the subject's face, iris/eyes, or product geometry.
- `/shallowdepth`, `/bokeh`: Wide-aperture (`f/1.4`) shallow depth of field with creamy circular background bokeh separation.
- `/deepfocus`: Small-aperture (`f/11`) deep focus keeping foreground, midground, and background simultaneously sharp.
- `/splitdiopter`: Classic cinema split-diopter lens effect keeping both an extreme foreground face and a distant background subject in sharp focus.
- `/14mm`, `/24mm`, `/35mm`, `/50mm`, `/85mm`, `/135mm`: Exact prime cinema lens focal length simulation (`14mm ultra-wide`, `35mm anamorphic narrative`, `50mm human-eye natural`, `85mm portrait bokeh`, `135mm compressed telephoto`).
- `/anamorphic`, `/cinemascope`: Panavision/ARRI anamorphic cinema lens with oval bokeh and horizontal optical characteristics (`2.39:1` feel).
- `/macro`, `/probe`, `/microscope`: Laowa 24mm Probe / Extreme Macro lens capturing microscopic surface textures at millimeter distance.
- `/fisheye`, `/tiltshift`, `/pinhole`: Specialized optical distortion profiles.

### D. Shot Framing & Dynamic Camera (`SHOT_FRAMING` & `DYNAMIC_CAMERA`)
- **Framing**: `/extremecloseup` (`ECU`), `/closeup` (`CU`), `/mediumcloseup` (`MCU`), `/medium` (`MS`), `/cowboyshot`, `/mediumwide`, `/fullshot`, `/wide` (`WS`), `/extremewide` (`EWS`), `/establishing`, `/twoshot`, `/groupshot`, `/insertshot`.
- **Angles & Identity-Safe Framing**: `/lowangle` (heroic upward angle), `/highangle`, `/overhead` / `/birdseye` / `/topdown` (90-degree vertical God's-eye view), `/overshoulder` (`OTS`), `/profile` (90-degree side profile), `/firstperson` / `/pointofview` (`POV`), `/dutchangle` (tilted tension horizon).
- **Stabilization & Rig**: `/handheld` (organic human camera operator micro-sway), `/steadicam` / `/gimbal` / `/stabilized` (weightless floating motion), `/shakycam` (intense kinetic documentary tremor), `/whippan` (high-speed motion-blurred pan), `/vertigo` (dolly-zoom Hitchcock contra-zoom), `/bodycam`, `/dashcam`, `/cctv`, `/gopro`.
- **Drone**: `/drone`, `/droneup`, `/dronedown`, `/droneforward`, `/dronebackward`, `/droneorbit`, `/dronefollow`, `/fpvdrone` (high-speed acrobatic FPV racing drone weaving through tight spaces), `/dronedive`, `/satelliteview`.

### E. Lighting, Color, Environment FX & Speed (`LIGHTING_STYLE`, `ART_COLOR`, `ENVIRONMENT_FX`, `SPEED_MOTION`)
- **Lighting**: `/natural`, `/goldenhour` (warm 3200K low-sun directional glow), `/sunset`, `/moonlight`, `/neon` (cyberpunk/urban bi-color neon reflections), `/rimlight` / `/backlight` / `/silhouette`, `/softlight` (diffused octabox wrap), `/hardlight`, `/volumetric` / `/godrays` (Tyndall light beams cutting through atmospheric haze), `/candlelight`, `/firelight`, `/lowkey`, `/highkey`, `/chiaroscuro` (dramatic high-contrast Caravaggio shadow sculpting), `/noir`, `/studiolighting`, `/cinematiclighting`.
- **Color & Look**: `/tealandorange`, `/cinematiclut`, `/vibrant`, `/pastel`, `/neoncolors`, `/blackandwhite`, `/monochrome`, `/sepia`, `/vintage`, `/filmgrain` (`35mm Kodak Vision3 500T film grain`), `/hdr`, `/photorealistic`, `/hyperrealistic`.
- **Art Styles**: `/anime`, `/3drender`, `/claymation`, `/stopmotion`, `/cyberpunk`, `/steampunk`, `/watercolor`, `/oilpainting`, `/comicbook`, `/pixelart`, `/sketch`.
- **Environment FX**: `/rain`, `/snow`, `/fog`, `/mist`, `/wind`, `/smoke`, `/fire`, `/water`, `/particles`, `/dust`, `/lensflare`, `/motionblur`, `/sparks`, `/explosion`, `/underwater`, `/lightning`.
- **Speed & Time**: `/slowmotion`, `/speedramp` (fast entry -> slow-motion apex -> fast exit), `/timelapse`, `/hyperlapse`, `/realtime`, `/freezeframe`, `/reverse`, `/pingpong`.

### F. Subject, Audio & Reference Locks (`SUBJECT_EMOTION`, `AUDIO_SOUND`, `REFERENCE_EDITING`)
- **Subject & Identity**: `/identitylock`, `/characterconsistency`, `/facialconsistency`, `/facefocus`, `/eyetrack`, `/expression`, `/reaction`, `/microexpression`, `/lipsync`, `/smiling`, `/crying`, `/heroentrance`, `/emotionalpush`.
- **Audio & Sound**: `/dialogue`, `/voiceover`, `/whisper`, `/sfx`, `/foley`, `/ambient`, `/cityambience`, `/footsteps`, `/thunder`, `/bassdrop`, `/whoosh`, `/riser`, `/cinematicaudio`, `/realisticsound`, `/music`.
- **References & Aspect Ratio**: `/useimage`, `/maintainidentity`, `/preserveappearance`, `/styletransfer`, `/colormatch`, `/interpolate`, `/ar 9:16`, `/ar 16:9`, `/ar 1:1`, `/ar 21:9`, `/4k`, `/8k`, `/fps 24`, `/fps 60`.

---

## 4. The 8-Layer Prompt Stacking Compiler & Anti-AI Sheen Protocol (`بروتوكول محو اللمسة البلاستيكية`)

### 4.1 The 8-Layer Stacked Prompt Formula
Every visual prompt compiled for Google Flow / Veo follows this sequential order so the Attention Mechanism weights each constraint properly:

```text
[1. IDENTITY & SETTING ANCHORS: Lock [Character ID] / Lock [Product ID] / Setting DNA]
+ [2. NARRATIVE SUBJECT & 100% PHYSICAL ACTION + BODY LANGUAGE MICRO-CUES]
+ [3. CAMERA GEAR, LENS OPTICS & FRAMING: e.g., ARRI Alexa 65, 35mm Anamorphic, MCU]
+ [4. CAMERA MOVEMENT & TRAJECTORY: e.g., Slow Dolly-In / Orbit / Tracking]
+ [5. LIGHTING HANDSHAKE & ATMOSPHERE: e.g., Chiaroscuro low-key, volumetric dust motes]
+ [6. COLOR GRADING & HYPER-REALISM TEXTURE: e.g., Cinematic Warm LUT, 35mm film grain ISO 800, microscopic skin pores & fabric weave]
+ [7. MOTION SCOPE & PHYSICS LOCK: Moving elements vs. Locked background/product]
+ [8. ANTI-CGI & NEGATIVE GUARDRAILS]
```

### 4.2 Anti-AI Sheen & Hyper-Realism Protocol
For all **Live-Action**, **Commercial**, and **Documentary** scenes, automatically inject:
- **Optical Imperfections ("Dirtying the Image")**: `35mm film grain, ISO 800, subtle optical halation around highlights, natural lens breathing`.
- **Physical Materiality**: `microscopic skin pores, natural skin subsurface scattering, authentic fabric weave texture, tangible surface dust`.
- **Mandatory Defensive Guardrail Suffix**:
  `--no CGI, no 3D render, no plastic skin, no smooth airbrushed textures, no unreal engine 5, no video game look, no AI sheen, no warped hands, no extra fingers, no garbled text, no identity drift`

---

## 5. CMU/Harvard CHAI 5-Aspect Universal Video Language & Model-Specific Prompt Architectures (`اللغة البصرية الخماسية وهندسة النماذج`)

### 5.1 The Canonical 5-Aspect Prompt Skeleton (CHAI Standard)
Vision-language and video diffusion models reliably render Subject and Scene when prompted casually, but fail on Motion, Spatial Framing, and Camera unless all **five slots** are explicitly populated in order:

```text
[1. Subject]        Type + 3-6 disambiguating visual attributes repeated VERBATIM in every shot (never use pronouns or "the same character" across cuts) + Subject Transitions (revealing / disappearing / switching / complex-alternating + cause: "by subject movement" or "by camera movement")
[2. Subject Motion] Actions in strict temporal order ("First X enters, then Y reacts"); locomotion vs. gesture vs. facial micro-expression (replace emotional adjectives like "sad" with physical causes like "tears on cheek, shoulders slumped")
[3. Scene]          Overlays listed SEPARATELY (titles, HUD, lower-thirds are NEVER part of FG/MG/BG depth) + POV (first-person, drone, OTS, top-down oblique, dashcam, objective) + setting + time of day + environmental dynamics
[4. Spatial]        Shot size (ECU/CU/MCU/MS/FS/WS/EWS) + subject position in frame + depth (FG/MG/BG) + camera height relative to ground (aerial, overhead, eye, hip, ground, water, underwater) & angle relative to subject (bird's-eye = strict 90° top-down ≠ aerial, high, level, low, worm's-eye, Dutch fixed/rolling) — and how framing changes across the shot
[5. Camera]         Playback speed (time-lapse, fast-motion, slow-motion, stop-motion, speed-ramp, time-reversed) -> Lens distortion (fisheye vs. barrel vs. anamorphic) -> Focus/DoF (deep focus, shallow DoF, rack focus [snap], pull focus [gradual], focus tracking) -> Steadiness (locked, handheld, gimbal) -> Movement
```

> [!IMPORTANT]
> **Strict Camera Motion Separation (`dolly ≠ zoom`, `pan ≠ truck`, `static = strict zero motion`)**:
> - **Translation (Rig Physically Moves)**: `dolly in/out` (along lens axis), `truck left/right` (lateral), `pedestal up/down` (vertical).
> - **Rotation (Rig Stays Put, Camera Pivots)**: `pan left/right` (yaw), `tilt up/down` (pitch), `roll CW/CCW` (Dutch Z-axis).
> - **Lens-Only (No Rig or Camera Move)**: `zoom in/out` (focal length change), `rack focus` / `pull focus` / `focus tracking`.
> - **Strict Stillness (`static`)**: Zero camera movement, zero focus change, zero zoom. If any optical or physical shift occurs, never write `"static camera"`.

### 5.2 Model-Specific Prompt Structures & Empirical Word-Count Sweet Spots
| Target Model | Optimal Word Count | Structural Formula & Model-Specific Rules |
| :--- | :--- | :--- |
| **`Google Veo 3.1 / Veo 3`** | **`100 – 250 words`** (plateaus past 250w) | **14-Component Structure**: `Subject + Action + Scene/Context + Camera Angles + Camera Movements + Lens/Optical Effects (rack/pull/tracking focus, split diopter, vertigo) + Lighting + Tone/Mood + Artistic Style/Art Movement + Ambiance + Temporal Elements + Audio (dialogue in quotes) + Cinematic Terms (match cut, jump cut) + Negative Prompt ("no subtitles, no captions, no text overlays")`. |
| **`Seedance 2.0` (`Standard / Fast`)** | **`200 – 400 words`** (hero / multi-shot) \| `80–150w` (inserts) | **8-Component Multi-Shot Structure**: Supports `Shot 1 (...) / Shot 2 (...) / Shot 3 (...)` inside a single generation with native synchronized audio (`generate_audio=true`) and lip-sync (`Character says: "..."`, max `<= 6 words` on fast cuts). Repeat the character's 3–6 visual attributes verbatim in every `Shot N` block. |
| **`Gemini Omni Flash 1.1`** | **`80 – 180 words`** | Conversational turn-by-turn multimodal video generation and editing; start at `360p` draft (`half credit`) and upscale to `720p` (`0 credits`) with `@Voice` and `@Character` locks. |
| **`Sora 2 / Sora 2 Pro`** | **`100 – 250 words`** | Structured cinematography template emphasizing lens filtration, photochemical grade, wardrobe materiality, and diegetic soundstage. |
| **`Kling 2.6 / Kling Official Omni`** | **`80 – 160 words`** | 4-part structure (`Subject + Movement + Scene + Camera/Lighting`) supporting `++emphasis++` tokens, multi-reference Omni syntax, and explicit face-selected lip-sync. |
| **`Wan 2.2 / HunyuanVideo 1.5`** | **`200 – 400 words`** | Fine-tuned on dense 5-aspect descriptive captions (`Subject + Motion + Scene + Shot + Camera + Lighting + Style + Atmosphere`). |
| **`LTX-2` / `Runway Gen-4`** | **`<= 60 – 80 words`** | Keep prompts tight and motion-focused (`"Focus on motion, not appearance"`; one clear action per clip). |

---

## 6. Continuous Semantic 3D World & Blender / Three.js Production (`توليد العوالم ثلاثية الأبعاد المستمرة`)

When a cinematic trailer, game/product showcase, or architectural film requires a continuous, navigable 3D environment rather than isolated 2D clips:
1. **Two Fidelity Tiers (`fidelity_tier`)**:
   - **`blockout`**: Coarse semantic layout and camera path iteration in Three.js.
   - **`production`**: Hero/reference-grade world using licensed CC0 GLTF/GLB PBR catalogs for repeated environment assets, `Atlas Cloud Tripo H3.1` (text-to-3D) or `fal.ai Hunyuan 3D / SAM 3D` (image-conditioned 3D) for unique hero meshes, and **Blender 4.5 LTS (`Eevee Next` / `Cycles`)** or **HyperFrames + Three.js (`html-in-canvas` WebGL + UnrealBloom)** for final rendering.
2. **Continuous Coordinate System & Diagnostics**:
   - Define `global`, `regional`, and `walk-level` camera beats inside one continuous coordinate system (`world.json`).
   - Enforce terrain slope and ground-contact constraints on all scattered instances, and verify via semantic/wireframe passes that the camera never tunnels through terrain or clips the far plane.
