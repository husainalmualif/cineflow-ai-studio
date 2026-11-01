# 08 — Model Registry, Tuned Empirical Defaults, Compliance & Analytics Loop

> **Last Verified:** `2026-11-01`  
> **Verify On-Screen Before Generation:** `true` (Always run `A0_Probe` on the live UI before locking durations or credit budgets).

---

## 1. Dated Model & Pricing Registry (`verify_on_screen_before_use: true`)

Model identifiers, clip duration options, and credit multipliers change frequently across AI video platforms. Treat the table below as the **baseline registry as of `2026-11-01`** and always override with live UI inspection when browser access is available.

| Platform / Engine | Current Model IDs (`2026-11-01`) | Allowed Clip Durations (s) | Extend Chain Cap (s) | Relative Cost Tier | Primary Strength |
|---|---|---|---|---|---|
| **Google Flow (Cinema)** | `Veo 3.1` / `Veo 3.1 Fast` | `4, 6, 8, 10` | `40` | `1.0x` (Standard) / `0.25x` (Fast Draft) | Photorealistic cinema, native lip-sync, Ingredients `[ID]` lock |
| **Google Flow (Draft / Edit)** | `Gemini Omni Flash 1.1` | `4, 6, 8` | `24` | `0.25x` | Rapid turn-by-turn video editing & style transfer |
| **Google Labs (Image Lock)** | `Nano Banana Pro` / `Nano Banana 2 Lite` | Static `0s` | N/A | `0.0x` (Zero-Credit Reference Stage) | Character turnarounds (`[CHAR_01]`), environment plates (`[ENV_01]`) |
| **Seedance** | `Seedance 2.0` | `4, 6, 8, 10` | `30` | `0.85x` | Fluid dance, high-BPM choreography, rhythmic camera arcs |
| **Kling** | `Kling Omni` | `5, 10` (Map to `6, 10` in schema) | `30` | `0.80x` | Long facial performance & physics |
| **Flow Music / Suno** | `Flow Music Studio v2` | `15–180` | N/A | `0.0x–0.2x` | Instrumental stems (`120 BPM` oud/electronic/orchestral beds) |
| **Programmatic Motion** | `Remotion` + `Three.js WebGL` + `HyperFrames` | Frame-exact (`60fps`) | Unlimited | `0.0x` (Local CPU/GPU) | Deterministic Arabic typography, 3D HUDs, zero AI text distortion |

---

## 2. Tier-2 Tuned Empirical Defaults (Overridable)

The values below are **empirically tuned studio defaults** (not immutable physical laws). Override any of them in `project` or `post_production_timeline` whenever the creative brief requires a different look or mix:

| Parameter | Default Value | Empirical Rationale | When to Override |
|---|---|---|---|
| `UnrealBloomPass` | `{strength: 0.42, radius: 0.45, threshold: 0.78}` | Prevents white-clipping on `#F8FAFC` Arabic text while keeping gold/teal HUD edges glowing on dark `#050811` canvases. | Set `strength: 0.0` for flat editorial/corporate minimalism or `0.65` for neon cyberpunk. |
| Integrated Loudness | `-14.0 LUFS` (`<= -1.0 dBTP`) | Matches YouTube, Reels, and TikTok normalization target without limiter pumping. | Use `-16.0 LUFS` for Apple Podcasts or `-23.0 LUFS` (EBU R128) for broadcast TV deliverables. |
| Sidechain Ducking | `-9.5 dB` (`180ms` attack / `450ms` release) | Keeps Arabic consonants crisp over `120 BPM` percussion beds. | Reduce to `-5.0 dB` for music-driven sizzle reels without spoken narration. |
| Silence-Cut Threshold | `-32 dB` (`min_silence_ms: 280`, `pad_ms: 90`) | Removes dead air in talking-head reels while preserving natural Arabic breath pauses (`وقفات التنفس`). | Relax to `min_silence_ms: 500` for dramatic storytelling or poetry. |
| Vocalized Base-Letter Ratio | `>= 0.75` (`MIN_DIACRITIC_RATIO`) | Prevents Arabic TTS homograph errors (`عَلِمَ` vs `عِلْمٌ`) when counting vocalized Arabic base letters (`[\u0621-\u063A\u0641-\u064A][\u064B-\u0652\u0651]+`). | Lower to `0.50` only for human voice actors reading natural script. |

