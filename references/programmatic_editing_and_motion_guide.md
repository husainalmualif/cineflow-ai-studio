# Programmatic Video Editing, Motion Graphics Stage, Depth Moments & Audio Mastering Reference

This reference manual documents the programmatic post-production, talking-head editing, motion graphics staging, Arabic kinetic typography, and audio mastering architecture of **CineFlow AI Studio** (`FFmpeg + Whisper + Remotion / HTML5 Canvas + NLE Export`).

---

## 1. Twelve Autonomous Production & Editing Pipelines (`مسارات الإنتاج والمونتاج الاثنا عشر`)

Automatically route the user's input to the matching production pipeline without interrogating them with unnecessary questionnaires:

| Input / User Request | Active Pipeline (`pipeline_type`) | Core Execution Architecture |
| :--- | :--- | :--- |
| **1. Raw Idea, Topic, or Script for AI Cinema** | **`route_1_generative_cinema`** | 5-Batch Research ➔ `Nano Banana 2 Lite` (0-credit Keyframes) ➔ `Gemini Omni 1.2 Flash` / `Veo 3.1` / `Seedance 2.0` with `@Character`/`@Product` Lock & Scene Handshake |
| **2. Talking-Head Camera Recording (`فيديو متحدث للكاميرا`)** | **`route_2_talking_head_reel`** | Dropped-frame & HDR check ➔ Dual-threshold silence cut (`120ms/150ms` breath pad) ➔ Whisper hallucination & dialect fix ➔ 4-state layout (`R_FULL/R_DOWN/R_LOWER/R_OFF`) + Depth Moments + RTL captions |
| **3. Text/Script Only — 60fps Motion Film** | **`route_3_motion_stage_60fps`** | Voiceover ➔ 60fps `Remotion` or `HyperFrames` HTML/CSS/GSAP stage (`one-take`, `slideWall`, Action-Verb Stage actors anchored to spoken words) |
| **4. Folder of Silent Clips (`مقاطع بلا كلام`)** | **`route_4_silent_broll_montage`** | Multi-clip quality scan (`Clarity × Motion × Exposure × Color`, trim first/last `0.33s`) ➔ Contact sheet review ➔ Beat/Onset grid cut (`[1.0, 0.82, 1.24, 0.94]` cadence) ➔ `-14 LUFS` master |
| **5. Multi-Cam or Long Episode (`بودكاست / حلقة 16:9`)** | **`route_5_multicam_podcast`** | Diarized transcript mining ➔ Dynamic face-tracked `9:16` crop (`facetrack`) ➔ Mandatory 3-variant Hook Banner from strongest quote ➔ Batch Clip Factory delivery |
| **6. Website URL or App Walkthrough (`شرح موقع أو تطبيق`)** | **`route_6_3d_device_explainer`** | Automated screen/scroll capture (`website-to-video` or synthetic `TerminalScene`) ➔ `1080x1220` safe-zone framing (`<= 1.25x` zoom) ➔ Pointer click ripples & 3D iPhone/MacBook framing |
| **7. Real-Footage Documentary Montage (`مونتاج وثائقي من لقطات حقيقية`)** | **`route_7_documentary_montage`** | **Retrieval-First Real-Footage Engine**: Builds CLIP-searchable corpus from `Archive.org`, `NASA`, `Wikimedia Commons`, `Pexels`, & `Unsplash` (`corpus >= 8x slots`, `score >= 0.22`, semantic `diversify`), cuts by Kuleshov juxtaposition, applies uniform LUT across mixed-era footage, and composites a mandatory philosophical Remotion ProRes 4444 alpha `end_tag` |
| **8. Hand-Drawn Doodle or Rigged Cartoon (`تحريك شخصيات / Ink Theater`)** | **`route_8_character_animation_ink_theater`** | **3-Step Xiaohei Metaphor (`Abstract Concept ➔ Physical Action ➔ Low-Tech Contraption`)** + `InkPuppet` CMU Mocap catalog (`walk, run, climb, march, shuffle, jump, kick, sit, wave, twist, dance_spin, dance_glide` — never hand-tuned sine curves, never looping a single clip) + FABRIK inverse kinematics (`.reachL/.reachR`) |
| **9. Continuous 3D World Fly-Through (`عالم ثلاثي الأبعاد متصل`)** | **`route_9_3d_world_generation`** | Coarse-to-fine semantic terrain (`blockout` ➔ `production`), CC0 GLTF/GLB catalogs + `Atlas Tripo H3.1` / `fal Hunyuan 3D`, slope/contact constraints, and continuous `global ➔ regional ➔ walk` camera path rendered in **Blender 4.5 LTS (`Eevee Next`)** or **HyperFrames + Three.js** |
| **10. Reference Video URL / Clip (`فيديو مرجعي: اصنع لي مثل هذا`)** | **`route_10_reference_video_cloner`** | Inspects `motion_type` (`motion_clip / animated_still / static_image`) + `flow_variance` ➔ Outputs **CHAI 5-Aspect Shot Breakdown** ➔ Proposes **2–3 differentiated concepts** (never a carbon copy) ➔ Renders **10–15s Sample-First Preview** before full production |
| **11. Avatar Presenter & Lip-Sync Spokesperson (`مذيع ذكي`)** | **`route_11_avatar_spokesperson`** | `Google Flow Voice Lock`, `Kling Official Avatar / Lip-Sync`, or local `SadTalker / MuseTalk / Wav2Lip` + Remotion `TalkingHead` composition (`<= 6 words` per fast cut) |
| **12. Multi-Language Localization & Dubbing (`ترجمة ودبلجة`)** | **`route_12_localization_dub`** | Diarized transcript truth ➔ Glossary-locked translation ➔ Timing-risk mapping ➔ `Google Chirp3-HD` (700+ voices) / `ElevenLabs` / `Azure SSML` dubbing + optional lip-sync |

