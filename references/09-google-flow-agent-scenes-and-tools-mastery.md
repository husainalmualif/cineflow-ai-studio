# 09 — Google Flow Complete Ecosystem Mastery (`google-flow-director v3.0.0 — Pure Gemini Omni 1.2 Flash Native Edition`): Flow Agent JSON Init, 6 Core Pillars, 3 Purged Legacy Rules, Multi-Speaker Dialect Engine, Voices/Characters/Avatars, Scene Builder (`Add to Scene` / `Extend`), and Flow Tools (`Mondo Sónico` & `+ Create tool`)

This reference manual codifies the complete architecture and operational workflows of **Google Flow (`https://flow.google.com/`)** powered natively by **Gemini Omni 1.2 Flash** (`macaron_cookie`, `gemini-omni-1.2-flash`, released `2026-11-05`) and **Nano Banana Pro** across its browser workspace, **Flow Agent**, **Asset Picker (`Voices / Characters / Avatars`)**, **Scene Builder (`Scenes` / `Scenebuilder`)**, **Flow Tools (`Explore tools / Create tool`)**, and our **11-mode `flow-connector` MCP bridge**.

---

## 0. Pure Gemini Omni 1.2 Flash Native Edition (`google-flow-director v3.0.0`)

### 0.1 Official Release Specifications (`2026-11-05` — Google DeepMind)
- **Source**: `https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/`
- **Model Identifiers**:
  - **Google Flow UI (`flow.google.com`)**: `Omni 1.2 Flash` (internal RPC prefix: `macaron_cookie`)
  - **Gemini API & Google AI Studio**: `gemini-omni-1.2-flash`
  - **Vertex AI Model Garden**: `omni-1-2-flash`
  - **Image & Reference Engine**: `Nano Banana Pro`
- **Pricing & Live Flow Credit Schedule (`status: verify_live`)**:
  - **API Price**: **`$0.07/second`** for `720p` video (**30% reduction** compared to Gemini Omni 1.1).
  - **Flow `360p` Draft (`macaron_cookie_*_360p`)**: **`1 credit/s`** for `3s..10s` (`3s=3c`, `8s=8c`, `10s=10c`) and **`+2 credits/s`** for `11s..15s` (`15s=20c`).
  - **Flow `720p` (`macaron_cookie_*`)**: **`3 credits/s`** for `3s..10s` (`10s=30c`) and **`+6 credits/s`** for `11s..15s` (`15s=60c`).
  - **Multi-Turn Conversational Edit (`macaron_cookie_edit` & `macaron_cookie_edit_360p`)**: **`0 credits`** (free turn-by-turn edits!).
  - **Upscaling**: `360p -> 720p` (`omni_upsampler_360p`) = **`0 credits`**; `1080p` (`veo_3_1_upsampler_1080p`) = **`0 credits`**; `4K` (`veo_3_1_upsampler_4k`) = **`50 credits`**.
- **Native Duration Slider (`role="slider" aria-label="Length"`)**:
  - Selecting `Omni 1.2 Flash` in Flow replaces the legacy `4s/6s/8s/10s` buttons with a continuous **`3 Sec` to `15 Sec` slider in `1-second` increments** (`aria-valuemin="0" aria-valuemax="12"`) for `t2v`, `i2v`, and `r2v` (`Ingredients`), and **`3 Sec` to `10 Sec` in `1-second` increments** for `i2v_fl` (`Frames` First-to-Last Keyframe Interpolation) and `extend` (`Video Extension`).

