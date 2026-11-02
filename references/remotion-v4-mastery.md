# دليل إتقان Remotion v4.0.539 الرسمي — Official Remotion v4.0.539 Mastery Reference (`references/remotion-v4-mastery.md`)

يُوثّق هذا المرجع القواعد الهندسية والبصرية المستخلصة من حزمة المهارات الرسمية **`Remotion v4.0.539` (`packages/skills/skills/*`)** لضمان بناء فيديوهات سينمائية وتفاعلية احترافية خالية من التكديس البصري أو تشوه الحروف العربية.

---

## 1. قانون تصميم الفيديو أولاً (`video-layout.md` — Video-First Layout Law)

> **القاعدة الذهبية:** أنت تصمّم **فيديو سينمائياً متحركاً وليس صفحة ويب أو لوحة تحكم (`Dashboard`)**.

### 1.1 نقطة ارتكاز بصرية واحدة لكل مشهد (`Single Visual Focal Point`)
1. **حدد ما يجب أن يلاحظه المشاهد أولاً في كل مشهد:** ابنِ الكادر بالكامل حول **عنصر بطل واحد (`One Primary Thing`)**، واجعل كل العناصر الأخرى في المشهد تخدم هذا العنصر أو تترك له مساحة تنفس سلبية (`Negative Space`).
2. **امنع تكديس البطاقات (`Zero Dashboard Clutter`):** لا تضع `3` أو `4` بطاقات صغيرة مكدسة في شاشة واحدة كما في مواقع الويب. إذا تعددت الأفكار، افردها زمنياً على مشاهد متتالية (`<TransitionSeries>`).
3. **احذف العناصر المكررة (`No Redundant Elements`):** لا تضع شارة علويّة وبطاقة وسطى وكابشن سفلي يقولون نفس الجملة في اللحظة ذاتها.

### 1.2 الحدود الدنيا الإلزامية لأحجام الخطوط (`Minimum Typography Scale for 1080px-Wide Video`)
في أي تكوين بعرض `1080px` (`1080×1920` طولي أو `1920×1080` عرضي)، يُمنع استخدام أحجام خطوط صفحات الويب الصغيرة (`16px–28px`):
- **العنوان الرئيسي (`Main Headline`):** **`>= 84px`** (عريض `fontWeight: 800–900`، بارز فوراً على شاشة الجوال).
- **النص الداعم المهم (`Important Supporting Text`):** **`>= 44px`** (واضح ومقروء من النظرة الأولى دون تقريب الشاشة).
- **قياس النص ومنع الالتفاف غير المقصود (`@remotion/layout-utils`):**
  استخدم `fitText()` أو `measureText()` أو `fillTextBox()` من `@remotion/layout-utils` لضبط حجم الخط تلقائياً داخل العرض المتاح بدلاً من ترك النص ينكسر عشوائياً.

### 1.3 الهوامش الآمنة السخية (`Generous Safe Area Margins`)
- **الهامش الأفقي (`Left / Right`):** لا يقل عن **`80px`** من يمين ويسار الشاشة (`X: 80..1000` في عرض `1080px`).
- **الهامش الرأسي (`Top / Bottom`):** لا يقل عن **`100px`** في الفيديو العادي، وفي ريلز/تيك توك (`9:16`) يُدمج مع منطقة الأمان الخاصة بالمنصة (`Top >= 220px`, `Bottom <= 1500px`, `Right <= 920px`).

---

## 2. تحريك النصوص العربية والاتجاه ثنائي اللغة (`remotion-markup/arabic-text.md`)

### 2.1 كشف الاتجاه التلقائي (`isRtl` Word-Majority Detector)
اضبط العنصر الأب دائماً على `dir="rtl"` و `lang="ar"` للنصوص العربية، أو اكشف الاتجاه تلقائياً بأغلبية الكلمات:
```ts
const RTL = /[\u0591-\u07FF\uFB1D-\uFDFD\uFE70-\uFEFC]/;
export const isRtl = (text: string): boolean => {
  const words = text.trim().split(/\s+/);
  return words.filter((w) => RTL.test(w)).length > words.length / 2;
};
```

### 2.2 التحريك بالكلمة (`Word-Level Animation` — الخيار الافتراضي الآمن)
- في العربية، الحروف متصلة ويتغير شكل الحرف بحسب موقعه (`بـ / ـبـ / ـب`). لذلك **التحريك كلمةً بكلمة (`split(/\s+/)`) هو الخيار الافتراضي** لأنه يحافظ على اتصال الحروف وتشكيلها ورباط `لا` تلقائياً.

