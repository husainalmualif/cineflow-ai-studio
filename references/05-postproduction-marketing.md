# Post-Production & Marketing Expansion (`ما بعد الإنتاج، الماستر الصوتي، والتوسع التسويقي`)

## 1. Post-Production & Mastering (`A12`)
- **Edit Decision List (`09_post_plan.md`)**: frame-accurate timecodes; cut on beats/action; `J-cuts` and `L-cuts` (`120ms` pre-roll / `150ms` post-roll breath padding) for dialogue.
- **Subtitles (`.srt` & Kinetic Captions)**:
  - Arabic RTL, `1–2 lines`, `<= 32 chars` per line (`<= 6 words` per overlay pill), high contrast, strictly inside the safe zone (`Y: 1380..1490` in `9:16`).
  - Always render from clean orthographic `display_text` (never raw `tts_text`).
  - Generate `.srt` automatically via `python scripts/make_srt.py studio/<project>/06_package.json studio/<project>/out.srt`.
- **Audio Mastering (`audio.py` / `FFmpeg`)**:
  - Normalize to **`-14.0 LUFS` integrated** (`True Peak <= -1.0 dBTP`) using pure `numpy.fft` DSP (`fft_filter`, `fft_convolve`, `180ms` speech-envelope sidechain ducking `-9.5 dB`, vectorized lookahead limiter).
- **Exports & Cutdowns**:
  - `9:16` (`1080×1920`), `16:9` (`1920×1080` / `4K`), `1:1` (`1080×1080`), H.264 (`CRF 18` / `10–16 Mbps`, `60fps`).
  - Archive a clean master without subtitles + `6 / 10 / 15 / 30 s` social cutdowns.

## 2. Marketing Expansion (`A10`), On Request (`10_marketing.md`)
- **Posters / Ad Layouts**: headline, subhead, hero visual prompt (`[CHAR_01]` & `[PROD_01]`), CTA badge, `35%` clean negative space, RTL layout.
- **Instagram & LinkedIn Carousels**: `5–8 slides`, one clear idea per slide, flawless Arabic spelling.
- **Social Publishing Pack & Series Planner**: platform-distinct captions, hashtags, Arabic comment-keyword variants (`أ/إ/ا، ي/ى، ة/ه`), A/B plan (`2 hooks × 2 thumbnails`), and analytics learning loop.
