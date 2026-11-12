# 10 — Google Flow CLI, Scripting v1.6.0, Omni Flash UGC & Browser Automation Mastery

This reference synthesizes the engineering contracts, mechanical script validators, storyboard contact-sheet generators, DOM/CDP automation selectors, credit economics, and 6-step checkpointed UGC pipelines from four specialized Google Flow repositories:
1. **`google-flow-scripting-skill` (`v1.6.0`)** — Continuity Auditor, Storyboard Director, Surface × Model × Mode × Duration Matrix, and 30-Row Failure Modes Table.
2. **`google-flow-cli`** — Zero-Bot-Flag Chrome CDP (`port 9222`), 5-Stage Agent Lifecycle, Angular CDK & ProseMirror DOM Selector Map, and Declarative `flow.json` Chained-Keyframe Pipelines.
3. **`google-flow-api` (`omni-flash-video` & `ugc-product-video`)** — Exact Credit Economics (`360p` vs `720p` + Free `1080p` Upscale), Physical-Action-First Prompting, Voice-Needs-a-Face Contract, and the 6-Step Checkpointed UGC Product Video Pipeline.
4. **`Google-Flow-Automation`** — React/HTMLInputElement Native Prototype Value/File Setters, Stem-Based Asset Matching (`matchAssets`), and Queue Error Classification (`Policy Error` vs `Server Busy`).

---

## Part 1 — Mechanical Script Validation & Continuity Engineering (`google-flow-scripting v1.6.0`)

### 1.1 Surface × Model × Mode × Duration Matrix (`MODE_DURATIONS`)
Every video segment must declare a valid `(surface, model, mode, duration_s)` tuple enforced by `lint_flow_continuity_and_platform_profile()` in [`scripts/governance_and_omni.py`](../scripts/governance_and_omni.py):

| Surface | Model | Supported Modes & Allowed Durations (`seconds`) | Key Operational Notes |
| :--- | :--- | :--- | :--- |
| **`flow`** | **`veo-3.1-lite`** | `text-to-video`: `{4, 6, 8}`<br>`first-frame`: `{4, 6, 8}`<br>`first-last-frame`: `{4, 6, 8}`<br>`references-to-video`: `{8}`<br>`extend`: `{8}` | Cheapest Veo tier; Flow routes **Extend** operations through Veo 3.1 Lite (`+8s`). |
| **`flow`** | **`veo-3.1-fast`** | `text-to-video`: `{4, 6, 8}`<br>`first-frame`: `{4, 6, 8}`<br>`first-last-frame`: `{4, 6, 8}`<br>`references-to-video`: `{8}` | Best balance of speed and motion quality on Veo (`10 credits` on Ultra, `20 credits` on Pro). |
| **`flow`** | **`veo-3.1-quality`** | `text-to-video`: `{8}`<br>`first-frame`: `{8}`<br>`first-last-frame`: `{8}` | Highest realism; `8s` only (`references-to-video` is **not** supported on Quality). |
| **`flow`** | **`omni-1.2-flash` / `gemini-omni-1.2-flash`** | `text-to-video`: `{3..15}` (`1s` increments)<br>`first-frame`: `{3..15}`<br>`references-to-video`: `{3..15}`<br>`video-edit`: `{3..15}` (`0 credits`)<br>`first-last-frame`: `{3..10}`<br>`extend`: `{3..10}` | **Default Google Flow Engine (`macaron_cookie`, `$0.07/s` at `720p`, `30%` cheaper than Omni 1.1)**. Native `3–15s` slider, Multi-Speaker Conditioning (`4+` characters with `1s` voice references), front/back + `3s` motion clips, `0-credit` Multi-Turn Conversational Editing & Motion Transfer, unbroken FPV/crash-zoom/360-orbit camera paths. |
| **`flow`** | **`omni-flash`** | `text-to-video`: `{3..15}`<br>`first-frame`: `{3..15}`<br>`first-last-frame`: `{3..15}`<br>`references-to-video`: `{3..15}`<br>`video-edit`: `{3..15}` | Generic alias mapping to `Omni 1.2 Flash` (`3–15s`) for standard modes (`Omni 1.1 Flash` / `abra` remains selectable for legacy `4/6/8/10s` workflows). |
| **`gemini-api`** | **`veo-3.1-lite`** / **`fast`** | `text-to-video`, `first-frame`, `first-last-frame`: `{4, 6, 8}`<br>`references-to-video` (`fast` only): `{8}`<br>`extend`: `{7}` | API Extend adds `7s` (up to `20` hops, `148s` ceiling) at `720p`. |
| **`gemini-api`** | **`omni-1.2-flash` / `omni-flash`** | `text-to-video`, `first-frame`, `first-last-frame`, `references-to-video`, `video-edit`, `extend`: `{3..15}` | Continuous `3–15s` integer durations (`1s` increments) on the Gemini API / Interactions API surface (`gemini-omni-1.2-flash`). |

