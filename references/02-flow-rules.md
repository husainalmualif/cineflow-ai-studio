# Google Flow Engineering Rules (`قواعد الهندسة والتوليد في Google Flow`)

Verify every number below in **Phase 1 (`01_research.md`)** because platform limits evolve. Store confirmed values in `06_package.json > project.verified_capabilities`.

## 1. Duration & Block Chunking (`Gemini Omni 1.2 Flash` & `Veo 3.1`)
- **Native unit (`Gemini Omni 1.2 Flash` / `macaron_cookie`)**: **`3s` to `15s` in `1-second` increments** (`3..15s` slider on `flow.google.com` for `Text-to-Video`, `Image-to-Video`, and `Ingredients`; `3..10s` for `Frames` First-to-Last Interpolation and `Extend`; `4 / 6 / 8 s` on `Veo 3.1 Lite / Fast / Quality`).
- **Longer sequences**: use native `15s` multi-beat generations or chain `Extend` in `3–10 s` steps up to the verified cumulative cap (`~40 s`). Plan each extension from the last seconds of the previous clip (`ffmpeg -sseof -0.04` `Scene Handshake`) + a continuity note.
- **Beyond cap**: start a new sequence linked by the **Identity Bible** (`03_identity_bible.md`) + short `3s` motion reference clip or first/last frame (`Frames` mode).
- **Shot density**: Up to `4` shots in a `15s` macro/product explainer or `2–3` shots per standard block.

## 2. Generation Modes & Multi-Modal Reference Adherence
- **Text-to-Video**: initial exploration at `360p` (`1 credit/s` for `3..10s`) or `720p` (`$0.07/s`, `30%` cheaper than Omni 1.1).
- **Frames-to-Video / First-Last Frame (`3..10s`)**: exact exterior-to-interior continuous camera pushes, sequential `5-layer` studio poster builds, and `Scene Handshake` continuity.
- **Ingredients / Multi-Modal Reference Conditioning (`3..15s`)**: combine up to `~7` references — **front-and-back garment/product photos + architectural photos + `3s` motion clips + `1s` voice cues** (generated at `0 credits` in Stage 1 via `Nano Banana Pro` / `Labs`) to lock faces, fabric drape, back details, packaging typography, and brand colors across `360°` turns and match cuts.
- **Multi-Turn Conversational Edit & Motion Transfer (`0 credits`)**: refine `15s` clips turn-by-turn (swap backgrounds, props, lighting/weather, or aspect ratio `16:9 <-> 9:16`, or transfer Turn 1 fluid motion onto a new subject in Turn 2) without re-generating from scratch.
- **Extend (`3..10s`)**: seamless temporal continuation from a previous block (`extend_from_block`).

## 3. Prompt Anatomy (Fixed Order, `<= 120 words` per block)
`[Format & style] + [Subject + ID] + [Action beat-by-beat with timestamps] + [Environment/time] + [Camera: lens, framing, movement] + [Lighting & grade] + [Audio: ambience, SFX, music, dialogue in quotes] + [Negatives]`

## 4. Dialogue, Multi-Speaker Conditioning, Dialect Phonetics & Anti-Uncanny-Valley Law
- **Native Multi-Speaker Conditioning (`Gemini Omni 1.2 Flash` — Single-Speaker Lock Purged)**:
  - `Gemini Omni 1.2 Flash` eliminates visual drift/gender morphing from first to last frame and natively routes distinct **`1-second` voice references** to **`4+` characters** inside a single `15-second` clip with expressive lip-sync and natural timing.
  - Keep individual spoken phrases concise (`<= 8 words` and `<= 2.5 words/s`), with natural pauses (`..`) and explicit timestamped speaker turns (`- At 01s, Yousef speaks... - At 07s, Noura replies...`).
- **Explicit Voice & Native Accent Lock (`يتحدث باللهجة البحرينية:`)**:
  - Always place **`يتحدث باللهجة البحرينية:`** directly before the quoted Arabic dialogue (`speaking in a warm, authentic native Bahraini Khaleeji voice (zero South-Asian/Indian or foreign accent)، يتحدث باللهجة البحرينية: "..."`).
  - **Visual-Audio Conditioning Guardrail**: In joint audio-visual models (`Gemini Omni 1.2 Flash` / `Veo 3.1`), character wardrobe directly biases voice accent! Repeat the **full verbatim character + wardrobe + headwear/bareheaded descriptor** in every single block.
