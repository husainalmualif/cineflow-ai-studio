#!/usr/bin/env python3
"""Centralized configuration, constants, dialect lexicons, and 185+ slash macros for CineFlow AI Studio.

Single Source of Truth (fixes H2, H3, H5, H6, D4, D6):
- All scripts (cineflow_compiler.py, validate_package.py, estimate_cost.py,
  make_srt.py, multi_agent_orchestrator.py) import thresholds from this module.
"""

from typing import Any, Dict, List, Set, Tuple

# ---------------------------------------------------------------------------
# 1. Empirical Defaults & Hard Guardrails (Single Source of Truth)
# ---------------------------------------------------------------------------
# Percentage of Arabic base letters that must carry at least one diacritic mark
# in broadcast TTS scripts (tts_text / dialogue_tts_ar).
# CR3: Default 0.75 for standard text and 1.0 target for AI-spoken text (tuned_default).
MIN_DIACRITIC_RATIO: float = 0.75
MIN_DIACRITIC_RATIO_AI_TTS: float = 1.0

# CR1: Allowed per-clip generative durations (seconds) vs. Short-Form total video duration
ALLOWED_CLIP_DURATIONS: Tuple[int, ...] = (4, 6, 8, 10)
ALLOWED_CLIP_SECONDS: List[int] = [4, 6, 8, 10]
HARD_ALLOWED_CLIP_DURATIONS: Set[int] = {4, 6, 8, 10}
MAX_SINGLE_SHOT_SECONDS: int = 10
SHORT_FORM_TOTAL_SECONDS: Tuple[int, int] = (10, 15)
LONG_FORM_CHAPTER_THRESHOLD_SECONDS: int = 60
LONG_FORM_CHAPTER_RANGE_SECONDS: Tuple[int, int] = (60, 90)
CAPABILITY_VERIFICATION_STATUS: str = "verify_live"

# Cumulative duration cap (seconds) for chained Extend blocks before requiring a new sequence
MAX_EXTEND_CHAIN_SECONDS: int = 40

# Block & shot density limits
MAX_SHOTS_PER_BLOCK: int = 3
MAX_PROMPT_WORDS_PER_BLOCK: int = 120
MAX_LIPSYNC_WORDS_PER_PHRASE: int = 8
MAX_WORDS_PER_SECOND_AR: float = 2.5
MAX_OVERLAY_WORDS: int = 6

# Rhythmic Montage & Beat Grid tuned defaults (CR2 & rhythmic_montage_engine)
SNAP_TOLERANCE_MS: float = 40.0
MIN_RAMP_SPEED: float = 0.25
MAX_RAMP_SPEED: float = 4.0
MAX_RAMPS_PER_CLIP: int = 1
MAX_SFX_PER_TWO_BEATS: int = 1
MAX_SFX_EVENTS_PER_MIN_STANDARD: int = 15

# Outro Safe-Zone tuned defaults (9:16) & Remotion v4.0.539 Video-First Layout Law (video-layout.md)
OUTRO_SAFE_ZONES: Dict[str, Any] = {
    "aspect_ratio": "9:16",
    "logo_zone": "Y 420..820",
    "cta_zone": "Y 950..1280, X 120..900",
    "avoid": ["أعلى 220", "أسفل من 1500", "يمين من 920"],
    "status": "tuned_default",
}
VIDEO_LAYOUT_MIN_HEADLINE_PX: int = 84
VIDEO_LAYOUT_MIN_SUPPORTING_PX: int = 44
VIDEO_LAYOUT_SAFE_MARGIN_X_PX: int = 80
VIDEO_LAYOUT_SAFE_MARGIN_Y_PX: int = 100
VIDEO_LAYOUT_MAX_FOCAL_POINTS_PER_SCENE: int = 1

# Gemini Omni Flash Stateful Interactions API & FastMCP Agent (`omni-skill-agy`)
# Single Source of Truth for Model IDs and Verification Metadata
MODEL_REGISTRY_LAST_VERIFIED: str = "2026-11-02"
OMNI_FLASH_MODEL_DEFAULT: str = "gemini-omni-flash-preview"
OMNI_FLASH_STABLE_MODEL: str = "gemini-omni-1.1-flash"
VEO_PRIMARY_MODEL: str = "veo-3.1-quality"
SEEDANCE_PRIMARY_MODEL: str = "seedance-2.0"
KEYFRAME_REFERENCE_MODEL: str = "nano-banana-pro"
TEXT_REASONING_MODEL: str = "gemini-2.5-pro"