### 1.2 The 8-Point Continuity Audit (`flow-continuity-auditor`)
Each generation call is stateless unless anchored by `@PascalCase` reference handles or an incoming frame. Prompts **fail mechanical validation** if they violate any of these rules:

1. **Zero Backward References (`BACKWARD_REFS`)**:
   - **Forbidden**: `"from segment 1"`, `"as in scene 2"`, `"the same trader/man/woman/person/prop/room"`, `"as before"`, `"as previously"`, `"continuing from before"`, `"still wet/dirty/holding/wearing"`.
   - **Fix**: Re-state the physical state directly (`"rain-soaked linen shirt"`, `"holding the brass lantern in his right hand"`) and anchor identity with `@PascalCase`.
2. **Zero Token-Bleed Leaks (`TOKEN_LEAKS`)**:
   - **Forbidden**: Colour-temperature numbers (`3500K`, `5600K`), hex colour codes (`#FFAA00`, `#050811`), and bracketed set names (`(Market Lane)`). Video models frequently paint these literal tokens onto signs, walls, or lower-thirds inside the generated frame.
   - **Fix**: Replace with sensory visual descriptions (`"warm tungsten glow"`, `"deep midnight indigo"`, `"inside the narrow market lane"`).
3. **Canonical `@PascalCase` Handle Discipline**:
   - Every recurring character, set, or hero prop must be declared with a single `@PascalCase` handle matching `^@[A-Za-z][A-Za-z0-9]*$` (no spaces, no hyphens: `@Kwame`, `@SidewalkCafe`, `@AmberFlacon` — never `@Sidewalk-Cafe` or `@Cafe Ladies`).
   - Once `@Kwame` is declared, bare uses of `Kwame` in visual prompts are flagged as `BARE_HANDLE` errors and rewritten to `@Kwame`.
4. **Explicit Handoff Classification (`FIRST` | `CUT` | `CONTINUATION`)**:
   - **`CUT`**: Independent camera setup or angle; uses `@PascalCase` ingredients without inheriting the preceding final frame.
   - **`CONTINUATION`**: Seamless temporal handoff; exports the preceding clip's final frame (`s01_end.png`) as the next clip's `start` frame (`first-frame` mode) and echoes the outgoing pose, eyeline, and lighting.
5. **Turnaround Sheet Single-Subject Guard**:
   - Never pass a multi-angle turnaround sheet directly as a `references-to-video` ingredient (causes duplicate clones of the same character in one shot). Crop a **single clean view** before attaching as an ingredient, or use a unified pre-composited start frame.
6. **Insert/Remove Before Extend Rule**:
   - Flow `Insert`, `Remove`, and `Camera` edits fail or degrade on clips that have already been extended. Always perform object insertion/removal on the base clip **before** running `Extend`.
7. **One Dominant Camera Move + Single Beat Per 4s–8s Segment**:
   - Packing multiple camera trajectories (`dolly in + orbit + crane up`) or more than two story beats into an `8s` clip causes mid-shot morphing and rushed motion.
8. **Punctuation Hygiene (No Em Dashes `—`)**:
   - Strip em dashes (`—`) from copy-paste storyboard and video prompts to prevent token parser splitting.

