# 12 — Human-Level Arabic Dialectology, Cultural Anthropology, Social Etiquette & Media/Advertising Psychology

This reference equips the agent with human-level linguistic intuition, Arab/Gulf cultural and social etiquette (`الأعراف المجتمعية`), visual wardrobe/prop accuracy, and behavioral media/advertising psychology so every script, visual prompt, and edit feels authored by a seasoned native creative director.

---

## Part 1 — Deep Arabic Dialectology & Sociolinguistic Matrix (`12` Dialects)

Never mix lexical markers from different regions inside a single character's speech (e.g., never put Egyptian `دلوقتي` or Levantine `هلق` inside a Saudi Najdi or Bahraini speaker's mouth), and never translate English idioms literally (`"حرفياً هذا يغير اللعبة"` -> replace with natural native phrasing like `"هالشي يفرق معك من أول تجربة"`).

| Dialect Code | Region | Key Phonological Shifts & Prosody | Authentic Everyday Connectors & Idioms | Anti-Cringe / Forbidden Mixes |
| :--- | :--- | :--- | :--- | :--- |
| **`SAUDI_NAJDI`** | Riyadh, Qassim, Central KSA | `ق -> گ` (`قال -> گال`), `ك -> تس/چ` in select feminine suffixes; measured, confident cadence | `وش رايك، وش دعوة، أبشر، لا تشيل هم، توّنا، الصدق، يبي لها، على هالخشم` | Do not mix Hijazi `دحين / مرّة` or Kuwaiti `وايد / معود`. |
| **`SAUDI_HIJAZI`** | Jeddah, Makkah, Madinah | `ق -> گ` (or `أ` in select urban words), `ث -> ت / س`, melodic urban rhythm | `دحين، إيش تبغى، مرّة، عشان، سيبك، يا سيدي، على طول، من جد` | Do not mix Najdi `وش دعوة` or Eastern `چيف`. |
| **`SAUDI_SHARQAWI`** | Dammam, Khobar, Al-Ahsa, Qatif | Warm coastal cadence; shares Gulf `ج -> ي` (`ريال` for `رجال`) in traditional speech | `الحين، شخبارك، ما قصرت، يبيله، خوش، عساك على القوة` | Keep distinct from inland Najdi or western Hijazi. |
| **`BAHRAIN_URBAN`** | Manama, Muharraq, Riffa | Warm, hospitable island prosody; `ق -> گ` (`گعد`), `ج -> ي` in select words | `شحالك، شخبارك، الحين، جذي، يا خويي، ما عليه، يبيله، كلش، عفر` | Never overwrite `ويش / جذي / الحين` into stiff MSA. |
| **`KUWAITI`** | Kuwait City | Expressive, fast-paced theatrical & conversational cadence; `ك -> چ` (`چذي`), `ج -> ي` (`ياي`) | `شنو هذا، شدعوة، صج، وايد، يا معود، يبه، اشلونك، خوش، تو الناس` | Do not replace `وايد` with `مرّة` or `كثير`. |
| **`QATARI`** | Doha | Dignified, calm Gulf cadence; `ق -> گ`, `ج -> ي` | `شخبارك، الحين، ما عليك زود، يبيله، صج، كفو، لبيه` | Avoid non-Gulf fillers. |
| **`EMIRATI`** | Abu Dhabi, Dubai, Sharjah (`الرمسة`) | Distinct `ج -> ي` (`مسيد، يديد، ريال`), `ك -> چ` (`چيف حالك`) | `اشحالك، هيه، ما يقصر، غاوي، طارش، يا ريال، فالك طيب، مرحبا الساع` | Never use `أيوة` instead of Emirati `هيه`. |
| **`OMANI`** | Muscat, Nizwa, Salalah | Clear, courteous cadence; retains `ق` or `گ` by region, distinctive intonation | `كيف الحال، مو الأخبار، ما شاء الله، تمام، حياك، أحسنت` | Respect Omani dress (`الدشداشة العمانية والكمّة أو المصر`) in visuals. |
| **`IRAQI`** | Baghdad, Basra | Rich Mesopotamian rhythm; `ق -> گ` (`گلب`), `ك -> چ` (`چبير`) | `شلونك، شكو ماكو، هسه، كلش، آني، عاشت إيدك، تدلل، يمعود` | Never mix Gulf `الحين` with Iraqi `هسه`. |
| **`LEVANTINE`** | Damascus, Beirut, Amman, Jerusalem | Soft urban flow; `ق -> ء` (urban Damascus/Beirut) or `گ` (rural/Jordanian) | `شو رأيك، هلأ، كتير، كرمال، عنجد، ولا يهمك، تكرم عينك، يعطيك العافية` | Keep Syrian, Lebanese, and Jordanian nuances consistent per speaker. |
| **`EGYPTIAN`** | Cairo, Alexandria | High-wit, rhythmic, punchy delivery; `ج -> g` (hard `G`), `ق -> ء` | `إزيك، دلوقتي، كده، أوي، عشان، مفيش مشكلة، يا باشا، بص بقى` | Never pronounce `ج` as soft `J` in Cairo dialect TTS. |
| **`MAGHREBI`** | Casablanca, Algiers, Tunis | Fast consonant-clustered rhythm; for pan-Arab reach use **White Darija (`الدارجة البيضاء`)** | `كيداير، دابا، بزاف، برشا، واش، مزيان، على خاطر، مرحبا بيك` | Avoid heavy local slang when targeting GCC audiences; use clear White Darija. |

