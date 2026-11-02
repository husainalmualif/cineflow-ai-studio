# B Studio (`v1.0.10`) & Video-Edit (`v1.1`) Mastery — Zero-Loss Pipeline, 4 Window States, Vox Collage & Interactive NLE

> **Integration Scope**: Synthesizes the field-tested production rules (`1–118`), preflight/post-render quality gates (`05b_sfx_audit`, `18_stage_from_scenes`, `19_scene_audit`, `20_voice_check`, `21_color_check`, `22_preflight`, `23_gaze_check`, `24_cut_align`, `25_flash_check`), the **Vox Paper-Collage Kit**, and the **Interactive NLE Timeline & Studio-Chat** architecture into `cineflow-ai-studio`.

---

## 1. Zero-Loss Voice & Color Preservation Pipeline (Rules 4, 19, 28, 74, 87, 90)

### 1.1 Two Separate Audio Streams (Never Render Final Audio from the Whisper Track)
- **Whisper Transcription Track (`a.wav`)**: `16 kHz` mono (`-ar 16000 -ac 1`) used **exclusively** for word-timestamp extraction (`01_transcribe.py`). Deleting or muxing this track into the final video destroys high frequencies (`> 8 kHz`) and stereo image.
- **Master Voice Track (`voice.wav`)**: Extracted from the cut source (`cutz.mp4` / `src.mov`) at **full `48 kHz` 24-bit stereo (`pcm_s24le`, `-ar 48000 -ac 2`)**.
- **Default `0 dB` Voice Policy (Rule 19)**:
  - Never apply dynamic normalizers (`dynaudnorm`, `loudnorm`, `acompressor`) to the speaker's voice unless explicitly requested; dynamic filters pump the noise floor during pauses and alter vocal timbre.
  - If the user explicitly requests loudness normalization to `-16 LUFS`, measure integrated loudness first (`ebur128`) and apply a **single fixed gain (`volume=<diff>dB`)** so crest factor and vocal dynamics remain `100%` untouched.
- **Post-Render Voice Verification (`20_voice_check.py`)**:
  - Subtracts `sfx.wav` from the delivered `.mp4` audio stream (`c = out_audio - sfx_audio`) and compares `c` against `voice.wav`:
    - **Waveform Correlation**: $\text{corr}(v, c) \ge 0.999$
    - **Gain Drift**: $|\Delta \text{RMS}| < 0.15\text{ dB}$

### 1.2 Zero-Loss Color & Luma Pipeline (`bt709 / tv` + `4:4:4` Intermediate)
- **Why Default Remotion Shifts Color**: Feeding standard `4:2:0` video into headless Chromium without explicit color tags causes an untagged `bt601` decode (`\Delta Y \approx -1.7`, red-blue tilt `\approx +1.8`).
- **Mandatory 3-Step Fix**:
  1. Convert the cut source (`cutz.mp4`) into a **4:4:4 intermediate (`cutz444.mp4` / `video.mp4`)** explicitly tagged `bt709 / tv`:
     ```bash
     ffmpeg -y -i cutz.mp4 -c:v libx264 -crf 10 -pix_fmt yuv444p \
       -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv \
       -an remotion/public/video.mp4
     ```
  2. In Remotion, render **silent PNG frames** (`setVideoImageFormat('png')`, `<OffthreadVideo muted>`) with `--color-space bt709` and `--crf 15` (ensuring output bitrate $\ge \frac{1}{3}$ of source bitrate per **Rule 87**).
  3. Mux the rendered video with `voice.wav` + `sfx.wav` using `-c:v copy -c:a aac -b:a 256k -ar 48000`.
- **Post-Render Color Verification (`21_color_check.py`)**:
  - Samples quiet `FULL` windows (duration $\ge 2.0\text{s}$ and $< 8.0\text{s}$, starting after the `4.6s` hook zoom) across stored `Y/U/V` planes and player-decoded `RGB`:
    - Stream tags must equal `color_space = bt709`, `color_range = tv`.
    - Stored plane drift: $|\Delta Y| \le 0.6$, $|\Delta U| \le 0.4$, $|\Delta V| \le 0.4$.
    - Player RGB red-blue tilt: $|\Delta R - \Delta B| \le 0.8$.

