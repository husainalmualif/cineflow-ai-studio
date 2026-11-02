# Field-Tested Production Lessons & Engineering Guardrails (`خلاصة الخبرات العملية والتجارب الميدانية`)

This reference codifies the battle-tested engineering, linguistic, visual, and audio lessons discovered during real-world multi-agent production and 60fps rendering experiments. Every subagent (`A1..A12`) and the Showrunner MUST enforce these rules.

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

---

## 5. Google Flow (`Veo 3.1 / Omni 1.1 Flash`) Dialect Phonetics, Voice Lock & Anti-Text-Hallucination Guardrails (`قواعد إتقان اللهجة البحرينية/الخليجية ومنع اللكنة الأجنبية والنصوص العشوائية`)

### What Failed in Field Experiments (`Bahraini Father Story Case Study`)
1. **The "South-Asian / Indian Accent" Bug (`Visual-Audio Conditioning Drift`)**:
   - *Symptom*: In Block 7, omitting the character's exact outfit (`dark charcoal tailored suit jacket over a white collared shirt`) caused `Omni 1.1 Flash` to dress the actor in a beige South-Asian Mandarin-collar tunic (Kurta). Because `Omni 1.1 Flash` generates video and audio jointly, the South-Asian wardrobe immediately biased the synthesized voice toward an Indian/South-Asian accent (`Retroflex R/D` and foreign intonation)!
   - *Symptom*: Writing `"بَاجِرْ"` with standard Arabic `ج` and `"تِقُوْلْ / دَقَايِقْ"` with `ق` caused the model to pronounce `ج` as a foreign/retroflex `j` instead of the authentic Bahraini hard `G` (`گ` as in *Good*: `بَاگِرْ / Baagir`) or Gulf `Ch` (`چ`: `بَاچِرْ / Baachir`).
2. **The "Mixed Dialect + Fusha Tanween" Bug (`MSA Case-Ending Trap`)**:
   - *Symptom*: Applying 100% MSA grammatical diacritics (`تنوين ضم/كسر` and word-final `ضمة/فتحة`) to colloquial Bahraini words—such as `"مَشْغُوْلٌ وَاجِدْ"`, `"لَيْلَةِ مَطَرٍ"`, `"أَقُوْلُ"`, `"كَانَ"`, `"وَالْبِيْزَاتُ"`—forced the TTS engine to switch mid-sentence into formal textbook Fusha (`mashghūlun wājid`)!
3. **The "Floating Random Arabic Text & Garbled Paper Note" Bug**:
   - *Symptom 1*: Ending the prompt with `"No text, no watermark"` caused `Omni 1.1 Flash` to treat `"text"` as a positive attention token, pulling Arabic letters from the spoken dialogue (`"سامحني هالحزة..."`) and rendering floating white gibberish (`"س شحني الر القني ال خريه اقارم .."`) across the ceiling in Block 3!
   - *Symptom 2*: Prompting for a `"folded handwritten paper note"` (`ورقة صغيرة`) on the table produced creepy, deformed pseudo-Arabic squiggles in Blocks 4, 5, and 8.
4. **Narrator vs. Character Direct-Speech Confusion**:
   - *Symptom*: In Block 3B, the prompt showed the 68-year-old father moving his lips while the dialogue string included the narrator's reporting clause `"كَانَ يِبْتِسِمْ وَيِقُوْلُ لِيْ مَعْذُوْرْ..."`, making the father narrate about himself in the 3rd person!

### Mandatory Production Rules (`LOCKED`)
1. **Dialect Sukun Law (`قانون التسكين اللهجي المطلق ومنع التنوين`)**:
   - **ZERO Tanween (`ـٌ / ـٍ / ـً`) and ZERO word-final `ضمة / كسرة / فتحة إعرابية` in any Gulf/Bahraini/colloquial script.**
   - **Lock every word-final letter with `سُكُون (ْ)`** (`مَشْغُولْ وَاجِدْ، لَيْلَةْ مَطَرْ، أَگُولْ، يِگُولْ، چَانْ، مَضْمُونْ، البِيْزَاتْ`).
   - **Explicit Phonetic Letters for Bahraini/Gulf**:
     - Use **`گ` (`U+06AF`)** + inline pronunciation tag for hard `G` (as in *Good* / Egyptian Geem): `بَاگِرْ [pronounced Baa-gir with hard G as in Good]`, `تِگُولْ`, `يِگُولْ`, `دَگَايِگْ`, `عُگُبْ`, `گَبِلْ`, `اِگْعِدْ`, `يْوَفِّگَكْ`.
     - Use **`چ` (`U+0686`)** for Gulf `Ch` (as in *Chair*): `الچَايْ`, `چَانْ` (and `بَاچِرْ` when the `Ch` variant is desired).
2. **Verbatim Wardrobe Lock + Explicit Native Voice Declaration**:
   - Repeat the character's **complete verbatim wardrobe and headwear/bareheaded descriptor** in every single block (`wearing a dark charcoal tailored suit jacket over a white collared shirt without tie, bareheaded with short dark hair`) so the model never generates a South-Asian tunic or random ghutra.
   - Precede every spoken line with: `speaking in a warm, deep, 100% native Gulf Bahraini Arab male voice with authentic Khaleeji prosody (zero South-Asian, Indian, or foreign accent): "..."`.
3. **Anti-Hallucination Text, Still-Life Lens-HUD & Prop Guardrail**:
   - **NEVER include the words `text`, `subtitles`, `captions`, `letters`, or `watermark` (even with `no`) inside a Flow video prompt.** Use positive optical phrasing instead: `Clean unblemished cinema frame, pure optical lens capture, clear background.`
   - **NEVER include numeric camera lens specs (e.g., `85mm f/1.8 Anamorphic`) inside still-life / object-only shots (where no human subject appears)** — `Omni 1.1 Flash` can burn `"85mm f/1.8 Anamorphic"` as a lens-test HUD caption at the bottom of the frame (discovered and resolved in Block 8 V2). Use natural descriptive framing (`close-up hero table composition, shallow depth of field`) instead.
   - **NEVER prompt for handwritten notes, letters, or readable Arabic signs inside generative video** — and ensure reference ingredient images (`PROD_01`) have zero paper notes in the frame. Replace written notes with non-text physical heirlooms (`silver reading glasses, amber prayer beads, vintage wristwatch`) or a phone voice note.
   - **Single-Line Prompt Law for `flow_generate`**: Flatten multi-line prompts by replacing newline characters (`\n`) with spaces before calling `flow_generate` so the Google Flow Slate.js editor never rejects the paste (`typeText: editor rejected text via all safe strategies`).
4. **Mandatory Post-Generation 10-Frame Contact Sheet + Audio Dialect Audit**:
   - After generating any video clip in Google Flow, extract a **10-frame contact sheet (`0.5s .. 9.5s`)** AND inspect the **audio track** directly (`read_file` on `.mp4` + `whisper.cpp`) before merging. Any clip with floating text, wardrobe drift, foreign/Indian accent, or Fusha Tanween MUST be re-rolled with corrected phonetic spelling immediately.