### 1.3 Contract-Compliant Storyboard Contact-Sheet Generator (`generate_contract_storyboard_prompt`)
Follow the three-phase visual approval workflow: **Panels First -> Approval Second -> Video Third**.
- **Default Contact-Sheet Grid by Segment Duration**:
   - `4s` segment -> **`2` panels (`2x1` horizontal strip)**
   - `6s` segment -> **`3` panels (`3x1` horizontal strip)**
   - `8s` segment -> **`3` panels (`3x1` horizontal strip)**
   - `10s` segment -> **`4` panels (`2x2` grid)**
   - *(A `3x3` 9-panel grid is only emitted when `allow_nine_panel=True` and all 9 distinct panels are explicitly authored).*
- **Mandatory Prompt Contract**:
   - Section 1 (`Internal Operator Notes — Do Not Paste Into Image Generator`) lists surface, model, mode, duration, aspect ratio, grid layout, and `@PascalCase` asset bindings.
   - Section 2 (`Copy-Paste Prompt`) **must open with the exact directive**:
     `GENERATE THE STORYBOARD IMAGE NOW.`
   - Every panel description must state static framing at a specific timestamp (`PANEL B FRAMING: the static composition visible at 3 seconds`) and avoid motion-verb chains or em dashes.
   - Section 3 (`Approval Checklist`) stays outside the fenced prompt block.

---

## Part 2 — Google Flow CLI (`flow`), CDP Architecture & Angular CDK DOM Map (`google-flow-cli`)

### 2.1 Zero-Bot-Flag Chrome CDP Architecture (`port 9222`)
Standard Playwright/Puppeteer launches inject `--enable-automation` and `navigator.webdriver = true`, which trigger Google account login blocks and lower reCAPTCHA v3 scores on `labs.google/fx/tools/flow`.
- **Solution**: Launch the user's native system Google Chrome binary with a dedicated persistent profile (`~/.config/google-chrome-flow`) and `--remote-debugging-port=9222`, then attach via `chromium.connectOverCDP('http://127.0.0.1:9222')`.
- **5-Stage Agent State Machine**:
  1. **Pre-Flight (`flow doctor`)**: Verify Chrome binary, CDP port `9222`, active Flow tab, and Google authentication state.
  2. **Canvas Inspection (`flow status`)**: Read current project URL, active settings pill (`mediaType`, `mode`, `aspect`, `outputs`, `model`), and virtualized tile count.
  3. **Configuration & Frames (`flow config` / `flow frames`)**: Apply settings and attach start/end keyframes or ingredient references.
  4. **Trigger Generation (`flow generate` / `flow run flow.json`)**: Inject prompt into `.ProseMirror` and click `Create`.
  5. **Verify & Retrieve (`flow wait` / `flow download`)**: Poll generation progress until completion and download via signed CDN URL.

### 2.2 Complete Angular CDK & ProseMirror DOM Selector Map
| UI Target | Canonical Selector / Automation Procedure | Critical Operational Rule |
| :--- | :--- | :--- |
| **App Shell** | `aisandbox-root > flow-project-shell` | Confirm presence before interacting with workspace controls. |
| **Settings Trigger Pill** | `.settings-trigger-button` or `button[aria-label="Settings trigger"]` | Opens the `.cdk-overlay-pane` settings popover. |
| **Media Type Toggle** | `.cdk-overlay-pane mat-button-toggle:has-text("Video" \| "Image")` | **Must be switched FIRST** before opening the model dropdown, because the model list dynamically re-renders based on `mediaType`. |
| **Mode Toggle** | `.cdk-overlay-pane mat-button-toggle:has-text("Frames" \| "Ingredients")` | `Frames` enables Start/End keyframe slots; `Ingredients` enables up to 7 multi-asset reference slots on Omni 1.1 Flash. |
| **Aspect / Res / Duration / Count** | ``role="slider"[aria-label="Length"]` (`3s..15s` in `1s` steps on `Omni 1.2 Flash`) or `.cdk-overlay-pane mat-button-toggle` (`16:9 | 9:16 | 720p | 360p | 4s/6s/8s` on Veo)` | Click matching toggle inside `.cdk-overlay-pane`. |
| **Model Dropdown** | `button[aria-label="Select model family"]` -> `.cdk-overlay-pane button[role="menuitem"]:has-text("<Model>")` | After selecting a model or closing settings, **always send `Escape` + wait `250ms`** to dismiss `.cdk-overlay-backdrop` so it does not intercept subsequent clicks. |
| **Prompt Editor** | `.ProseMirror` (`div[contenteditable="true"].ProseMirror`) | Focus, select-all (`Control+A` / `Meta+A`), `Backspace`, insert text, and dispatch bubbling `input` event. |
| **Virtualized Video Tiles** | `cdk-virtual-scroll-viewport flow-video-tile` | Flow unmounts off-screen `<video>` nodes. Scroll viewport and **hover (`tile.hover()`)** over the target `flow-video-tile` to force-mount the `<video src="https://flow-content.google/video/...">` element. |
| **Signed CDN Download** | `<video src="https://flow-content.google/video/<UUID>?Expires=...&KeyName=labs-flow-prod-cdn-key&Signature=...">` | Extract `video.currentSrc` or `video.src` after hover-mount for direct zero-recompression MP4 download. |

