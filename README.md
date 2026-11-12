# استوديو سينما فلو الذكي — CineFlow AI Studio 🎬 (`v8.0.0`)

**الإصدار `8.0.0` (`Unified Production Agent, Google Flow Omni 1.2 Native, Multi-NLE Exporters & On-Demand Tool Factory`)** — الوكيل الشامل لإنتاج الفيديوهات السينمائية والإعلانية والقصيرة، وإخراج مشاريع **[Google Flow](https://flow.google.com/)** (`Gemini Omni 1.2 Flash • Nano Banana Pro • Veo 3.1 • Seedance 2.0 • Runway Gen-4 • Kling 3.0 • Hailuo Director • Wan VACE • Higgsfield DoP • MagicLight.AI`) عبر **14 مساراً إنتاجياً ذاتياً (`route_1..route_14`)**، ومصدّرات التايم لاين والمشاريع لبرامج المونتاج الاحترافية (`CapCut • Premiere Pro / FCPXML • CMX 3600 EDL • DaVinci Resolve 7-Node DWG • After Effects .jsx • Blender AgX • Remotion v4.0.539 • HyperFrames check • ManimCE AST-Verified • FFmpeg Zero-Loss`)، مع **مصنع أدوات المونتاج الفوري (`on_demand_tool_synthesizer.py`)** الذي يكتشف غياب أي برنامج تحرير ويبني أدوات المونتاج والمؤثرات الصوتية والتايم لاين التفاعلي في المتصفح لحظياً.

> 📖 **الدستور الكامل والمعمارية التفصيلية:** راجع [`SKILL.md`](SKILL.md) و[`references/13-on-demand-tool-synthesis-and-nle-automation.md`](references/13-on-demand-tool-synthesis-and-nle-automation.md) و[`references/09-google-flow-agent-scenes-and-tools-mastery.md`](references/09-google-flow-agent-scenes-and-tools-mastery.md) و[`references/10-google-flow-cli-scripting-and-automation-mastery.md`](references/10-google-flow-cli-scripting-and-automation-mastery.md) و[`references/architecture-and-pipelines.md`](references/architecture-and-pipelines.md) و[`references/b-studio-and-video-edit-mastery.md`](references/b-studio-and-video-edit-mastery.md) و[`references/11-22-tool-video-ecosystem-and-nle-mastery.md`](references/11-22-tool-video-ecosystem-and-nle-mastery.md) و[`references/12-human-cultural-dialects-and-media-psychology.md`](references/12-human-cultural-dialects-and-media-psychology.md).

---

## 1. التثبيت السريع (Installation & Setup)

```bash
# تثبيت المهارة وتسجيل خادم MCP
bash mcp/project-setup.sh --global

# تثبيت مكتبات التشغيل والاختبار الاختيارية
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## 2. التشغيل البرمجي السريع عبر سطر الأوامر (Quickstart CLI)

```bash
# 1. فحص البيئة والأدوات المتاحة (Rule Zero Probe) وحساب شبكة النبض (120 BPM)
python scripts/post_production_engine.py probe
python scripts/beat_grid.py --bpm 120 --time-signature 4/4 --fps 30 --duration 15 --pattern build_up

# 2. تجميع مخطط إنتاج متكامل وتدقيقه وحساب الأرصدة وتوليد ملف الترجمة (.srt)
python scripts/cineflow_compiler.py \
  --idea "إعلان عطر شرقي فاخر في صحراء ذهبية وقت الغروب /dollyin /warmgold /ar 9:16" \
  --purpose "Commercials & TVCs" \
  --format "Live-Action" \
  --style-variant "Commercial Promo" \
  --dialogue "عبيرٌ يَروي حِكايةَ الفَخامةِ الأصيلةِ في كُلِّ لَحظة." \
  --runtime 16 \
  --output examples/generated_perfume_ad.json
python scripts/validate_package.py examples/example_03_showrunner_package.json
python scripts/estimate_cost.py examples/example_03_showrunner_package.json 10 1
python scripts/make_srt.py examples/example_03_showrunner_package.json examples/out_subtitles.srt
python scripts/lint_package.py check examples/example_03_showrunner_package.json

# 3. تصدير المشاريع القابلة للتعديل لجميع برامج المونتاج (CapCut, FCPXML, EDL, Resolve, AE, Blender)
python scripts/nle_project_exporters.py export-all examples/example_03_showrunner_package.json --output studio/nle_exports

# 4. صناعة أدوات المونتاج الفورية عند عدم توفر البرامج (Browser NLE Studio / FFmpeg / 48kHz SFX / Manim / HyperFrames)
python scripts/on_demand_tool_synthesizer.py synthesize browser_nle_studio --output-dir studio/browser_nle --package examples/example_03_showrunner_package.json
python scripts/on_demand_tool_synthesizer.py synthesize procedural_sfx_pack --output-dir studio/sfx

# 5. تشغيل فحص المراجع والاختبارات الآلية الشاملة
python scripts/verify_skill_references.py
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## 3. هيكل ملفات المستودع (Repository Structure)

```text
cineflow-ai-studio/
├── SKILL.md                                     # الدستور الرئيسي للمهارة (name: cineflow-ai-studio — v8.0.0)
├── README.md                                    # المدخل السريع للتثبيت والاستخدام
├── CHANGELOG.md                                 # سجل تغييرات الإصدارات
├── LICENSE                                      # رخصة Apache-2.0
├── pyproject.toml                               # إعدادات المشروع الموحدة
├── templates/
│   ├── package.template.json                    # قالب حزمة الإنتاج القياسي (06_package.json)
│   └── flow_agent_project_init.template.json    # قالب تهيئة وكيل Google Flow بصيغة JSON
├── mcp/
│   ├── server.py                                # خادم FastMCP بـ 8 أدوات لتوليد وتعديل الفيديو عبر Gemini Omni 1.2
│   ├── requirements.txt                         # متطلبات خادم FastMCP
│   └── project-setup.sh                         # سكربت تثبيت المهارة وتسجيل الخادم
├── scripts/
│   ├── studio_config.py                         # المصدر الموحد للثوابت وسجل النماذج والـ 14 مساراً والماكروهات البصرية
│   ├── arabic_helpers.py                        # اللهجات الـ 12، الكشيدة خلف الرأس (headGap)، ترقيع الرقعة (ZWJ)، وباني أوامر Omni 1.2
│   ├── governance_and_omni.py                   # الحوكمة، باني حمولات Omni الحفظية، ومطهر أوامر Google Flow
│   ├── cineflow_compiler.py                     # المترجم الرئيسي لمخططات الإنتاج (JSON Blueprint Compiler)
│   ├── beat_grid.py                             # حاسبة شبكة النبض الموسيقي وخريطة القطع والـ Speed Ramps
│   ├── post_production_engine.py                # محرك ما بعد الإنتاج: فحص الميديا، قص الصمت ثلاثي الأوضاع، SFX 48kHz، والمعايرة المزدوجة (-20/-14 LUFS)
│   ├── nle_project_exporters.py                 # مصدّر التايم لاين لبرامج CapCut وPremiere/FCPXML وEDL وDaVinci Resolve وAfter Effects وBlender
│   ├── on_demand_tool_synthesizer.py            # مصنع أدوات المونتاج الفوري، التايم لاين غير التدميري، فاحص أمان AST، وبوابة وصلات HyperFrames
│   ├── multi_agent_orchestrator.py              # منسق الوكلاء السبعة والـ 13 دوراً + مدقق الصوتيات الإذاعية
│   ├── validate_package.py                      # مدقق الحزم القياسي
│   ├── estimate_cost.py                         # حاسبة الأرصدة قبل GATE 2
│   ├── make_srt.py                              # مولد ملفات الترجمة العربية (.srt)
│   ├── lint_package.py                          # واجهة سطر الأوامر الموحدة: check / sanitize / storyboard / tool-payload / cultural-audit / export-nle / synthesize-tool / validate-seams
│   ├── verify_skill_references.py               # مدقق الروابط والمراجع الديناميكي للـ CI
│   ├── sync_remotion_skills.py                  # أداة تحديث وتوثيق مراجع Remotion الرسمية
│   └── Compile-CineFlowBlueprint.ps1            # غلاف PowerShell
├── references/
│   ├── 13-on-demand-tool-synthesis-and-nle-automation.md # دليل مصنع الأدوات الفوري ومصدرات NLE وبوابة HyperFrames ومحركات الصوت واللون
│   ├── 01-team-and-roles.md .. 12-human-cultural-dialects-and-media-psychology.md
│   ├── architecture-and-pipelines.md .. taxonomy.md
│   └── remotion_skills_official/                # مكتبة قواعد Remotion v4.0.539 المرجعية الرسمية (مع UPSTREAM_ATTRIBUTION.md)
├── resources/ & evals/ & examples/              # مخططات JSON Schema وحالات التقييم والأمثلة القياسية
└── tests/
    ├── test_cineflow_compiler.py
    ├── test_montage.py
    ├── test_omni_agent.py
    ├── test_lint_package.py
    └── test_post_and_tool_factory.py            # اختبارات محركات v8.0.0 ومصدرات NLE ومصنع الأدوات الفوري
```

---

## 4. نسب المصادر الخارجية والترخيص (External Attribution & License)

- **مكتبة قواعد Remotion الرسمية ([`references/remotion_skills_official/`](references/remotion_skills_official/UPSTREAM_ATTRIBUTION.md)):** منسوخة من [`remotion-dev/remotion`](https://github.com/remotion-dev/remotion/tree/v4.0.539/packages/skills/skills/remotion) (`v4.0.539`).
- **ترخيص المستودع:** مرخص بموجب رخصة [**Apache License 2.0**](LICENSE).