---

## 3. Arabic & Gulf Pronunciation Glossary + Sacred Text Rule (`A7`)

### 3.1 Sacred & Quranic Text Prohibition (Tier-1 Hard Safety Rule)
- **NEVER generate Quranic verses (`آيات قرآنية`), sacred Hadith, or religious recitations using synthetic AI TTS or AI lip-sync.**
- Synthetic TTS frequently distorts Tajweed rules (`أحكام التجويد`) and sacred vocalization, which is unacceptable.
- **Required Action:** If a project includes a Quranic verse or sacred recitation, display verified Uthmani script (`الرسم العثماني`) via deterministic Remotion/Canvas typography and use a **verified, licensed human recitation recording** (or keep the segment respectful silent/ambient).

### 3.2 Tricky Arabic & Gulf Broadcast Vocalization Glossary
| Raw Word | Ambiguity Risk | Mandatory `dialogue_tts_ar` Form | Notes |
|---|---|---|---|
| `قهوة مختصة` | Pronounced with Taa (`ت`) at pause | `قَهْوَهْ مُخْتَصَّهْ` | Rewrite pause-final `ة` as `هْ` inside `dialogue_tts_ar` |
| `حياكم الله` | Unvocalized Shadda on Ya | `حَيَّاكُمُ اللَّهْ` | Keep `الله` intact; never insert Kashida inside `الله` |
| `وش رايك` | Misread as `وَشَ` in MSA TTS | `وِشْ رَايِكْ` | Saudi/Gulf Kasra on Waw (`وِشْ`) |
| `شلونك` | Misread as `شَلَوْنَكَ` | `شْلُونِكْ` | Gulf/Iraqi Sukun on Sheen |
| `ما شاء الله` | Merged or clipped glottal stop | `مَا شَاءَ اللَّهْ` | Explicit Hamza vowel before `الله` |
| `2026` / `100%` | Read in English mid-Arabic sentence | `أَلْفَيْنِ وَسِتَّهْ وَعِشْرِينْ` / `بِالْمِئَهْ` | Always spell numbers & symbols as full Arabic words in `dialogue_tts_ar` |

---

## 4. Marketing Claims & Regulatory Compliance Checklist (`A8`)

Before compiling or rendering any **Commercial Promo**, **Testimonial Video**, or **Corporate Video**, verify these 4 compliance gates:

1. **Substantiated Claims Only:** Flag unverified medical, health, financial-return, or "100% guaranteed" claims. Frame benefits around verifiable product attributes stored in `facts_ledger`.
2. **Competitor Trademarks:** Never generate competitor logos or disparaging named comparisons inside visual prompts.
3. **Likeness & Voice Consent:** Never clone a real living person's face or voice without documented consent; use fictional synthesized `[CHAR_01]` identities from `Nano Banana Pro` by default.
4. **Commercial Licensing:** Ensure all background stems (`Flow Music`), fonts (`Cairo`, `Tajawal`, `Almarai`, `IBM Plex Sans Arabic`), and archival clips (`CLIP` montage) are cleared for commercial redistribution.

---

## 5. Post-Publish Analytics Feedback Loop (`A9`)

When the user shares post-publish metrics from TikTok, Instagram Reels, YouTube Shorts, or Meta Ads, update `studio/taste_profile.json` using these rules:

- **3-Second Hold Rate `< 65%`:** Switch default Scene 1 hook archetype from `authority` to `contrarian` or `visual_payoff`, and require a camera/layout cut within the first `1.8s`.
- **Average Watch Duration drops sharply at `t = X` seconds:** Inspect the block covering `t = X`. If `shot_count == 1` for `> 6s`, increase shot density (`2 shots` per `8s` block) or insert a `R_FULL` B-roll cutaway.
- **High Watch Time (`> 75%`) but Low CTR (`< 1.2%`):** Move the spoken value proposition `3 seconds` earlier before the outro and simplify `outro.cta_ar` to `<= 4` bold words.
