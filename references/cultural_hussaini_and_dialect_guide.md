# Specialized Cultural & Heritage Audio-Visuals (Husayni Elegies), Arabic Dialect Lock & Lip-Sync Reference

This reference manual governs **Specialized Cultural & Heritage Productions (`المراثي والقصائد الحسينية — Husayni Elegies / Latmiyat`)**, **Arabic & Gulf Dialect Locks (`قفل اللهجات العربية والخليجية`)**, **Neural Lip-Sync Phrasing (`مزامنة الشفاه العصبية`)**, and **Safe-Zone Outro Standardization (`مشهد النهاية المعياري`)** in **CineFlow AI Studio**.

---

## 1. Husayni Elegies & Latmiyat Audio-Visual Engine (`منظومة الإنتاج البصري والصوتي للمراثي والقصائد الحسينية`)

When the user inputs a Husayni poem (`قصيدة حسينية، لطمية، نعي، موال، أبوذية، شور، زنجيل، بندري`) or requests a mourning/heritage visual production:

### 1.1 Melodic, Maqam & Poetic Meter Alignment (`ضبط الأطوار والمقامات وبحر القصيدة`)
Lock the emotional tone to authentic sorrowful, reverent, or epic mourning meters while granting creative flexibility in rhythmic and vocal foley distribution:
- **Poetic Meters (`البحور الشعرية الحسينية`)**:
  - **بحر النصاري (`Bahr Al-Nassari`)**: Deep weeping, `Na'i`, `Muhammarawi`, and `Bahrani Faizi` (`56–58 BPM` or `0 BPM Rubato`).
  - **بحر الموشح (`Bahr Al-Muwashah`)**: Solemn, stately `Iraqi Nazla` (`58–62 BPM`) and `Bahrani Modern Tawshih` (`66–76 BPM`).
  - **البحر الطويل / الفايزي (`Bahr Al-Fayzi`)**: Wide emotional expanses for `Lisan Al-Hal` narratives.
  - **بحر التجليب / الگعدية والميمر (`Bahr Al-Tajleeb & Al-Maymar`)**: Rising rhythmic momentum (`68–76 BPM`).
  - **الزنجيل الموكبي والبندري (`Zanjeel & Bandari`)**: Steady processional march (`76–84 BPM`) or active synchronized strike (`100–110 BPM`).
  - **الشور الحسيني (`Karbalaei Shoor`)**: High-intensity chest-slap surge (`125–140 BPM`).
- **Primary Maqam-to-Visual Mood Mapping**:
  - **مقام الصبا (`Maqam Saba`)**: Acute grief and tragedy ➔ Visual palette: **Desaturated Ash & Deep Crimson (`#8B0000`)**, heavy chiaroscuro shadows, slow grieving camera push-ins (`/slowpush`, `/lowkey`, `/chiaroscuro`), tearful micro-expressions, dust motes in single light shafts.
  - **مقام البياتي (`Maqam Bayati`)**: Grounded, authentic mourning assembly (`Matam / Husseiniya`) ➔ Visual palette: **Warm Candlelight Amber & Deep Charcoal**, synchronous congregation chest-slap (`Latm`) ripples, overhead geometric architectural framing.
  - **مقام الحجاز (`Maqam Hijaz`)**: Distant calling (`النداء والاستغاثة`) and epic processions ➔ Visual palette: **Golden-Hour Desert Ochre & Night Indigo**, fluttering black silk banners in the wind (`/wind`, `/slowmotion`), dramatic low-angle tracking shots (`/lowangle`, `/track`).
  - **مقام اللامي (`Maqam Lami`)**: Estrangement, orphanhood, and desert solitude (`الغربة والوحشة`) ➔ Visual palette: **Moonlit Silver-Blue & Deep Obsidian**, wide lonely desert horizons (`/extremewide`, `/moonlight`, `/fog`), footprints fading in blowing sand.
  - **مقام الكرد والنهاوند (`Maqam Kurd / Nahawand`)**: Flowing emotional elegies and youth martyrdom ➔ Visual palette: **Soft Volumetric Light Rays (`/godrays`) & Warm Sepia Contrast**, slow orbital camera motion (`/sloworbit`, `/85mm`, `/bokeh`).

### 1.2 Frame-Accurate Visual-Rhythmic Synchronization (`مزامنة اللقطات واللطم الإيقاعي مع النبض الصوتي الصاعد والهابط`)
Every Husayni visual scene breakdown MUST synchronize camera motion, visual cuts, and physical action with the **4-Stage Vocal Register Arc (`قوس الطبقات الصوتية`)**:

| Vocal Stage (`المرحلة الصوتية`) | Vocal Register & Pulse | Visual Pacing, Camera & Cut Synchronization | Audio & Foley Sync (`audio_foley_sync`) |
| :--- | :--- | :--- | :--- |
| **1. المستهل (`Mustahal — Opening`)** | **القرار (`Qarar`)**: Deep, calm, velvety chest voice | **Measured Establishing Shots (`5–8s`)**: Slow camera dolly-in or crane descent (`/slowpush`, `/35mm`), minimal subject motion, atmospheric particles (incense smoke, candle flicker, gentle wind on banner). Cut every **4 beats**. | Soft room tone, subtle `Ahaat` harmonic pad (`-18dB`), gentle opening `55Hz` bare-palm chest thud on Beat 1, `285ms` analog tape echo. |
| **2. المقطع الأول (`Stanza 1 — Rising Grief`)** | **الوسط / الجواب الأول (`Mayan / Jawab`)**: Rising sorrow & natural vocal rasp | **Medium & Close-Up Narrative Coverage (`4–6s`)**: Slow orbital tracking (`/orbitright`, `/85mm`), expressive grief body language (bowed head, hand over chest, trembling eyelids). Cut every **2 to 4 beats** with `J-Cut` audio lead (`0.20s`). | Rhythmic `55Hz` chest-slap locked to poetic meter (`60–68 BPM`), unison male `Raddada` response, `-3.0 dB` smart sidechain ducking under lead vocal. |
| **3. ذروة الشجن (`Climax — Jawab Al-Jawab`)** | **جواب الجواب (`High Chest-Voice Peak`)**: Powerful emotional cry & climax | **Dynamic Speed-Ramped Visual Peak (`3–5s`)**: Curved speed ramp (`1.75x` fast entry ➔ `0.55x` slow-motion impact exactly on the chest-slap/Dammam strike ➔ `1.65x` exit), dramatic camera push or crane rise (`/craneup`, `/godrays`, `/sparks` or `/rain`). Cut every **2 beats** on the rhythmic strike. | Full congregation `Latm` surge + deep `Dammam` / sub-bass thud (`55Hz–90Hz`) + `3.2s` Husseiniya hall reverb tail (`sfx_climax_boom.wav` on beat drop). |
| **4. القفلة والنعي (`Qafla / Na'i — Resolution`)** | **العودة للقرار والوقف بالسكون (`Sudden Drop to Qarar`)** | **Contemplative Pull-Back (`5–8s`, `0 BPM Rubato`)**: Slow dolly-out (`/dollyout`) to silhouette or lone flickering lantern fading into darkness, leaving clean vertical safe-zone space for poem title/calligraphy. | Sudden rhythmic drop to zero percussion (`Pure Solo Acapella`), `450ms` tape delay tail decaying into reverent silence. |

### 1.3 Sacred & Cultural Visual Guardrails (`الضوابط الشرعية والثقافية الصارمة للمشاهد الحسينية`)
- **Identity-Safe Reverence**: Never generate direct facial depictions of infallible holy figures (`المعصومين وأهل البيت ع`). Always use **Identity-Safe Symbolic Cinematography**:
  - Backlit silhouettes (`/silhouette`, `/backlight`) or radiant light halos obscuring facial features.
  - Over-the-shoulder (`OTS`), macro detail shots of hands, prayer beads (`سبحة تربة`), cloaks (`عباءة`), swords, water skins (`قربة الماء`), arrows in sand, or empty saddles.
  - Contemporary mourning visuals: Authentic Radood on the Minbar, black-clad mourning congregation (`موكب عزاء`) in candlelight, traditional Bahraini/Iraqi Matam architecture, and Arabic Kufi calligraphy overlays.

---

## 2. Arabic Dialect Lock & Neural Lip-Sync Optimization (`قفل اللهجة ومزامنة الشفاه المتقدمة`)

### 2.1 Autonomous Dialect Detection & Lexicon Matrix
Detect the user's dialect automatically from their prompt or dialogue and lock it across all scenes:

