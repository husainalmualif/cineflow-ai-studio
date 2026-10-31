# Auditor Rubric, Compliance & Re-Roll Protocol (`معايير التدقيق والجودة وبروتوكول إصلاح الأخطاء`)

## 1. 13-Item Auditor Rubric (`A8`)
Score **`0–2` each** (`2 = Pass`, `1 = Minor Warning`, `0 = Fail`).
**Passing Threshold**: Total **`>= 22 / 26`** AND **no `0` in critical items `1–6`**.

1. **Identity consistency** (`[CHAR_01]`, `[PROD_01]`, `[ENV_01]` descriptors & reference plates locked)
2. **Duration limits respected** (`per_clip_s_options` verified, `<= 3 shots/block`, `Extend` properly linked)
3. **Arabic text, dialogue & broadcast phonetics correct** (100% dialect-consistent; `tts_text` has `>= 75%` Tashkeel + pause `هْ` + zero `\u0670` + `whisper.cpp` verified; `display_text` typo-free)
4. **Lip-sync & Anti-Uncanny-Valley compliance** (`<= 8 words/phrase` with `dialogue_gloss_en` for generative lip-sync, OR 60fps 3D/2D motion stage — **zero static-JPEG mouth-patch flapping**)
5. **Safe zones & Outro compliance** (`9:16` central `80%`, bottom `20%` & top `8%` clear, `--safe` preview verified with zero header-pill overlap)
6. **Safety, legal & cultural pass (`A11`)** (no unauthorized likeness/voice/trademarks)
7. **Hook strength (first `2 s`)** (visual shock, 3D slideWall zoom, or contrarian hook within `0–2s`)
8. **Story logic & block continuity** (`Scene Handshake` `-sseof -0.04` or match-cut transition between blocks)
9. **Camera & lighting specificity** (explicit lens, framing, single strong camera move, motivated lighting, `UnrealBloomPass` `{0.42, 0.45, 0.78}`)
10. **Audio map complete, no conflicts** (`-14.0 LUFS`, `<= -1.0 dBTP`, dialogue > music > SFX, sidechain ducking active)
11. **Prompt concision (`<= 120 words/block`)** (data-dense 8-layer anatomy, zero conversational filler)
12. **Platform specs match** (aspect ratio, resolution, FPS, runtime, cutdowns)
13. **Credit estimate & re-roll risk stated** (`estimate_cost.py` output included before `GATE 2`)

Output **`07_audit.md`**: full 13-row score table + exact constructive fixes (`"replace X with Y in block N"`).

## 2. Error & Re-Roll Protocol (Max `2 Re-Rolls` per Block, Then Redesign the Shot)
| Symptom | Root Cause & Exact Fix |
|---|---|
| **Face / outfit drift** | Attach more reference plates (`Ingredients`), repeat identical descriptor string verbatim, shorten block to `4–6s`, or use previous block's last frame (`-sseof -0.04`) as `<FIRST_FRAME>`. |
| **Distorted hands / objects** | Simplify physical action, reframe to `MS / CU`, remove complex finger/hand manipulation. |
| **Garbled in-frame Arabic text** | Remove in-frame text from generator prompt (`--no text`); render clean Arabic in post-production (`display_text` + `drawKashida`). |
| **Lip-sync off / uncanny mouth** | Shorten phrase to `<= 5–8 words` with `.. [0.3s pause]`, switch to frontal unobstructed framing, or replace static-photo avatar with 60fps 3D WebGL + 2D Motion Stage. |
| **TTS mispronunciation (`Whisper` fail)** | Add 100% Tashkeel (`>= 75%` ratio) in `tts_text`, replace pause-final `ة` with `هْ`, remove `\u0670`, replace English transliterations with pure Arabic, and re-run `voice.py`. |
| **3D card white-out / header collision** | Lower `UnrealBloomPass` to `{ strength: 0.42, radius: 0.45, threshold: 0.78 }` and shorten RTL panel header title to `<= 30 chars` (`24–26px`); verify with `render.js preview --safe`. |