---

## Part 3 — Credit Economics, Gemini Omni 1.2 Flash Rules & 6-Step UGC Product Video Pipeline (`google-flow-api` & `google-flow-director v3.0.0`)

### 3.1 Exact Google Flow Credit & Pricing Table (`Omni 1.2 Flash` vs `Omni 1.1 Flash` vs `Veo 3.1`)
- **Account Tiers**:
  - **Free Google Account**: `50` daily Flow credits (`$0`).
  - **Google AI Pro (`$19.99/mo`)**: `1,000` monthly Flow credits.
  - **Google AI Ultra (`$199.99/mo`)**: `25,000` monthly Flow credits (plus discounted `Veo 3.1 Fast` at `10` credits instead of `20`).
- **Per-Generation Credit Costs**:
  - **Still Images (`Nano Banana` / `Nano Banana Pro` / `Nano Banana 2`)**: **`0 credits`** (`1K`, `2K`, `4K` image upscales are also **`0 credits`**).
  - **`Omni 1.2 Flash` (`macaron_cookie`) Video (`$0.07/s` at `720p` on API — `30%` cheaper than Omni 1.1)**:
    - **`360p` Draft (`macaron_cookie_*_360p`)**: **`1 credit/second`** for `3s..10s` (`3s=3c`, `4s=4c`, `6s=6c`, `8s=8c`, `10s=10c`) and **`+2 credits/second`** for `11s..15s` (`11s=12c`, `12s=14c`, `13s=16c`, `14s=18c`, `15s=20c`).
    - **`720p` Standard (`macaron_cookie_*`)**: **`3 credits/second`** for `3s..10s` (`3s=9c`, `8s=24c`, `10s=30c`) and **`+6 credits/second`** for `11s..15s` (`15s=60c`).
    - **Multi-Turn Conversational Edit (`macaron_cookie_edit` & `macaron_cookie_edit_360p`)**: **`0 credits` (FREE)** across full `15s` clips!
  - **`Omni 1.1 Flash` (`abra`) Legacy Video (`720p` / `360p` half-cost draft)**:
    - `4s`: **`7 credits`** (`720p`) / **`4 credits`** (`360p`)
    - `6s`: **`10 credits`** (`720p`) / **`5 credits`** (`360p`)
    - `8s`: **`12 credits`** (`720p`) / **`6 credits`** (`360p`)
    - `10s`: **`15 credits`** (`720p`) / **`7 credits`** (`360p`)
    - `Video-to-Video Edit`: **`20 credits`** (`720p`) / **`10 credits`** (`360p`)
  - **Post-Generation Video Upscale**:
    - **`360p -> 720p` (`omni_upsampler_360p`)**: **`0 credits` (FREE)**
    - **`1080p` Upscale (`veo_3_1_upsampler_1080p`)**: **`0 credits` (FREE)** on all tiers -> **Golden Cost Rule (Pillar 1)**: Draft at `360p` or `720p` in `Omni 1.2 Flash`, refine via **`0-credit` conversational edits**, and run the **`0-credit` `1080p` upscale** (or `50-credit` `4K` upscale) only on approved takes!