### 0.2 The 3 Purged Legacy Rules (`purged_legacy_rules`)
| Purged Legacy Rule | Why It Is Obsolete & Purged in Gemini Omni 1.2 Flash |
| :--- | :--- |
| **1. `Single-Speaker Shot Lock` (`قانون منع تحول الولد إلى بنت وفصل المتحدثين`)** | **Purged:** Gemini Omni 1.2 Flash eliminates visual drift/morphing from first to last frame and introduces native **Multi-Speaker Conditioning**, routing distinct `1-second` voice references to multiple characters (e.g., `4+` characters in one scene) with expressive lip-sync and natural timing across a single `15-second` clip. |
| **2. `تجنب إرفاق مراجع متعددة الزوايا (الأمام والخلف) في لقطة واحدة`** | **Purged:** Gemini Omni 1.2 Flash natively combines model photos with **front-and-back shots** of multiple outfits/products, **`3-second` motion clips**, and **`1-second` audio cues**, keeping faces, garment drape, back details, and packaging typography locked across `360-degree` turns and match cuts. |
| **3. `إعادة توليد اللقطة بالكامل عند الرغبة في تغيير الخلفية أو الإضاءة أو المقاس`** | **Purged:** Replaced by **`0-credit` Multi-Turn Conversational Editing & Motion Transfer** across full `15-second` clips, allowing turn-by-turn background swaps (`pavilion tent -> oak forest -> stable -> market fair -> stone castle`), lighting/weather shifts, product/prop replacements, aspect ratio switches (`16:9 <-> 9:16`), and Turn-1-to-Turn-2 motion transfer while preserving character performance and armor/garment reflections. |

### 0.3 The 6 Core Pillars of `google-flow-director v3.0.0` (`core_pillars_v3`)
1. **Pillar 1 — بروتوكول التوفير الذكي للنقاط (`360p/720p Draft -> Conversational Edit -> 1080p/4K Upscale`)**:
   - Start every generation at `360p` or `720p` in `Gemini Omni 1.2 Flash`. Use `0-credit` multi-turn conversational editing to refine backgrounds, lighting, weather, props, or aspect ratio without re-generating. Upscale only the final approved take to `1080p` (`0 credits`) or `4K` (`50 credits`).
2. **Pillar 2 — التوليد الأصلي المرِن (`3 إلى 15 ثانية`) وتمديد المشاهد الطويلة (`Video Extension`)**:
   - Specify exact duration in `1-second` increments from `3s` to `15s` for complete multi-beat scenes, `4-shot` `15s` macro science/product explainers with accurately spelled motion-tracked callouts from a single style frame, or full vertical `15s` social ad spots. Use **First-to-Last Keyframe Interpolation** for continuous exterior-to-interior pushes or `5-layer` sequential poster builds, and **Video Extension** to elongate clips into long continuous sequences with locked consistency.
3. **Pillar 3 — الالتزام الفائق بالمراجع المتعددة (`صور أمامية/خلفية + مقاطع حركة 3 ثوانٍ + عينات صوتية`)**:
   - Combine character sheets, front-and-back product/garment photos, `3-second` motion reference clips, and `1-second` voice cues. Rely on `Omni 1.2 Flash` to lock faces, fabric drape, back details, coiled/3D packaging typography, and brand colors across `360-degree` spins and match cuts.
4. **Pillar 4 — الحوار الجماعي الأصلي (`Multi-Speaker Conditioning`) وقفل اللهجة البحرينية**:
   - Direct multi-character conversations natively inside a single `15-second` clip using character, mouth, and `1-second` voice references. Always pass verbatim Bahraini Arabic dialogue inside quotes with an explicit Bahraini dialect instruction (`يتحدث باللهجة البحرينية: "..."`) so each speaker delivers authentic local inflection and crisp lip-sync.
5. **Pillar 5 — حركات الكاميرا السينمائية المتصلة بدون تقطيع (`Unbroken Camera Control`)**:
   - Direct unbroken **FPV drone flythroughs** (e.g., sweeping across a piazza, through bronze doors, and up through a coffered dome to the oculus with zero jump cuts, guided by two architectural reference photos), **continuous crash zoom-outs** (from a tight shoreline close-up to an aerial island vista in one continuous shot), and smooth **`360-degree` orbits** and match cuts.
6. **Pillar 6 — تنظيم الخط الزمني في `Scenebuilder`**:
   - Keep static reference plates and unapproved `360p` drafts out of `Scenebuilder`. Assemble only the final, conversationally refined, `1080p/4K` upscaled clips in chronological order (`Shot 1 -> Shot N`) and verify full playback from `00:00` to the end.

