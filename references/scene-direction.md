# معاملات التوجيه الإخراجي وتوحيد الخاتمة — Scene Direction & Outro Standardization (`references/scene-direction.md`)

> **قاعدة التشغيل الذاتي (`instruction`):** كل مشهد يحصل على هذه المعاملات؛ تُولَّد تلقائياً بشكل متسق مع الغرض والجمهور، ولا يُسأل المستخدم إلا عمّا لا يمكن تخمينه.

---

## 1. نبرة الصوت (`tone_of_voice`)
تُضبط نبرة الأداء الصوتي والتعبير الوجهي لكل مشهد ضمن الأنماط القياسية التالية:
- `غاضب` (`Angry / Intense`)
- `ضاحك` (`Joyful / Laughing`)
- `باكي` (`Emotional / Tearful`)
- `جاد` (`Serious / Authoritative`)
- `ماكر` (`Cunning / Intriguing`)
- `متأمل` (`Contemplative / Reflective`)
- `هازئ` (`Sarcastic / Wry`)
- `دافئ واثق` (`Warm & Confident` — الافتراضي للإعلانات والشروحات)

---

## 2. لغة الجسد وقاعدة الفيزيائية (`body_language` & `physicality_rule`)

### الحالات الجسدية القياسية:
- `مرتاح` (`Relaxed`) | `متوتر` (`Tense`) | `كاذب` (`Evasive / Deceptive`) | `واثق` (`Confident`) | `متردد` (`Hesitant`) | `ودود` (`Friendly / Welcoming`).

### قاعدة الفيزيائية الصارمة (`physicality_rule`):
- **اكتب الانفعال كأفعال جسدية قابلة للتصوير (`كتفان مشدودتان، نظرة جانبية، يدان ثابتتان، تنفس هادئ`) لا كصفات عاطفية مجردة.**

---

## 3. محاكاة العتاد وحركة الكاميرا (`camera_gear` & `camera_movements`)

### خيارات العتاد (`camera_gear`):
1. `محاكاة كاميرا سينمائية احترافية` (`ARRI Alexa 65 / RED V-Raptor + Anamorphic / Prime Lenses`)
2. `محاكاة تصوير هاتف ذكي (Phone Style)` (`UGC / Handheld iPhone Pro Natural Depth`)
3. `كاميرا فيلم` (`35mm / 16mm Kodak Vision3 Film Stock Emulation`)

### حركات الكاميرا الست (`camera_movements`):
- `Pan` (التفات أفقي) | `Tilt` (إمالة عمودية) | `Zoom` (تقريب/تبعيد بصري) | `Dolly` (دفع/سحب فيزيائي للكاميرا) | `Crane` (رافعة عمودية) | `Orbit` (دوران قوسي حول الهدف).

> **قاعدة الحركة الواحدة (`single_move_rule`):** حركة كاميرا رئيسية واحدة لكل لقطة لتقليل التشوه البصري (`AI Warping`).

---

## 4. التصحيح اللوني (`color_grading` — `tier: stylistic`)
- `سينمائي` (`Cinematic Teal/Amber or Rich Contrast`)
- `دافئ` (`Warm Golden Hour`)
- `واقعي` (`True-to-Life Photorealistic`)
- `ألوان طبيعية` (`Natural Balanced Skin Tones`)
- `درامي مظلم` (`Dark Moody Chiaroscuro`)

---

## 5. قفل الهوية البصرية (`identity_lock`)
- **العناصر المستخرجة من المرجع (`extract_from_reference`):** `الملامح`، `الملابس`، `الشعارات`.
- **المعرّفات القياسية (`ids`):** `CHAR_xx` (الشخصيات)، `PROD_xx` (المنتجات)، `ENV_xx` (البيئات).
- **القاعدة (`rule`):** تُكرَّر أوصاف الهوية حرفياً في كل لقطة، وتُستخدم الصورة المرجعية في كل توليد، وآخر إطار من لقطة يصير أول إطار للتالية (`Frames / Extend`) عند الحاجة.
- **عند انحراف الهوية (`on_drift`):** أرفق مراجع إضافية، أو قصّر اللقطة، أو أعد تصميمها بإطار أقرب وأبسط بعد محاولتين.

---

## 6. توحيد الخاتمة والمناطق الآمنة (`outro_standardization` — `status: tuned_default`)

- **الأبعاد القياسية للريلز والشورتس:** `9:16` (`1080×1920`).
- **القواعد:**
  1. اترك مساحة آمنة للعلامة التجارية والتواصل ودعوة اتخاذ الإجراء (`CTA`) دون تداخل مع المحتوى أو أزرار المنصة.
  2. لقطة الخاتمة نظيفة الخلفية بمساحة سلبية واضحة (`35% Clean Negative Space`).
  3. تُحدَّد الإحداثيات في [`scripts/studio_config.py`](../scripts/studio_config.py) وتُراجع بمعاينة آمنة (`--safe`).
- **الإحداثيات الافتراضية (`OUTRO_SAFE_ZONES`):**
  - **`logo_zone`:** `Y 420..820`
  - **`cta_zone`:** `Y 950..1280, X 120..900`
  - **مناطق تُتجنب (`avoid`):** `أعلى 220`، `أسفل من 1500`، `يمين من 920`.
