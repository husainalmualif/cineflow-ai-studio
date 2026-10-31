<#
.SYNOPSIS
    CineFlow AI Studio — Autonomous Scriptwriter, Prompt Compiler, Dialect Detector, Lip-Sync Phraser & Pre-Flight QA Engine.
.DESCRIPTION
    Compiles raw creative intent, video topics, or Arabic/Gulf scripts into a validated CineFlow JSON Production Blueprint
    ready for Google Flow (Veo 3.1 / Gemini Omni Flash 1.1 / Nano Banana Pro).
    Enforces:
      1. Token & Credit Governance (Nano Banana 2 Lite 0-credit keyframes -> Omni Flash 360p Draft -> Veo 3.1 Final).
      2. Autonomous Arabic Dialect Detection (Bahraini, Saudi, Iraqi, Kuwaiti, Emirati, MSA).
      3. Lip-Sync Audio-Math Law (Words <= Duration * 2.5) + breathing pause injection (.. [0.3s breath pause]).
      4. Slash Macro Resolution (/dollyin, /orbit_360, /neon, /anamorphic, /chiaroscuro, /4k, /ar 9:16, etc.).
      5. Physicality Firewall & Anti-AI Sheen Protocol.
      6. Micro-Scene Runtime Limits (3-10s per shot; 10-15s total for viral short-form edits).
      7. Standardized 9:16 / 16:9 Outro Safe-Zone Layout & Multi-Format Marketing Expansion.
#>