### 0.4 Canonical Prompt Templates (`prompt_templates_v3` — `compile_omni_1_2_native_prompt`)

#### Template 1: `1_multi_speaker_15s_scene_360p_draft`
```text
[MODEL: Gemini Omni 1.2 Flash | RESOLUTION: 360p Draft | DURATION: 15s | ASPECT RATIO: 16:9]
[REFERENCES: Scene Image + Character A & B Portraits + 1s Voice Reference A + 1s Voice Reference B]
Continuous 15-second cinematic two-shot inside a futuristic Manama command center. Yousef stands on the left in a dark tactical jacket; Noura stands on the right beside a glowing holographic map. Camera executes a slow, unbroken orbital push-in.
MULTI-SPEAKER BAHRAINI DIALECT LOCK (حوار ثنائي باللهجة البحرينية العامية الأصيلة بتزامن شفاه دقيق): Route Voice Reference A to Yousef and Voice Reference B to Noura with expressive lip-sync and natural timing.
- At 01s, Yousef speaks in authentic Bahraini dialect (يتحدث باللهجة البحرينية: "شوفي الإشارة وين تطلع.. عند باب البحرين بالضبط!"): "شوفي الإشارة وين تطلع.. عند باب البحرين بالضبط!"
- At 07s, Noura turns to him and replies in authentic Bahraini dialect (يتحدث باللهجة البحرينية: "عيل لازم نتحرك الحين قبل لا تقفل البوابة، ما عندنا وقت!"): "عيل لازم نتحرك الحين قبل لا تقفل البوابة، ما عندنا وقت!"
```

#### Template 2: `2_multi_turn_conversational_edit`
```text
[MULTI-TURN CONVERSATIONAL EDIT — TURN 2]
Keep both Yousef and Noura's exact performances, multi-speaker Bahraini dialogue, lip-sync, garment reflections, and camera framing completely intact across all 15 seconds. Swap the interior command center background to a rainy rooftop overlooking the illuminated Manama skyline at night, and switch the aspect ratio to 9:16 vertical.
```

#### Template 3: `3_product_or_virtual_try_on_15s_with_references`
```text
[MODEL: Gemini Omni 1.2 Flash | RESOLUTION: 360p Draft -> 4K Upscale | DURATION: 15s | ASPECT RATIO: 9:16]
[REFERENCES: Attach Front & Back Product Packaging Photos + Brand Logo Lock + 3s Motion Reference Clip]
15-second commercial showcase with match cuts and a smooth 360-degree product spin on a sleek dark marble counter. Lock all Arabic and English packaging typography, brand colors, and surface textures from the first frame to the final frame with zero distortion, adding motion-tracked callouts.
```

---

## 1. Flow Agent Mode & Structured JSON Project Initialization (`تهيئة المشروع في وكيل Flow بصيغة JSON`)

### 1.1 How the Flow Agent, `Agent instructions` (`article_spark`), and `Agent settings` (`tune`) Work
- Clicking the **`Agent`** pill in the bottom composer bar (`+ | Agent`) opens the persistent **Flow Agent Side-Panel** (`flow-agent-panel`).
- **`Agent instructions` (`button[aria-label="Agent instructions"]`, icon `article_spark`)**:
  - Opens the persistent project-level instruction manager (`+ Add instruction`).
  - Each instruction card contains:
    1. **`Instruction title`** (`input[placeholder="Instruction title"]`)
    2. **`Instruction description`** (`textarea[placeholder="Create a guideline for your agent"]`) — supports pasting our **JSON Project Initialization Brief** or natural-language dialect & cinematography rules.
    3. **`+ Reference`** button — attaches character/environment reference images directly to the Agent's standing instructions!
