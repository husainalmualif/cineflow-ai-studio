# Post-Production & Marketing Expansion (`ما بعد الإنتاج، الماستر الصوتي، والتوسع التسويقي`)

## 1. Post-Production & Mastering (`A12`)
- **Edit Decision List (`09_post_plan.md`)**: frame-accurate timecodes; cut on beats/action; `J-cuts` and `L-cuts` (`120ms` pre-roll / `150ms` post-roll breath padding) for dialogue.
- **Subtitles (`.srt` & Kinetic Captions)**:
  - Arabic RTL, `1–2 lines`, `<= 32 chars` per line (`<= 6 words` per overlay pill), high contrast, strictly inside the safe zone (`Y: 1380..1490` in `9:16`).
  - Always render from clean orthographic `display_text` (never raw `tts_text`).
  - Generate `.srt` automatically via:
    `python scripts/make_srt.py studio/<project>/06_package.json studio/<project>/out.srt`
- **Audio Mastering (`audio.py` / `FFmpeg`)**:
  - Normalize to **`-14.0 LUFS` integrated** (`True Peak <= -1.0 dBTP`).
  - Duck background music under voiceover (`-9.5 dB` with `180ms` speech-envelope smoothing and `40ms` lookahead).
  - Add procedural or stem foley (`<= 15 events/min`, peak `< -18 dBFS`) and smooth fade-in/fade-out at endpoints.
  - Uses pure `numpy.fft` DSP (`fft_filter`, `fft_convolve`, vectorized lookahead limiter) so it runs in any Python environment without `scipy`.
- **Color & Visual Polish**:
  - Lock one unified LUT grade across all blocks; fix exposure jumps between blocks.
  - For 60fps 3D WebGL (`Three.js`) + 2D Canvas renders, run `node render.js preview --safe` first to verify zero safe-zone violations and balanced bloom (`{0.42, 0.45, 0.78}`).
- **Exports**:
  - `9:16` (`1080×1920`), `16:9` (`1920×1080` / `4K`), `1:1` (`1080×1080`), H.264 (`CRF 18` / `10–16 Mbps`, `yuv420p`, `60fps` for motion films or `24/30fps` for cinema).
  - Always archive a **clean master without burned-in subtitles** alongside the subtitled master.
- **Cutdowns**: `6 s / 10 s / 15 s / 30 s` social cutdowns derived from the master timeline.
- **Thumbnails & First-Frame Cover**:
  - `3 options`, one hero face/product, `<= 3 words`, high contrast, centered inside the `1080×1080` safe square (`Y: 420..1500`) so it crops cleanly across `9:16`, `4:5`, and `1:1` grids.

---

## 2. Marketing Expansion (`A10`), On Request (`10_marketing.md`)
- **Posters / Ad Layouts (`poster_prompt`)**:
  - Headline, subhead, hero visual prompt (locking `[CHAR_01]` & `[PROD_01]`), CTA badge, `35%` clean negative space, safe margins, RTL typography hierarchy (`Cairo` / `Amiri`).
- **Instagram & LinkedIn Carousels (`carousel_ar`)**:
  - Written in flawless Arabic MSA (`الفصحى`) or native Gulf/regional dialect (`العامية الخليجية/البحرينية/السعودية/العراقية/الشامية/المصرية`) as requested.
  - `Slide 1`: Hook (`<= 15 words`) ➔ `Slides 2–6`: One clear idea per slide ➔ `Final Slide`: Save/Share CTA.
- **Social Publishing Pack**:
  - Platform-distinct captions, mixed Arabic/English hashtags, Arabic comment-keyword spelling variants (`أ/إ/ا، ي/ى، ة/ه`), optimal posting windows (verified via `A1`), and **A/B Test Plan (`2 hooks × 2 thumbnails`)**.
- **Series Planner (`/series`)**:
  - Multi-episode arc map, recurring visual/audio motifs, cliffhangers, and strict reuse of the existing **Identity Bible (`03_identity_bible.md`)** and **Style Bible (`04_style_bible.md`)**.
- **Analytics Learning Loop**:
  - When the user shares retention/CTR analytics from a published video, diagnose the drop-off timestamp and specify exact adjustments for the next episode's hook, pacing, or visual density.
