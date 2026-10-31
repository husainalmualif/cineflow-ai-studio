# Direction Parameters, Classification & Audio DSP (`التوجيه الإخراجي، التصنيف، والهندسة الصوتية`)

## 1. Direction Parameters (Lock per Shot)
1. **Emotion / Tone**: `angry`, `laughing`, `crying`, `serious`, `sly`, `reflective`, `mocking`, `proud`, `awe`, `tender`.
2. **Body Language (100% Physical Micro-Cues)**: `relaxed`, `tense`, `deceitful`, `confident`, `hesitant`, `friendly`; specify eye line, breathing cadence, and hand posture.
3. **Gear**: `large-format digital (ARRI/RED/Venice look)`, `anamorphic`, `vintage 35mm film stock (ISO 800 grain)`, `handheld mobile UGC`.
4. **Lens / Framing**: `18 / 24 / 35 / 50 / 85 / 135 mm` feel; `ECU`, `CU`, `MS`, `WS`; shallow or deep depth of field (`f/1.4` to `f/8`).
5. **Movement**: `Pan`, `Tilt`, `Dolly in/out`, `Truck`, `Crane`, `Orbit`, `Handheld`, `Gimbal`, `Whip-pan`, `FPV`, `Locked-off`, `Rack focus`. **One strong camera move per shot**.
6. **Lighting**: `key / fill / rim`, motivated sources, time of day, practicals, volumetrics, `chiaroscuro`.
7. **Grade**: `cinematic warm`, `teal-orange`, `bleach bypass`, `naturalistic Rec.709`, `moody dark`, `pastel kids`, `high-key commercial`. Never tint real human skin (`grade: false` on real faces).
8. **Pacing**: shot length vs. BPM; cut on action or beat (`[1.0, 0.82, 1.24, 0.94]` cadence).

## 2. Audio, Music & Broadcast DSP (`A6`)
- **Music Brief**: genre, BPM, key/mode, instruments, timestamped structure. Operate **Flow Music (`flowmusic.app`)** via browser if available, or synthesize multi-bus beat beds (`kick, clap, hat, bass, pad, arp, top`) via `audio.py`.
- **Voice Direction & Arabic Phonetics**: specify age, dialect, pace, emotion. Feed 100% vocalized `tts_text` (`>= 75%` diacritics, pause-final `تاء مربوطة` as `هْ`, zero `\u0670`) to TTS and verify with `whisper.cpp` (`ggml-medium.bin`).
- **Broadcast Mix Targets (Pure-NumPy DSP)**: `dialogue > music > SFX`; **`-14.0 LUFS` integrated** for social platforms; **true peak `<= -1.0 dBTP`**; `180ms` speech-envelope sidechain ducking (`-9.5 dB` music reduction during speech).

## 3. 2D/3D & 60fps Motion Engine (`A4`)
- Calibrate `UnrealBloomPass` to `{ strength: 0.42, radius: 0.45, threshold: 0.78 }` so dark panels never wash out into white blocks.
- Combine `ctx.stage3D` (3D PBR meshes, orbital rings, camera sweeps), `ctx.slideWall` (3D 6×5 perspective card wall with motion blur and match-cut landing), `MOTION.stage` (choreographed 2D cards), and `ctx.text.drawKashida` (pixel-sliced Arabic tatweel).
