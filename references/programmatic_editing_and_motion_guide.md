# Programmatic Video Editing, Motion Graphics Stage, Depth Moments & Audio Mastering Reference

This reference manual documents the programmatic post-production, talking-head editing, motion graphics staging, Arabic kinetic typography, and audio mastering architecture of **CineFlow AI Studio** (`FFmpeg + Whisper + Remotion / HTML5 Canvas + NLE Export`).

---

## 1. Six Production & Editing Routes (`مسارات الإنتاج والمونتاج الستة`)

Automatically route the user's input to the matching production mode without interrogating them with unnecessary questionnaires:

| Input / User Request | Active Route | Core Pipeline |
| :--- | :--- | :--- |
| **1. Raw Idea, Topic, or Script for AI Video** | **`Generative AI Cinema Studio`** | Scriptwriting ➔ `Nano Banana 2 Lite` (0-credit Keyframes) ➔ `Gemini Omni Flash 1.1` / `Veo 3.1` with `@Character`/`@Product` Lock & Scene Handshake |
| **2. Talking-Head Camera Recording (`فيديو متحدث للكاميرا`)** | **`Talking-Head Reel & Ad Editor`** | Dropped-frame & HDR check ➔ Dual-threshold silence cut ➔ Whisper word-level transcription & hallucination check ➔ Dynamic zoom & 4-state layout ➔ Word-anchored motion & RTL captions |
| **3. Folder of Silent Clips (`مقاطع بلا كلام: مقهى، منتج، فعالية`)** | **`Beat-Synced B-Roll Montage`** | Multi-clip quality scan (`Clarity × Motion × Exposure × Color`, trim first/last `0.33s`) ➔ Contact sheet review ➔ Beat/Onset grid cut (`[1.0, 0.82, 1.24, 0.94]` cadence) ➔ `-14 LUFS` audio master |
| **4. Multi-Cam or Long Episode (`بودكاست / حلقة 16:9`)** | **`Podcast & Long-Form Clipper`** | Topic segmentation ➔ Dynamic face-tracked `9:16` crop (`facetrack`) ➔ Mandatory 3-variant Hook Banner from strongest quote ➔ Multi-clip Reel delivery |
| **5. Text/Script Only — No Presenter (`فيلم موشن جرافيك من نص`)** | **`60fps Full Motion Graphics Film`** | Voiceover generation/ingest ➔ 60fps 3D/2D Canvas/Remotion stage (`one-take`, `slideWall`, kinetic Arabic typography, action-verb actors) |
| **6. Website URL or App Walkthrough (`شرح موقع أو تطبيق`)** | **`3D Device & Screen Explainer`** | Automated screen/scroll capture ➔ `1080x1220` safe-zone framing (`max 1.25x` zoom to preserve text sharpness) ➔ Pointer click ripples, highlight callouts, & 3D iPhone/MacBook framing |

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

### 2.2 Dual-Threshold Silence Cutting with Breath Padding (`قص الوقفات مع حماية التنفس`)
1. **Silence Detection**:
   ```bash
   ffmpeg -i raw_aroll.mp4 -af "silencedetect=noise=-32dB:d=0.35" -f null -
   ```
   - Deliberate/calm speakers (e.g., Qur'an recitation, contemplative storytelling): ask before cutting silence (`--keep-silence`).
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

### 6.2 Platform Safe-Zone Enforcement (`1080x1920` Vertical 9:16)
- **Top Dead Zone**: `Y: 0 – 220` (Instagram/TikTok header & status bar).
- **Bottom Dead Zone**: `Y: 1500 – 1920` (Account handle, caption drawer, audio marquee, Shop CTA).
- **Right Action Column**: `X: 920 – 1080` between `Y: 1050 – 1750` (Like, Comment, Share, Save icons).

---

## 7. 4-Bus Audio Mastering & NLE / Studio Delivery (`معايرة الصوت والتسليم المتعدد`)

1. **Loudness & Dynamic Mastering**:
   - Normalize integrated loudness to **`-14.0 LUFS`** with True Peak capped at **`-1.0 to -1.5 dBTP`** (`loudnorm=I=-14:TP=-1.5:LRA=11`).
2. **Meaningful SFX Discipline**:
   - Trigger SFX (`whoosh_up`, `whoosh_down`, `thud`, `tap`, `pop`, `tick`, `sub_drop`) **only on real visual state changes** (maximum **15 SFX events per minute**, peak capped below **`-18 dBFS`**).
   - Call background audio `"ملف صوتي بالخلفية"` (`bg-audio.mp3`) rather than assuming music, and auto-duck it under speech (`sidechaincompress` `attack=15ms, release=450ms`).
3. **Multi-Target Export & Live Timeline Editor**:
   - Deliver the mastered `.mp4` (with the `1080x1080` Safe-Square Cover injected into the first `0.1s` frame and file size optimized `< 29 MB`), alongside `.srt` subtitles, `.txt` transcript, **CapCut editable project (`draft_content.json`)**, or launch the **Interactive Browser Timeline Editor (`editor.mjs` / `studio.html`)** so the creator can tweak cuts, captions, and scene timings visually.