---

## Part 2 — Cultural Anthropology, Social Etiquette & Visual Semiotics (`الأعراف المجتمعية والرمزية البصرية`)

Generative video models frequently commit cultural blunders unless explicitly constrained in the visual prompt. Enforce these **6 Cultural Authenticity Laws (`audit_cultural_and_dialect_authenticity`)**:

1. **The Arabic Coffee (`القهوة العربية / السعودية`) & Majlis Hand Etiquette Law**:
   - **Hard Cultural Rule**: The host **always holds the `Dallah` (`الدلة`) in the LEFT hand** and **presents/receives the `Finjan` (`الفنجان`) with the RIGHT hand** (`Dallah in left hand, Finjan offered with right hand`). Offering a `Finjan` or food with the left hand is a severe social faux pas in Arab/Islamic culture.
   - **Cup Fill Level**: An authentic Arabic `Finjan` is poured to **one-third full (`bottom third of the finjan`)** — filling it to the brim signals "drink and leave", whereas a small pour honors the guest with repeated fresh pours.
2. **Right-Hand Protocol (`تيامُن — أخذ وعطاء وأكل باليمين`)**:
   - All eating, drinking, shaking hands, handing over gifts/products, and greeting gestures must explicitly specify `with his/her right hand` in the English visual prompt so the video model does not default to a left-handed gesture.
3. **Regional Gulf & Arab Wardrobe Precision (`دقة الهوية البصرية للأزياء`)**:
   - **Saudi**: Crisp white `Thobe` (`ثوب سعودي بياقة قلاب أو سادة`), red-and-white `Shemagh` (`شماغ`) or white `Ghutra` (`غترة`) held by a black double-cord `Iqal` (`عقال أسود`).
   - **Emirati**: Collarless `Kandura` (`كندورة إماراتية بدون ياقة`) with dangling tassel (`فرخة / طربوشة`) and `Ghutra` tied in `Hamdaniya / Asama` (`عصامة`) or with `Iqal`.
   - **Omani**: Collarless `Dishdasha` with asymmetrical tassel (`فراخة`) and embroidered `Kuma` (`كمّة عمانية`) or folded `Mussar` (`مصر عماني`).
   - **Bahraini / Kuwaiti / Qatari**: Tailored `Thobe / Dishdasha` with classic `Ghutra` and `Iqal` (with subtle regional collar and drape differences).
4. **Intergenerational Respect (`توقير الكبير وبر الوالدين`)**:
   - Younger characters stand when an elder enters, pour coffee for the elder first, kiss the forehead/head of parents (`يقبل رأس والده/والدته`), and never sit with the soles of their shoes pointing toward another person in the Majlis (`never show shoe soles facing guests`).
5. **Modesty & Family Context (`الحشمة والذوق العام`)**:
   - Ensure wardrobe, physical interactions, and background settings respect local cultural norms (no clinking glasses in toast gestures that mimic alcohol toasts in family/GCC commercials, no inappropriate background props).
