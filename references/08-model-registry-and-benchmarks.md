# 08 — Model Registry, Tuned Empirical Defaults, Compliance & Analytics Loop

> **Last Verified:** `2026-11-01`  
> **Status:** `verify_live` (Always inspect live platform UI via `A0_Probe` before locking durations or spending credits; see also [`references/model-registry.md`](model-registry.md)).

---

## 1. Dated Model & Pricing Registry (`status: verify_live`)

Model identifiers, clip duration options (`allowed_clip_seconds`), and credit multipliers evolve rapidly. Treat the table below as the **baseline assumption as of `2026-11-01`** and override with live UI inspection when browser access is available.

| Platform / Engine | Current Model IDs (`2026-11-01`) | Allowed Clip Seconds (`allowed_clip_seconds`) | Extend Chain Cap (s) | Relative Cost Tier | Primary Strength |
|---|---|---|---|---|---|
| **Google Flow (Cinema)** | `Veo 3.1` / `Veo 3.1 Fast` | `4, 6, 8, 10` | `40` | `1.0x` (Standard) / `0.25x` (Fast Draft) | Photorealistic cinema, native lip-sync, Ingredients `[ID]` lock |
| **Google Flow (Draft / Edit)** | `Gemini Omni Flash 1.1` | `4, 6, 8` | `24` | `0.25x` | Rapid turn-by-turn video editing & style transfer |
| **Google Labs (Image Lock)** | `Nano Banana Pro` / `Nano Banana 2 Lite` | Static `0s` | N/A | `0.0x` (Zero-Credit Reference Stage) | Character turnarounds (`[CHAR_01]`), environment plates (`[ENV_01]`) |
| **Seedance** | `Seedance 2.0` | `4, 6, 8, 10` | `30` | `0.85x` | Fluid choreography, rhythmic camera arcs |
| **Flow Music** | `Flow Music Studio v2` | `15–180` | N/A | `0.0x–0.2x` | Instrumental stems with locked `BPM` and section structure |
| **Programmatic Motion** | `Remotion` + `Three.js WebGL` + `HyperFrames` | Frame-exact (`30/60fps`) | Unlimited | `0.0x` (Local CPU/GPU) | Deterministic Arabic typography, 3D HUDs, beat-accurate cutting |

---

## 2. Tuned Empirical Defaults (`tier: tuned_default` — Overridable)

The values below are **empirically tuned studio defaults** (not immutable laws). Override any of them in `project` or `post_production_timeline` whenever the creative brief requires a different look or mix:

| Parameter | Default Value | Empirical Rationale | When to Override |
|---|---|---|---|
| `snap_tolerance_ms` | `40 ms` | Maximum imperceptible cut-to-beat offset at `30–60fps`. | Relax to `60 ms` for dialogue-driven J-cuts. |
| `sfx_density` (`CR2`) | `<= 1 SFX per 2 beats` (Montage) / `15/min` (Standard) | Prevents SFX clutter during high-BPM rhythmic cuts while keeping music bed clear. | Reduce for slow dramatic montages (`breathe` pattern). |
| `UnrealBloomPass` | `{strength: 0.42, radius: 0.45, threshold: 0.78}` | Prevents white-clipping on `#F8FAFC` Arabic text while keeping HUD edges glowing on dark `#050811` canvases. | Set `strength: 0.0` for flat editorial minimalism. |
| Integrated Loudness | `-14.0 LUFS` (`<= -1.0 dBTP`) | Matches YouTube, Reels, and TikTok normalization target without limiter pumping. | Use `-16.0 LUFS` for podcasts or `-23.0 LUFS` for broadcast TV. |
| Vocalized Base-Letter Ratio (`CR3`) | `0.75` (Standard floor) / `1.0` (AI TTS target) | Counts vocalized Arabic base letters (`[\u0621-\u063A\u0641-\u064A][\u064B-\u0652\u0651]+`) to prevent TTS homograph errors. | Lower only for human voice actors reading natural script. |

---

## 3. Arabic & Gulf Broadcast Vocalization Glossary

| Raw Word | Ambiguity Risk | Recommended `dialogue_tts_ar` Form | Notes |
|---|---|---|---|
| `قهوة مختصة` | Pronounced with Taa (`ت`) at pause | `قَهْوَهْ مُخْتَصَّهْ` | Rewrite pause-final `ة` as `هْ` inside `dialogue_tts_ar` |
| `حياكم الله` | Unvocalized Shadda on Ya | `حَيَّاكُمُ اللَّهْ` | Keep `الله` intact; never insert Kashida inside `الله` |
| `وش رايك` | Misread as `وَشَ` in MSA TTS | `وِشْ رَايِكْ` | Saudi/Gulf Kasra on Waw (`وِشْ`) |
| `شلونك` | Misread as `شَلَوْنَكَ` | `شْلُونِكْ` | Gulf/Iraqi Sukun on Sheen |
| `2026` / `100%` | Read in English mid-Arabic sentence | `أَلْفَيْنِ وَسِتَّهْ وَعِشْرِينْ` / `بِالْمِئَهْ` | Spell numbers & symbols as full Arabic words in `dialogue_tts_ar` |

---

## 4. Verifiable Marketing Claims & Platform Disclosure (`marketing_expansion`)

1. **Verifiable Claims Checklist:** Flag unverified medical/health claims, undocumented halal certifications, unsupported competitor comparisons, and sourceless statistics (`facts_ledger`).
2. **AI-Generated Content Disclosure:** Include platform-appropriate AI disclosure metadata/tags according to TikTok, Instagram/Meta, and YouTube policies when publishing synthetic scenes.

---

## 5. Post-Publish Analytics Feedback Loop

Record post-publish metrics (3-second hold rate, full-watch completion rate, and CTR) in `project_state.json` / `taste_profile.json` to feed the next production iteration:
- **Low 3s Hold (`< 65%`):** Switch Scene 1 hook to `visual_payoff` or `contrarian` with an immediate beat cut in the first `1.5s`.
- **Mid-Video Drop-off:** Switch `cut_cadence` pattern (e.g., `steady` -> `build_up`) so no single cadence repeats across consecutive sections (`MQ2`).
- **High Completion but Low CTR:** Simplify `outro.cta_ar` inside `cta_zone` (`Y 950..1280, X 120..900`).
