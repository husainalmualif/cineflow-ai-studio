# سجل النماذج وحدود المدد الزمنية — Model Registry & Runtime Limits (`references/model-registry.md`)

> **المصدر البرمجي الموحد (`Single Source of Truth`):** [`scripts/studio_config.py`](../scripts/studio_config.py) (`MODEL_REGISTRY`، `MODEL_REGISTRY_LAST_VERIFIED = "2026-11-03"`، `OMNI_FLASH_MODEL_DEFAULT = "gemini-omni-flash-preview"`)  
> **الحالة (`status`):** `verify_live`  
> **تاريخ آخر تحقق (`last_verified`):** `2026-11-03`  
> **قاعدة التحقق:** جميع أرقام المدد، أسماء النماذج، وتكاليف الأرصدة هي **افتراضات قابلة للتحقق (`verify_live`) وليست قوانين جامدة**. يجب قراءة القيم البرمجية من `scripts/studio_config.py` وقراءة القيم الحية من المنصة قبل بدء التوليد.

---

## 1. حسم تعارض المدد الزمنية (`CR1` & `runtime_limits`)

لا تخلط أبداً بين **مدة اللقطة الواحدة المولَّدة (`allowed_clip_seconds`)** وبين **مدة الفيديو القصير الكامل (`short_form_total_seconds`)**:

| البند | القيمة الافتراضية (`verify_live`) | التوضيح والسبب الهندسي |
|---|---|---|
| **`allowed_clip_seconds`** | `[4, 6, 8, 10]` ثوانٍ | طول اللقطة/الكتلة الواحدة المولَّدة داخل محرك الفيديو (`max_single_shot_seconds = 10`؛ في `Veo 3.1` المدد هي `4, 6, 8` وفي `Omni 1.1 Flash` هي `4, 6, 8, 10`). |
| **`short_form_total_seconds`** | `[10, 15]` ثانية (مع لقطات فرعية `5–8s` أو `4–10s`) | الطول الإجمالي للفيديو القصير (`Reels / Shorts / TikTok Edit`) لتقليل التدهور البصري (`AI Degradation`) والحفاظ على ريتم المشاهدة. |
| **`long_form.threshold_seconds`** | `>= 60` ثانية | الفيديوهات الطويلة (قنوات تعليمية، فودكاست بصري، وثائقيات، أو قصص `MagicLight.AI` حتى 30–50 دقيقة) تُقسّم إلى **فصول من `60` إلى `90` ثانية**، وكل فصل يتكون من لقطات بطول `10` ثوانٍ فأقل (مع سقف سلسلة `Extend <= 40s`). |

---

## 2. سجل النماذج الموحد (`MODEL_REGISTRY` في `scripts/studio_config.py`)

| المنصة / المحرك | المعرف البرمجي (`default_model_id`) | الاسم التسويقي / البدائل (`aliases`) | المدد المسموحة (`allowed_clip_seconds`) | سقف التمديد (`extend_cap_s`) | الاستخدام الأمثل |
|---|---|---|---|---|---|
| **Google Flow (Veo Cinema)** | `veo-3.1-generate-preview` | `Veo 3.1 Lite`, `Veo 3.1 Fast`, `Veo 3.1 Quality` | `[4, 6, 8]` (`[8]` فقط على `Quality`) | `40` (`+8s` عبر `Lite`) | التصوير السينمائي الواقعي، مزامنة الشفاه، وقفل الهوية `Ingredients` |
| **Google Flow / Interactions API** | `gemini-omni-flash-preview` | `gemini-omni-1.1-flash`, `Omni 1.1 Flash` | `[4, 6, 8, 10]` (`[3..10]` عبر API) | `40` | حتى 7 مراجع و5 أصوات، تعديل الفيديو بالنص، والتفاعلات الحفظية عبر `mcp/server.py` |
| **Google Labs (Image Lock)** | `imagen-3.0-generate-002` | `Nano Banana Pro`, `Nano Banana 2 Lite` | صورة مرجعية ثابتة (`0 credits`) | غير منطبق | توليد أوراق قفل الهوية (`@Char`, `@Prod`, `@Env`) وترقية الصور `4K` مجاناً |
| **Seedance / Dreamina** | `seedance-2.0` | `Seedance 2.0`, `Seedream 3.0` | `[4, 6, 8, 10]` | `30` | نظام وسوم `@Image1` و`@Video1` و`@Audio1` واللقطات المتعددة في توليد واحد |
| **22-Tool Creative & AI Ecosystem** | `multi-platform-22` | `Runway Gen-4`, `Kling 3.0`, `Hailuo Director`, `Wan VACE`, `Higgsfield DoP`, `MagicLight.AI`, `HeyGen`, `Synthesia`, `Veed.io`, `OpusClip`, `Blender`, `C4D`, `After Effects`, `Apple Motion`, `Premiere Pro`, `DaVinci Resolve`, `CapCut`, `Filmora` | `[4, 5, 6, 8, 10]` (أو بالـ Frame في برامج المونتاج) | `30–40` (غير محدود في NLE) | راجع الدليل التفصيلي في [`references/11-22-tool-video-ecosystem-and-nle-mastery.md`](11-22-tool-video-ecosystem-and-nle-mastery.md) |
| **Flow Music** | `flow-music-studio` | `Flow Music Studio` | `15–180` | غير منطبق | توليد الموسيقى الخلفية المحددة بـ `BPM` ومفتاح موسيقي وبنية أقسام |
| **Programmatic Motion** | `remotion-v4.0.539` | `Remotion` + `Three.js WebGL` + `HyperFrames` | بالـ Frame (`30/60fps`) | غير محدود | التايبوغرافي العربي النظيف (`split_arabic_letters_zwj`)، الموشن جرافيك، والقطع الدقيق على النبض (`beat_grid.py`) |