6. **Seasonal & Cultural Moment Anchors**:
   - **Ramadan (`رمضان`)**: Warm lantern/sunset `Iftar` table anticipation, spiritual calm, generosity, family gathering around dates and coffee.
   - **Eid (`العيد`)**: Crisp morning `Bakhoor` (`بخور وعود`), `Eidiya` (`العيدية`), joyful greetings (`عساكم من عواده / عيدكم مبارك`).
   - **Winter / Kashta (`موسم الشتاء والكشتة`)**: Desert dunes at twilight, glowing `Samar` firewood (`شبة النار`), wool `Farwa` or `Bisht`, steaming tea on embers.

---

## Part 3 — Business, Media, Advertising & Neuro-Cinematic Psychology (`عبقرية الإعلام والإعلان والتسويق`)

### 3.1 Eugene Schwartz's 5 Stages of Market Awareness -> Video Hook Mapping
Match the first `3.0 seconds` of every video to the audience's exact awareness stage:
1. **`Unaware` (لا يعلم بوجود المشكلة)**: Open with a **relatable human story, visceral emotion, or surprising cultural observation** — never open with a product name or price.
2. **`Problem-Aware` (يشعر بالمشكلة ولا يعرف الحل)**: Open by **naming and visualizing the exact frustration** (`pain_point` hook) in the first `1.5s`.
3. **`Solution-Aware` (يعرف الحلول العامة ولا يعرف منتجك)**: Open with a **contrarian mechanism comparison** (`contrarian` / `visual_payoff` hook) showing *why* standard options fail and how your mechanism works physically.
4. **`Product-Aware` (يعرف منتجك ومتردد)**: Open with **tangible social proof, objection busting, or a side-by-side stress test** (`authority` hook).
5. **`Most Aware` (جاهز للشراء وينتظر العرض)**: Open directly with the **hero product, limited-time offer, and frictionless CTA**.

### 3.2 Kahneman System 1 / System 2 & Visual Cognitive Ease
- **System 1 (Fast, Intuitive, Emotional — `0.0s–3.0s`)**: Processes faces, eye direction, physical motion, high-contrast color, and concrete sensory actions (`pouring espresso crema`, `slicing crisp crust`) in `< 200ms`.
- **System 2 (Slow, Analytical, Logical — `3.0s–12.0s`)**: Activates only after System 1 is hooked. Feed System 2 **one concrete number or mechanism per card** (`<= 6 words` on screen, `>= 84px` headline) while keeping visual motion alive.
- **The Concrete Noun Law**: Replace abstract marketing adjectives (`"منتج مبتكر بجودة استثنائية"`) with tangible sensory proof (`"قهوة محمصة اليوم على حطب السمر، توصلك خلال 24 ساعة"`).

### 3.3 Binet & Field Dual-Engine Advertising Law + Cialdini's 6 Triggers
- **Brand Building (`60%` Emotional Memory)**: Uses human warmth, humor, cultural belonging, and distinctive brand assets (sonic logo, signature color palette, recurring character).
- **Sales Activation (`40%` Immediate Response)**: Uses clear problem-solution demonstration, **Social Proof** (`الكل يسأل عنه`), **Authority** (`خبرة 20 سنة`), **Scarcity/Urgency** (`الكمية محدودة لهالموسم`), and **Risk Reversal** (`ضمان استرجاع كامل`).

### 3.4 2026 Social Platform Retention Engineering (`TikTok / Reels / Shorts / Snap / LinkedIn`)
- **`0.0s–1.5s` (`Scroll-Stop Gate`)**: Must combine **(a) physical camera/subject movement**, **(b) a 3–4 word high-contrast Arabic hook headline**, and **(c) an immediate spoken curiosity gap** (zero throat-clearing, zero `"السلام عليكم معكم فلان في هذا الفيديو سنتحدث عن..."`).
- **`3.0s` (`Hold Rate Gate >= 65%`)**: First visual cut or camera angle shift happens between `1.8s` and `2.8s`.
- **`50%` Midpoint (`Re-Hook Gate`)**: Introduce a pattern interrupt ("والأهم من هذا كله..." + window state shift `FULL -> CARD` or B-Roll mechanism reveal) to prevent mid-video swipe-away.
- **Final `1.5s` (`Seamless Loop Gate`)**: Match the outgoing camera framing and ambient tone to Frame 0, or end the spoken sentence so it grammatically bridges back into the first word of the hook (`100%+` replay loop).