MODEL_REGISTRY: Dict[str, Any] = {
    "last_verified_date": MODEL_REGISTRY_LAST_VERIFIED,
    "verification_policy": CAPABILITY_VERIFICATION_STATUS,
    "models": {
        "omni_flash_stateful": {
            "id": OMNI_FLASH_MODEL_DEFAULT,
            "stable_alias": OMNI_FLASH_STABLE_MODEL,
            "api": "interactions",
            "allowed_clip_seconds": ALLOWED_CLIP_SECONDS,
            "max_extend_chain_seconds": MAX_EXTEND_CHAIN_SECONDS,
        },
        "veo_quality": {
            "id": VEO_PRIMARY_MODEL,
            "platform": "google_flow",
            "allowed_clip_seconds": ALLOWED_CLIP_SECONDS,
        },
        "seedance": {
            "id": SEEDANCE_PRIMARY_MODEL,
            "platform": "dreamina_capcut",
            "allowed_clip_seconds": ALLOWED_CLIP_SECONDS,
        },
        "keyframe_reference": {
            "id": KEYFRAME_REFERENCE_MODEL,
            "platform": "google_labs",
            "cost_credits": 0,
        },
        "text_reasoning": {
            "id": TEXT_REASONING_MODEL,
            "platform": "gemini_api",
        },
    },
}

OMNI_INLINE_MAX_MB: float = 4.0
OMNI_FILE_API_TIMEOUT_SECONDS: int = 300
OMNI_MCP_TOOLS: Tuple[str, ...] = (
    "generate_video",
    "edit_video",
    "animate_image",
    "interpolate_images",
    "generate_with_subjects",
    "edit_user_video",
    "upload_to_youtube",
    "get_help",
)

# Runtime bounds (seconds)
MIN_TOTAL_RUNTIME_SECONDS: int = 4
MAX_TOTAL_RUNTIME_SECONDS: int = 600

# Audio & 3D WebGL empirical defaults (overridable in user config)
TARGET_INTEGRATED_LUFS: float = -14.0
MAX_TRUE_PEAK_DBTP: float = -1.0
SIDECHAIN_DUCKING_DB: float = -9.5
SILENCE_THRESHOLD_DB: float = -32.0
DEFAULT_UNREAL_BLOOM: Dict[str, float] = {
    "strength": 0.42,
    "radius": 0.45,
    "threshold": 0.78,
}

# ---------------------------------------------------------------------------
# 2. Canonical Taxonomy Sets (fixes H3: reject unknown values explicitly)
# ---------------------------------------------------------------------------
VALID_PURPOSES: Set[str] = {
    "Commercials & TVCs",
    "Corporate Videos",
    "Educational & Training",
    "Explainer Videos",
    "Testimonial Videos",
    "Documentaries",
    "Event Videos",
    "Entertainment Videos",
}

VALID_FORMATS: Set[str] = {
    "Live-Action",
    "Animation",
    "Animation (2D / 3D)",
    "Motion Graphics",
    "Live Streaming",
    "360 & Interactive",
}

VALID_STYLE_VARIANTS: Set[str] = {
    "Montage Sequence",
    "Music Videos",
    "Commercial Promo",
    "Short-Form Edits / AMV",
    "Edits / AMV",
    "Sizzle Reel",
    "Sizzle Reel / Recap",
    "Narrative Continuity Sequence",
    "montage_sequence",
    "music_video",
    "commercial_promo",
    "short_form_edit",
    "sizzle_reel",
    "none",
}

VALID_MONTAGE_STYLES: Set[str] = {
    "montage_sequence",
    "music_video",
    "commercial_promo",
    "short_form_edit",
    "sizzle_reel",
    "none",
}

