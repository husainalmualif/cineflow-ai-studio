# 09 — Google Flow Complete Ecosystem Mastery: Flow Agent JSON Init, Native Dialect Engine, Voices/Characters/Avatars, Scene Builder (`Add to Scene` / `Extend`), and Flow Tools (`Mondo Sónico` & `+ Create tool`)

This reference manual codifies the complete architecture and operational workflows of **Google Flow (`https://flow.google.com/`)** across its browser workspace, **Flow Agent**, **Asset Picker (`Voices / Characters / Avatars`)**, **Scene Builder (`Scenes`)**, **Flow Tools (`Explore tools / Create tool`)**, and our **11-mode `flow-connector` MCP bridge**.

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
  - **`Video generation default`**: Aspect ratio (`16:9 | 9:16`), batch count (`x1 | x2 | x3 | x4`), and model (`Omni 1.1 Flash | Veo 3.1 - Lite | Veo 3.1 - Fast | Veo 3.1 - Quality`).
- **Direct Mode Switcher (`Settings trigger` on the prompt bar)**:
  - Switches between **`Frames`** (`First/Last frame`) and **`Ingredients`**, aspect ratio (`16:9 | 9:16`), resolution (`360p` draft vs. `720p+`), and duration (`4s | 6s | 8s | 10s`, displaying exact credit usage e.g. `Generating will use 15 credits`).

### 1.2 Mandatory Pre-Production Step: JSON Project Initialization Brief
Before generating any image or video in a new project, initialize the **Flow Agent** (or compile the project state) by pasting a structured **Project Initialization JSON** into the Agent chat. This locks character identities, dialect rules, voice profiles, and visual guardrails across the entire session:

```json
{
  "flow_agent_init": {
    "version": "2.0",
    "project_meta": {
      "title": "Project Title",
      "aspect_ratio": "9:16",
      "image_engine": "nano-banana-2.1",
      "video_engine": "omni-flash",
      "extension_engine": "veo-3.1-lite",
      "confirm_before_generating": true
    },
    "dialect_and_voice_engine": {
      "primary_dialect": "Bahraini Gulf Arabic (Muharraq/Manama conversational)",
      "omni_flash_dialect_law": "Write Arabic dialogue in natural conversational dialect spelling WITHOUT heavy MSA harakat/tanween so Omni 1.1 Flash uses its native dialect prosody instead of stiff textbook Fusha recitation.",
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

## 2. Why `Omni 1.1 Flash` Understands Dialects Natively (`قانون اللهجة الطبيعية في Omni 1.1 Flash`)

### 2.1 The Root Cause of Dialect Stiffness (`لماذا يربك التشكيل المدرسي الثقيل محرك Omni 1.1 Flash؟`)
- **Crucial Distinction**:
  1. **Traditional External TTS (`edge-tts`, `ElevenLabs`)**: Are text-to-phoneme readers trained primarily on Modern Standard Arabic (`الفصحى`). They require heavy diacritics (`التشكيل الكامل`) to avoid misreading vowels.
  2. **`Gemini Omni 1.1 Flash` inside Google Flow**: Is a **native multimodal LLM** that understands spoken Arabic dialects (`لهجة بحرينية، كويتية، إماراتية، سعودية، عمانية، عراقية، مصرية، شامية`) directly from context and natural dialect orthography!
- **What Happens When You Over-Diacritize (`التشكيل الكامل لكل حرف`) in `Omni 1.1 Flash`**:
  - In Arabic training corpora, 100% diacritized text (`فَتْحَة، ضَمَّة، كَسْرَة، سُكُون على كل حرف`) appears almost exclusively in classical Fusha, poetry, and school textbooks.
  - Therefore, feeding `"الدُّنْيَا گَصِيْرَهْ وَالْعُمُرْ يِرْكُضْ فِيْنَا"` with heavy Harakat on every letter causes `Omni 1.1 Flash` to slow down and pronounce the words with a stiff, syllable-by-syllable Fusha/schoolbook cadence instead of natural Bahraini connected speech (`وصل الكلام والنبر العفوي`)!

### 2.2 The Locked 4-Point Rule for 100% Authentic Dialect in `Omni 1.1 Flash`
1. **Write Dialogue in Clean, Natural Dialect Orthography (`بدون تشكيل مدرسي ثقيل`)**:
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