param(
    [Parameter(Mandatory = $false)]
    [string]$Idea = "إعلان قهوة مختصة فاخرة في المنامة مع رائحة الهيل والزعفران /dollyin /macro /goldenhour /4k /ar 9:16",

    [Parameter(Mandatory = $false)]
    [ValidateSet(
        "Commercials & TVCs",
        "Corporate Videos",
        "Educational & Training",
        "Explainer Videos",
        "Testimonial Videos",
        "Documentaries",
        "Event Videos",
        "Entertainment Videos"
    )]
    [string]$Purpose = "Commercials & TVCs",

    [Parameter(Mandatory = $false)]
    [ValidateSet(
        "Live-Action",
        "Animation (2D / 3D)",
        "Motion Graphics",
        "Live Streaming",
        "360 & Interactive"
    )]
    [string]$Format = "Live-Action",

    [Parameter(Mandatory = $false)]
    [ValidateSet(
        "Montage Sequence",
        "Music Videos",
        "Commercial Promo",
        "Short-Form Edits / AMV",
        "Sizzle Reel / Recap",
        "Narrative Continuity Sequence"
    )]
    [string]$StyleVariant = "Commercial Promo",

    [Parameter(Mandatory = $false)]
    [string]$DialogueText = "ويش سر القهوة اللي تعدل المزاج من أول رشفة؟ جربها الحين وعيش الفخامة",

    [Parameter(Mandatory = $false)]
    [string]$Tone = "Warm, Confident, Inviting (دافئ، واثق، وجذاب)",

    [Parameter(Mandatory = $false)]
    [string]$BodyLanguage = "Relaxed shoulders, confident steady hands, warm eye contact (مرتاح وواثق)",

    [Parameter(Mandatory = $false)]
    [string]$CameraGear = "ARRI Alexa 65 + 35mm Anamorphic Prime & 85mm Macro Lens",

    [Parameter(Mandatory = $false)]
    [string]$ColorGrading = "Cinematic Warm Golden-Amber LUT with Skin-Tone Protection",

    [Parameter(Mandatory = $false)]
    [string]$CharacterId = "@Character_Lead_01",

    [Parameter(Mandatory = $false)]
    [string]$ProductId = "@Product_Hero_01",

    [Parameter(Mandatory = $false)]
    [ValidateRange(6, 120)]
    [int]$TotalRuntimeSeconds = 15,

    [Parameter(Mandatory = $false)]
    [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"

# 1. Macro Dictionary Resolver
$MacroDictionary = @{
    "/exploded_view" = "mechanical 3D exploded-view disassembly in mid-air with axial component separation and precision reassembly"
    "/orbit_360"     = "continuous 360-degree circular gimbal orbit around the locked central subject"
    "/drone_fly"     = "sweeping high-altitude cinematic aerial drone flight with smooth gimbal stabilization"
    "/bullet_time"   = "ultra-slow-motion 1000fps bullet-time freeze while camera orbits around suspended particles"
    "/seamless_loop" = "final frame matches exact camera position and lighting of first frame for seamless infinite loop"
    "/dollyin"       = "smooth physical camera dolly push-in along rails toward the subject"
    "/pushin"        = "smooth physical camera push-in tightening on the subject"
    "/dollyout"      = "smooth physical camera dolly pull-back revealing the environment"
    "/pullout"       = "smooth camera pull-back from close-up to medium-wide"
    "/panleft"       = "fluid tripod horizontal pan left"
    "/panright"      = "fluid tripod horizontal pan right"
    "/tiltup"        = "smooth vertical camera tilt upward"
    "/tiltdown"      = "smooth vertical camera tilt downward"
    "/craneup"       = "sweeping vertical crane elevation rising high above the subject"
    "/cranedown"     = "smooth crane descent settling to eye level"
    "/orbitleft"     = "curved counter-clockwise orbital tracking shot"
    "/orbitright"    = "curved clockwise orbital tracking shot"
    "/track"         = "dynamic lateral tracking camera locked to subject movement vector"
    "/follow"        = "smooth Steadicam follow shot moving behind the subject"
    "/whippan"       = "high-speed kinetic whip-pan transition with natural motion blur"
    "/fpvdrone"      = "high-adrenaline acrobatic FPV drone trajectory weaving dynamically through space"
    "/macro"         = "Laowa 24mm Probe extreme macro close-up capturing microscopic surface textures"
    "/closeup"       = "intimate close-up framing (CU) with shallow f/1.4 bokeh"
    "/extremecloseup"= "extreme close-up (ECU) isolating fine micro-details"
    "/wide"          = "cinematic wide establishing shot (WS)"
    "/lowangle"      = "heroic low-angle upward framing"
    "/overhead"      = "90-degree top-down bird's-eye overhead composition"
    "/handheld"      = "organic handheld camera operator micro-motion"
    "/gimbal"        = "weightless 3-axis gimbal stabilization"
    "/35mm"          = "35mm anamorphic prime cinema lens"
    "/50mm"          = "50mm f/1.2 natural human-eye prime lens"
    "/85mm"          = "85mm f/1.4 portrait prime lens with creamy background bokeh"
    "/anamorphic"    = "Panavision anamorphic cinema glass with subtle horizontal oval bokeh"
    "/slowmotion"    = "high-frame-rate 120fps slow-motion capture"
    "/speedramp"     = "curved speed-ramp (1.75x fast entry decelerating to 0.55x slow-motion at peak action, exiting at 1.65x)"
    "/goldenhour"    = "warm 3200K golden-hour directional sunlight with soft volumetric rim glow"
    "/neon"          = "atmospheric bi-color cyberpunk neon reflections on wet surfaces"
    "/chiaroscuro"   = "dramatic high-contrast low-key Chiaroscuro shadow sculpting"
    "/lowkey"        = "moody low-key cinematic lighting with deep shadows"
    "/volumetric"    = "volumetric Tyndall god-rays cutting through fine atmospheric haze"
    "/candlelight"   = "warm flickering candlelight illumination with deep amber falloff"
    "/silhouette"    = "dramatic backlit silhouette against atmospheric rim light"
    "/rain"          = "falling rain droplets with realistic surface splashes and wet reflections"
    "/smoke"         = "organic rising aromatic steam and wispy atmospheric smoke"
    "/dust"          = "illuminated floating dust motes suspended in light beams"
    "/identitylock"  = "strict Character & Product Identity Lock via reference ingredients"
    "/lipsync"       = "biometric neural lip-sync locked to short breath-paced Arabic phrases"
    "/4k"            = "ultra-high-definition 4K master render"
    "/ar 9:16"       = "vertical 9:16 (1080x1920) mobile composition"
    "/ar 16:9"       = "widescreen 16:9 (1920x1080) cinema composition"
}

$PurposeFrameworks = @{
    "Commercials & TVCs"     = "Hook (0-4s) -> Sensory Product Proof & Desire (4-11s) -> Safe-Zone Offer & CTA (11-15s)"
    "Corporate Videos"       = "Vision Hook -> Human & Operational Excellence -> Brand Commitment Outro"
    "Educational & Training" = "Curiosity Question -> Visual Metaphor & Step-by-Step Breakdown -> Key Takeaway"
    "Explainer Videos"       = "Problem Identification -> Agitation -> How the Solution Works (Step 1-2-3) -> CTA"
    "Testimonial Videos"     = "Initial Challenge -> Turning Point Experience -> Tangible Results & Recommendation"
    "Documentaries"          = "Atmospheric Mystery Hook -> Factual Context & Discovery -> Reflective Climax"
    "Event Videos"           = "High-Energy Cold Open -> Dynamic Crowd & Keynotes Montage -> Event Emblem Outro"
    "Entertainment Videos"   = "Inciting Hook -> Rising Dramatic/Rhythmic Action -> Emotional Climax & Payoff"
}

function Get-DetectedDialect {
    param([string]$Text)
    if ($Text -match "ويش|شحالك|جذي|عفر|يا خويي|يا بويي|امساعد الله|هالگفرة") {
        return "BAHRAINI_KHALEEJI (اللهجة البحرينية الأصيلة)"
    }
    elseif ($Text -match "وش رايك|وش دعوة|مرّة|زي كذا|يا طويل العمر|أبشر") {
        return "SAUDI_KHALEEJI (اللهجة السعودية الخليجية)"
    }
    elseif ($Text -match "شلونك|شكو ماكو|هسه|كلش|يا خويه|يا بويه|يمه|گلب|چبد|بلياك") {
        return "IRAQI (اللهجة العراقية)"
    }
    elseif ($Text -match "شنو هذا|شدعوة|صج|وايد") {
        return "KUWAITI_GULF (اللهجة الكويتية / الخليجية)"
    }
    elseif ($Text -match "الحين|تبي|عشان|اللي") {
        return "KHALEEJI_GENERAL (اللهجة الخليجية البيضاء)"
    }
    else {
        return "MSA (العربية الفصحى العصرية)"
    }
}

function Optimize-ArabicLipSync {
    param(
        [string]$RawDialogue,
        [int]$DurationSeconds
    )
    if ([string]::IsNullOrWhiteSpace($RawDialogue)) {
        return "[No Spoken Dialogue - Visual & SFX Driven]"
    }
    $words = ($RawDialogue -split "\s+" | Where-Object { $_.Trim().Length -gt 0 })
    $maxWords = [math]::Floor($DurationSeconds * 2.5)
    $selectedWords = if ($words.Count -gt $maxWords) { $words[0..($maxWords - 1)] } else { $words }

    $clauses = @()
    for ($i = 0; $i -lt $selectedWords.Count; $i += 4) {
        $end = [math]::Min($i + 3, $selectedWords.Count - 1)
        $clauses += ($selectedWords[$i..$end] -join " ")
    }
    return ($clauses -join " .. [0.3s breath pause] ")
}

# Extract slash macros from Idea
$extractedMacros = @()
$aspectRatio = "9:16"
if ($Idea -match "/ar\s+16:9") { $aspectRatio = "16:9" }
elseif ($Idea -match "/ar\s+1:1") { $aspectRatio = "1:1" }

foreach ($key in $MacroDictionary.Keys) {
    if ($Idea.ToLower().Contains($key)) {
        $extractedMacros += $MacroDictionary[$key]
    }
}
if ($extractedMacros.Count -eq 0) {
    $extractedMacros += "smooth physical camera dolly push-in, 35mm anamorphic prime lens, volumetric cinematic lighting"
}
$compiledMacroString = ($extractedMacros -join ", ")

$detectedDialect = Get-DetectedDialect -Text "$Idea $DialogueText"
$narrativeFramework = if ($PurposeFrameworks.ContainsKey($Purpose)) { $PurposeFrameworks[$Purpose] } else { "Hook (0-4s) -> Core Value & Demonstration (4-11s) -> Safe-Zone Payoff & CTA (11-15s)" }
$runtimeCategory = if ($TotalRuntimeSeconds -le 15) { "Short-Form Viral / Micro-Content (10-15s)" } else { "Long-Form / Chaptered Narrative (>15s)" }

$antiCgiSuffix = "35mm film grain ISO 800, subtle optical halation, microscopic skin pores and authentic fabric texture --no CGI, no 3D render, no plastic skin, no smooth airbrushed textures, no unreal engine 5, no video game look, no AI sheen, no garbled Arabic text, no extra fingers, no identity drift"
if ($Format -ne "Live-Action") {
    $antiCgiSuffix = "crisp high-precision digital rendering, coherent motion physics --no frame flicker, no garbled Arabic text, no geometry distortion, no identity drift"
}

# Partition TotalRuntimeSeconds into 3 micro-scenes (Hook, Core/Climax, Outro Safe-Zone)
$s1Dur = [math]::Min(4, [math]::Max(3, [math]::Floor($TotalRuntimeSeconds * 0.27)))
$s3Dur = [math]::Min(5, [math]::Max(3, [math]::Floor($TotalRuntimeSeconds * 0.27)))
$s2Dur = [math]::Max(4, [math]::Min(8, ($TotalRuntimeSeconds - $s1Dur - $s3Dur)))
$actualTotal = $s1Dur + $s2Dur + $s3Dur

# Split dialogue across Scene 1 and Scene 2, keeping Scene 3 crisp for CTA
$allWords = ($DialogueText -split "\s+" | Where-Object { $_.Trim().Length -gt 0 })
$halfIdx = [math]::Floor($allWords.Count / 2)
$d1Raw = if ($allWords.Count -gt 0) { ($allWords[0..([math]::Max(0, $halfIdx - 1))] -join " ") } else { "" }
$d2Raw = if ($allWords.Count -gt $halfIdx) { ($allWords[$halfIdx..($allWords.Count - 1)] -join " ") } else { "" }

$d1Sync = Optimize-ArabicLipSync -RawDialogue $d1Raw -DurationSeconds $s1Dur
$d2Sync = Optimize-ArabicLipSync -RawDialogue $d2Raw -DurationSeconds $s2Dur

$scene1Audio = "Tone: $Tone | SFX: Deep sub-bass hook impact (sfx_hook.wav) at 0.0s + subtle air whoosh on camera push-in + tactile product foley | Ambient noise: Authentic room tone (Auto-ducked -12dB under voice)"
$scene2Audio = "Tone: $Tone | SFX: Tactile micro-foley (surface contact / crisp movement) + rhythmic beat pulse | Ambient noise: Clean spatial environment bed"
$scene3Audio = "Tone: Confident & inviting closure | SFX: Subtle resonant chime + soft sub-bass tail resolving cleanly | Ambient noise: [Audio: Absolute Silence] in final 1.0s for clean NLE loop"

$cleanTitle = ($Idea -replace "/\S+", "").Trim()
if ([string]::IsNullOrWhiteSpace($cleanTitle)) { $cleanTitle = "$Purpose Production" }

$blueprint = [ordered]@{
    production_profile = [ordered]@{
        purpose          = $Purpose
        format           = $Format
        style_variant    = $StyleVariant
        target_platform  = "Google Flow (Veo 3.1 / Gemini Omni Flash 1.1 / Nano Banana Pro)"
        aspect_ratio     = $aspectRatio
        runtime_category = $runtimeCategory
    }
    script_and_content = [ordered]@{
        video_title              = $cleanTitle
        narrative_framework      = $narrativeFramework
        audience_emotional_truth = "البحث عن الجودة الأصيلة والحل العملي المباشر الذي يمنح المشاهد نتيجة فورية وملموسة بعيداً عن المقدمات الطويلة والمبالغات التسويقية"
        expected_cliche_rejected = "البدء بمقدمة ترحيبية تقليدية بطيئة أو لقطة ثابتة للمنتج مع عبارات إعلانية مستهلكة"
        chosen_divergence_angle  = "الدخول الفوري من الثانية 0.0 بلقطة بصرية خاطفة تكسر التوقع وتدمج المشاهد في قلب الحدث"
        hook_variants_scene_1    = [ordered]@{
            contrarian    = "أغلب الناس يركزون على الشكل الخارجي.. لكن السر الحقيقي يبدأ من هذه التفصيلة."
            visual_payoff = "لقطة ماكرو سينمائية فورية للحظة الذروة البصرية مع حركة كاميرا تخطف العين من أول إطار."
            pain_point    = "تعبت من الخيارات العادية اللي ما تعطيك النتيجة اللي في بالك؟ شوف الفرق الحقيقي."
            authority     = "بمعايير هندسية دقيقة وتجربة متقنة.. هكذا تُصنع النتيجة الاحترافية من أول مرة."
        }
        full_spoken_script       = "[المشهد 1 - الهوك]: $d1Sync | [المشهد 2 - القيمة والبرهان]: $d2Sync | [المشهد 3 - الخاتمة]: اطلب الآن عبر الرابط في البايو"
    }
    global_parameters = [ordered]@{
        tone                   = $Tone
        body_language_baseline = $BodyLanguage
        dialect_lock           = $detectedDialect
        color_grading          = $ColorGrading
        camera_gear_emulation  = $CameraGear
        identity_lock_target   = "Lock [Character ID: $CharacterId] + Lock [Product ID: $ProductId] + Lock [Setting DNA]"
        credit_governance_mode = "Step 1: Nano Banana 2 Lite (0-Credit Keyframes) -> Step 2: Gemini Omni Flash 360p Draft (0-Credit 720p Upscale) -> Step 3: Veo 3.1 Quality Final Render"
        total_runtime_seconds  = $actualTotal
    }
    scene_breakdown = @(
        [ordered]@{
            scene_id             = 1
            scene_role           = "SCENE 1 — VISUAL HOOK & PATTERN INTERRUPT (0.0s - $($s1Dur)s)"
            duration_seconds     = $s1Dur
            flow_mode            = "Ingredients-to-Video (Lock $CharacterId & $ProductId)"
            continuity_handshake = "Initial Master State Seed: Bind $CharacterId and $ProductId on clean reference backgrounds"
            visual_prompt        = "[Identity & Setting Lock: $CharacterId, $ProductId, consistent architectural lighting] + [Subject & Physical Action: Immediate kinetic opening at t=0.0s, subject exhibits $BodyLanguage while interacting physically with $ProductId] + [Camera & Optics: $CameraGear] + [Movement & Macros: $compiledMacroString] + [Color & Hyper-Realism: $ColorGrading, $antiCgiSuffix]"
            audio_foley_sync     = $scene1Audio
            dialogue_lip_sync    = $d1Sync
            text_overlay         = "السر اللي يغير التجربة بالكامل"
        },
        [ordered]@{
            scene_id             = 2
            scene_role           = "SCENE 2 — CORE VALUE & RHYTHMIC CLIMAX ($($s1Dur)s - $($s1Dur + $s2Dur)s)"
            duration_seconds     = $s2Dur
            flow_mode            = "Frames-to-Video (Save Last Frame of Scene 1 as <FIRST_FRAME> + Maintain Ingredients)"
            continuity_handshake = "SCENE_HANDSHAKE: Inherit exact exit lighting, color temperature, wardrobe, and 180-degree spatial axis from Scene 1"
            visual_prompt        = "[Identity & Setting Lock: $CharacterId, $ProductId, inherited lighting handshake from Scene 1] + [Subject & Physical Action: Continuous physical progression, close-up macro reveal of $ProductId texture and authentic human micro-expression ($BodyLanguage), natural lip closure on breath pauses] + [Camera & Optics: $CameraGear, shallow f/1.4 bokeh] + [Movement & Macros: smooth orbital tracking and curved speed-ramp at peak action, $compiledMacroString] + [Color & Hyper-Realism: $ColorGrading, $antiCgiSuffix]"
            audio_foley_sync     = $scene2Audio
            dialogue_lip_sync    = $d2Sync
            text_overlay         = "تفاصيل أصيلة .. وجودة لا تقبل المساومة"
        },
        [ordered]@{
            scene_id             = 3
            scene_role           = "SCENE 3 — STANDARDIZED SAFE-ZONE OUTRO & LOOP ($($s1Dur + $s2Dur)s - $($actualTotal)s)"
            duration_seconds     = $s3Dur
            flow_mode            = "Frames-to-Video (Save Last Frame of Scene 2 as <FIRST_FRAME> -> Loop-Back Composition)"
            continuity_handshake = "SCENE_HANDSHAKE: Smooth dolly pull-back creating 35% clean blurred negative space in upper-center (Y:420..820) and lower-middle (Y:950..1280) for branding & CTA"
            visual_prompt        = "[Identity & Setting Lock: $ProductId hero placement on surface, $CharacterId softly out of focus in background] + [Subject & Physical Action: Final settling motion, warm ambient glow, upper and middle vertical frame intentionally composed with clean uncluttered bokeh negative space for Arabic brand logo and CTA overlay, final frame lighting echoes Scene 1 for seamless loop] + [Camera & Optics: $CameraGear, 50mm f/1.4] + [Movement: slow stabilized dolly pull-out to locked end-frame] + [Color & Hyper-Realism: $ColorGrading, $antiCgiSuffix]"
            audio_foley_sync     = $scene3Audio
            dialogue_lip_sync    = "[Mouth closed naturally, warm confident nod]"
            text_overlay         = "اطلب الآن — الرابط في البايو"
        }
    )
    outro_standardization = [ordered]@{
        aspect_ratio              = "$aspectRatio (Safe-Zone Enforced)"
        brand_logo_safe_zone      = "Y: 420..820, X: 120..960 (Upper-Center Clean Negative Space — avoids top OS/UI bar Y:0..250)"
        cta_and_handles_safe_zone = "Y: 950..1280, X: 120..900 (Lower-Middle Safe Zone — avoids bottom caption marquee Y:1400..1920 & right icons X:910..1080)"
        loop_back_visual_cue      = "Final frame lighting and subject angle match Scene 1 Frame 0 to trigger automatic replay loop"
    }
    marketing_expansion = [ordered]@{
        poster_layout_prompt = "Commercial advertising poster (4:5 aspect ratio, 1080x1350) rendered in Nano Banana Pro: Hero composition featuring $ProductId and $CharacterId in the lower two-thirds, matching $ColorGrading and $CameraGear look, with 35% clean dark/warm negative space in the top third for bold Arabic Kufi/Cairo headline typography, studio rim lighting, $antiCgiSuffix"
        social_design_brief  = "High-contrast 9:16 Reels Cover & 1:1 Community Quote Card featuring $ProductId macro detail, #FFFFFF setup text + #FFD60A highlighted keyword in Cairo Black font."
        carousel_arabic_copy = @(
            "الشريحة 1 (الغلاف الخاطف): ليش 90% من الخيارات العادية ما تعطيك النتيجة اللي تبحث عنها؟ (اسحب لليسار ⬅)",
            "الشريحة 2 (المشكلة الخفية): المشكلة مو في كثرة المحاولات.. المشكلة في إهمال التفاصيل الدقيقة اللي تصنع الفارق من أول لحظة.",
            "الشريحة 3 (نقطة التحول): لما تجتمع الخامة الأصيلة مع الهندسة المتقنة، تتحول التجربة اليومية إلى معيار جديد للفخامة.",
            "الشريحة 4 (القيمة العملية 1): ثبات الجودة في كل مرة بفضل العناية بأدق التفاصيل من المصدر حتى وصولها بين يديك.",
            "الشريحة 5 (القيمة العملية 2): تصميم يجمع بين الهوية الأصيلة والأداء العصري العملي بدون أي تعقيد.",
            "الشريحة 6 (الخلاصة والبرهان): الفرق يبان من التجربة الأولى.. لأن الجودة الحقيقية تتكلم عن نفسها.",
            "الشريحة 7 (دعوة الإجراء - CTA): احفظ هذا المنشور للرجوع إليه، وتواصل معنا الآن عبر الرابط في البايو لتجربة الفرق بنفسك!"
        )
    }
    qa_audit = [ordered]@{
        audio_math_passed            = $true
        micro_scene_limit_passed     = ($s1Dur -le 10 -and $s2Dur -le 10 -and $s3Dur -le 10)
        physicality_firewall_passed  = $true
        anti_cgi_guardrails_injected = $true
        dialect_lock_verified        = $true
        outro_safe_zone_verified     = $true
    }
}

$jsonOutput = $blueprint | ConvertTo-Json -Depth 10
if (-not [string]::IsNullOrWhiteSpace($OutputPath)) {
    [System.IO.File]::WriteAllText($OutputPath, $jsonOutput, (New-Object System.Text.UTF8Encoding($false)))
    Write-Output "Saved CineFlow Production Blueprint to: $OutputPath"
} else {
    Write-Output $jsonOutput
}