MONTAGE_STYLE_ALIAS_MAP: Dict[str, str] = {
    "Montage Sequence": "montage_sequence",
    "montage_sequence": "montage_sequence",
    "Music Videos": "music_video",
    "music_video": "music_video",
    "Commercial Promo": "commercial_promo",
    "commercial_promo": "commercial_promo",
    "Short-Form Edits / AMV": "short_form_edit",
    "Edits / AMV": "short_form_edit",
    "short_form_edit": "short_form_edit",
    "Sizzle Reel": "sizzle_reel",
    "Sizzle Reel / Recap": "sizzle_reel",
    "sizzle_reel": "sizzle_reel",
    "Narrative Continuity Sequence": "none",
    "none": "none",
}

VALID_PLATFORMS: Set[str] = {
    "tiktok_reels_shorts_9x16",
    "youtube_16x9",
    "feed_4x5",
    "square_1x1",
    "cinema_21x9",
}

VALID_DELIVERY_PROMISES: Set[str] = {
    "motion_led",
    "dialogue_led",
    "music_led",
    "info_led",
}

# Protected Arabic words that must NEVER receive a tatweel/kashida (ـ)
KASHIDA_PROTECTED_WORDS: Set[str] = {
    "الله",
    "لله",
    "اللهم",
    "بسم",
    "الرحمن",
    "الرحيم",
    "محمد",
    "لا",
    "لأ",
    "لإ",
    "لآ",
}

# Non-connecting right-hand Arabic letters (cannot place kashida after them)
NON_CONNECTING_ARABIC_LETTERS: Set[str] = set("اأإآدذرزوؤةءى")

# ---------------------------------------------------------------------------
# 3. Comprehensive Arabic Dialect Lexicon Matrix
# ---------------------------------------------------------------------------
DIALECT_LEXICON: Dict[str, List[str]] = {
    "BAHRAIN_URBAN": [
        "ويش",
        "شحالك",
        "شخبارك",
        "الحين",
        "جذي",
        "عفر",
        "يا خويي",
        "يا خوي",
        "يا بويي",
        "ما عليه",
        "هالگفرة",
        "امساعد",
        "يبيله",
    ],
    "SAUDI_NAJDI": [
        "وش دعوة",
        "وش رايك",
        "يا طويل العمر",
        "أبشر",
        "ابشر",
        "لا تشيل هم",
        "توّنا",
        "تونا",
        "وشلون",
        "الربع",
    ],
    "SAUDI_HIJAZI": [
        "ايش تبغى",
        "إيش تبغى",
        "تبغى",
        "دحين",
        "يا واد",
        "سيبك",
        "كيف حالك",
        "مرّة",
        "عشان",
        "بكرة",
    ],
    "KUWAITI": [
        "شنو هذا",
        "شدعوة",
        "صج",
        "وايد",
        "يبه",
        "معود",
        "يا معود",
        "چذي",
        "اشلونك",
    ],
    "EMIRATI": [
        "رمسة",
        "هيه",
        "ما يقصر",
        "غاوي",
        "طارش",
        "اشحالك",
        "يا ريال",
    ],
    "IRAQI": [
        "شلونك",
        "شكو ماكو",
        "هسه",
        "كلش",
        "آني",
        "اني",
        "يا خويه",
        "يا بويه",
        "گلب",
        "چبد",
        "بلياك",
        "اريد",
    ],
    "LEVANTINE": [
        "كيفك",
        "شو أخبارك",
        "شو اخبارك",
        "شو",
        "هلق",
        "هلأ",
        "كثير",
        "كتير",
        "منيح",
        "بدي",
        "هيك",
        "معقول",
    ],
    "EGYPTIAN": [
        "إزيك",
        "ازيك",
        "عامل إيه",
        "عامل ايه",
        "كويس",
        "دلوقتي",
        "كده",
        "عايز",
        "عاوز",
        "أوي",
        "اوي",
        "مفيش",
        "فين",
    ],
    "MSA": [
        "إن",
        "حيث",
        "لقد",
        "سوف",
        "الذي",
        "التي",
        "الذين",
        "هذا",
        "هذه",
        "ذلك",
        "تلك",
        "يعد",
        "تتميز",
        "منظومة",
        "استراتيجية",
        "بواسطة",
        "خلال",
        "يمكنك",
        "نقدم",
        "الأول",
        "الذكي",
        "الفخامة",
        "الذاكرة",
    ],
}