---

## 2. Balanced Two-Line Word-Reveal Captions (`Captions.tsx` — Rule 76)

### 2.1 Balanced Word Partitioning (`even(ws, n)` — No Orphan Words)
- **Max 2 Lines per Caption Card (`maxLines = 2`)**: A caption card must never exceed 2 visual lines.
- **Balanced Splitting**: When a sentence exceeds `maxWidth` (`820px` on `1080×1920`, `1160px` on `1920×1080`) or `2` lines, split its words into $k = \lceil \text{lines} / 2 \rceil$ cards of **equal word count** (`split_caption_cards_balanced`), never leaving a single orphan word alone on a card or second line.

### 2.2 Pre-Spoken `visibility: 'hidden'` Layout Lock
- In word-by-word reveal captions, words that have not yet been spoken (`t < word.s - 0.04`) MUST render with `visibility: 'hidden'` (and `background: 'transparent'`) rather than `display: 'none'`.
- **Why**: `visibility: 'hidden'` reserves the exact final two-line bounding box from frame 1 of the card, eliminating layout reflow and horizontal text jumping as each Arabic word lights up.

### 2.3 Dynamic Caption Repositioning (`CAPMOVE`)
- Default caption top is `Y = 1230px` (`9:16`) or `Y = 890px` (`16:9`).
- When a scene graphic extends into the lower third, `CAPMOVE` smoothly interpolates caption `Y` (`capTop(t)`) over `0.28s` (`eio` cubic ease) to a safe coordinate (`1380px` or `1550px`) without colliding with the graphic.

---

## 3. The 4 Window States (`FULL`, `CARD`, `SIDE`, `NONE`) & Face/Hair Guard (Rules 77–82)

### 3.1 Tall `9:16` (`1080×1920`) Window Geometry
| Window Mode | Speaker Frame (`X, Y, W×H`) | Graphic Drawing Zone | Usage Rule |
|---|---|---|---|
| **`FULL`** | Full screen `1080×1920` | Above hair only: `Y: 200 .. fullFloor` (`fullFloor = face_top_y - 158`, default `420px`) | Quick `< 3s` badges/numbers (`<= 2` elements). Never draw over forehead or hair. |
| **`CARD`** | Centered card `940×612` at `X: 70, Y: 545` (`borderRadius: 28`) | Wide horizontal stage above card: `X: 70..1010, Y: 215..505` (`940×290`) | Horizontal comparisons, timelines, wide bars, 3-card strips. |
| **`SIDE`** | Half-frame right `470×835` at `X: 566, Y: 310` (`borderRadius: 26`) | Tall vertical column left: `X: 56..544, Y: 300..1160` (`488×860`) | Vertical stacks, ladders, gauges, multi-row lists, tall flowcharts. |
| **`NONE`** | Speaker hidden (`opacity: 0`) | Full canvas above captions: `X: 70..1010, Y: 215..1120` | Full-board scenes, large maps, complex mechanisms. |