- **`Agent settings` (`button[aria-label="Settings"]`, icon `tune`)**:
  - **`Confirm before generating`**: `Always` (*"Agent will ask for confirmation before generating media"*) vs. `Never` (*"Agent will generate media and spend credits automatically"*).
  - **`Image generation default`**: Aspect ratio (`16:9 | 4:3 | 1:1 | 3:4 | 9:16`), batch count (`x1 | x2 | x3 | x4`), and model (`🍌 Nano Banana Pro | 🍌 Nano Banana 2 Lite | 🍌 Nano Banana 2.1`).
  - **`Video generation default`**: Aspect ratio (`16:9 | 9:16`), batch count (`x1 | x2 | x3 | x4`), and model (`Omni 1.2 Flash | Omni 1.1 Flash | Veo 3.1 - Lite | Veo 3.1 - Fast | Veo 3.1 - Quality`).
- **Direct Mode Switcher (`Settings trigger` on the prompt bar)**:
  - Switches between **`Frames`** (`First/Last frame`) and **`Ingredients`**, aspect ratio (`16:9 | 9:16`), resolution (`360p` draft vs. `720p+`), and duration (`3s..15s` in `1s` steps via the `Length` slider on `Omni 1.2 Flash`, displaying exact credit usage e.g. `10 credits` for `10s 360p` or `20 credits` for `15s 360p`).

### 1.2 Mandatory Pre-Production Step: JSON Project Initialization Brief
Before generating any image or video in a new project, initialize the **Flow Agent** (or compile the project state) by pasting a structured **Project Initialization JSON** into the Agent chat. This locks character identities, dialect rules, voice profiles, and visual guardrails across the entire session:

```json
{
  "flow_agent_init": {
    "version": "3.0",
    "edition": "Pure Gemini Omni 1.2 Flash Native Edition",
    "project_meta": {
      "title": "Project Title",
      "aspect_ratio": "9:16",
      "image_engine": "nano-banana-pro",
      "video_engine": "gemini-omni-1.2-flash",
      "extension_engine": "gemini-omni-1.2-flash",
      "native_duration_range_s": "3-15s (1s increments)",
      "confirm_before_generating": true
    },
    "dialect_and_voice_engine": {
      "primary_dialect": "Bahraini Gulf Arabic (Muharraq/Manama conversational)",
      "omni_flash_dialect_law": "Write Arabic dialogue in natural conversational dialect spelling WITHOUT heavy MSA harakat/tanween and prepend 'يتحدث باللهجة البحرينية:' directly before the quote so Gemini Omni 1.2 Flash uses its native dialect prosody and Multi-Speaker Conditioning.",
      "phonetic_lexicon": {
        "باجر": "Pronounced 'Baa-gir' (الباء والألف با + الجيم بصوت G مثل Good + الراء مخففة في النهاية)",
        "تقول / أقول / عقب / قبل / دقايق": "Pronounced with hard Gulf G (گ as in Good)",
        "كان / الجاي": "Pronounced with Gulf Ch (چ as in Chair: چان / الچاي)"
      },
      "forbidden_vocal_traits": [
        "No Modern Standard Arabic (Fusha) case endings or tanween (-un, -in, -an)",
        "No South-Asian, Indian, or non-native foreign accent",
        "No robotic syllable-by-syllable recitation"
      ]
    },
    "visual_guardrails": {
      "forbidden_prompt_tokens": [
        "Never write numeric focal/aperture strings like '85mm f/1.8' or 'Anamorphic' inside raw clip prompts (prevents camera-HUD text overlays burned onto still-life shots)",
        "Never write the words 'text', 'subtitles', 'watermark', or 'letters' even with 'no' (prevents positive-token text hallucinations)"
      ],
      "positive_frame_lock": "Clean unblemished cinema frame, pure optical capture, natural shallow depth of field"
    },
    "cast_registry": [
      {
        "tag": "@Jassim",
        "role": "Protagonist (30-year-old Bahraini man)",
        "visual_lock": "Bareheaded with short dark hair, neatly trimmed beard, wearing a dark charcoal tailored suit jacket over a crisp white collared shirt without tie",
        "voice_tag": "@Voice_Jassim_Bahraini"
      },
      {
        "tag": "@BuJassim",
        "role": "Father (68-year-old Bahraini elder)",
        "visual_lock": "Weathered kind Gulf Arab face, white beard, silver-rimmed reading glasses, traditional cream Bahraini thobe and white ghutra",
        "voice_tag": "@Voice_BuJassim_Elder"
      }
    ],
    "scene_plan": {
      "use_scene_builder": true,
      "workflow": "Generate base clips -> Add to scene (+ New scene / Add clip) -> Extend continuous takes with Veo 3.1 Lite -> Export unified timeline"
    }
  }
}
```

