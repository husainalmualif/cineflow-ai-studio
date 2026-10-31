# Google Flow Engineering Rules (`قواعد الهندسة والتوليد في Google Flow`)

Verify every number below in **Phase 1 (`01_research.md`)** because platform limits evolve. Store confirmed values in `06_package.json > project.verified_capabilities`.

## 1. Duration & Block Chunking
- **Native unit**: up to `~10 s` per clip; use `4 / 6 / 8 s` for single-action shots (`Veo 3.1 Lite / Fast / Quality` and `Omni 1.1 Flash`).
- **Longer sequences**: chain `Extend` in `~10 s` steps up to the verified cumulative cap (was `~40 s`). Plan each extension from the last seconds of the previous clip (`ffmpeg -sseof -0.04` `Scene Handshake`) + a continuity note.
- **Beyond cap**: start a new sequence linked by the **Identity Bible** (`03_identity_bible.md`) + short reference clip or first/last frame (`Frames` mode).
- **Shot density**: Max `2–3 shots` per block. Never waste one block per micro-shot.

## 2. Generation Modes
- **Text-to-Video**: initial exploration.
- **Frames-to-Video / First-Last Frame**: exact transitions and `Scene Handshake` continuity.
- **Ingredients / Image-to-Video**: attach up to `~7 reference images` (`identity`, `product`, `environment` generated at `0 credits` in Stage 1 via `Nano Banana 2 Lite` / `Labs`). Prefer reference-driven modes for characters and products to minimize re-rolls.
- **Extend**: seamless temporal continuation from a previous block (`extend_from_block`).

## 3. Prompt Anatomy (Fixed Order, `<= 120 words` per block)
`[Format & style] + [Subject + ID] + [Action beat-by-beat with timestamps] + [Environment/time] + [Camera: lens, framing, movement] + [Lighting & grade] + [Audio: ambience, SFX, music, dialogue in quotes] + [Negatives]`

## 4. Dialogue, Lip-Sync & Anti-Uncanny-Valley Law
- **Generative Lip-Sync**: Short phrases (`<= 8 words` and `<= 2.5 words/s`), natural pauses (`.. [0.3s pause]`), one speaker at a time, face to camera, mouth unobstructed. Provide an English gloss (`dialogue_gloss_en`) for QC.
- **Hard Ban on Static JPEG Mouth-Flapping**: Never crop rectangular mouth patches (`open/mid/closed`) onto a static image. If not using generative lip-sync or real presenter footage, use the **60fps 3D WebGL (`Three.js`) + 2D Canvas Motion Stage**.
- **Broadcast TTS (`tts_text` vs. `display_text`)**: When synthesizing voiceover (`edge-tts`), feed 100% vocalized `tts_text` (`diacritic_ratio >= 0.75`, pause-final `تاء مربوطة` written as `هْ`, zero `\u0670` dagger alifs) and verify with `whisper.cpp` (`ggml-medium.bin`).

## 5. Text in Frame & Safe Zones (`9:16` Vertical `1080×1920`)
- Default: generate clean plates with empty text areas, and render Arabic text as crisp post-production overlays (`Cairo`, `Tajawal`, `IBM Plex Sans Arabic`, `Amiri`) with pixel-accurate `drawKashida`.
- Keep key action in the central `80%`; reserve bottom `20%` (`Y: 1500..1920`) and top `8%` (`Y: 0..160`) for platform UI, subtitles, and CTA/outro.
- In 60fps 3D/2D motion panels, keep RTL panel header titles `<= 30 chars` (`24–26px`) so they never collide with left-side status pills (`X = 130..310`), and verify with `node render.js preview --safe`.

## 6. Identity Lock & Default Negatives
- Define IDs `[CHAR_01]`, `[PROD_01]`, `[ENV_01]` with fixed descriptors; paste identical descriptor strings in every block.
- **Default Negatives**: `no extra fingers, no distorted or random text, no logo morphing, no watermark, no burned-in subtitles, no extra characters, no face drift, no CGI plastic skin, no AI sheen, no static-photo mouth cutout`