### 2.3 خوارزمية تقسيم الحروف العربية مع الحفاظ على الاتصال (`splitArabicLetters` via `U+200D` ZWJ)
إذا طُلب تحريك النص العربي **حرفاً بحرف (`Per-Letter Animation`)**، يُمنع منعاً باتاً استخدام `text.split('')` العادي لأنه يكسر اتصال الحروف ويُفصل التشكيل. يجب استخدام خوارزمية **`splitArabicLetters()`** الرسمية التي تحقن **الرابط الصفري (`\u200D` — Zero-Width Joiner)** قبل وبعد كل حرف متصل، وتُبقي التشكيل (`Harakat`) ملتصقاً بالحرف، وتحفظ رباط **`لا / لأ / لإ / لآ`** كوحدة واحدة، وتُبقي الأرقام والكلمات الإنجليزية (`LTR runs`) ككتلة واحدة:

```ts
const HARAKAT = /[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]/;
const ARABIC = /[\u0621-\u064A\u066E-\u066F\u0671-\u06D3\u06F0-\u06FC]/;
// الحروف التي تتصل بما قبلها فقط ولا تتصل بما بعدها (حروف القطع + التاء المربوطة + الهمزة على السطر)
const RIGHT_JOIN_ONLY = new Set('اأإآدذرزوؤةءٱ');
const ALEF_WITH_LAM = new Set('اأإآٱ');
const ZWJ = '\u200D';

export const splitArabicLetters = (word: string): string[] => {
  const clusters: { base: string; marks: string }[] = [];
  for (const ch of word) {
    if (HARAKAT.test(ch) && clusters.length > 0) {
      clusters[clusters.length - 1].marks += ch;
    } else {
      clusters.push({ base: ch, marks: '' });
    }
  }

  const units: { text: string; firstBase: string; lastBase: string; isArabic: boolean }[] = [];
  for (let i = 0; i < clusters.length; i++) {
    const c = clusters[i];
    const next = clusters[i + 1];
    // دمج ل + ا (لا، لأ، لإ، لآ) في وحدة واحدة لمنع تفكك الرباط الطباعي
    if (c.base === 'ل' && next && ALEF_WITH_LAM.has(next.base)) {
      units.push({
        text: c.base + c.marks + next.base + next.marks,
        firstBase: c.base,
        lastBase: next.base,
        isArabic: true,
      });
      i++;
    } else if (ARABIC.test(c.base)) {
      units.push({ text: c.base + c.marks, firstBase: c.base, lastBase: c.base, isArabic: true });
    } else if (units.length > 0 && !units[units.length - 1].isArabic) {
      // إبقاء الأرقام والحروف اللاتينية (مثل "2026" أو "iOS") متصلة في كتلة LTR واحدة
      units[units.length - 1].text += c.base + c.marks;
    } else {
      units.push({ text: c.base + c.marks, firstBase: c.base, lastBase: c.base, isArabic: false });
    }
  }

  const joinsRight = (u: (typeof units)[number]) => u.isArabic && u.firstBase !== 'ء';
  const joinsLeft = (u: (typeof units)[number]) => u.isArabic && !RIGHT_JOIN_ONLY.has(u.lastBase);

  return units.map((u, i) => {
    const prev = units[i - 1];
    const next = units[i + 1];
    const prefix = prev && joinsLeft(prev) && joinsRight(u) ? ZWJ : '';
    const suffix = next && joinsLeft(u) && joinsRight(next) ? ZWJ : '';
    return prefix + u.text + suffix;
  });
};
```
- **تنبيه الخطوط لـ `U+200D`:** عند تحريك الحروف بـ `splitArabicLetters`، استخدم **`Noto Sans Arabic`** أو **`Noto Naskh Arabic`** (مُحمّلة عبر `@remotion/google-fonts` مع `subsets: ['arabic']`) لأن بعض الخطوط (مثل `Cairo` و `Amiri`) لا تدعم `U+200D` عبر حدود عناصر `<span>` المنفصلة في محرك Chromium.

---

## 3. صياغة التحريك والـ Markup الحديثة في Remotion 4.0.539 (`remotion-markup`)