### 1.3 Sending Structured Per-Shot JSON Commands to the Flow Agent
Once initialized, you can command the Flow Agent using compact JSON shot directives:
```json
{
  "command": "generate_shot",
  "scene_id": "Scene_01",
  "shot_id": "Shot_01A",
  "mode": "ingredients_to_video",
  "model": "omni-flash",
  "duration_s": 10,
  "aspect_ratio": "9:16",
  "cast": ["@Jassim"],
  "voice": "@Voice_Jassim_Bahraini",
  "camera": "Medium close-up at eye level, slow dolly-in, soft shallow depth of field",
  "action": "@Jassim stands in the rain-washed Muharraq courtyard holding his glowing smartphone with trembling hands, a tear rolling down his cheek",
  "dialogue_dialect_ar": "أربعطعش مكالمة من أبوي.. رديت عليها عقب ما فات الفوت، ويش يفيد الندم الحين والكرسي العود صار خالي؟",
  "pronunciation_notes": "Natural Bahraini Muharraq dialect; عقب with hard G (ugub); zero Fusha tanween",
  "soundscape": "Soft rain on courtyard stone, melancholic solo Bahraini oud",
  "scene_action": "add_to_scene"
}
```

---

## 2. Why `Gemini Omni 1.2 Flash` Understands Dialects & Multi-Speaker Routing Natively (`قانون اللهجة الطبيعية والحوار الجماعي في Omni 1.2 Flash`)

### 2.1 The Root Cause of Dialect Stiffness (`لماذا يربك التشكيل المدرسي الثقيل محرك Omni 1.2 Flash؟`)
- **Crucial Distinction**:
  1. **Traditional External TTS (`edge-tts`, `ElevenLabs`)**: Are text-to-phoneme readers trained primarily on Modern Standard Arabic (`الفصحى`). They require heavy diacritics (`التشكيل الكامل`) to avoid misreading vowels.
  2. **`Gemini Omni 1.2 Flash` inside Google Flow**: Is a **native multimodal LLM** that understands spoken Arabic dialects (`لهجة بحرينية، كويتية، إماراتية، سعودية، عمانية، عراقية، مصرية، شامية`) directly from context and natural dialect orthography, and natively routes distinct `1-second` voice references across `4+` characters in a single `15-second` clip!
- **What Happens When You Over-Diacritize (`التشكيل الكامل لكل حرف`) in `Omni 1.2 Flash`**:
  - In Arabic training corpora, 100% diacritized text (`فَتْحَة، ضَمَّة، كَسْرَة، سُكُون على كل حرف`) appears almost exclusively in classical Fusha, poetry, and school textbooks.
  - Therefore, feeding `"الدُّنْيَا گَصِيْرَهْ وَالْعُمُرْ يِرْكُضْ فِيْنَا"` with heavy Harakat on every letter causes `Omni 1.2 Flash` to slow down and pronounce the words with a stiff, syllable-by-syllable Fusha/schoolbook cadence instead of natural Bahraini connected speech (`وصل الكلام والنبر العفوي`)!

### 2.2 The Locked 5-Point Rule for 100% Authentic Dialect & Borderless Frame in `Gemini Omni 1.2 Flash`
1. **Write the Explicit Arabic Dialect Prefix Immediately Before the Spoken Text (`يتحدث باللهجة البحرينية: "..."`)**:
   - For `flow.google.com` to lock onto the Bahraini dialect with maximum clarity, always write **`يتحدث باللهجة البحرينية:`** (in Arabic) directly before the quoted speech:
     - ✅ `يتحدث باللهجة البحرينية: "يا ولدي جاسم.. شحالك يبه؟ سويت لك القهوة اللي تحبها، متى بتجي تقعد وياي شوي؟"`