| Dialect Code | Regional Identity | Authentic Lexical & Phonetic Markers (Examples) |
| :--- | :--- | :--- |
| **`BAHRAINI_KHALEEJI`** | البحرينية (المدنية والبحرانية الأصيلة) | `ويش فيك، شحالك، الحين، جذي، عفر، يا خويي، يا بويي، امساعد الله، هالگفرة، ما عليه` |
| **`SAUDI_KHALEEJI`** | السعودية (النجدية والحجازية والخليجية) | `وش دعوة، وش رايك، الحين، مرّة، زي كذا، يا طويل العمر، أبشر، لا تشيل هم، كيف الحال` |
| **`KUWAITI_GULF` / `EMIRATI` / `OMANI`** | الكويتية / الإماراتية / العمانية | `شنو هذا، شدعوة، صج، وايد، يبه` (كويتي) / `شحالك، رمسة، وايد، هيه، ما يقصر` (إماراتي) |
| **`IRAQI`** | العراقية (البغدادية، الكربلائية، الفراتية) | `شلونك، شكو ماكو، هسه، كلش، آني، يا خويه، يا بويه، يمه، گلب، چبد، إش صار، بلياك` |
| **`MSA`** | العربية الفصحى العصرية الرشيقة | لغة إعلامية ووثائقية جزلة، واضحة المخارج، مضبوطة أواخر الكلمات بالسكون عند الوقف |

### 2.2 Neural Lip-Sync & Arabic Phrasing Engineering (`هندسة الجمل العربية لمزامنة الشفاه الواقعية`)
To enable Google Flow / Veo 3.1's Lip-Sync engine to close the mouth naturally and match facial micro-expressions with zero robotic jaw-flapping:
1. **The `2.5 Words/Second` Ceiling (`قاعدة التزامن الصوتي الصارمة`)**:
   $$\text{Max Arabic Words per Scene} \le \lfloor \text{Duration\_Seconds} \times 2.5 \rfloor$$
   - For a `4s` shot: **Max 8–10 words**.
   - For a `6s` shot: **Max 12–15 words**.
2. **Short Breath-Paced Clauses (`تقسيم الحوار إلى جمل قصيرة تفصلها وقفات تنفس طبيعية`)**:
   - Break every dialogue line into **short bursts of 3 to 5 words**, separated by explicit pause markers (`.. [0.3s breath pause]`).
3. **Labial Closure Anchors (`قفل إغلاق الشفاه`)**:
   - Prompt the visual performance with explicit lip-closure cues at each pause: `"delivers short Arabic phrase with crisp lip-sync articulation, naturally closing lips during the 0.3s breath pause with a subtle nod and eye blink"`.
4. **Verbatim Script Law (`قانون النص الحرفي`)**:
   - Never translate, paraphrase, or "correct" user-supplied Gulf/Bahraini/Saudi/Iraqi dialect into Modern Standard Arabic (`MSA`). Pass the exact Arabic string into `dialogue_lip_sync`.

---

## 3. Text Integrity & Outro Standardization (`سلامة النصوص ومشهد النهاية المعياري`)

### 3.1 Text & Arabic Typo Integrity (`سلامة النصوص العربية ومنع التشوه`)
- **Diegetic vs. Non-Diegetic Separation**:
  - **Diegetic Text (Inside the AI Video)**: Keep embedded Arabic text on products, storefronts, or packaging **locked via `<IMAGE_REF_0>` (`Lock [Product ID]`)** or restricted to **1–2 ultra-clear words**. Always append `negative_guardrails: "no garbled Arabic letters, no disconnected Arabic script, no floating random text, no distorted logo typography"`.
  - **Non-Diegetic Text (`text_overlay` — Titles, Subtitles, Prices, CTAs)**: Output the exact, grammatically verified, vocalized Arabic string in `text_overlay` to be rendered cleanly in post-production using connected RTL Arabic fonts (**Cairo Black, Tajawal Bold, Noto Kufi Arabic**).

### 3.2 Standardized Outro & Platform Safe Zones (`إطار الخاتمة المعياري والمناطق الآمنة`)
Every final scene (`Scene N — Outro / CTA`) in vertical (`9:16` — `1080x1920`) or horizontal (`16:9` — `1920x1080`) format MUST allocate a clean, uncluttered visual zone so branding and CTAs never collide with faces or platform UI buttons:

- **Vertical `9:16` (`1080x1920`) Outro Layout**:
  - **Top Dead Zone (`Y: 0..250`)**: Reserved for TikTok/Reels/Shorts top bar (keep clear).
  - **Brand Logo & Tagline Zone (`Y: 420..820`, `X: 120..960`)**: Upper-center clean negative space.
  - **Primary CTA & Social Handles Zone (`Y: 950..1280`, `X: 120..900`)**: Lower-middle safe zone above platform captions and left of the right-hand engagement icons (`X: 910..1080`).
  - **Bottom Dead Zone (`Y: 1400..1920`)**: Reserved for platform account name, caption marquee, and progress bar (keep clear).
  - **Visual Loop-Back Rule**: Compose the final 2 seconds of the Outro so its lighting, camera vector, or subject framing visually echoes `Scene 1 (0.0s)` for seamless algorithmic replay.
