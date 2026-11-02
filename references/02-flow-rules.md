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

## 4. Dialogue, Lip-Sync, Dialect Phonetics & Anti-Uncanny-Valley Law
- **Generative Lip-Sync**: Short phrases (`<= 8 words` and `<= 2.5 words/s`), natural pauses (`..`), one speaker at a time, face to camera, mouth unobstructed. Provide an English gloss (`dialogue_gloss_en`) for QC. Keep dialect consistent (`Gulf / Bahraini / Saudi / Kuwaiti / Emirati / Iraqi / Egyptian / Levantine` vs. `MSA` as requested).
- **Explicit Voice & Native Accent Lock (Anti-Foreign/Indian Accent Rule)**:
  - Always include an explicit vocal timbre and native accent lock before the quoted Arabic line: `speaking in a warm, authentic native Bahraini Khaleeji male voice with natural Gulf Arab cadence (zero South-Asian/Indian or foreign accent): "..."`.
  - **Visual-Audio Conditioning Guardrail**: In joint audio-visual models (`Omni 1.1 Flash` / `Veo 3.1`), character wardrobe directly biases voice accent! Never omit the character's exact wardrobe descriptor in any block (e.g., omitting a suit or Gulf thobe can cause the model to generate a South-Asian tunic/kurta, which immediately shifts the voice to an Indian accent). Repeat the **full verbatim character + wardrobe + headwear/bareheaded descriptor** in every single block.
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