2. **Never Write Film-Stock Codes (`Kodak Vision3 500T`, `35mm film grain`, `Arri Alexa`, `9:16 framing`)**:
   - Writing `"Kodak Vision3 500T"` or `"35mm film"` causes Google Flow to render black analog film-strip borders with `"KODAK VISION3 500T"` edge text around the video instead of a full-screen frame. Always use **`full-bleed borderless frame filling 100% of the canvas edge-to-edge`**.
3. **Write Dialogue in Clean, Natural Dialect Orthography (`بدون تشكيل مدرسي ثقيل`)**:
   - Write the sentence exactly as a native Bahraini writes it in dialect:
     - ✅ `"يا خويي لا تقول باجر.. ترى باجر يمكن ما يجي، بوس راس أمك وأبوك اليوم واقعد وياهم لو خمس دقايق"`
     - ❌ Avoid putting `ـْ / ـَ / ـُ / ـِ` on every single letter when prompting `Omni 1.1 Flash`.
2. **Use English Phonetic Brackets ONLY for Key Dialect Words (`توجيه صوتي ذكي بين قوسين`)**:
   - Instead of cluttering the Arabic script with heavy Harakat, guide specific regional phonemes in brief English brackets right before the quote:
     - `speaking in natural conversational Bahraini Gulf Arabic dialect (pronouncing "باجر" as "Baa-gir" with hard G as in Good and soft r, and "تقول / دقايق / عقب / قبل" with hard Gulf G): "..."`
3. **Bind a Persistent `@Voice` Profile (`Voices` / `flow-set-voice`)**:
   - Create and lock a dedicated Bahraini/Gulf voice profile in Google Flow's **`Voices`** tab so the vocal identity, age, and regional cadence remain 100% identical across all clips.
4. **Use Conversational Turn-by-Turn Audio Refinement**:
   - Because `Omni 1.1 Flash` is stateful, if a clip's visual performance is great but a single word's dialect inflection needs adjustment, use Flow's conversational edit (`Keep the exact same video and character, but re-speak the line in a warmer, more natural Bahraini Muharraq accent, pronouncing باجر as Baa-gir`).

---

## 3. Eliminating Camera Lens Numbers (`85mm f/1.8`) & Text Artifacts Permanently

### 3.1 Why `85mm f/1.8 Anamorphic` Appeared on Screen in `7958497c-7da8-4462-a7cc-d8c44bc050b1`
- When a prompt starts with technical camera/lens strings like `"ARRI Alexa Mini LF Anamorphic ... (0-5s, 85mm f/1.8 MS hero table composition)"`, especially in shots without a talking human face, `Omni 1.1 Flash` interprets `"85mm f/1.8 Anamorphic"` as a **camera lens comparison / test-footage overlay** and renders `"85mm f/1.8 Anamorphic"` in white text at the bottom of the video!

### 3.2 Mandatory Anti-Overlay Law (`حظر أرقام العدسات والكلمات النصية داخل أوامر الفيديو`)
- **NEVER put numeric focal lengths or f-stops (`85mm`, `50mm`, `35mm`, `f/1.4`, `f/1.8`, `ISO 800`, `24fps`) inside a generative video prompt.**
- Translate technical lens numbers into **pure visual optics descriptions**:
  - Instead of `"85mm f/1.4 MCU"`, write: **`"Intimate medium close-up portrait with creamy shallow depth of field and soft bokeh background"`**.
  - Instead of `"35mm f/2.0 WS"`, write: **`"Wide cinematic establishing frame with deep environmental focus"`**.
  - Instead of `"Anamorphic"`, write: **`"Widescreen cinematic optics with subtle horizontal warm light bloom"`**.

---

## 4. Mastering the Google Flow Left Sidebar, Asset Picker & 11 MCP Modes