### 3.1 كتابة `interpolate()` مباشرة في `style` مع `perceptual-scale`
1. **تجنب المتغيرات الوسيطة غير الضرورية:** ضع `interpolate()` أو `spring()` مباشرة داخل خاصية `style`.
2. **استخدم خصائص CSS المستقلة (`scale`, `translate`, `rotate`) بدلاً من سلسلة `transform` النصية:**
   ```tsx
   <div
     style={{
       opacity: interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' }),
       scale: interpolate(frame, [0, 20], [0.5, 1], {
         output: 'perceptual-scale',
         easing: Easing.out(Easing.cubic),
         extrapolateRight: 'clamp',
       }),
       translate: `0 ${interpolate(frame, [0, 20], [40, 0], { extrapolateRight: 'clamp' })}px`,
     }}
   />
   ```
3. **`output: 'perceptual-scale'`:** إلزامي عند تحريك التكبير/التصغير عبر مدى واسع (مثل `0.5x -> 3x`) لجعل سرعة التقريب تبدو خطية للعين البشرية.

### 3.2 الطبقات والتنقل بين المشاهد (`<TransitionSeries>` & `<Track>`)
- استخدم `<AbsoluteFill>` لتكديس الطبقات، أو `<Track>` في التايم لاين التفاعلي.
- استخدم `<TransitionSeries>` من `@remotion/transitions` لربط المشاهد:
  - `<TransitionSeries.Sequence durationInFrames={...}>` للمشاهد.
  - `<TransitionSeries.Transition presentation={fade() | slide() | wipe() | flip() | clockWipe() | cube() | iris()} timing={springTiming({ durationInFrames: 20 })} />` للانتقالات.
  - `<TransitionSeries.Overlay durationInFrames={...}>` لمؤثرات الانتقال الفوقية مثل ومضات الإضاءة (`Light Leaks`).

### 3.3 التفاعلية في الاستوديو (`@remotion/studio` `<Interactive.*>` & `InteractivitySchema`)
- لتمكين المستخدم من تحريك العناصر وتغيير حجمها وتدويرها مباشرة بالسحب داخل Remotion Studio، استخدم `<Interactive.Div>`, `<Interactive.Img>`, `<Interactive.Span>` مع `InteractivitySchema` في `zod` schema الخاصة بالـ `<Composition>`.

### 3.4 المؤثرات البصرية WebGL2/WebGPU (`@remotion/effects`) وضبابية الحركة (`@remotion/motion-blur`)
- **تصحيح الألوان والمؤثرات (`@remotion/effects`):**
  استخدم `colorCorrection()`, `levels()`, `curves()`, `lut()`, `lightLeak()`, `vignette()`, `blur()`, `chromaticAberration()`, `glitch()`, `pixelate()`, `noise()` داخل `<HtmlInCanvas>` لمعالجة البيكسلات بسرعة GPU.
- **ضبابية الحركة الفيزيائية (`<HtmlInCanvasMotionBlur>`):**
  غلّف المشاهد السريعة بـ `<HtmlInCanvasMotionBlur shutterAngle={180} samples={10}>` من `@remotion/motion-blur` لإضافة ضبابية حركة سينمائية حقيقية، مع تمرير `canvasSize={{ width, height }}` لأي عنصر `3D` بالداخل.

### 3.5 الكابشن والتفريغ الصوتي (`@remotion/captions` & `@remotion/whisper-webgpu`)
- التزم بمخطط `Caption` القياسي: `{ text, startMs, endMs, timestampMs, confidence, pageBreakAfter }`.
- لتحويل ملفات `.srt` إلى مصفوفة `Caption[]` برمجياً، استخدم `parseSrt({ input })` من `@remotion/captions`.

### 3.6 الكشف التكيّفي عن الصمت على مرحلتين (`remotion-markup/silence-detection.md`)
بدلاً من تثبيت عتبة صمت جامدة تفشل مع التسجيلات المنخفضة أو الصاخبة، استخدم **الفحص التكيّفي ذا المرحلتين (`Two-Pass Adaptive Silence Detection`)**:
1. **المرحلة الأولى (`Pass 1 — Measure Audio Floor`):** قياس `input_thresh` الفعلي للملف عبر فلتر `loudnorm`:
   ```bash
   ffmpeg -hide_banner -vn -i input.mp4 -af "loudnorm=print_format=json" -f null -
   ```
2. **المرحلة الثانية (`Pass 2 — Adaptive Silence Detect`):** تمرير `input_thresh` المستخرج كعتبة `noise` لفلتر `silencedetect`:
   ```bash
   ffmpeg -hide_banner -vn -i input.mp4 -af "silencedetect=noise=${INPUT_THRESH}dB:d=0.5" -f null -
   ```
   مع إضافة هامش التنفس الطبيعي (`120ms` قبل الكلمة و `150ms` بعدها لحماية أواخر الحروف العربية).
