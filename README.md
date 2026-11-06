# استوديو سينما فلو الذكي — CineFlow AI Studio 🎬

**الإصدار `7.0.0` (`Pure Gemini Omni 1.2 Flash Native Edition — google-flow-director v3.0.0`)** — الاستوديو الشامل للتوليد السينمائي بالذكاء الاصطناعي (`Google Flow • Gemini Omni 1.2 Flash • Nano Banana Pro • Veo 3.1 • Seedance 2.0 • Runway Gen-4 • Kling 3.0 • Hailuo Director • Wan VACE • Higgsfield DoP • MagicLight.AI`)، بالتوليد الأصلي من `3` إلى `15` ثانية بزيادة ثانية واحدة، والتعديل الحواري المجاني (`0 credits`)، والحوار الجماعي الأصلي (`Multi-Speaker Conditioning`) بـ 12 لهجة عربية (`يتحدث باللهجة البحرينية:`) مع مراعاة الأعراف المجتمعية وعلم نفس الإعلان، والمونتاج الإيقاعي المقفول على النبض (`beat_grid.py`)، والمونتاج البرمجي والاحترافي (`Remotion v4.0.539 • B Studio v1.0.10 • Blender • Cinema 4D • After Effects • Apple Motion • Premiere Pro • DaVinci Resolve Studio • CapCut • Filmora • HeyGen • Synthesia • Veed.io • OpusClip`).

> 📖 **الدستور الكامل والمعمارية التفصيلية:** راجع [`SKILL.md`](SKILL.md) و[`references/architecture-and-pipelines.md`](references/architecture-and-pipelines.md) و[`references/b-studio-and-video-edit-mastery.md`](references/b-studio-and-video-edit-mastery.md) و[`references/09-google-flow-agent-scenes-and-tools-mastery.md`](references/09-google-flow-agent-scenes-and-tools-mastery.md) و[`references/10-google-flow-cli-scripting-and-automation-mastery.md`](references/10-google-flow-cli-scripting-and-automation-mastery.md) و[`references/11-22-tool-video-ecosystem-and-nle-mastery.md`](references/11-22-tool-video-ecosystem-and-nle-mastery.md) و[`references/12-human-cultural-dialects-and-media-psychology.md`](references/12-human-cultural-dialects-and-media-psychology.md).

---

## 1. التثبيت السريع (Installation & Setup)

### أ) التثبيت عبر `npx skills`:
```bash
npx skills add husainalmualif/cineflow-ai-studio
```