### 4.1 Asset Picker & Sidebar Tabs (`All | Images | Videos | Voices | Characters | Avatars | Uploads`)
| Flow Tab / Feature | Purpose in Production | MCP Mode (`flow_generate`) / UI Action |
| :--- | :--- | :--- |
| **`Characters`** | Builds a persistent digital actor from reference images + wardrobe/personality traits. Referenced anywhere via `@CharacterName` or **`Add to prompt`**. Eliminates face and clothing drift across scenes. | `mode: "flow-create-character"` or Left Sidebar ➔ `Characters` ➔ `New Character` |
| **`Voices`** | Creates or selects a persistent voice profile (gender, age, Gulf/Bahraini accent, warm/melancholic tone). Prevents voice changes between clips. | `mode: "flow-set-voice"` or Asset Picker ➔ `Voices` ➔ `Add to prompt` |
| **`Avatars`** | Captures/locks a speaking avatar with synchronized facial micro-expressions and lip-sync bound to a Voice profile. | Asset Picker ➔ `Avatars` ➔ `Add to prompt` |
| **`Uploads`** | Houses uploaded clean reference plates (`PROD_01`, `ENV_01`, `CHAR_01`), clickable via **`Add to prompt`**. | `mode: "flow-upload-assets"` or Asset Picker ➔ `Uploads` |
| **`Rename`** | Renames generated clips/assets inside Flow (`PROJECT_EP01_B01_S01`) so the workspace stays organized. | `mode: "flow-rename-asset"` or Clip Menu (`⋮`) ➔ `Rename` |

### 4.2 Scene Builder & Native Timeline Assembly (`Scenes`: `Add to scene`, `+ New scene`, `Add clip`, `Extend`)
Instead of treating Google Flow as an isolated clip generator, use its built-in **Scene Builder (`Scenes`)**:
1. **`Add to scene` ➔ `+ New scene`**:
   - Click the three-dot menu (`⋮`) on your generated opening clip (Screenshot 1) and choose **`Add to scene` ➔ `+ New scene`** to initialize the project timeline inside Flow.
2. **`Add clip` / `Add to scene`**:
   - For each subsequent approved clip, click **`Add to scene`** (or **`+ Add clip`** inside the Scene track) to assemble the full narrative sequence in order.
3. **`Extend (Veo 3.1 - Lite)` (`mode: "flow-extend-video"`)**:
   - When a scene needs continuous, unbroken action beyond 8–10 seconds (up to 40s), select the clip inside the Scene editor and click **`Extend (Veo 3.1 - Lite)`** (or call `flow_generate` with `mode: "flow-extend-video"` and `prompt: "what happens next"`).
   - Flow automatically feeds the final frames and audio of the clip into `Veo 3.1 - Lite` (or `Omni 1.1 Flash`) to generate a seamless continuation without a jump cut.
4. **Native Scene Export & Direct Publishing**:
   - Once all clips and extensions are linked in `Scenes`, export/download the assembled multi-scene master file directly from Google Flow (at `1080p` or `2K/4K` upscale) or use **`Publish to YouTube`**.

### 4.3 Flow `Tools` Ecosystem (`Explore tools` · `Mondo Sónico` · `+ Create tool`)
- **`Explore tools` (`Community` & `Templates`)**:
  - **`Mondo Sónico`** (*by Ricardo Villavicencio & Sebastián Carvallo*): Built-in professional multi-track sound design studio inside Google Flow featuring **cross-layer fade synchronization for `Ambiance`, `Foley`, and `SFX`**. Use it to layer authentic courtyard rain, footsteps on wet stone, tea pouring, and prayer-bead clicks with frame-accurate crossfades.
- **`+ Create tool` (Custom Studio Mini-Apps)**:
  - Allows building a custom tool inside Google Flow (`My Tools`) using natural language instructions — e.g., a **"Gulf Dialect Cinematic Shot Compiler"** that takes `(Character @tag, Scene Action, Dialect Line)` and automatically outputs a clean, lens-number-free, dialect-locked video generation block.