---

## 2. Talking-Head Intake, Silence Cutting & Transcript Integrity (`معالجة التسجيل وقص الصمت وتدقيق التفريغ`)

### 2.1 Pre-Cut Signal Diagnostics (`فحص الفريمات والإضاءة والـ HDR`)
1. **Dropped-Frame Detection & Optical-Flow Repair**:
   - Mobile browser recordings frequently drop `13%–54%` of frames. Inspect frame PTS gaps (`delta > 0.07s`) via `ffprobe`; if gaps exist, repair before cutting using optical flow:
     ```bash
     ffmpeg -i src.mov -vf "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" -c:a copy src_fixed.mov
     ```
2. **iPhone HDR-to-SDR Protection**:
   - Convert 10-bit HLG / Dolby Vision iPhone footage using accurate tone-mapping to `BT.709` so skin tones never look washed out or artificially graded.
3. **Zero Unwanted Color Grading on Presenter Skin (`grade: false` Default)**:
   - Never apply heavy LUTs, tints, or blurs over a real presenter's face unless explicitly requested. Theme colors apply strictly to motion cards, backgrounds, and typography. Only offer `"grade": "auto"` if scopes detect severe underexposure or yellow color cast, and show a 1-frame Before/After first.

### 2.2 Adaptive Two-Pass Silence Cutting with Breath Padding (`قص الوقفات التكيّفي مع حماية التنفس`)
1. **Two-Pass Adaptive Silence Detection (`remotion-markup/silence-detection.md`)**:
   - **Pass 1 (Measure Audio Floor):** Extract `input_thresh` dynamically via `loudnorm`:
     ```bash
     ffmpeg -hide_banner -vn -i raw_aroll.mp4 -af "loudnorm=print_format=json" -f null -
     ```
   - **Pass 2 (Detect Silence Using Measured Floor):** Feed `input_thresh` (or fallback `-32dB`) into `silencedetect`:
     ```bash
     ffmpeg -hide_banner -vn -i raw_aroll.mp4 -af "silencedetect=noise=${INPUT_THRESH}dB:d=0.35" -f null -
     ```
   - Deliberate/calm speakers (contemplative storytelling): ask before cutting silence (`--keep-silence`).
2. **Natural Breath Padding Window**:
   - Expand every kept speech segment `[word_start, word_end]` by **Pre-Roll = `120ms`** (preserves natural breath intake) and **Post-Roll = `150ms`** (protects Arabic final consonants `ق، ط، ك، ت، ب، د`).
   - Merge consecutive speech segments separated by `< 180ms`, and apply a `20ms` triangular audio crossfade (`acrossfade=d=0.02:c1=tri:c2=tri`) at every splice to eliminate clicks.