### ب) التثبيت وتفعيل خادم `FastMCP` (`cineflow-omni-agent`):
```bash
# تثبيت المهارة وتسجيل خادم MCP على مستوى المستخدم أو المشروع
bash mcp/project-setup.sh --global

# تثبيت مكتبات التشغيل والاختبار
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## 2. أوامر التشغيل التفاعلية العشرة (`Showrunner Command Modes`)

| الأمر | الاستخدام | مثال سريع |
| :--- | :--- | :--- |
| **`/quick`** | توليد فوري (بحث + سكربت مشكول + `06_package.json` + تدقيق) في رد واحد | `/quick صمم لي إعلان 15 ثانية لعطر رجالي فخم باللهجة الخليجية 9:16` |
| **`/full`** | دورة عمل كاملة (`00_brief.md` ➔ `10_marketing.md`) مع بوابتي اعتماد `GATE 1` و`GATE 2` | `/full أريد إنتاج فيديو 30 ثانية لإطلاق تطبيق مالي ذكي بموشن 60fps` |
| **`/series`** | بناء سلسلة حلقات مترابطة بنفس قفل الهوية (`03_identity_bible.md`) | `/series صمم لي سلسلة من 5 حلقات قصيرة تشرح الذكاء الاصطناعي` |
| **`/audit`** | تدقيق حزمة إنتاج أو سكربت من 26 نقطة (`>= 22/26`) | `/audit دقق لي ملف examples/example_03_showrunner_package.json` |
| **`/fix`** | إصلاح لقطة واحدة عبر بروتوكول الإعادة (`Re-Roll Protocol`) | `/fix اللقطة الثانية فيها سطوع زائد على البطاقة ثلاثية الأبعاد` |
| **`/sync`** | ضبط التشكيل الإذاعي (`>= 75%` + وقف `هْ`) ومزامنة الشفاه | `/sync اضبط تشكيل وتزامن هذا النص الإذاعي على إيقاع 120 BPM` |
| **`/expand`** | توليد الغلاف الآمن `1080×1080` + البوستر `4:5` + الكاروسيل `5–8 شرائح` | `/expand حول هذا الفيديو إلى بوستر وكاروسيل إنستجرام من 6 شرائح` |
| **`/research`** | التحقق الحي من حدود النماذج والترندات (`01_research.md`) | `/research ابحث عن أحدث حدود Google Flow وترندات إعلانات القهوة` |
| **`/cost`** | حساب تكلفة الأرصدة المتوقعة والقصوى قبل `GATE 2` | `/cost احسب تكلفة الأرصدة لحزمة examples/example_03_showrunner_package.json` |
| **`/post`** | توليد ملف الترجمة `.srt` وخطة المونتاج والماستر الصوتي `-14.0 LUFS` | `/post جهز ملف الترجمة .srt وخطة المونتاج للمشروع` |

---

## 3. التشغيل البرمجي السريع عبر سطر الأوامر (Quickstart CLI)

جميع الملفات الناتجة أدناه (`examples/generated_perfume_ad.json`، `examples/multi_agent_plan.json`، `examples/script_source.json`) متوفرة كنسخ نموذجية جاهزة في مجلد [`examples/`](examples/) ويمكن إعادة توليدها مباشرة بالأوامر التالية:

```bash
# 1. حساب شبكة النبض وخريطة القطع للمونتاج الإيقاعي (120 BPM, 30 fps)
python scripts/beat_grid.py --bpm 120 --time-signature 4/4 --fps 30 --duration 15 --pattern build_up

# 2. تجميع مخطط إنتاج متكامل (يُولَّد بهذا الأمر في examples/generated_perfume_ad.json)
python scripts/cineflow_compiler.py \
  --idea "إعلان عطر شرقي فاخر في صحراء ذهبية وقت الغروب /dollyin /gold /ar 9:16" \
  --purpose "Commercials & TVCs" \
  --format "Live-Action" \
  --style-variant "Commercial Promo" \
  --dialogue "عبيرٌ يَروي حِكايةَ الفَخامةِ الأصيلةِ في كُلِّ لَحظة." \
  --runtime 16 \
  --output examples/generated_perfume_ad.json

# 3. توليد وفحص خطة عمل الوكلاء السبعة وفحص التشكيل الإذاعي
#    (ملاحظة: examples/multi_agent_plan.json هو خطة تنسيق وكلاء يُفحص بـ --verify-plan وليس حزمة blueprint)
python scripts/multi_agent_orchestrator.py \
  --topic "إعلان تقني ثلاثي الأبعاد لتطبيق ذكي" \
  --pipeline route_3_motion_stage_60fps \
  --duration 30 \
  --validate-script examples/script_source.json \
  --output-plan examples/multi_agent_plan.json
python scripts/multi_agent_orchestrator.py --verify-plan examples/multi_agent_plan.json

# 4. التحقق من الحزمة، حساب التكلفة، وتوليد ملف الترجمة (.srt)
python scripts/validate_package.py examples/example_03_showrunner_package.json
python scripts/estimate_cost.py examples/example_03_showrunner_package.json 10 1
python scripts/make_srt.py examples/example_03_showrunner_package.json examples/out_subtitles.srt
python scripts/lint_package.py check examples/example_03_showrunner_package.json   # فحص الحوكمة: استمرارية Flow + SFX Governor + حارس الوجه/النوافذ