# ---------------------------------------------------------------------------
# 4. Complete 185+ Cinematic Slash Macro Dictionary
# ---------------------------------------------------------------------------
MACRO_DICTIONARY: Dict[str, str] = {
    # Camera Translation (Dolly / Truck / Pedestal / Crane)
    "/dollyin": "smooth physical camera dolly push-in toward subject on precision rails",
    "/pushin": "smooth physical camera push-in tightening on the subject",
    "/dollyout": "controlled physical camera dolly pull-back revealing surrounding environment",
    "/pullout": "smooth camera pull-back from close-up to medium-wide",
    "/slowpush": "ultra-slow creeping camera push-in building psychological tension",
    "/fastpush": "rapid high-energy dolly rush toward hero subject",
    "/pullback": "wide cinematic pull-back unveiling spatial scale",
    "/truckleft": "lateral camera truck left parallel to moving subject",
    "/truckright": "lateral camera truck right with foreground parallax",
    "/pedestalup": "vertical camera pedestal rise keeping level horizon",
    "/pedestaldown": "vertical camera pedestal descent to low perspective",
    "/craneup": "sweeping jib crane ascent rising above scene action",
    "/cranedown": "graceful crane descent settling into eye-level framing",
    "/orbit": "continuous 180-degree orbital camera arc around central subject",
    "/orbit_360": "continuous 360-degree circular gimbal orbit around the locked central subject",
    "/orbitleft": "smooth counter-clockwise orbital camera movement",
    "/orbitright": "smooth clockwise orbital camera movement",
    "/sloworbit": "contemplative low-speed 45-degree orbital camera drift",
    "/track": "stabilized gimbal tracking shot following subject stride",
    "/follow": "smooth Steadicam follow shot moving behind the subject",
    "/leadtrack": "backward-moving lead tracking shot facing walking subject",
    "/followtrack": "over-the-shoulder follow tracking shot behind subject",
    "/fpv": "agile FPV drone flight threading through architectural gaps",
    "/fpvdrone": "high-adrenaline acrobatic FPV drone trajectory weaving dynamically through space",
    "/drone_fly": "sweeping high-altitude cinematic aerial drone flight with smooth gimbal stabilization",
    "/fpvdive": "vertical FPV proximity dive down facade with motion blur",
    "/flythrough": "seamless spatial camera fly-through across rooms",
    "/steadicam": "fluid Steadicam long-take movement with natural inertia",
    "/gimbal": "weightless 3-axis gimbal stabilization",
    "/handheld": "organic cinema handheld micro-motion with documentary urgency",
    "/locked": "tripod-locked zero-translation static architectural composition",
    "/static": "strictly motionless locked-off camera frame",
    "/slider": "precision motorized slider horizontal parallax glide",
    "/bullet_time": "ultra-slow-motion 1000fps bullet-time freeze while camera orbits around suspended particles",
    "/seamless_loop": "final frame matches exact camera position and lighting of first frame for seamless infinite loop",
    "/closeup": "intimate close-up framing (CU) with shallow f/1.4 bokeh",
    "/extremecloseup": "extreme close-up (ECU) isolating fine micro-details",
    "/wide": "cinematic wide establishing shot (WS)",
    "/slowmotion": "high-frame-rate 120fps slow-motion capture",
    "/identitylock": "strict Character & Product Identity Lock via reference ingredients",
    "/lipsync": "biometric neural lip-sync locked to short breath-paced Arabic phrases",
    "/ar 9:16": "vertical 9:16 (1080x1920) mobile composition",
    "/ar 16:9": "widescreen 16:9 (1920x1080) cinema composition",
    "/ar 1:1": "square 1:1 (1080x1080) social feed composition",
    # Camera Rotation & Lens Mechanics
    "/panleft": "smooth tripod pan left across horizon",
    "/panright": "smooth tripod pan right following action vector",
    "/whippan": "high-velocity whip-pan transition with directional motion blur",
    "/tiltup": "gradual camera tilt upward revealing towering verticality",
    "/tiltdown": "gradual camera tilt downward onto tabletop hero details",
    "/dutch": "canted 18-degree Dutch roll angle creating dynamic tension",
    "/roll": "360-degree barrel roll rotation around optical axis",
    "/rackfocus": "precision focus pull shifting from foreground silhouette to sharp background subject",
    "/pullfocus": "smooth optical focus transition isolating hero expression",
    "/crashzoom": " vintage snap crash-zoom onto subject eyes",
    "/slowzoom": "subtle optical servo zoom-in maintaining flat perspective",
    "/vertigo": "contrazoom dolly-zoom effect warping background perspective",
    "/splitdiopter": "split-field diopter keeping both extreme foreground and deep background razor-sharp",
    "/tiltshift": "selective-plane tilt-shift lens miniature focus band",
    # Framing & Camera Angles
    "/ecu": "extreme close-up isolating microscopic texture and eye reflections",
    "/cu": "intimate close-up framing face and collarbones",
    "/mcu": "medium close-up chest-up conversational framing",
    "/ms": "medium waist-up narrative shot with hand gesture space",
    "/mws": "medium-wide knee-up cowboy framing",
    "/ws": "wide establishing shot anchoring subject inside environment",
    "/ews": "extreme wide epic landscape framing with miniature human scale",
    "/macro": "100mm 1:1 macro probe lens capturing sub-millimeter droplets and surface grain",
    "/probe": "Laowa 24mm bug-eye macro probe gliding through tight tabletop objects",
    "/lowangle": "heroic low-angle camera looking up at subject against sky",
    "/highangle": "elevated high-angle camera looking down on subject",
    "/birdseye": "strict 90-degree overhead zenith top-down knolling perspective",
    "/overhead": "direct 90-degree flat-lay tabletop overhead framing",
    "/wormseye": "ground-level worm's-eye perspective looking straight up",
    "/ots": "over-the-shoulder conversational depth framing",
    "/pov": "first-person subjective point-of-view perspective",
    "/twoshot": "balanced two-shot framing both subjects in shared plane",
    "/insert": "tight narrative insert shot of hands and object interaction",
    "/silhouette": "high-contrast backlit silhouette against glowing horizon",
    "/profile": "strict 90-degree side-profile portrait composition",
    # Lenses & Optical Format
    "/14mm": "14mm rectilinear ultra-wide lens with dramatic perspective lines",
    "/18mm": "18mm wide cinema prime with deep environmental context",
    "/24mm": "24mm wide-angle cinema prime with tactile proximity",
    "/28mm": "28mm street-documentary focal length with natural field of view",
    "/35mm": "35mm classic narrative cinema prime lens",
    "/50mm": "50mm human-vision standard prime with natural proportions",
    "/85mm": "85mm f/1.4 portrait prime with creamy circular bokeh",
    "/100mm": "100mm macro telephoto prime isolating fine craft details",
    "/135mm": "135mm telephoto compression stacking background layers",
    "/200mm": "200mm long-telephoto lens compressing distant atmosphere",
    "/anamorphic": "2x anamorphic cinema lens with oval bokeh and horizontal blue streak flares",
    "/vintage": "vintage Cooke Speed Panchro glass with warm edge halation",
    "/fisheye": "ultra-wide 8mm circular fisheye distortion",
    "/shallowdof": "f/1.2 razor-thin depth of field melting background into bokeh",
    "/deepdof": "f/11 deep-focus cinematography sharp from foreground to infinity",
    "/bokeh": "luminous specular background bokeh spheres",
    # Lighting & Atmosphere
    "/goldenhour": "warm low-angle golden-hour sunlight with long amber shadows",
    "/bluehour": "twilight cobalt blue-hour ambient sky with warm practical tungsten glow",
    "/chiaroscuro": "dramatic Caravaggio chiaroscuro high-contrast single-key lighting",
    "/rembrandt": "classic 45-degree Rembrandt key light with cheek triangle highlight",
    "/rimlight": "crisp hair and shoulder rim backlight separating subject from dark background",
    "/backlight": "powerful motivated逆光 backlight creating translucent edge glow",
    "/lowkey": "moody low-key cinema lighting with 8:1 shadow-to-fill ratio",
    "/highkey": "bright commercial high-key softbox studio illumination",
    "/neon": "cyberpunk bi-color magenta and cyan wet-pavement neon reflections",
    "/volumetric": "dense volumetric Tyndall light beams cutting through atmospheric haze",
    "/godrays": "crepuscular sunbeams streaming through architectural windows",
    "/candlelight": "warm flickering 1800K candlelight with organic shadow falloff",
    "/moonlight": "cool silvery 5600K moonlight casting crisp night shadows",
    "/softbox": "large diffused overhead octabox beauty lighting",
    "/hardlight": "direct theatrical Fresnel hard spotlight with razor-sharp shadow edges",
    "/practicals": "motivated warm in-frame practical lamps and sconces",
    "/neonnoir": "rain-slicked neo-noir sodium-vapor and teal neon contrast",
    "/studio": "controlled 3-point commercial studio cyclorama lighting",
    "/overcast": "giant natural overcast sky diffusion with zero harsh shadows",
    "/sunset": "fiery crimson-gold horizon sunset backlighting",
    "/sunrise": "crisp misty dawn sunrise with cool shadows and warm highlights",
    "/dappled": "organic dappled sunlight filtering through wind-blown tree leaves",
    "/cyberlight": "holographic RGB screen-glow illuminating subject face",
    "/firelight": "dynamic dancing amber hearth firelight glow",
    # Film Stocks, Cameras & Color Grades
    "/arri": "shot on ARRI Alexa 65 large-format sensor with wide dynamic range",
    "/red": "shot on RED V-Raptor 8K VV with crisp micro-contrast",
    "/venice": "shot on Sony Venice 2 8.6K dual-base ISO cinema camera",
    "/c500": "shot on Canon EOS C500 Mark II full-frame cinema system",
    "/kodak2383": "Kodak Vision3 500T 5219 film print emulation with Kodak 2383 LUT",
    "/fuji": "Fujifilm Eterna 250D soft pastel highlight roll-off",
    "/35mmfilm": "authentic 35mm photochemical film stock ISO 800 organic grain and halation",
    "/16mmfilm": "textured Super 16mm documentary film grain with gate weave",
    "/8mmfilm": "nostalgic Super 8mm home-movie Kodachrome texture",
    "/tealorange": "blockbuster complementary teal shadows and warm amber skin tones",
    "/bleachbypass": "gritty silver-retention bleach-bypass desaturated high-contrast grade",
    "/monochrome": "high-contrast Leica Monochrom silver-gelatin black and white",
    "/noir": "high-contrast classic 1940s film noir monochrome shadows",
    "/pastel": "Wes Anderson symmetrical warm pastel color palette",
    "/warmgold": "luxury royal gold and deep espresso warm commercial grade",
    "/cybergrade": "obsidian dark slate with electric cyan and violet accents",
    "/rec709": "true-to-life calibrated broadcast Rec.709 neutral color science",
    "/hdr": "16-stop high dynamic range specular highlights and deep shadow detail",
    "/vhs": "1990s analog VHS tape scanlines and chroma bleed",
    "/polaroid": "instant-film creamy highlights and warm faded blacks",
    # Motion, Speed & Physics
    "/slowmo": "120fps high-speed Phantom Flex slow-motion physics capture",
    "/240fps": "ultra-slow 240fps fluid micro-droplet suspension in mid-air",
    "/speedramp": "dynamic speed-ramp accelerating at 1.8x then dropping to 0.4x on impact",
    "/timelapse": "compressed hyper-timelapse of moving clouds and city light trails",
    "/hyperlapse": "stabilized moving-camera architectural hyperlapse",
    "/stopmotion": "tactile 12fps handcrafted Dragonframe stop-motion animation feel",
    "/exploded_view": "precision engineering exploded-view assembly floating in mid-air",
    "/morph": "seamless geometric liquid-metal morph transition between forms",
    "/matchcut": "frame-accurate geometric match-cut preserving subject silhouette",
    "/whipcut": "invisible whip-pan hidden cut on peak motion blur",
    "/jcut": "J-cut audio lead where next scene's sound enters 0.15s before visual cut",
    "/lcut": "L-cut audio trail where voiceover resonates over incoming B-roll",
    "/loop": "seamless infinite visual loop matching final frame to frame 0",
    "/parallax": "multi-plane 2.5D foreground/midground/background depth parallax",
    "/zerog": "weightless zero-gravity floating product choreography",
    # Weather, Particles & Environmental VFX
    "/rain": "heavy cinematic rain streaks with wet asphalt specular puddles",
    "/mist": "low-lying morning ground mist swirling around subject ankles",
    "/fog": "dense atmospheric fog diffusing distant streetlights",
    "/smoke": "wispy aromatic steam and incense plumes rising in slow motion",
    "/steam": "curling hot espresso steam catching warm rim backlight",
    "/sparks": "glowing鍛造 ember sparks drifting across dark foreground",
    "/dust": "illuminated floating dust motes dancing inside a sunbeam",
    "/snow": "gentle falling snowflakes catching warm shopfront light",
    "/wind": "dynamic breeze rippling fabric and hair with natural physics",
    "/waterdrop": "crystalline water splash crown frozen at peak surface tension",
    "/goldleaf": "shimmering 24k gold-leaf particles drifting in dark studio air",
    "/confetti": "celebratory metallic confetti shower in slow motion",
    "/lensflare": "subtle organic optical lens flare from warm key source",
    "/wetstreet": "mirror-like rain-soaked cobblestone reflections at night",
    "/sandstorm": "blowing golden desert dune sand particles catching low sun",
    # 3D, UI, Typography & Stage Styles
    "/3drender": "physically based Octane/Redshift 3D studio render with subsurface scattering",
    "/unreal5": "Unreal Engine 5 Lumen global illumination and Nanite micro-geometry",
    "/blender": "Blender 4.5 Cycles procedural shader and clean studio lighting",
    "/clay": "tactile matte claymation shader with subtle thumbprint micro-texture",
    "/lowpoly": "stylized geometric low-poly isometric diorama",
    "/cel": "hand-drawn 2D anime cel-shaded linework with dynamic smears",
    "/glassui": "frosted acrylic glassmorphism UI cards with specular borders",
    "/keynote": "Apple Keynote dark-mode precision typography and spring physics",
    "/blueprint": "technical CAD cyan-on-navy engineering blueprint schematic",
    "/inksketch": "expressive sumi-e black ink brush strokes on textured rice paper",
    "/papercut": "layered craft paper-cut shadowbox diorama with drop shadows",
    "/swiss": "International Typographic Style bold grid and asymmetric hierarchy",
    "/brutal": "neo-brutalist high-contrast raw Swiss grid with bold strokes",
    "/terminal": "crisp developer CLI terminal window with syntax highlighting",
    "/hologram": "translucent volumetric sci-fi holographic projection",
    "/kashida": "pixel-sliced Arabic tatweel typography extending behind subject head",
    "/headout": "subject head breaking out above card border for 3D depth pop",
    # Resolution, Aspect Ratio & Audio Flags
    "/4k": "ultra-sharp 4K UHD master resolution with pristine micro-texture",
    "/8k": "8K large-format master resolution with zero compression artifacts",
    "/60fps": "butter-smooth 60fps progressive motion cadence",
    "/24fps": "classic 24fps cinema shutter (180-degree shutter angle)",
    "/9x16": "vertical 9:16 (1080x1920) mobile-first social composition",
    "/16x9": "widescreen 16:9 (1920x1080) horizontal cinema composition",
    "/21x9": "ultra-wide 2.39:1 anamorphic theatrical widescreen",
    "/1x1": "square 1:1 (1080x1080) social feed composition",
    "/4x5": "portrait 4:5 (1080x1350) editorial feed composition",
    "/ar": "aspect ratio override flag",
    "/asmr": "hyper-detailed close-up ASMR acoustic foley (crisp pour, fizz, tap)",
    "/dolby": "wide spatial stereo soundstage with sub-bass impact",
    "/cleanplate": "clean background plate with 35% negative space for RTL Arabic overlays",
    "/safezone": "strict 9:16 platform safe-zone framing keeping central 80% clear of UI",
    "/ugc": "authentic creator-shot iPhone 16 Pro UGC natural daylight aesthetic",
    "/packshot": "hero commercial tabletop packshot with revolving specular rim light",
    "/knolling": "symmetrical 90-degree overhead knolling arrangement of components",
}
