# 08 — Model Registry, Tuned Empirical Defaults, Compliance & Analytics Loop

> **Last Verified:** `2026-11-03`  
> **Status:** `verify_live` (Always inspect live platform UI via `A0_Probe` before locking durations or spending credits; see also [`references/model-registry.md`](model-registry.md) and [`references/11-22-tool-video-ecosystem-and-nle-mastery.md`](11-22-tool-video-ecosystem-and-nle-mastery.md)).

---

## 1. Dated Model & Pricing Registry (`status: verify_live`)

Model identifiers, clip duration options (`allowed_clip_seconds`), and credit multipliers evolve rapidly. Treat the table below as the **baseline assumption as of `2026-11-03`** and override with live UI inspection when browser access is available.

| Platform / Engine | Current Model IDs (`2026-11-03`) | Allowed Clip Seconds (`allowed_clip_seconds`) | Extend Chain Cap (s) | Relative Cost Tier | Primary Strength |
|---|---|---|---|---|---|
| **Google Flow (Veo Cinema)** | `Veo 3.1 Lite` / `Fast` / `Quality` | `4, 6, 8` (`8` only on Quality) | `40` (`+8s` Lite on Flow, `+7s` on API) | `1.0x` (Standard) / `0.5x` (Lite/Ultra Fast) | Photorealistic cinema, native lip-sync, Ingredients `[ID]` lock |
| **Google Flow (Omni Flash)** | `Omni 1.1 Flash` (`gemini-omni-flash-preview`) | `4, 6, 8, 10` (`3..10` on Gemini API) | `40` | `0.25x–0.5x` (`4–15 credits`, `0-credit` `1080p` upscale) | Up to 7 references, 5 voices, natural-language video editing |
| **Google Labs (Image Lock)** | `Nano Banana Pro` / `Nano Banana 2 Lite` | Static `0s` | N/A | `0.0x` (`0 credits` Reference & `1K/2K/4K` Upscale) | Character turnarounds (`@Char`), environment plates (`@Env`) |
| **Seedance / Dreamina** | `Seedance 2.0` + `Seedream 3.0` | `4, 6, 8, 10` | `30` | `0.85x` | `@Image1`/`@Video1`/`@Audio1` multi-shot cuts & choreography |
| **Runway / Kling / Hailuo / Wan / Higgsfield** | `Gen-4`, `Kling 2.1/3.0`, `I2V-01-Director`, `Wan VACE`, `Higgsfield DoP` | `4, 5, 6, 8, 10` | `30–40` | `0.5x–1.0x` | Bracketed camera moves, `Elements`, `VACE` inpainting, `DoP` cinema rigs |
| **Flow Music** | `Flow Music Studio v2` | `15–180` | N/A | `0.0x–0.2x` | Instrumental stems with locked `BPM` and section structure |
| **Programmatic & NLE Studio** | `Remotion v4.0.539` + `Blender` + `C4D` + `AE` + `DaVinci Resolve` + `CapCut` | Frame-exact (`30/60fps`) | Unlimited | `0.0x` (Local CPU/GPU) | Deterministic Arabic typography, 3D WebGL, `-14 LUFS` Fairlight mastering |

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