# 5. تشغيل الفحص الديناميكي للمراجع والاختبارات الآلية وفحص pylint
python scripts/verify_skill_references.py
pytest
pylint scripts/*.py mcp/server.py tests/*.py
```

---

## 4. هيكل ملفات المستودع (Repository Structure)

```text
cineflow-ai-studio/
├── SKILL.md                                     # الدستور الرئيسي للمهارة (name: cineflow-ai-studio)
├── README.md                                    # المدخل السريع للتثبيت والاستخدام (هذا الملف)
├── CHANGELOG.md                                 # سجل تغييرات الإصدارات
├── LICENSE                                      # رخصة Apache-2.0
├── pyproject.toml                               # إعدادات المشروع الموحدة لـ pytest و pylint
├── requirements.txt                             # متطلبات التشغيل الاختيارية لخادم MCP
├── requirements-dev.txt                         # أدوات التطوير والفحص الآلي (pytest, pylint)
├── .gitignore                                   # حماية مفاتيح API وملفات OAuth والكاش
├── templates/
│   ├── package.template.json                    # قالب حزمة الإنتاج القياسي (06_package.json)
│   └── flow_agent_project_init.template.json    # قالب تهيئة وكيل Google Flow بصيغة JSON (Flow Agent Init)
├── mcp/
│   ├── server.py                                # خادم FastMCP بـ 8 أدوات لتوليد وتعديل الفيديو (تجميع كسول للـ Client + JSON OAuth)
│   ├── requirements.txt                         # متطلبات خادم FastMCP (google-genai, mcp)
│   └── project-setup.sh                         # سكربت تثبيت المهارة (cineflow-ai-studio) وتسجيل الخادم (cineflow-omni-agent)
├── scripts/
│   ├── studio_config.py                         # المصدر الوحيد للحقيقة للثوابت وسجل النماذج (MODEL_REGISTRY) والـ 190+ ماكرو
│   ├── arabic_helpers.py                        # أدوات العربية: كشف اللهجة، الكشيدة الآمنة، تقسيم ZWJ، وفحص تخطيط الفيديو
│   ├── governance_and_omni.py                   # فاحص خطر الشرائح، التنوع البصري، وباني حمولات Gemini Omni Flash الحفظية
│   ├── cineflow_compiler.py                     # المترجم الرئيسي لمخططات الإنتاج (JSON Blueprint Compiler)
│   ├── beat_grid.py                             # حاسبة شبكة النبض الموسيقي وخريطة القطع والـ Speed Ramps (MQ1..MQ7)
│   ├── multi_agent_orchestrator.py              # منسق الوكلاء السبعة والـ 13 دوراً + مدقق الصوتيات الإذاعية
│   ├── validate_package.py                      # مدقق الحزم القياسي ومخرجات الـ Showrunner
│   ├── estimate_cost.py                         # حاسبة الأرصدة ثلاثية السيناريوهات قبل GATE 2
│   ├── make_srt.py                              # مولد ملفات الترجمة العربية (.srt)
│   ├── lint_package.py                          # واجهة سطر أوامر لقواعد الحوكمة: check / sanitize / storyboard / tool-payload / cultural-audit
│   ├── verify_skill_references.py               # مدقق الروابط والمراجع الديناميكي للـ CI
│   ├── sync_remotion_skills.py                  # أداة تحديث وتوثيق مراجع Remotion الرسمية
│   └── Compile-CineFlowBlueprint.ps1            # غلاف PowerShell يستدعي cineflow_compiler.py
├── references/
│   ├── architecture-and-pipelines.md            # المعمارية التفصيلية والمسارات الاثنا عشر والتخطيط الرباعي
│   ├── taxonomy.md                              # التصنيف الخماسي القياسي
│   ├── rhythmic-montage.md                      # قواعد المونتاج الإيقاعي (MQ1..MQ7)
│   ├── scene-direction.md                       # معاملات التوجيه الإخراجي وقفل الهوية
│   ├── arabic-text-and-lipsync.md               # سلامة النص العربي ومزامنة الشفاه
│   ├── model-registry.md                        # سجل النماذج الموحد (MODEL_REGISTRY) وتاريخ آخر تحقق
│   ├── remotion-v4-mastery.md                   # دليل إتقان Remotion v4.0.539
│   ├── b-studio-and-video-edit-mastery.md       # إتقان B Studio v1.0.10 و Video-Edit v1.1 (حفظ الصوت واللون، النوافذ الأربع، كولاج Vox، وحاكم المؤثرات)
│   ├── gemini-interactions-api.md               # دليل واجهة التفاعلات الحفظية لـ Gemini Omni Flash
│   ├── 09-google-flow-agent-scenes-and-tools-mastery.md # إتقان Google Flow Agent وVoices/Characters/Scenes وMondo Sónico
│   ├── 10-google-flow-cli-scripting-and-automation-mastery.md # إتقان Google Flow CLI وScripting v1.6.0 وUGC
│   ├── 11-22-tool-video-ecosystem-and-nle-mastery.md # الموسوعة العملية لـ 22 أداة مونتاج و3D وتوليد فيديو بالذكاء الاصطناعي
│   ├── 12-human-cultural-dialects-and-media-psychology.md # فقه اللهجات الـ 12 والأعراف المجتمعية وعلم نفس الإعلام والإعلان
│   ├── 01-team-and-roles.md .. 08-model-registry-and-benchmarks.md
│   └── remotion_skills_official/                # مكتبة قواعد Remotion v4.0.539 المرجعية الرسمية (مع UPSTREAM_ATTRIBUTION.md)
├── resources/
│   ├── blueprint_schema.json                    # عقد الـ JSON Schema الموحد
│   ├── flow_pipeline_schema.json                # عقد خطوط إنتاج المشاهد لـ Google Flow (flow.json)
│   └── evals.json                               # حالات التقييم القياسية (متزامنة مع evals/evals.json)
├── evals/
│   └── evals.json                               # حالات تقييم التفعيل والقبول
├── examples/
│   ├── example_01_commercial_promo.json         # مثال 1 (Blueprint): إعلان تجاري خليجي موحد
│   ├── example_02_explainer_and_story_script.json # مثال 2 (Blueprint): فيديو شرح وموشن جرافيك
│   ├── example_03_how_to_use_cineflow.json      # مثال 3 (Blueprint): ريل تعليمي لاستخدام المهارة
│   ├── example_03_showrunner_package.json       # مثال 4 (Blueprint): حزمة إنتاج Showrunner متكاملة
│   ├── generated_perfume_ad.json                # مثال 5 (Blueprint): حزمة ناتجة عن cineflow_compiler.py
│   ├── flow_pipeline.example.json               # مثال صالح لـ resources/flow_pipeline_schema.json (تتحقق منه الاختبارات)
│   ├── multi_agent_plan.json                    # خطة تنسيق الوكلاء السبعة (تُفحص بـ multi_agent_orchestrator.py --verify-plan)
│   └── script_source.json                       # مدخل سكربت إذاعي مشكول (يُفحص بـ multi_agent_orchestrator.py --validate-script)
└── tests/
    ├── test_cineflow_compiler.py                # اختبارات المترجم واللغة العربية والحوكمة
    ├── test_montage.py                          # اختبارات المونتاج الإيقاعي وRemotion v4 وOmni API
    ├── test_omni_agent.py                       # اختبارات خادم FastMCP بالمحاكاة (Mocked GenAI)
    └── test_lint_package.py                     # اختبارات lint_package.py والـ 22 أداة وفحص اللهجات والأعراف
```

---

## 5. نسب المصادر الخارجية والترخيص (External Attribution & License)

- **مكتبة قواعد Remotion الرسمية ([`references/remotion_skills_official/`](references/remotion_skills_official/UPSTREAM_ATTRIBUTION.md)):**
  - منسوخة من المستودع الرسمي [`remotion-dev/remotion`](https://github.com/remotion-dev/remotion/tree/v4.0.539/packages/skills/skills/remotion) — المسار `packages/skills/skills/remotion`، الإصدار **`v4.0.539`**، وتخضع لترخيص Remotion / MIT لقوالب وتوثيق المهارات ([`LICENSE.md`](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md)).
  - لتحديث المجلد برمجياً من نسخة محلية بدلاً من النسخ اليدوي:
    ```bash
    python scripts/sync_remotion_skills.py --source /path/to/remotion/packages/skills/skills/remotion --version v4.0.539
    ```
- **ترخيص المستودع:** مرخص بموجب رخصة [**Apache License 2.0**](LICENSE).