### 3.2 Wide `16:9` (`1920×1080`) Window Geometry (`faceSide: 'right' | 'left'`)
- **`FULL`**: Full screen `1920×1080`; graphics stay in the opposite column (`X: 80..980` when `faceSide = 'right'`, never entering the speaker's face column `faceX ± 0.16 * FW`).
- **`SIDE`**: Speaker window `780×860` on `faceSide`; graphic stage `~1000×860` on the opposite half.
- **`CARD`**: Speaker window `1280×720` centered; graphic header above.
- **`NONE`**: Full `1920×1080` canvas above `Y = 860`.

### 3.3 Hard Window Transition & Pacing Laws (`validate_window_schedule_and_face_guard`)
1. **Minimum Window Hold (`>= 2.0s`)**: Never switch between `FULL`, `CARD`, `SIDE`, and `NONE` in less than `2.0s`. Merge adjacent graphics into the same window mode if the gap between them is `< 2.5s`.
2. **Minimum Speaker Return (`>= 2.5s`)**: Whenever the speaker returns to `FULL` between two graphics, they must stay in `FULL` for at least `2.5s` (otherwise keep the graphic window open and transition the graphic inside it).
3. **Full-Hide Cap (`NONE <= 2` per `2` minutes)**: Hide the speaker completely (`NONE`) at most twice per 120 seconds (excluding the first `3s` visual hook), so the video remains a human-led piece rather than a faceless slideshow.
4. **No Empty Windows (`<= 0.35s`) & No Frozen Graphics (`<= 2.5s`) (`19_scene_audit.py`)**:
   - Every non-`FULL` window must have an active graphic inside it within `<= 0.35s` of opening and until `<= 0.35s` before closing.
   - No graphic may remain static without a word-synced `p(t, a, b)` animation pulse for `> 2.5s` while the speaker moves on to a new clause.
5. **`baked_faces` Guard**: Never bake the speaker's video frame inside a pre-rendered graphic asset; the speaker video (`video.mp4`) must always remain a live timeline layer controlled by `stage.json`.

---

## 4. The 10 Visual Metaphor Mechanisms & Anti-Repeat Ledger (Rules 31, 63)

Every spoken concept is translated into a concrete **visual mechanism** (never a bulleted text slide or decorative icon beside a repeat of the caption):

| # | Mechanism ID | Visual Behavior | Ideal Concept |
|---|---|---|---|
| 1 | **`odometer`** | Rolling mechanical digit drums (`0→9` vertical strip) | Big numbers, prices, years, percentages |
| 2 | **`dotGrid`** | Grid of `20–100` dots where $K$ dots light up or drop out | Scarcity, odds (`1 in 25`), conversion ratios |
| 3 | **`donutSplit`** | Ring/pie slice that physically separates on the keyword | Market share, budget split, time allocation |
| 4 | **`flipCard`** | 3D/2D card that flips from "Myth/Before" to "Truth/After" | Corrections, plot twists, before/after |
| 5 | **`stackBlocks`** | Weighted blocks dropping and stacking with spring bounce | Compounding costs, accumulating steps/debts |
| 6 | **`growBars`** | Two competing horizontal/vertical bars racing from zero | Direct A vs. B speed/performance comparison |
| 7 | **`iconStrip`** | 3–4 tactile cards lighting sequentially on spoken items | Enumerated categories or toolkit items |
| 8 | **`windingPath`** | Dashed SVG path drawing between milestone pins | Chronological journey, pipeline stages |
| 9 | **`rings`** | Concentric target/orbit rings expanding from core | Core vs. peripheral layers, spheres of impact |
| 10 | **`gauge`** | Semicircular dial with needle sweeping into red zone | Risk level, pressure, saturation, urgency |

- **Anti-Repeat Mechanism Ledger (`mechanisms.json` & `13_repeat_check.js`)**:
  - Never repeat the same mechanism twice inside the same video.
  - Cross-check `mechanisms.json` across the creator's last `2` videos so consecutive episodes never reuse the same visual metaphors.
- **Behind-the-Person Accent Text (`11_behind_text.js`)**:
  - Used `1–2` times per video on a single peak keyword (`1–2` words, `160–230px` bold display font, positioned at `Y = 230..300px`) rendered **behind** the segmented speaker (`mask.mp4` via `rembg`/`u2net_human_seg`) with **Rule 53 Safe Kashida** (`1–2` tatweels in `ب/ت/ث/ن/ي/س/ش/ص/ض/ط/ظ/ف/ق/ك/ل/م/هـ`, never in `ا/د/ذ/ر/ز/و/ة/ء` or inside `لله`), keeping $\ge 70\%$ of the word visible above the shoulders.

---

## 5. Vox Paper-Collage Kit (`styles/collage/STYLE.md` & `kit/vox.tsx`)

When `style = "collage" | "vox" | "board"` is selected, scenes are built on a tactile investigation board (`BoardTexture` / cork / dark felt / grid paper) using physical paper props:

1. **Posterized 15fps Time (`step(t) = Math.floor(t * 15) / 15`)**:
   - Collage elements (`Scrap`, `Paper`, `HandStamp`, `Cut`, `Print`) animate using `step(t)` (**15fps "on twos" stop-motion feel**), while camera pans/zooms and the speaker's video remain at smooth `30/60fps`.
2. **Physical Fasteners (`PushPin`, `Tape`, `Yarn` / `yarnPath`)**:
   - Every pinned card has a `PushPin` near its top edge.
   - Red wool `Yarn` (`yarnPath(x1, y1, x2, y2, sag)`) connects pins across cards with gravity sag (`sag`), routing **around card edges** rather than cutting across text in the middle of a card.
3. **`HandStamp` & `RedX`**:
   - `HandStamp` animates a halftone hand entering from the top/outer edge (never crossing over the speaker's `CARD`/`SIDE` window), stamping an ink `Stamp` at `hit` timestamp (`±0.05s` of the spoken word) and retracting.
4. **Highlighter Isolation (`isolation: 'isolate'`)**:
   - `Highlight` uses `mixBlendMode: 'multiply'`. Its parent container MUST set `isolation: 'isolate'` so the yellow/red marker blends with the paper card underneath rather than darkening the dark background board into mud.

---

## 6. Measured Audio SFX Governor (`05b_sfx_audit.py` — Rules 1, 29, 54, 55, 70, 86)

Every SFX track is audited against **5 hard quantitative gates** (`audit_sfx_governor`):

1. **Word-Lock Accuracy (`<= 120 ms`)**: Every SFX timestamp must fall within $\pm 120\text{ ms}$ of a spoken word timestamp in `caps.json`.
2. **Onset Lead Compensation (`<= 60 ms`)**: Rising SFX (`whoosh`, `swell`) have a pre-peak rise time (`lead` in `sfx.lead.json`). Place the audio clip at `t_event - lead` so the **acoustic peak (`argmax > 0.25 * peak`)** lands within $\pm 60\text{ ms}$ of `t_event`.
3. **Minimum Inter-SFX Spacing (`>= 1.0 s`)**: No two SFX events may occur within $< 1.0\text{ s}$ of each other (prevents cluttered rapid-fire noise).
4. **Spectral Centroid Budget (`<= 2.0 / min` above `4 kHz`)**: At most `2` synthetic SFX per minute may have a spectral centroid $> 4000\text{ Hz}$ (sharp clicks/dings/snaps cause listener fatigue; low-centroid warm paper/wood/cloth sounds are preferred). Creator-owned custom library sounds (`lib`) are exempt.
5. **Dual Density Caps (`<= 10 / min` Transitions, `10..20 / min` Total, `<= 3` Repeats)**:
   - Transition SFX (`whoosh`, `tap`, `thud`, `swipe`, `ding`) $\le 10\text{ / min}$.
   - Total SFX (transitions + semantic word-locked sounds) between $10\text{ and }20\text{ / min}$.
   - Any single semantic sound effect may be used at most $3$ times in one video.
   - Peak SFX level is calibrated to **`+6 to +7 dB` above speaker voice RMS** (audibly present without masking speech).

---

## 7. Gaze-Raise Cuts, Source-Cut Alignment & Flash Prevention (`23`, `24`, `25`)

1. **Gaze-Raise Cut (`23_gaze_check.py` — Rule 91)**:
   - When a speaker glances down at notes between sentences, never cut back from `NONE` to `FULL` while their eyes are still lowered. Delay the window boundary to the **first frame their gaze rises to the lens**, even if the first syllable of the sentence begins slightly before the visual cut (J-cut).
2. **Source-Cut Alignment & Camera Velocity (`24_cut_align.py` — Rule 112)**:
   - If the source video already contains a hard edit at $t_{\text{cut}}$ and a graphic window ends at $B$ where $0.02\text{s} < t_{\text{cut}} - B \le 0.30\text{s}$, viewers see a jarring double-cut flash. Snap $B = t_{\text{cut}}$.
   - Never overlap two camera keyframes (`t1 >= t0 + d0`).
   - When panning across periodic/striped backgrounds (e.g., green-bar ledger paper with `168px` period) at peak smootherstep velocity $v_{\text{peak}} = \frac{1.875 \cdot \Delta d}{\text{dur} \cdot 30} > 120\text{ px/frame}$, keep pan duration $\ge 0.85\text{s}$ and apply directional motion blur (`feGaussianBlur stdDeviation="0 N"`).
3. **1–2 Frame White Flash Prevention (`25_flash_check.py`)**:
   - Never load images via CSS `backgroundImage: url(...)` in Remotion (Chromium does not block frame rendering on CSS background decode, causing 1–2 white frames). Always use Remotion's `<Img>` component or hidden `<Img>` preloaders.

---

## 8. Interactive `B Studio` NLE Operations (`edit-studio v1.0.10` & `studio-chat`)

### 8.1 Non-Destructive Timeline Operations (`ops-help.txt`)
When operating on an interactive timeline (`project.json`), prefer atomic timeline operations over regenerating from scratch:
- **Editorial Cuts & Timing**: `blade` (split clip), `rollSpine` (adjust cut point between two clips without shifting total duration), `slideSpine` (move clip between neighbors), `slip` (shift source in/out inside clip duration), `cutWords` (excise specific transcript word ranges), `capPauses` (clamp all silences above threshold to target ms), `detachVoice` (separate audio from video spine for J-cuts and L-cuts).
- **Framing, Openings & Motion**: `addOpening` (9 curated opening moves across 3 intensity tiers: gentle, medium, bold), `addMoveKey` / `addMoveFx` (keyframed zoom/pan curves), `setBehind` (toggle person segmentation depth for behind-the-speaker titles/scenes), `addTransition`.
- **Live Parameterized Scenes (`live scenes`)**: Scene components bind directly to `k.words` (live transcript timing) and `k.brand` (10 curated two-color palettes `bg + acc` from `onboarding.md`), so editing text or swapping brand palettes updates the motion graphics immediately without rewriting code.

### 8.2 Structured 5+1 Inspiration Session (`3أ — دوّر لي إلهام`)
When the user asks for creative direction before editing:
1. Present **5 distinct visual worlds** (`3` derived from the script's subject matter + `2` unexpected cross-domain worlds) plus a **6th hybrid mix option**, each pairing real reference frames with an actual rendered preview frame of the user's clip.
2. Once a direction is chosen, generate a **single-image 8–10 moment storyboard** classifying every key beat into one of four honest density levels:
   - `وجهه بس` (Speaker only — emotional/direct connection),
   - `صورة بسيطة` (Light badge/keyword above or beside speaker),
   - `الحقيقي بشكله` (Real screenshot/document/artifact framed cleanly),
   - `مشهد من الاتجاه` (Full thematic visual mechanism — capped at $\le \frac{1}{3}$ of moments so the piece breathes).

### 8.3 Reference Clip Dissection (`3ب — شرّح لي هالمقطع`)
When the user provides a reference video to study or emulate:
1. Run automated shot, cut, motion-curve, caption, SFX onset, and color-palette extraction (`dissect.json`).
2. Generate 6-frame contact sheets (`-2, -1, 0, +1, +2, +5` frames) around every cut and graphic entry.
3. Produce `analysis.json` grading each technique's fit for the current script (`fit: "yes" | "maybe" | "no"`) so only techniques that serve the content are adopted.