- **Dialect Sukun Law vs. MSA Case-Ending Trap (`قانون التسكين اللهجي ومنع التنوين الفصيح`)**:
  - **NEVER put MSA grammatical case endings (`ضمة ـُ / كسرة ـِ`) or Tanween (`ـٌ / ـٍ / ـً`) on colloquial/Gulf/Bahraini words** (e.g., never write `مَشْغُوْلٌ وَاجِدْ`, `لَيْلَةِ مَطَرٍ`, `أَقُوْلُ`, `كَانَ`). Seeing Tanween or word-final damma causes `Veo 3.1 / Omni 1.1 Flash` to switch mid-sentence into formal textbook Fusha!
  - **Rule for Colloquial/Gulf Dialects**: Place **`سُكُون (ْ)` on the final letter of every word** (`أَگُولْ، يِگُولْ، مَشْغُولْ وَاجِدْ، لَيْلَةْ مَطَرْ، چَانْ، مَضْمُونْ`), convert pause-final `تاء مربوطة` (`ة`) to `هْ` (`مُكَالَمَهْ، هَالْحَزَّهْ، الطَّاوْلَهْ`), and write dialectal phonemes explicitly so the TTS never guesses:
    - Hard `G` (`الجيم القاهرية / القاف الخليجية` as in *Good*): write with **`گ` (`U+06AF`)** + inline phonetic hint when needed (e.g., `بَاگِرْ [pronounced Baa-gir with hard G as in Good]`, `تِگُولْ`, `دَگَايِگْ`, `عُگُبْ`, `گَبِلْ`, `اِگْعِدْ`, `يْوَفِّگَكْ`).
    - Gulf `Ch` (`الكشكشة / الچيم` as in *Chair*): write with **`چ` (`U+0686`)** (e.g., `الچَايْ`, `چَانْ`, or `بَاچِرْ` when `Ch` variant is desired).
- **Narrator vs. Character Direct-Speech Separation**:
  - Never put 3rd-person narrator reporting verbs (`"كان يبتسم ويقول لي..."`, `"يقول لي يا ولدي..."`) inside a secondary character's on-screen lip-sync dialogue! If the father is on screen moving his lips, his quoted dialogue must contain **only his 1st-person direct words** (`"مَعْذُوْرْ يَا وَلْدِيْ .. اللَّهْ يْوَفِّگَكْ يَا نَظَرْ عَيْنِيْ"`).
- **Hard Ban on Static JPEG Mouth-Flapping**: Never crop rectangular mouth patches (`open/mid/closed`) onto a static image. If not using generative lip-sync or real presenter footage, use the **60fps 3D WebGL (`Three.js`) + 2D Canvas Motion Stage**.
- **Broadcast TTS (`tts_text` vs. `display_text`)**: When synthesizing voiceover (`edge-tts`), feed vocalized `tts_text` (`diacritic_ratio >= 0.75`, pause-final `تاء مربوطة` written as `هْ`, zero `\u0670` dagger alifs) and verify with `whisper.cpp` (`ggml-medium.bin`).

## 5. Text in Frame & Anti-Hallucination Rules
- **Hard Ban on Handwritten Paper Notes / Letters in Video Prompts**: Never prompt for a `"handwritten note"`, `"folded letter with writing"`, or `"paper note"` (`ورقة صغيرة مكتوب فيها`) in `Veo 3.1 / Omni 1.1 Flash`. Video diffusion models cannot render legible Arabic handwriting and will hallucinate creepy, garbled pseudo-Arabic squiggles on the paper. Replace written notes with **non-text physical heirlooms** (`silver reading glasses, amber prayer beads, vintage wristwatch`) or a **spoken voice message on a phone**.
- **Positive-Token Trap (`NEVER write "no text" or "no subtitles" in Flow Prompts`)**:
  - Diffusion video models (`Omni 1.1 Flash` / `Veo 3.1`) treat words like `"text"`, `"subtitles"`, `"captions"`, `"letters"`, and `"watermark"` at the end of a prompt—even when preceded by `"No"`—as positive attention tokens, causing the model to pull characters from the Arabic dialogue and hallucinate floating gibberish Arabic text at the top of the frame!
  - **Rule**: Never include the words `text`, `subtitles`, `captions`, `lettering`, or `watermark` anywhere in the Flow prompt string. Instead, describe a clean visual frame positively: `Clean unblemished cinema frame, pure optical lens capture, clear ceiling and background.`
- Render all Arabic titles and subtitles as crisp post-production overlays (`Cairo`, `Tajawal`, `IBM Plex Sans Arabic`, `Amiri`).

## 6. Safe Zones (`9:16` Vertical `1080×1920`)
- Keep key action in the central `80%`; reserve bottom `20%` (`Y: 1500..1920`) and top `8%` (`Y: 0..160`) for platform UI, subtitles, and CTA/outro.
- In 60fps 3D/2D motion panels, keep RTL panel header titles `<= 30 chars` (`24–26px`) so they never collide with left-side status pills (`X = 130..310`), and verify with `node render.js preview --safe`.

## 7. Identity Lock
- Define IDs `[CHAR_01]`, `[PROD_01]`, `[ENV_01]` with fixed descriptors (face geometry, hair, outfit, hex colors, logo position, materials).
- Paste **identical descriptor strings** in every block and attach the same reference images.

## 8. Default Negatives
`no extra fingers, no distorted or random text, no logo morphing, no watermark, no burned-in subtitles, no extra characters, no face drift, no CGI plastic skin, no AI sheen, no static-photo mouth cutout`

## 9. Iteration Rule
- If a clip is `~80%` right: re-roll with the same references and change **ONE variable** only. Record winning settings in `08_flow_runlog.md`.