3. **Duplicate Take & Retake Removal**:
   - When a speaker repeats a sentence to correct a slip of the tongue, **the first take is the mistake and the second take is the correction**. Flag duplicate sentences in the numbered transcript and drop the faulty first take before designing scenes.

### 2.3 Whisper Word-Level Verification & Dialect Fixing
1. **Hallucination & Missing-Speech Check**:
   - Scan Whisper JSON output for hallucination loops (same phrase repeated `3x` consecutively, single word repeated `4x`, or known YouTube outro hallucinations like `"اشترك في القناة"`) and speech-energy gaps with zero transcribed words.
   - Re-transcribe flagged `< 25s` audio windows in isolation with `--condition_on_previous_text False` and merge back with offset adjustment.
2. **Word-Count-Locked Dialect Correction (`fixes.json`)**:
   - Correct Gulf/Arabic colloquial words misheard by Whisper while keeping the **exact word count per sentence** identical to Whisper's token count so word-level timestamps remain 100% locked.

---

## 3. The 4-State Spatial Layout & Headout Architecture (`قاعدة التخطيط البصري الرباعية`)

Every moment of a vertical (`1080x1920`) video dynamically transitions across four spatial states based on semantic meaning:

| Layout Mode | Visual Structure (`1080x1920`) | When to Use | Mandatory Framing & Caption Rules |
| :--- | :--- | :--- | :--- |
| **`R_FULL`** | **Full-Screen Presenter / Hero Shot** | Opening `0–1.5s` hook, emotional direct-to-camera delivery, narrative transitions | Caption sits below chin (`bottom Y: 1460` or `chunk` center `Y: 1395`), progress bar at `Y: 1492`. Dynamic zoom punch-in (`1.0x <-> 1.12x–1.18x`) locked per cut. |
| **`R_DOWN`** | **Top Graphic (`Y: 280–520`) + Full-Width Bottom Presenter** | Quick visual illustrations, icons, or compact stage animations while keeping strong speaker presence | Fixed crop `1.5%` above the speaker's highest head point (`cardTop`) — **never crop the forehead and never leave an empty ceiling gap**. Caption sits **above** the video card seam, never on the face. |
| **`R_LOWER` + `Headout`** | **Top 2/3 Design Board + Small Bottom Presenter with `Headout`** | Rich infographics, multi-actor stage scenes, comparisons, or B-roll showcases needing 2/3 screen height | Use `headout` (speaker's head pops above the small bottom card border with locked `headbox` coordinates so the card never jitters). Set `nocap: true` when the top graphic already displays the spoken words. |
| **`R_OFF` (`Takeover`)** | **100% Full-Screen Visual Stage / B-Roll / 3D UI** | Data-heavy breakdowns, numbers, lists, 3D product reveals, or full Veo 3.1 cinematic B-roll | Presenter hidden while voiceover continues (`J-Cut / L-Cut` `0.15s–0.25s` audio lead). Return cleanly to `R_FULL` by expanding the focal graphic element to `>= 1080x1920` over `0.32s` before an instant `0.001s` underlying cut. |

### Calmness & Visual Pacing Guardrails (`حدود الهدوء والتوازن البصري`)
- **No Graphic in the First `1.5 Seconds`**: Open on the speaker (`R_FULL`) with immediate kinetic motion (`hookZoom` or a 3-layer `stack` hook behind the head).
- **Breathing Room**: Leave at least **`2.0 seconds` of `R_FULL` speaker** between consecutive graphics scenes.
- **Density Ceiling**: Maximum **`5` graphics scenes per `30 seconds`** (at most `3` full-screen `R_OFF` takeovers), and total graphics duration must not exceed **`70%` of the video**.
- **Scene Lifespan**: Full-screen `R_OFF` scenes last **`2.0s – 6.0s`**; split-screen (`R_DOWN` / `R_LOWER`) scenes last **`2.0s – 9.0s`**.
- **The `+0.45s` Hold-After-Last-Word Law**: A motion graphic or caption **must never vanish on the exact millisecond the speaker finishes the last word**. Hold the resolved state for **`0.3s – 0.6s` (`+0.45s` standard)** after the final word of the sentence, then ease out smoothly over `0.4s` (`end_time = last_word_end + 0.45s`).
- **Facts Ledger (`facts.md`)**: Every number, price, percentage, date, or proper noun displayed on screen must be verified verbatim from the speaker's transcript or supplied source—never invented.

---

## 4. Action-Verb Stage (`stage`) & Word-Anchored Timing (`التحريك بالفعل والتوقيت المربوط بالكلمة`)

### 4.1 Draw the Verb, Never Repeat the Subtitle (`الرسمة تشرح بالفعل لا بالكتابة`)
The viewer already hears the speech and reads the captions. Cards that merely repeat the spoken sentence as bullet text look like dated templates. At least **two-thirds (`67%+`) of all graphic scenes** must be **Action-Verb Stages (`stage`)** that translate the sentence's **verb** into moving visual actors (`3 to 6 actors` per scene):

| Sentence Action / Verb | Stage Choreography (`actors` + `camera`) |
| :--- | :--- |
| **Aggregation (`تجميع`)** | Central hero actor (`building` / `store` at `x:0.5, y:0.48, hot:true`); supporting actors (`laptop`, `person`, `truck`, `gear`) enter from edges on their exact spoken `word` and connect via animated dotted `link` lines. |
| **Import / Source (`استيراد / مصدر`)** | `globe` spawns first; child objects emerge from it (`enter: "from:globe"`) and fly in a curved arc (`to`, `toWord`) into the central recipient, triggering a particle pulse. |
| **Transformation (`تحويل`)** | Actor A pulses on `pulseWord`, flies into Actor B (`to`, `toWord`), and Actor B scales up with a golden/accent halo. |
| **Replacement (`استبدال`)** | Old choice steps aside and shrinks (`moveX: 0.24, moveSize: 0.34, moveWord`), while the new solution rises into center stage (`enter: "rise", hot: true`). |
| **Growth / Metric (`نمو / أرقام`)** | `chart` or `up` arrow paired with a tabular-numeral counter (`value: "80", unit: "ألف"`) while the stage camera pushes in (`zoom: 1.15`). |
| **Risk / Penalty (`خطر / غرامة`)** | `doc` appears, followed by `warning` pulsing on `pulseWord` alongside the penalty `value`. |
| **Comparison (`مقارنة`)** | Two options flank a central `scale`; the winning side triggers `hot: true` and `pulseWord` on the verdict word. |

### 4.2 Word-Anchored Timing (`اربط بالكلمة، لا تكتب أرقاماً عشوائية`)
Bind every actor's entrance, movement, link, and pulse directly to the **exact spoken Arabic word** from the corrected transcript (`word`, `toWord`, `pulseWord`, `moveWord`, `outWord`) rather than guessing seconds:
```json
{
  "type": "stage",
  "layout": "split",
  "actors": [
    {"id": "co", "obj": "building", "x": 0.5, "y": 0.48, "size": 0.88, "word": "الشركة", "hot": true},
    {"id": "sw", "obj": "laptop", "x": 0.16, "y": 0.22, "size": 0.38, "enter": "left", "word": "البرامج", "label": "برامج", "link": "co"},
    {"id": "tm", "obj": "team", "x": 0.84, "y": 0.22, "size": 0.38, "enter": "right", "word": "الفريق", "label": "فريق العمل", "to": "co", "toWord": "تشغيل"}
  ],
  "camera": [{"word": "تشغيل", "zoom": 1.12, "x": 0.5, "y": 0.48}]
}
```

---

## 5. The 17 Visual Styles, 8 Color Palettes & Signature Depth Moments (`بنك الستايلات ولحظات العمق`)

### 5.1 The 17 Visual Design Styles (`styles`) & Style Fusion (`A+B`)
Select one coherent visual style (or fuse two complementary styles like `explainer+keynote`) based on the video's purpose:
1. **`keynote`**: Minimalist high-impact reveal; single massive word behind speaker's head, single accent color.
2. **`glassUI` (`liquid-glass`)**: Frosted glassmorphic UI cards, notifications, and app walkthroughs.
3. **`explainer` (`section-deck`)**: Journalism/investigative look with yellow highlighter sweeps, pinned clippings, and red connector strings.
4. **`paperCut` (`kinetic-paper` / `paper-collage`)**: Tactile cutout paper aesthetic with white sticker borders and 12fps stop-motion quantization (`tq(t)`).
5. **`archive` (`documentary`)**: Sepia/grain background layer, typewriter labels, map routes (`map-route`), and official stamps (`claim-proof`).
6. **`editorial` (`magazine-interview`)**: High-fashion/business magazine layout with thin rules, chapter quotes, and `verdict` cards.
7. **`swiss`**: International Typographic Grid (`Red / Black / White`), tabular data, zero rotation.
8. **`doodle`**: Hand-drawn animated circles, boiling arrows (`doodleBoil`), and sketchy emphasis.
9. **`terminal`**: Dark developer console, monospace LTR command lines, and AI tool showcases.
10. **`riso`**: Two-ink print plate misregistration with halftone dots (for hooks or artistic chapters).
11. **`newsprint`**: Unfolding broadsheet newspaper layout for breaking news and industry analysis.
12. **`blueprint`**: Technical cyan grid, white CAD line-work, dimension arrows, and mechanical breakdowns.
13. **`vhs`**: Retro analog scanlines & chromatic aberration (**1–3s moment only**, never over Arabic captions).
14. **`brutal`**: Neo-brutalist thick black borders, hard offset shadows, and kinetic shake (**1–3s hook/CTA moment only**).
15. **`studio3D`**: Matte 3D product stage with floating check tags and radial rim light.
16. **`stickerToon` (`cartoon`)**: Thick uniform black outlines, speech bubbles, and illustrated narrator mode (`sourceKind: "cartoon"`).
17. **`devCard` (`calligraphic-receipts` / `grid-glide`)**: Crisp white card over radial grid with Ruq'ah/Kufi accent words, `meter-receipt` bars, and `ticket-offer` cards.

### 5.2 The 8 Curated Color Palettes (`palettes`)
When the user does not supply custom brand hex codes (`colors: {acc, acc2, bg}`), select from:
- `midnight` (Electric Navy `#0B1026` + Cyan/Violet), `ocean` (Deep Sea + Turquoise), `sunset` (Deep Burgundy + Warm Orange/Pink), `emerald` (Dark Forest + Emerald/Lime), `gold` (Warm Luxury Black + Royal Gold `#FFD60A`), `neon` (Pitch Black + Cyber Neon Green), `mono` (High-Contrast Black/White/Slate), or `paper` (Warm Editorial Cream + Burnt Orange).

### 5.3 Planning 2–3 Signature Depth Moments per Reel (`لحظات العمق والواو البصري`)
Before rendering, design **2 to 3 signature depth moments** so the video feels custom-directed from the first second:
1. **3-Layer Stacked Hook (`stack`) & Behind-Head Kashida Text (`behind_text`)**:
   - **3-Layer Hook**: 1 massive Kashida-stretched word above the head (`Y >= 170`) + 1–2 words behind the head + remaining phrase below the chin (`Y <= 1490`).
   - **Strict Arabic Kashida Law (`قواعد الكشيدة الصارمة`)**:
     - Insert Kashida (`ـ`) **only after a letter that connects to the following letter**. Never insert Kashida after non-connecting letters (`ا أ إ آ د ذ ر ز و ؤ ة ء ى`), never split the `لا` ligature, and always place the Kashida **after** any diacritic (`Harakat: ّ َ ُ ِ ْ`), never between a base letter and its Shadda/Fatha.
     - Stretch Kashida smoothly **by pixel width** (never bydiscrete character count, which causes jitter) so the Arabic letters sit cleanly to the right and left of the speaker's head while **only the Kashida bar passes behind the head**.
2. **Voice-Reactive Waveform (`MV.env`) or Dot-Map (`dotMap`) Behind the Speaker**:
   - Render an audio-reactive bar waveform or expanding world dot-map on the `'video'` layer behind the rotoscoped speaker (`MV.person`).
3. **Brand-Colored Wall Illumination (`brandLight`)**:
   - When the brand name or key breakthrough is spoken, ignite the background wall behind the rotoscoped speaker with the brand's official hex colors (`multiply` + `screen` radial halo with a `0.3s` bulb-flicker ignition) while keeping the speaker's face 100% untouched.
4. **3D Orbital Ring (`orbit`) & Spark Shape Transitions (`sparkReveal`)**:
   - Orbit 3 key concepts in 3D space around the speaker (drawing the back half of the ellipse before `MV.person` and the front half after `MV.person`), and transition between major locations by expanding the brand's SVG emblem (`Path2D`) across the cut frame.

---

## 6. Arabic Kinetic Captions, Safe Zones & Pre-Flight Visual QA (`الكابشن العربي والمناطق الآمنة`)

### 6.1 Caption Presentation Modes (`capStyle`)
- **`chunk` (4-Word Capsule — Best for Natural Talking-Head & Educational Reels)**: Single-line rounded pill (`max width <= 800px`, centered at `Y: 1395` in `R_FULL` or above the card in `R_DOWN`/`R_LOWER`). Active spoken word highlights in accent color (`acc`) without vertical jumping; stays visible across micro-pauses `< 0.8s` and holds `+0.45s` after sentence end.
- **`word` / `card` / `shadow` / `bar` / `underline` / `type`**: Word-by-word highlight with optional `hot` word scale pop and word-level physics (`fx`: `drop`, `shake`, `crack`, `type`, `pulse`, `stretch`, `slam`).
- **Luxury Still Mode (`capStill: true`)**: For high-ticket luxury commercials, disable bounce/scale pops and transition captions purely via smooth opacity + color highlight.
- **Forbidden by Default**: Never animate Arabic text letter-by-letter (which breaks cursive contextual shaping); always animate whole words or connected glyph segments. Never place captions over the speaker's face, and automatically hide captions (`nocap: true`) during any window where motion graphics already write the spoken words on screen.

### 6.2 Platform Safe-Zone & Video-First Layout Enforcement (`1080x1920` Vertical 9:16 & `video-layout.md`)
- **Design a Video, Not a Webpage (`remotion-create/video-layout.md`)**:
  - Build each scene around **one primary visual focal point** rather than stacking 3–4 small dashboard panels.
  - **Minimum Typography Scale (`1080px`-wide compositions)**: Main headline **`>= 84px`**, Important supporting text **`>= 44px`** (use `@remotion/layout-utils` `fitText()` / `measureText()` to prevent overflow).
  - **Generous Safe Margins**: Keep all important text at least **`80px`** from left/right edges and **`100px`** from top/bottom edges.
- **Top Dead Zone (`9:16`)**: `Y: 0 – 220` (Instagram/TikTok header & status bar).
- **Bottom Dead Zone (`9:16`)**: `Y: 1500 – 1920` (Account handle, caption drawer, audio marquee, Shop CTA).
- **Right Action Column (`9:16`)**: `X: 920 – 1080` between `Y: 1050 – 1750` (Like, Comment, Share, Save icons).

---

## 7. 4-Bus Audio Mastering & NLE / Studio Delivery (`معايرة الصوت والتسليم المتعدد`)

1. **Loudness & Dynamic Mastering**:
   - Normalize integrated loudness to **`-14.0 LUFS`** with True Peak capped at **`-1.0 to -1.5 dBTP`** (`loudnorm=I=-14:TP=-1.5:LRA=11`).
2. **Meaningful SFX Discipline**:
   - Trigger SFX (`whoosh_up`, `whoosh_down`, `thud`, `tap`, `pop`, `tick`, `sub_drop`) **only on real visual state changes** (maximum **15 SFX events per minute**, peak capped below **`-18 dBFS`**).
   - Call background audio `"ملف صوتي بالخلفية"` (`bg-audio.mp3`) rather than assuming music, and auto-duck it under speech (`sidechaincompress` `attack=15ms, release=450ms`).
3. **Multi-Target Export & Live Timeline Editor**:
   - Deliver the mastered `.mp4` (with the `1080x1080` Safe-Square Cover injected into the first `0.1s` frame and file size optimized `< 29 MB`), alongside `.srt` subtitles, `.txt` transcript, **CapCut editable project (`draft_content.json`)**, or launch the **Interactive Browser Timeline Editor (`editor.mjs` / `studio.html`)** so the creator can tweak cuts, captions, and scene timings visually.

---

## 8. Dual Composition Runtimes (`Remotion` vs. `HyperFrames` HTML/CSS/GSAP) & Bespoke `Atelier` Doctrine

### 8.1 Runtime Decision Matrix (`render_runtime`: `remotion` | `hyperframes` | `ffmpeg`)
Lock `render_runtime` at the proposal stage and carry it through `edit_decisions` without silent swaps:

| Production Scenario | Optimal `render_runtime` | Engineering Rationale |
| :--- | :--- | :--- |
| **Talking-Head Reels, Word-by-Word RTL Captions (`remotion_caption_burn`), Avatar `TalkingHead`, ProRes 4444 End-Tags, `TerminalScene`** | **`remotion`** | React-based frame-accurate composition, native word-level caption overlays, and alpha-channel ProRes 4444 overlays. |
| **Kinetic Typography, Product Promos, Launch Reels, `website-to-video`, `Ink Theater` / Rigged SVG Characters (`npx hyperframes`)** | **`hyperframes`** | HTML/CSS/GSAP native medium with **36+ atomic motion rules** (`kinetic-beat-slam`, `3d-text-depth-layers`, `motion-blur-streak`), **7 runtime adapters** (`GSAP, Lottie, Three.js, Anime.js, CSS, WAAPI, TypeGPU` + `html-in-canvas` WebGL UnrealBloom), and `npx hyperframes beats` music-drop locking. |
| **Pure Multi-Clip Concat, Trim, LUT Grading, or Blender PNG Sequence Packaging** | **`ffmpeg`** | Zero browser overhead; direct stream copy or high-speed filtergraph mastering. |

### 8.2 Authoring Mode (`composition_mode`: `atelier` vs. `templated`) & No-Hero-Component-Spine Law
1. **Reuse Engine Knowledge, Never Creative Components (`Atelier` Default for Hero Work)**:
   - For marketing launches, brand films, and hero explainers, lock `composition_mode = "atelier"` (hand-authored composition with a custom `art_direction` and `taste_profile`). Reserve `"templated"` (`text_card, stat_card, bar_chart`) strictly for batch output, localization variants, or rapid internal drafts.
2. **The No-Hero-Component-Spine Law (`منع تكرار العنصر البصري بين المشاهد`)**:
   - Never reuse the same primary visual subject across multiple scenes with only the text changed underneath. Every scene must earn its own primary visual subject (a character, a diagram, a piece of evidence, a spatial transformation, a typographic beat).
   - The piece's **Signature Visual Device** may appear in **at most 1 to 2 climactic beats** — never as visual scaffolding across every scene.
3. **Captions vs. On-Screen Text Dedup Law (`منع ازدواجية الكابشن والنص المرسوم`)**:
   - Never display an on-screen headline (`SerifLine` / `TextCard`) and an auto-caption that echo the exact same spoken phrase simultaneously. Set `captions = []` (`nocap: true`) on any scene where the on-screen typography already carries the spoken line.

### 8.3 Hard-Earned HyperFrames & Stock-Footage Production Fixes
- **Preventing the `640x360` Letterbox Trap (Scale-to-COVER, Never Scale-to-FIT)**:
  Free stock clips often download at `640x360`. Pre-transforming with `force_original_aspect_ratio=decrease,pad=...` creates a tiny centered box inside black bars. Always pre-transform footage-forward clips with **Scale-to-COVER + Unsharp**:
  ```bash
  ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,unsharp=3:3:0.6" -c:v libx264 -r 30 -g 30 -keyint_min 30 -sc_threshold 0 -movflags +faststart prepped.mp4
  ```
- **Dense Keyframes (`-g 30 -keyint_min 30`) & `--workers 1`**: Prevents `video_heavy_parallel_timeout` and frame freezes in headless Chrome when rendering `> 5` video elements.
- **Deterministic Font Whitelist**: In HyperFrames, use `Outfit`, `Montserrat`, `Inter`, `JetBrains Mono`, `Poppins`, `Playfair Display`, or local full-charset `@font-face` `.ttf` files (`Cairo`, `Tajawal`, `PatrickHand`) — never `Space Grotesk` or subsetted Google Fonts `woff2` URLs.
- **Mandatory Pre-Render Gate**: Always run `npx hyperframes lint --json && npx hyperframes check --json --snapshots --caption-zone && npx hyperframes snapshot --review --json` before executing `npx hyperframes render`.
