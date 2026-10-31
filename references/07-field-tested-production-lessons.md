# Field-Tested Production Lessons & Engineering Guardrails (`خلاصة الخبرات العملية والتجارب الميدانية`)

This reference codifies the battle-tested engineering, linguistic, visual, and audio lessons discovered during real-world multi-agent production and 60fps rendering experiments. Every subagent (`A1..A12` & the 7-Agent Crew) and the Showrunner MUST enforce these rules.

---

## 1. Anti-Uncanny-Valley Avatar & Lip-Sync Doctrine (`حظر تحريك الشفاه البدائي للصور الثابتة`)

### What Failed in Experiments
- Cropping a rectangular mouth patch (`open / mid / closed` JPEG slices) onto a frozen static portrait and alpha-blending it to match voiceover amplitude produces a comical, unnatural "paper cutout" effect (`Uncanny Valley`).

### Mandatory Production Rule (`HARD_BAN`)
- **NEVER animate a static portrait by blending rectangular mouth patches (`static_jpeg_mouth_flap = HARD_FAIL`).**
- Choose one of two approved production paths for spoken Arabic videos:
  1. **True Generative Lip-Sync (`Google Flow Veo 3.1 / Omni 1.1 Flash` or `Kling Official Avatar`)**:
     - Keep spoken phrases `<= 8 words` (`<= 2.5 words/sec`) with natural breath pauses (`.. [0.3s pause]`).
     - One speaker at a time, frontal camera framing, mouth completely unobstructed.
     - Always include `dialogue_gloss_en` in `06_package.json` for cross-language QC.
  2. **True 60fps 3D WebGL + 2D Canvas Motion Film (`Three.js` + `UnrealBloomPass` + `HTML5 2D Canvas` / `Remotion` / `HyperFrames`)**:
     - Express every spoken sentence through choreographed 3D/2D visual scenes (`ctx.stage3D` PBR meshes & orbital rings, `ctx.slideWall` 3D 6×5 perspective card wall with match-cut zoom, `MOTION.stage` kinetic cards, live waveforms, and `ctx.text.drawKashida` Arabic tatweel).

---

## 2. Dual-Layer Arabic Broadcast Scripting & `Whisper ASR` Gate (`ثنائية النص المشكول والفحص الآلي للنطق`)

### What Failed in Experiments
1. Passing unvocalized or partially vocalized Arabic to neural TTS (`edge-tts`, `ElevenLabs`, `Chirp3-HD`) caused incorrect grammatical case endings (`أواخر الكلمات`).
2. Ending a paused phrase with standard `تاء مربوطة` (`ة`) caused TTS engines to pronounce a clipped `-tu / -ta` instead of a natural broadcast `-ah` pause (`وقف بالسكون`).
3. Superscript dagger alifs (`ٰ` `\u0670`, as in `هٰذَا`) caused phoneme skipping in several TTS engines.
4. Writing raw English tech jargon in Arabic letters (`البرومبت`, `تشاي`, `كابشن`, `موشن`, `المايسترو`) caused robotic mispronunciation.

### Mandatory Production Rule
1. **Dual-String Schema (`tts_text` vs. `display_text`)**:
   - **`tts_text` (For TTS Engine Only)**:
     - Must carry **full Arabic diacritics (`التشكيل الكامل لكل حرف`)** with `diacritic_ratio >= 0.75` (`Harakat count / base Arabic letter count`).
     - Write every pause-final or sentence-final `تاء مربوطة` (`ة`) as **`هْ` (`هاء ساكنة`)** (e.g., `وَاحِدَهْ`, `الْمُتَكَامِلَهْ`, `لَقْطَهْ`, `الثَّانِيَهْ`, `الْجَاهِزَهْ`).
     - Zero superscript dagger alifs (`\u0670`).
     - Replace English loanword jargon with pure eloquent Arabic (`الْأَوَامِرُ الْإِخْرَاجِيَّهْ`, `مِعْيَارُ الْجَوْدَهِ الْخُمَاسِيّ`, `النُّصُوصُ الْمُتَحَرِّكَهْ`, `التَّحْرِيكُ السِّينَمَائِيّ`) or phonetically vocalized proper names (`جِيمِينَايْ`, `كْلُودْ`, `فْلُو`).
   - **`display_text` (For On-Screen Kinetic Typography & `.srt` Subtitles)**:
     - Clean, orthographically standard Arabic (preserving standard `ة`) and properly cased English (`Google Flow`, `Veo 3.1`, `60fps`).
2. **Mandatory Pre-Render `Whisper ASR` Verification (`whisper.cpp`)**:
   - Before rendering video frames, transcribe `vo_full.wav` using `whisper-cli -m ggml-medium.bin -l ar`.
   - Require `0` decode fallbacks (`fallbacks = 0 p / 0 h`) and verify that every spoken line matches the intended Arabic words. If any word is mispronounced, adjust `tts_text` and regenerate that line immediately.

---

## 3. 60fps 3D WebGL + 2D Motion Engine Calibration (`ضبط محرك الـ 60fps ثلاثي وثنائي الأبعاد`)

### What Failed in Experiments & How We Solved It
1. **`UnrealBloomPass` White-Out on 3D Cards**:
   - *Symptom*: High bloom (`strength >= 0.85, threshold <= 0.50`) washed out 3D cards and glassmorphic panels into overexposed white blocks.
   - *Locked Calibration*: Use `UnrealBloomPass(resolution, strength=0.42, radius=0.45, threshold=0.78)`. Keep 3D meshes and wireframe accents glowing while preserving deep `#050811` contrast behind Arabic typography.
2. **9:16 RTL Header & Left Status-Pill Collision**:
   - *Symptom*: In `1080×1920` vertical scenes, right-aligned Arabic panel titles (`X = 950`) collided with left-aligned English/badge pills (`X = 130..310`) when the Arabic string exceeded `~32 characters` at `28px`.
   - *Locked Rule*: Keep panel header titles `<= 30 characters` at `24–26px`, and **always run `node render.js preview --safe`** to inspect all scene midpoints with the safe-zone overlay before rendering 3,000+ frames.
3. **Zero-Dependency Headless Chrome WebGL (`Node 24 CDP Shim`)**:
   - When running in sandboxed or offline environments without external npm packages, drive `chrome-headless-shell` via Node 24's built-in `WebSocket` (`--remote-allow-origins=*`, `--enable-webgl`, `--ignore-gpu-blocklist`, `--use-angle=swiftshader`) and pipe raw RGBA frames directly to `ffmpeg -f rawvideo -r 60`.

---

## 4. Pure-NumPy Broadcast Audio DSP (`ماستر صوتي إذاعي بدون تبعيات خارجية`)

### What Failed in Experiments & How We Solved It
- Standard `audio.py` scripts that import `scipy.signal` (`butter`, `sosfilt`, `fftconvolve`) and `scipy.ndimage` (`maximum_filter1d`) fail in environments where `scipy` is not installed.
- **Locked Solution**:
  - Use **100% pure `numpy.fft`** (`rfft` / `irfft`) for Butterworth-style frequency-domain highpass/lowpass/bandpass filtering (`fft_filter`) and stereo room-impulse convolution (`fft_convolve`).
  - Use vectorized 180ms speech-envelope sidechain ducking (`-9.5 dB` music reduction during voiceover with `40ms` lookahead) and block-max lookahead true-peak limiting (`<= -1.0 dBTP`, `-14.0 LUFS` integrated via `ffmpeg loudnorm`).