### 3.2 High-Reliability Prompting Rules for `Gemini Omni 1.2 Flash`
1. **Physical Action First**: Put the subject's concrete physical action in the first sentence (`"@Aria lifts the @AmberFlacon to eye level and turns it toward the key light..."`). Video models drop or weaken clauses buried at the end of long paragraphs.
2. **Multi-Speaker Conditioning & Multi-Modal Reference Adherence**:
   - Combine front-and-back garment/product photos, `3-second` motion reference clips, and `1-second` voice cues.
   - Route distinct `1-second` voice references to `4+` characters inside a single `15s` clip with `يتحدث باللهجة البحرينية: "<النص>"` directly before quoted dialogue.

### 3.3 The 6-Step Checkpointed UGC Product Video Pipeline (`ugc_state.json`)
To produce multi-product UGC reels with **zero jump cuts** and **60 credits total for 40 seconds (`4 × 10s` at `1080p`)**:
1. **Step 1 — `2×2` 4-View Product Sheet (`0 credits`, `Nano Banana`)**: Generate a clean 4-angle reference sheet (`front, 3/4, side, back`) for each product so packaging geometry and labels are locked.
2. **Step 2 — Creator Portrait Sheet (`0 credits`, `Nano Banana`)**: Generate a front + 3/4 portrait of the UGC presenter (`@Creator`).
3. **Step 3 — Unified Anchor Still (`0 credits`, `Nano Banana`)**: Composite `@Creator` sitting at the table with all products arranged in their exact resting positions on the surface (`unified_anchor.png`).
4. **Step 4 — Seamless Loop Clips (`15 credits × N`, `Omni 1.1 Flash`, `10s`, `720p`)**:
   - For each product clip, pass `unified_anchor.png` as **BOTH `startImage` AND `endImage`** (`first-last-frame` mode).
   - Prompt the presenter to pick up Product `i`, demonstrate it while delivering the line, **place Product `i` back on its exact table mark by the `8.0s` mark**, and hold a natural breathing smile from `8.5s–10.0s`.
   - Because every clip starts and ends on `unified_anchor.png`, all `N` clips stitch together with an invisible match-frame transition!
5. **Step 5 — Free `1080p` Upscale (`0 credits`)**: Upscale each approved `720p` clip to `1080p`.
6. **Step 6 — Trim to Sound (Not Picture) & Concatenate (`0 credits`, FFmpeg)**: Inspect the audio waveform around the splice boundary, trim trailing dead air while keeping `0.15s–0.25s` natural room-tone breath, and concatenate.

---

## Part 4 — Browser Queue Resilience & React Prototype Injection (`Google-Flow-Automation`)

When automating browser-side queues directly inside the Flow DOM (`content.js` / `logic.js`):
1. **React 16+ / Angular Native Value & File Setter Bypass**:
   - Direct `el.value = text` assignments are ignored by synthetic event trackers. Call the native prototype setter:
     ```javascript
     const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
     setter.call(el, promptText);
     el.dispatchEvent(new Event('input', { bubbles: true }));
     el.dispatchEvent(new Event('change', { bubbles: true }));
     ```
   - For programmatic file uploads without OS dialogs, construct a `DataTransfer()`, append `File` blobs, invoke `Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'files').set.call(fileInput, dt.files)`, and dispatch bubbling `input` + `change` events.
2. **Filename-Stem Asset Matching (`matchAssets`)**:
   - Automatically bind local reference images (`@Aria.png`, `AmberFlacon.png`) to a prompt by matching normalized filename stems against `@PascalCase` tokens in the prompt text.
3. **Queue Error Classification (`Policy Error` vs `Server Busy`)**:
   - **`Policy Error` / Content Filter Rejection**: **Non-retryable**. Log the offending prompt ID, skip immediately, and advance the queue so repeated retries do not flag or throttle the Google account.
   - **`Server Busy` / `Rate Limited` / `503`**: **Retryable**. Apply a randomized `20–30s` backoff jitter before re-submitting the task.
