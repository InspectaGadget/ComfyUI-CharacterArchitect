import hashlib
import json
import re
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "data" / "categories.json"

CONTENT_RATING_MAP = {
    "normal": "tasteful styling",
    "glamour": "glamorous styling",
    "sexy": "sensual but tasteful styling",
    "explicit": "explicit styling",
}

ENHANCE_REALISM_SUFFIX = "Captured as a spontaneous real-life photograph, casual and unstaged, with natural body language, ordinary environmental details, believable lighting falloff, realistic camera exposure, subtle sensor texture, imperfect but plausible composition, restrained post-processing, authentic skin, hair and fabric detail, and the quiet visual randomness of an actual moment."
ANTHRO_FURRY_PREFIX = ["furry skin", "furry body", "realistic fur", "realistic animal eyes", "anthropomorphic paw hands with fur-covered fingers, visible paw pads, and short natural claws"]
SPECIES_MODE_SUBJECT_MAP = {
    "Human": {
        "woman": "woman",
        "man": "man",
        "androgynous femboy": "androgynous femboy",
        "androgynous tomboy": "androgynous tomboy",
        "transgender woman": "transgender woman",
        "transgender man": "transgender man",
    },
    "Anthro Furry": {
        "woman": "anthropomorphic female furry",
        "man": "anthropomorphic male furry",
        "androgynous femboy": "anthropomorphic furry androgynous femboy",
        "androgynous tomboy": "anthropomorphic furry androgynous tomboy",
        "transgender woman": "anthropomorphic furry transgender woman",
        "transgender man": "anthropomorphic furry transgender man",
    },
}


# Deliberately assertive phenotype anchors. Each selected ethnicity resolves to one
# concrete instruction block; alternatives belong in the randomizer, not in prose.
ETHNICITY_PROMPTS = {
    "northern european": "Swedish, Norwegian, Danish, Finnish, Icelandic, distinctly Nordic facial features, softly rounded oval face, youthful soft facial structure, soft cheek fullness, open {eye_color} eyes, straight narrow nose with a soft refined bridge and rounded tip, medium soft lips, smooth jawline, fair skin with soft peach-golden undertones and natural skin texture, lightly sun-kissed complexion, golden blonde hair, northern european",
    "western european": "French, Belgian, Dutch, German, balanced rectangular face, moderate facial projection, broad forehead, structured cheekbones, {eye_color} deep-set eyes, straight medium-width nose with a defined bridge, medium lips, firm square jaw, fair beige skin with neutral undertones and natural skin texture, western european",
    "eastern european": "Polish, Ukrainian, Russian, Romanian, broad compact face, high wide cheekbones, moderate facial projection, pronounced brow bone, {eye_color} deep-set eyes, straight prominent nose with a high bridge, medium lips, broad angular jaw, pale skin with cool undertones and natural skin texture, eastern european",
    "southern european": "Italian, Greek, Spanish, Portuguese, distinctly Mediterranean southern european facial features, soft oval face, graceful facial projection, defined dark brows, expressive {eye_color} almond-shaped eyes, straight-to-softly-aquiline nose with a refined bridge, full soft lips, gently defined cheekbones, smooth tapered jaw, warm light-olive skin with golden undertones and natural skin texture, rich dark brown hair, southern european",
    "middle eastern": "Lebanese, Syrian, Iraqi, Iranian, distinctly Middle Eastern facial features, soft tapered oval face, graceful facial projection, defined dark brow structure, deep-set elongated {eye_color} almond-shaped eyes, large prominent softly convex nose with a high well-defined bridge and a substantial refined rounded tip, full soft lips, gently defined cheekbones, smooth tapered jaw, warm medium-olive skin with golden undertones and natural skin texture, rich dark brown to black hair, middle eastern",
    "north african": "Maghrebi, Moroccan, Algerian, Tunisian, Libyan, compact face with a broad upper structure and softly tapered lower face, moderate facial projection, high prominent cheekbones, defined dark eyebrows, large deep-set {eye_color} almond-shaped eyes, short broad nose with a clearly defined bridge, rounded tip and slightly flared nostrils, full lips, firm tapered jaw, deep warm olive-brown skin with golden undertones and natural skin texture, north african",
    "sub-saharan african": "Nigerian, Ghanaian, Senegalese, Congolese, broad powerful facial structure, strong facial projection, high prominent cheekbones, large {eye_color} almond-shaped eyes, broad nose with a low bridge and wide nostrils, very full lips, strong rounded jaw, deep dark-brown skin with warm undertones and natural skin texture, sub-saharan african",
    "east asian": "Chinese, Korean, Japanese, short broad face, very low facial projection, flat midface, high broad cheekbones, narrow hooded {eye_color} almond-shaped eyes with epicanthic folds, small flat nose with a low bridge, compact lips, soft rounded jaw, pale beige asian skin with neutral undertones and natural skin texture, east asian",
    "southeast asian": "Cambodian, Thai, Laotian, short compact face, low facial projection, softly broad facial structure, small slightly hooded {eye_color} almond-shaped eyes, small broad nose with a low bridge and slightly flared nostrils, rounded cheeks, rich deep-brown asian skin with warm undertones and natural skin texture, southeast asian",
    "south asian": "Indian, Pakistani, Bangladeshi, Sri Lankan, softly angular face with a tapered lower face, strong facial projection, large deep-set {eye_color} almond-shaped eyes, thick arched brow structure, long prominent nose with a high bridge and broad tip, full lips, pronounced cheekbones, firm defined jaw, rich deep-brown south asian skin with golden undertones and natural skin texture, south asian",
    "central asian": "Kazakh, Uzbek, Kyrgyz, Turkmen, strongly recognizable central asian facial features, broad smooth upper face with a softly elongated tapered lower face, low facial projection, shallow flat midface, full gently prominent forehead, extremely narrow and squashed eyes, exceptionally long slender oblique {eye_color} eyes sweeping upward toward the temples, long flattened eyelid contours, very low vertical eye opening, particularly elevated outer eye corners, shallow-set eyes close to the facial plane, subtle epicanthic folds, high-set gently arched eyebrows with generous smooth space above the eyes, soft lateral cheek fullness, short low-projection nose with a low bridge and rounded tip, short philtrum, softly full lips, delicate tapered jawline, refined compact chin, warm golden-tan central asian skin with natural skin texture, central asian",
    "latin american": "Peruvian, Bolivian, Ecuadorian, Andean Colombian, strongly recognizable Andean indigenous-mestizo facial features, short compact face, very low facial projection, flat midface, high broad cheekbones, small narrow slightly hooded {eye_color} almond-shaped eyes, small broad nose with a low bridge and rounded tip, medium lips, soft broad jaw, rich copper-brown skin with warm earthy undertones and natural skin texture, latin american",
    "afro-caribbean": "Haitian, Jamaican, Trinidadian, Barbadian, broad angular face, strong facial projection, high pronounced cheekbones, large {eye_color} almond-shaped eyes, broad nose with a low bridge and wide nostrils, very full lips, powerful defined jaw, rich deep-brown skin with warm undertones and natural skin texture, afro-caribbean",
}

LEGACY_ETHNICITY_MAP = {
    "mediterranean": "southern european",
    "latina": "latin american",
    "mixed heritage": None,
}

LEGACY_PORTRAIT_STYLE_MAP = {
    "bedroom selfie": "spontaneous handheld selfie",
}

LEGACY_PHOTOGRAPHIC_EFFECT_MAP = {
    "fisheye optical distortion": "fisheye",
    "Petzval swirling bokeh": None,
    "split-diopter depth effect": None,
}

LEGACY_CATEGORY_VALUE_MAPS = {
    "lens_style": {
        "smartphone camera look": None,
    },
    "lighting_style": {
        "candlelit ambiance": None,
    },
    "camera_direction": {
        "high-angle view": "pronounced high-angle view, with the camera positioned above the subject",
        "low-angle view": "pronounced low-angle view, with the camera positioned below the subject",
    },
    "cosplay_type": {
        "tailored businesswoman cosplay": "tailored businesswoman cosplay with a fitted blazer, collared blouse, tailored trousers or pencil skirt, and structured briefcase",
        "corporate secretary cosplay": "corporate secretary cosplay with a fitted blouse, high-waisted pencil skirt, narrow neck scarf, and office badge",
        "flight attendant cosplay": "flight attendant cosplay with a fitted uniform jacket, knee-length skirt, neck scarf, and small pillbox hat",
        "pin-up nurse cosplay": "pin-up nurse cosplay with a fitted nurse dress, short apron, nurse cap, and stethoscope",
        "doctor cosplay": "doctor cosplay with a buttoned medical coat over scrubs, stethoscope, and clipped identification badge",
        "lab scientist cosplay": "lab scientist cosplay with a buttoned laboratory coat, protective goggles, fitted gloves, and specimen clipboard",
        "teacher cosplay": "teacher cosplay with a collared blouse, fitted cardigan, pleated skirt, and a book held as a classroom prop",
        "librarian cosplay": "librarian cosplay with a modest collared blouse, long fitted skirt, soft cardigan, and a small stack of books",
        "maid cosplay": "maid cosplay with a fitted dress, contrasting apron, ruffled maid headband, and matching wrist cuffs",
        "chef cosplay": "chef cosplay with a double-breasted chef jacket, checked trousers, waist apron, and tall chef hat",
        "mechanic cosplay": "mechanic cosplay with fitted work coveralls, rolled sleeves, practical work gloves, and a compact tool belt",
        "cowgirl cosplay": "cowgirl cosplay with a fitted Western shirt, fringed vest, denim bottoms, cowboy hat, and Western boots",
        "pin-up police cosplay": "pin-up police cosplay with a fitted uniform dress, peaked police cap, chest badge, and utility belt with handcuffs",
        "military officer cosplay": "military officer cosplay with a structured uniform jacket, epaulettes, tailored bottoms, peaked cap, and ceremonial medals",
        "pirate captain cosplay": "pirate captain cosplay with a ruffled blouse, long captain coat, fitted trousers, waist sash, tricorn hat, and tall boots",
        "magician cosplay": "stage magician cosplay with a fitted tailcoat, waistcoat, bow tie, short cape, top hat, and formal gloves",
        "circus ringmaster cosplay": "circus ringmaster cosplay with a fitted tailcoat, structured waistcoat, high boots, top hat, and ceremonial baton",
        "bunny hostess cosplay": "bunny hostess cosplay with a strapless bunny suit, detachable collar and bow tie, wrist cuffs, tights, and decorative bunny ears",
        "adult academy uniform cosplay": "adult academy uniform cosplay with a fitted blazer, collared shirt, necktie, pleated skirt, and knee-high socks",
        "neko kawaii two-piece cosplay with ears tail and paw gloves": "neko kawaii furry-inspired two-piece cosplay with a cropped top, short bottoms, paw gloves, decorative cat ears placed on top of the head, and a cat tail",
        "cow print mini-skirt and bra cosplay with horns": "cow-print two-piece cosplay with a mini skirt, fitted bra top, bell collar, decorative horns placed on top of the head, and a cow tail",
        "sailor uniform cosplay": "sailor uniform cosplay with a sailor-collar blouse, tied neckerchief, pleated skirt, and knee-high socks",
        "cheerleader cosplay": "cheerleader cosplay with a fitted sleeveless uniform top, pleated athletic skirt, sneakers, and a pair of pom-poms",
        "schoolgirl cosplay": "adult school-uniform cosplay with a collared blouse, fitted blazer, pleated skirt, necktie, and knee-high socks",
        "cat burglar cosplay": "cat burglar cosplay with a fitted catsuit, slim utility belt, flexible gloves, soft boots, and a small eye mask",
        "race queen cosplay": "race queen cosplay with a fitted motorsport mini dress, sponsor-style panels, long gloves, and knee-high boots",
        "devil costume cosplay": "devil costume cosplay with a fitted bodysuit or corset dress, decorative horns on top of the head, pointed tail, small wings, and pitchfork prop",
        "angel costume cosplay": "angel costume cosplay with a flowing fitted dress, large feathered wings, a floating halo above the head, and delicate wrist cuffs",
        "vampire hostess cosplay": "vampire hostess cosplay with a fitted gothic dress, corset bodice, high collar, short cape, ornate choker, and subtle fangs",
        "playboy bunny-inspired cosplay": "playboy bunny-inspired cosplay with a strapless bunny suit, collar and bow tie, wrist cuffs, sheer tights, and tall decorative bunny ears",
    },
}

GLASSES_RANDOM_PRESENCE_POOL = [False] * 67 + [True] * 33
BAG_RANDOM_PRESENCE_POOL = [False] * 60 + [True] * 40
SCARF_RANDOM_PRESENCE_POOL = [False] * 70 + [True] * 30

# These pools guide ordinary Random without turning Character Architect into a
# strict outfit validator. Each compatibility pass deliberately keeps a small
# wild-card share so surprising combinations remain part of the node's voice.
SOFT_COMPATIBILITY_POOL = [True] * 85 + [False] * 15
HAIR_COMPATIBILITY_POOL = [True] * 75 + [False] * 25
NECKLINE_COMPATIBILITY_POOL = [True] * 90 + [False] * 10
PHOTO_COMPATIBILITY_POOL = [True] * 80 + [False] * 20

BOTTOM_LENGTH_POOLS = {
    "jeans": ["mid-length", "long", "long"],
    "skinny jeans": ["mid-length", "long", "long"],
    "trousers": ["knee-length", "mid-length", "long", "long"],
    "wide-leg pants": ["mid-length", "long", "long"],
    "flared pants": ["long"],
    "cargo pants": ["knee-length", "mid-length", "long", "long"],
    "shorts": ["very short", "short", "short", "knee-length"],
    "denim shorts": ["very short", "short", "short", "knee-length"],
    "mini skirt": ["very short", "short"],
    "pleated skirt": ["very short", "short", "knee-length", "mid-length", "long"],
    "skater skirt": ["very short", "short", "knee-length", "mid-length"],
    "leggings": ["knee-length", "mid-length", "long", "long"],
    "joggers": ["mid-length", "long", "long"],
    "leather pants": ["mid-length", "long", "long"],
    "long skirt": ["mid-length", "long", "long"],
}

NECKLINE_TYPES_BY_DEPTH = {
    "high neckline": ["crew neck", "halter neckline"],
    "modest neckline": ["crew neck", "scoop neck", "square neckline", "halter neckline"],
    "open neckline": ["scoop neck", "V-neck", "sweetheart neckline", "square neckline", "off-shoulder neckline", "halter neckline"],
    "low neckline": ["scoop neck", "V-neck", "sweetheart neckline", "square neckline", "off-shoulder neckline", "halter neckline", "plunging neckline"],
    "deep neckline": ["V-neck", "sweetheart neckline", "off-shoulder neckline", "plunging neckline"],
}

SIMPLE_PHOTO_LIGHTING = [
    "soft studio lighting", "window light", "golden-hour light",
    "overcast daylight", "backlit glow", "rim lighting",
    "subdued low-key lighting with deep natural shadows",
]

CATEGORY_TOOLTIPS = {
    "media_type": "Defines the base medium at the very beginning of the prompt. Lock it to protect it from section and global randomization.",
    "gender": "Defines the subject wording. It never hides or forbids body, clothing, makeup, or facial-hair choices.",
    "content_rating": "Adds a styling direction only; it does not hide categories or prohibit manual choices.",
    "portrait_style": "Controls framing and portrait intent. Under ordinary Random, close-up and headshot receive one-third weight when body details call for visibility. Close-up, headshot, bust, and half-body framing suppress ordinary Random footwear; manual and Forced Random footwear remain free.",
    "setting": "Adds a contextual environment. Ordinary Random is suppressed when a bicycle, horse, car, carousel, or skateboard pose already supplies its own scene context. Manual choices, Forced Random, and text override remain authoritative.",
    "lens_style": "Adds optical and depth-of-field characteristics after the scene description. Ordinary Random only softens a few known harsh lens/lighting collisions; 20% remain deliberately wild.",
    "shot_composition": "Controls spatial framing and subject placement. Tight crop suppresses ordinary Random footwear to avoid detached shoes; manual and Forced Random footwear remain free.",
    "pose_mood": "Adds the overall attitude of the pose without replacing the concrete body position.",
    "pose": "Defines a concrete body action or position. Cycling, horse riding, driving, carousel riding, and skateboarding suppress an ordinary Random setting to prevent incompatible scenery; manual settings, Forced Random, and text override still apply. Dancing keeps its normal setting. Gaze wording is minimized to avoid contradicting Eye expression.",
    "camera_direction": "Controls the camera-facing angle. Complex back-facing directions live in Pose to reduce random contradictions.",
    "lighting_style": "Describes the light independently from the setting. Ordinary Random softens a few known clashes with duotone, infrared, disposable, and cheap-digital treatments while preserving a 20% wild-card share.",
    "optical_effect": "Opt-in photographic treatment placed before Media type for stronger adherence. Protected from global random buttons; manual Random yields no effect 70% of the time, while Forced Random always selects an effect.",
    "origin_age": "Adds an adult age range near the subject introduction.",
    "origin_ethnicity": "With Ethnicity guidance enabled, this supplies the phenotype anchor and weighted eye, hair, and skin pools. Manual and Forced Random choices remain free.",
    "body_type": "General stature and frame. Combine it with Body physique for independent weight or muscularity, such as very petite + plump physique.",
    "body_physique": "Weight, softness, fitness, or muscular development. It is independent from Body type and feminine curves.",
    "body_feminine_curves": "Adds a curve distribution independently from stature and physique. It is never restricted by gender.",
    "body_hair": "Protected from one-click randomization because explicit presence or absence strongly changes the result. Manual Random and Forced Random remain available.",
    "skin_finish": "Protected from one-click randomization. Ethnicity guidance may use a neutral compatible pool when this field is manually set to Random.",
    "bust": "Independent morphological descriptor; no gender or content-rating restriction is applied.",
    "cleavage_depth": "Works with Cleavage type and clothing. When either neckline field is on ordinary Random, compatible depth/type pairs are favored 90% of the time; manual and Forced Random choices stay free.",
    "cleavage_type": "Neckline shape combined with Neckline depth. Ordinary Random favors coherent pairs; halter and off-shoulder are also suppressed when a complete cosplay already specifies a structured jacket, coat, blazer, uniform, or robe. Manual and Forced Random remain free.",
    "butt_shape": "Independent lower-body descriptor; combines with Body type, physique, curves, and thighs.",
    "thigh_shape": "Independent thigh descriptor; combines with the other body controls.",
    "expression": "General facial expression. Keep Eye expression separate when you want a specific gaze quality.",
    "eye_expression": "Adds only the gaze quality; pose descriptions avoid duplicating it wherever possible.",
    "face_shape": "With Ethnicity guidance enabled, Random is drawn from the selected ethnicity's compatible pool.",
    "jawline": "With Ethnicity guidance enabled, Random is drawn from a compatible pool. Manual values are never overridden.",
    "chin_shape": "With Ethnicity guidance enabled, Random is drawn from a compatible pool. Manual values are never overridden.",
    "eye_shape": "Morphological eye shape. Ethnicity guidance can constrain Random; Eye expression remains independent.",
    "eye_color": "With Ethnicity guidance active, None and Random use a weighted ethnicity-specific pool. Forced Random or a manual color deliberately overrides that pool.",
    "eyelashes": "Independent from eye shape, color, and makeup.",
    "eyebrows": "Ethnicity guidance can constrain Random. Manual eyebrow choices remain untouched.",
    "nose_shape": "Ethnicity guidance can constrain Random. Manual nose choices remain untouched.",
    "lip_shape": "Ethnicity guidance can constrain Random. Manual lip choices remain untouched.",
    "facial_hair": "Protected from one-click randomization because it strongly changes identity. Manual Random and Forced Random remain available.",
    "hair_color": "Ethnicity guidance can constrain Random. Manual hair colors remain untouched.",
    "hair_texture": "Ethnicity guidance can constrain Random. Ordinary Random softly reduces only the strongest material clashes; 25% of unusual combinations remain untouched.",
    "hair_style": "Combined with texture, cut, length, and bangs. Length-dependent styles are softly guided, while experimental undercuts and mixed constructions remain possible.",
    "hair_cut": "Independent from length and styling. Ordinary Random favors workable geometry 75% of the time rather than forbidding unconventional cuts.",
    "hair_length": "Modifies cut and styling. Ordinary Random usually supplies enough length for buns, ponytails, braids, and locs, but keeps a deliberate wild-card share.",
    "bangs_style": "Optional fringe descriptor. Ordinary Random only reduces the clearest cropped-hair conflicts; manual and Forced Random choices are untouched.",
    "tattoo_style": "Tattoo coverage and style; independent from clothing and content rating.",
    "makeup_eye": "Eye makeup is independent from eye expression and eyelashes.",
    "makeup_complexion": "Protected from one-click randomization to avoid forcing makeup onto every subject. Manual Random remains available.",
    "makeup_lips": "Lip makeup is independent from lip shape.",
    "nail_style": "Automatically suppressed when the resolved outfit contains full hand-covering gloves. Fingerless gloves and open handwear keep nail prompts.",
    "clothing_archetype": "Guides only fields left on Random and silently casts a compatible Outfit style. Manual choices are never overwritten; cosplay is not selected automatically by archetypes.",
    "outfit_style": "When Random under an archetype, it uses that archetype's style pool. A fixed manual value remains authoritative.",
    "top_type": "A concrete top activates the separates family and suppresses competing ordinary Random garment families. Forced Random bypasses that protection.",
    "top_color": "Colors modify an active top; a color alone does not activate the separates family.",
    "bottom_type": "A concrete bottom activates the separates family. Ordinary Random softly favors a workable length for that garment while retaining 15% atypical combinations.",
    "bottom_length": "Controls leg coverage. Ordinary Random uses hidden type-compatible pools; manual and Forced Random lengths remain unrestricted. Long and mid-length bottoms partially conceal hosiery.",
    "bottom_color": "Colors modify an active bottom; a color alone does not activate the separates family.",
    "lingerie_type": "Can be the main outfit or a rare underlayer. Ordinary/Casual/most archetype Random layering is 10%; Emo is 50%; Forced Random is always honored. Under cosplay, automatic layering is limited to Casual and Emo.",
    "lingerie_color": "Colors the selected lingerie or swimwear. A color alone does not activate lingerie.",
    "sleepwear_type": "A complete main garment family. When selected, ordinary Random dress, separates, lingerie, and cosplay families are suppressed.",
    "sleepwear_color": "Colors active sleepwear; a color alone does not activate it.",
    "cosplay_type": "Complete generic costume. Its source draw is weighted for fair per-costume probability. Ordinary Random hosiery, outfit styling, outerwear, belts, and footwear are suppressed; manual choices, Forced Random, and text override remain available.",
    "cosplay_franchise_western": "Complete Western franchise outfit. All cosplay sources share one family and are weighted for fair per-costume probability.",
    "cosplay_franchise_asian": "Complete Asian franchise outfit. All cosplay sources share one family and are weighted for fair per-costume probability.",
    "cosplay_color": "Applies only to generic cosplay. Franchise costumes keep their authored colors unless you make an explicit manual color choice elsewhere.",
    "hosiery": "Layers beneath bottoms when both are active. Ordinary Random is suppressed under cosplay; Forced Random bypasses this rule.",
    "hosiery_color": "Colors active hosiery. Long and mid-length bottoms mark it as partly visible. Every cosplay suppresses ordinary Random hosiery and its color; manual and Forced Random remain valid.",
    "dress_type": "A concrete dress activates the dress family and suppresses competing ordinary Random main garments.",
    "dress_color": "Colors an active dress; a color alone does not activate the dress family.",
    "outerwear": "An optional layer placed over the resolved main outfit. Ordinary Random is suppressed for every cosplay; manual, Forced Random, and override remain available.",
    "outerwear_color": "Colors active outerwear. Every cosplay neutralizes ordinary Random outerwear and its color unless explicitly forced or selected.",
    "outerwear_wearing_style": "Controls how active outerwear is worn. New nodes start on None; an active outerwear without a selected style is worn conventionally. Ordinary Random favors conventional wear, while Forced Random gives every supported position an equal chance.",
    "belt": "An optional accessory layer. Ordinary Random is suppressed for every cosplay; manual, Forced Random, and override remain available.",
    "belt_color": "Colors an active belt. Every cosplay suppresses an ordinary Random belt and its color; manual and Forced Random choices remain valid.",
    "footwear": "Optional footwear. Ordinary Random is suppressed for every cosplay and through three-quarter framing; it remains probabilistic in wider portraits. Manual, Forced Random, franchise-authored footwear, and text override remain valid.",
    "footwear_color": "Colors active footwear. When probabilistic Random footwear is omitted, its Random color is removed atomically. Manual footwear/colors, Forced Random, and text override remain valid.",
    "head_accessory": "Optional hair/head item. Ordinary Random is suppressed when a complete cosplay already specifies headwear; manual and Forced Random can deliberately layer both. Loc cuffs remain possible everywhere and receive a gentle boost with dreadlocks and braids.",
    "accessories_scarf": "Protected from one-click randomization. When deliberately left on ordinary Random, a scarf appears about 30% of the time; Forced Random always adds one.",
    "accessories_jewelry": "General jewelry styling; combines with the more specific necklace, earrings, bracelet, and rings fields.",
    "accessories_necklace": "Specific necklace choice; can be combined deliberately with general jewelry styling.",
    "accessories_earrings": "Specific earrings choice; independent from other jewelry.",
    "accessories_bracelet": "Specific wrist jewelry; full gloves may visually obscure it but do not silently remove a manual choice.",
    "accessories_rings": "Specific hand jewelry; full gloves may visually obscure it but do not silently remove a manual choice.",
    "accessories_glasses": "Ordinary Random produces no glasses 67% of the time and a concrete pair 33% of the time. Forced Random always selects concrete glasses.",
    "armwear": "Full hand-covering gloves automatically suppress Random nail styling. Fingerless and transparent/open armwear do not.",
    "accessories_bag": "Optional bag. Ordinary Random adds one about 40% of the time; archetypes guide its type. Forced Random and manual choices remain authoritative.",
}

OPTIONAL_TOOLTIPS = {
    "lock_media_type": "Protects Media type from the global and section randomization buttons.",
    "lock_gender": "Protects Gender from the global and section randomization buttons.",
    "lock_content_rating": "Protects Content rating from the global and section randomization buttons.",
    "ethnicity_guidance": "When activated, facial anatomy uses a strong anchor; Eye color on None or Random uses its weighted ethnicity pool. Forced Random and manual values deliberately override guidance.",
    "enhance_realism": "Appends a realism suffix about plausible lighting, exposure, texture, composition, and natural photographic imperfections.",
    "species_mode": "Anthro Furry adds a furry subject prefix. It does not remove human-oriented clothing or morphology controls.",
    "seed": "Every Random field has its own deterministic stream derived from this seed. Fixing one field no longer changes unrelated random fields.",
    "control_after_generate": "ComfyUI seed behavior after each run. Use fixed to preserve all resolved Random choices while editing selected fields.",
    "free_prompt": "Free text inserted at the selected position without changing any structured category.",
    "free_prompt_position": "Places Free prompt after the introduction, after makeup, or at the very end.",
    "override_field": "Selects the structured property replaced by Override text. A non-empty connected string has absolute priority over manual choices, Forced Random, guidance, archetypes, probabilities, and compatibility rules. Overriding a main garment type also clears competing main garment families so the text is guaranteed to appear.",
    "override_text": "Connect one STRING here. When non-empty, it replaces the property selected by Override field exactly as written.",
    "inspect_property": "Selects one resolved property to expose through Inspected Value for overlays, comparisons, and statistics. It reports the final value after every rule and override.",
}

# Forced Random means that the requested feature must actually be present.
# Ordinary Random may still resolve to an explicit absence such as no bag or
# bare legs; Forced Random removes those absence values from its local pool.
FORCED_RANDOM_EXCLUDED_VALUES = {
    "no bangs",
    "no visible eye makeup",
    "bare lips",
    "bare legs",
    "no visible belt",
    "bare feet",
    "no head accessory",
    "no scarf",
    "no necklace",
    "no earrings",
    "no bracelet",
    "no rings",
    "no glasses",
    "no armwear",
    "no bag",
}

# When guidance is active, random anatomy fields already described by the selected
# anchor are omitted instead of appending a contradictory second instruction.
# Fixed manual selections remain untouched and therefore always stay possible.
ETHNICITY_GUIDED_SUPPRESS_RANDOM = {
    "face_shape", "jawline", "chin_shape", "eye_shape", "eyebrows",
    "nose_shape", "lip_shape",
}

NEUTRAL_SKIN_FINISH_POOL = [
    "smooth skin", "natural skin texture", "lightly textured skin", "dewy skin",
    "matte skin", "glowing skin", "beauty marks", "mature skin",
]

ETHNICITY_RANDOM_POOLS = {
    "northern european": {
        "eye_color": ["blue"] * 40 + ["grey"] * 30 + ["green"] * 20 + ["hazel"] * 5 + ["light brown"] * 5,
        "hair_color": ["platinum blonde", "icy platinum", "blonde", "beige blonde", "golden blonde", "dark blonde", "light brown", "cool ash brown", "auburn"],
        "hair_texture": ["straight", "silky straight", "slightly wavy", "wavy"],
    },
    "western european": {
        "eye_color": ["brown"] * 25 + ["blue"] * 25 + ["hazel"] * 20 + ["green"] * 15 + ["grey"] * 15,
        "hair_color": ["blonde", "dark blonde", "light brown", "medium brown", "dark brown", "cool ash brown", "warm chestnut brown", "auburn"],
        "hair_texture": ["straight", "silky straight", "slightly wavy", "wavy", "curly"],
    },
    "eastern european": {
        "eye_color": ["blue"] * 30 + ["grey"] * 30 + ["green"] * 20 + ["hazel"] * 10 + ["brown"] * 10,
        "hair_color": ["blonde", "dark blonde", "light brown", "medium brown", "dark brown", "cool ash brown", "auburn"],
        "hair_texture": ["straight", "silky straight", "slightly wavy", "wavy"],
    },
    "southern european": {
        "eye_color": ["dark brown"] * 35 + ["brown"] * 30 + ["hazel"] * 15 + ["light brown"] * 10 + ["green"] * 10,
        "hair_color": ["black", "blue-black", "espresso brown", "dark chocolate brown", "dark brown", "warm chestnut brown", "auburn"],
        "hair_texture": ["straight", "slightly wavy", "wavy", "curly", "voluminous texture"],
    },
    "middle eastern": {
        "eye_color": ["dark brown"] * 40 + ["brown"] * 30 + ["hazel"] * 15 + ["honey"] * 5 + ["light brown"] * 10,
        "hair_color": ["black", "blue-black", "espresso brown", "dark chocolate brown", "dark brown"],
        "hair_texture": ["straight", "slightly wavy", "wavy", "curly", "voluminous texture"],
    },
    "north african": {
        "eye_color": ["dark brown"] * 40 + ["brown"] * 30 + ["hazel"] * 15 + ["honey"] * 5 + ["light brown"] * 10,
        "hair_color": ["black", "blue-black", "espresso brown", "dark chocolate brown", "dark brown"],
        "hair_texture": ["straight", "slightly wavy", "wavy", "curly", "tightly curled", "voluminous texture"],
    },
    "sub-saharan african": {
        "eye_color": ["dark brown"] * 60 + ["brown"] * 30 + ["black"] * 10,
        "hair_color": ["black", "blue-black", "espresso brown", "dark brown"],
        "hair_texture": ["curly", "tightly curled", "coily", "voluminous texture"],
    },
    "east asian": {
        "eye_color": ["dark brown"] * 55 + ["brown"] * 35 + ["black"] * 10,
        "hair_color": ["black", "blue-black", "espresso brown", "dark brown"],
        "hair_texture": ["straight", "silky straight", "slightly wavy"],
    },
    "southeast asian": {
        "eye_color": ["dark brown"] * 55 + ["brown"] * 35 + ["black"] * 10,
        "hair_color": ["black", "blue-black", "espresso brown", "dark brown"],
        "hair_texture": ["straight", "silky straight", "slightly wavy", "wavy"],
    },
    "south asian": {
        "eye_color": ["dark brown"] * 45 + ["brown"] * 30 + ["black"] * 10 + ["honey"] * 10 + ["hazel"] * 5,
        "hair_color": ["black", "blue-black", "espresso brown", "dark chocolate brown", "dark brown"],
        "hair_texture": ["straight", "silky straight", "slightly wavy", "wavy", "curly", "voluminous texture"],
    },
    "central asian": {
        "eye_color": ["dark brown"] * 40 + ["brown"] * 30 + ["hazel"] * 15 + ["black"] * 15,
        "hair_color": ["black", "blue-black", "espresso brown", "dark brown", "medium brown", "cool ash brown"],
        "hair_texture": ["straight", "silky straight", "slightly wavy", "wavy"],
    },
    "latin american": {
        "eye_color": ["dark brown"] * 50 + ["brown"] * 35 + ["honey"] * 5 + ["black"] * 10,
        "hair_color": ["black", "blue-black", "espresso brown", "dark chocolate brown", "dark brown"],
        "hair_texture": ["straight", "silky straight", "slightly wavy", "wavy", "voluminous texture"],
    },
    "afro-caribbean": {
        "eye_color": ["dark brown"] * 55 + ["brown"] * 30 + ["black"] * 10 + ["honey"] * 5,
        "hair_color": ["black", "blue-black", "espresso brown", "dark brown"],
        "hair_texture": ["curly", "tightly curled", "coily", "voluminous texture"],
    },
}

CLOTHING_ARCHETYPE_CONFIG = {'Classy Chic': {'main_modes': ['separates', 'dress'],
                 'outfit_style': ['tailored chic style',
                                  'minimalist monochrome style',
                                  'light academia style',
                                  'dark academia style'],
                 'top_type': ['blouse',
                              'button-up shirt',
                              'fitted top',
                              'sweater',
                              'cardigan',
                              'waistcoat',
                              'lace-trim camisole'],
                 'top_color': ['black',
                               'white',
                               'cream',
                               'beige',
                               'camel',
                               'brown',
                               'grey',
                               'charcoal',
                               'navy',
                               'burgundy',
                               'ribbed knit texture',
                               'satin sheen',
                               'silky floral pattern'],
                 'bottom_type': ['trousers',
                                 'wide-leg pants',
                                 'flared pants',
                                 'mini skirt',
                                 'pleated skirt',
                                 'long skirt'],
                 'bottom_length': ['knee-length', 'mid-length', 'long'],
                 'bottom_color': ['black',
                                  'white',
                                  'cream',
                                  'beige',
                                  'camel',
                                  'brown',
                                  'grey',
                                  'charcoal',
                                  'navy',
                                  'burgundy',
                                  'corduroy texture',
                                  'velvet texture',
                                  'satin sheen'],
                 'dress_type': ['wrap dress',
                                'midi dress',
                                'shirt dress',
                                'sweater dress',
                                'satin dress',
                                'slip dress',
                                'maxi dress'],
                 'dress_color': ['black',
                                 'white',
                                 'cream',
                                 'beige',
                                 'camel',
                                 'navy',
                                 'burgundy',
                                 'red',
                                 'silky floral pattern',
                                 'velvet texture',
                                 'satin sheen'],
                 'outerwear': ['blazer', 'long coat', 'trench coat', 'cardigan', 'bolero'],
                 'belt': ['no visible belt', 'leather belt', 'wide waist belt'],
                 'footwear': ['heels',
                              'loafers',
                              'ankle boots',
                              'chelsea boots',
                              'strappy heels',
                              'Mary Janes',
                              'Oxford shoes'],
                 'footwear_color': ['black', 'white', 'cream', 'beige', 'camel', 'brown', 'navy', 'burgundy'],
                 'hosiery': ['sheer tights', 'opaque tights', 'bare legs'],
                 'lingerie_type': ['bralette and briefs set', 'satin lingerie set', 'high-waist lingerie set'],
                 'lingerie_color': ['black',
                                    'white',
                                    'cream',
                                    'red',
                                    'burgundy',
                                    'satin sheen',
                                    'lace-textured finish'],
                 'head_accessory': ['no head accessory',
                                    'beret',
                                    'padded headband',
                                    'pearl hair clips',
                                    'jeweled hair pins',
                                    'claw clip'],
                 'accessories_scarf': ['no scarf', 'silk scarf', 'neck ribbon'],
                 'accessories_jewelry': ['minimal jewelry',
                                         'delicate jewelry',
                                         'pearl jewelry',
                                         'gold-toned jewelry',
                                         'silver-toned jewelry'],
                 'accessories_necklace': ['no necklace',
                                          'delicate chain necklace',
                                          'pearl necklace',
                                          'pendant necklace',
                                          'locket necklace'],
                 'accessories_earrings': ['no earrings', 'stud earrings', 'pearl earrings', 'drop earrings'],
                 'accessories_bracelet': ['no bracelet', 'delicate bracelet', 'bangle bracelet'],
                 'accessories_rings': ['no rings', 'single ring', 'stacked rings'],
                 'accessories_glasses': ['no glasses',
                                         'thin metal round eyeglasses',
                                         'thin oval eyeglasses',
                                         'thin rectangular eyeglasses',
                                         'cat-eye eyeglasses',
                                         'rimless eyeglasses',
                                         'cat-eye sunglasses'],
                 'armwear': ['no armwear', 'lace arm sleeves'],
                 'accessories_bag': ['no bag', 'handbag', 'shoulder bag', 'clutch bag', 'structured handbag']},
 'Casual Everyday': {'main_modes': ['separates', 'dress'],
                     'outfit_style': ['contemporary casualwear',
                                      'minimalist monochrome style',
                                      'preppy style',
                                      'Y2K fashion'],
                     'top_type': ['t-shirt',
                                  'cropped t-shirt',
                                  'tank top',
                                  'fitted top',
                                  'button-up shirt',
                                  'blouse',
                                  'hoodie',
                                  'cardigan',
                                  'sweater',
                                  'polo shirt',
                                  'graphic baby tee'],
                     'top_color': ['black',
                                   'white',
                                   'cream',
                                   'beige',
                                   'brown',
                                   'grey',
                                   'navy',
                                   'blue',
                                   'green',
                                   'red',
                                   'pink',
                                   'striped pattern',
                                   'polka-dot print',
                                   'ribbed knit texture'],
                     'bottom_type': ['jeans',
                                     'skinny jeans',
                                     'wide-leg pants',
                                     'cargo pants',
                                     'shorts',
                                     'denim shorts',
                                     'mini skirt',
                                     'pleated skirt',
                                     'leggings',
                                     'joggers'],
                     'bottom_length': ['very short', 'short', 'knee-length', 'mid-length', 'long'],
                     'bottom_color': ['black',
                                      'white',
                                      'cream',
                                      'beige',
                                      'brown',
                                      'grey',
                                      'charcoal',
                                      'navy',
                                      'blue',
                                      'olive',
                                      'striped pattern',
                                      'corduroy texture'],
                     'dress_type': ['wrap dress', 'mini dress', 'midi dress', 'shirt dress', 'sweater dress'],
                     'dress_color': ['black',
                                     'white',
                                     'cream',
                                     'beige',
                                     'navy',
                                     'blue',
                                     'green',
                                     'red',
                                     'pink',
                                     'silky floral pattern',
                                     'striped pattern',
                                     'polka-dot print'],
                     'outerwear': ['cardigan',
                                   'denim jacket',
                                   'cropped jacket',
                                   'bomber jacket',
                                   'trench coat',
                                   'puffer jacket'],
                     'belt': ['no visible belt', 'leather belt'],
                     'footwear': ['sneakers',
                                  'canvas sneakers',
                                  'ankle boots',
                                  'loafers',
                                  'Mary Janes',
                                  'chelsea boots',
                                  'sandals'],
                     'footwear_color': ['black', 'white', 'cream', 'beige', 'brown', 'grey', 'navy', 'blue'],
                     'hosiery': ['sheer tights',
                                 'opaque tights',
                                 'knee-high socks',
                                 'ankle socks',
                                 'bare legs'],
                     'lingerie_type': ['simple bralette underlayer', 'visible bra straps'],
                     'lingerie_color': ['black', 'white', 'grey', 'pink', 'blue', 'lace-textured finish'],
                     'head_accessory': ['no head accessory',
                                        'beanie',
                                        'baseball cap',
                                        'headband',
                                        'decorative hair clips',
                                        'claw clip'],
                     'accessories_scarf': ['no scarf', 'knit scarf', 'silk scarf'],
                     'accessories_jewelry': ['minimal jewelry',
                                             'delicate jewelry',
                                             'silver-toned jewelry',
                                             'gold-toned jewelry'],
                     'accessories_necklace': ['no necklace',
                                              'delicate chain necklace',
                                              'pendant necklace',
                                              'locket necklace'],
                     'accessories_earrings': ['no earrings', 'stud earrings', 'hoop earrings'],
                     'accessories_bracelet': ['no bracelet', 'delicate bracelet', 'chain bracelet'],
                     'accessories_rings': ['no rings', 'single ring', 'multiple rings'],
                     'accessories_glasses': ['no glasses',
                                             'thin metal round eyeglasses',
                                             'thick round acetate eyeglasses',
                                             'thin rectangular eyeglasses',
                                             'square eyeglasses',
                                             'aviator sunglasses',
                                             'sunglasses resting on the head'],
                     'armwear': ['no armwear'],
                     'accessories_bag': ['no bag', 'shoulder bag', 'crossbody bag', 'tote bag', 'backpack']},
 'Streetwear': {'main_modes': ['separates'],
                'outfit_style': ['streetwear styling', 'techwear styling', 'Y2K fashion', 'soft grunge styling'],
                'top_type': ['hoodie',
                             'cropped t-shirt',
                             'crop top',
                             'tank top',
                             'graphic baby tee',
                             'fitted graphic top',
                             'band tee',
                             'sweater'],
                'top_color': ['black',
                              'white',
                              'grey',
                              'charcoal',
                              'navy',
                              'blue',
                              'green',
                              'olive',
                              'red',
                              'purple',
                              'geometric print',
                              'striped pattern',
                              'animal print'],
                'bottom_type': ['wide-leg pants',
                                'cargo pants',
                                'jeans',
                                'shorts',
                                'denim shorts',
                                'leggings',
                                'joggers',
                                'leather pants'],
                'bottom_length': ['short', 'knee-length', 'long'],
                'bottom_color': ['black',
                                 'white',
                                 'grey',
                                 'charcoal',
                                 'navy',
                                 'blue',
                                 'green',
                                 'olive',
                                 'brown',
                                 'geometric print'],
                'outerwear': ['bomber jacket',
                              'oversized coat',
                              'puffer jacket',
                              'denim jacket',
                              'biker jacket',
                              'cropped jacket'],
                'belt': ['no visible belt', 'chain belt', 'utility belt', 'studded belt'],
                'footwear': ['sneakers',
                             'chunky sneakers',
                             'canvas sneakers',
                             'combat boots',
                             'platform shoes',
                             'ankle boots'],
                'footwear_color': ['black', 'white', 'grey', 'charcoal', 'navy', 'blue', 'red', 'green'],
                'hosiery': ['opaque tights',
                            'knee-high socks',
                            'over-the-knee socks',
                            'ankle socks',
                            'bare legs'],
                'head_accessory': ['no head accessory', 'beanie', 'baseball cap', 'hood'],
                'accessories_scarf': ['no scarf', 'oversized scarf', 'knit scarf'],
                'accessories_jewelry': ['layered jewelry', 'statement jewelry', 'silver-toned jewelry'],
                'accessories_necklace': ['no necklace',
                                         'layered necklaces',
                                         'layered chain necklace',
                                         'choker necklace'],
                'accessories_earrings': ['no earrings', 'hoop earrings', 'ear cuffs', 'chain earrings'],
                'accessories_bracelet': ['no bracelet', 'chain bracelet', 'stacked bracelets', 'cuff bracelet'],
                'accessories_rings': ['no rings', 'multiple rings', 'stacked rings', 'silver rings'],
                'accessories_glasses': ['no glasses',
                                        'rectangular sunglasses',
                                        'sport wraparound sunglasses',
                                        'mirrored sunglasses',
                                        'tinted fashion sunglasses',
                                        'futuristic visor glasses'],
                'armwear': ['no armwear', 'mesh fingerless sleeves', 'detached sleeves'],
                'accessories_bag': ['no bag', 'crossbody bag', 'backpack', 'shoulder bag', 'chain-strap bag']},
 'Romantic / Feminine Soft': {'main_modes': ['separates', 'dress'],
                              'outfit_style': ['soft feminine styling',
                                               'romantic lace styling',
                                               'light academia style',
                                               'bohemian styling'],
                              'top_type': ['blouse',
                                           'lace top',
                                           'cardigan',
                                           'sweater',
                                           'lace-trim camisole',
                                           'fitted top'],
                              'top_color': ['white',
                                            'cream',
                                            'beige',
                                            'pink',
                                            'mauve',
                                            'blue',
                                            'purple',
                                            'silky floral pattern',
                                            'polka-dot print',
                                            'lace-textured finish',
                                            'ribbed knit texture'],
                              'bottom_type': ['pleated skirt',
                                              'skater skirt',
                                              'long skirt',
                                              'mini skirt',
                                              'wide-leg pants'],
                              'bottom_length': ['short', 'knee-length', 'mid-length', 'long'],
                              'bottom_color': ['white',
                                               'cream',
                                               'beige',
                                               'pink',
                                               'mauve',
                                               'blue',
                                               'purple',
                                               'silky floral pattern',
                                               'polka-dot print',
                                               'lace-textured finish'],
                              'dress_type': ['wrap dress',
                                             'mini dress',
                                             'midi dress',
                                             'maxi dress',
                                             'lace dress',
                                             'slip dress'],
                              'dress_color': ['white',
                                              'cream',
                                              'beige',
                                              'pink',
                                              'mauve',
                                              'blue',
                                              'purple',
                                              'silky floral pattern',
                                              'polka-dot print',
                                              'lace-textured finish'],
                              'outerwear': ['cardigan', 'bolero', 'trench coat', 'cape'],
                              'belt': ['no visible belt', 'wide waist belt', 'leather belt'],
                              'footwear': ['Mary Janes', 'heels', 'strappy heels', 'sandals', 'ankle boots'],
                              'footwear_color': ['white', 'cream', 'beige', 'pink', 'mauve', 'brown', 'burgundy'],
                              'hosiery': ['sheer tights',
                                          'opaque tights',
                                          'knee-high socks',
                                          'over-the-knee socks',
                                          'bare legs'],
                              'lingerie_type': ['bralette and briefs set',
                                                'lace lingerie set',
                                                'high-waist lingerie set'],
                              'lingerie_color': ['white',
                                                 'cream',
                                                 'pink',
                                                 'mauve',
                                                 'lace-textured finish',
                                                 'silky floral pattern'],
                              'head_accessory': ['no head accessory',
                                                 'headband',
                                                 'padded headband',
                                                 'decorative hair clips',
                                                 'decorative barrettes',
                                                 'pearl hair clips',
                                                 'bow hair accessory',
                                                 'ribbon headband'],
                              'accessories_scarf': ['no scarf', 'sheer scarf', 'silk scarf', 'neck ribbon'],
                              'accessories_jewelry': ['delicate jewelry', 'pearl jewelry', 'minimal jewelry'],
                              'accessories_necklace': ['no necklace',
                                                       'delicate chain necklace',
                                                       'pearl necklace',
                                                       'locket necklace',
                                                       'soft ribbon choker'],
                              'accessories_earrings': ['no earrings',
                                                       'stud earrings',
                                                       'pearl earrings',
                                                       'drop earrings'],
                              'accessories_bracelet': ['no bracelet', 'delicate bracelet', 'bangle bracelet'],
                              'accessories_rings': ['no rings', 'single ring', 'stacked rings'],
                              'accessories_glasses': ['no glasses',
                                                      'thin metal round eyeglasses',
                                                      'thin oval eyeglasses',
                                                      'cat-eye eyeglasses',
                                                      'rose-tinted glasses'],
                              'armwear': ['no armwear', 'lace arm sleeves'],
                              'accessories_bag': ['no bag', 'handbag', 'mini bag', 'shoulder bag', 'chain-strap bag']},
 'Glam / Night Out': {'main_modes': ['dress', 'separates'],
                      'outfit_style': ['glamorous eveningwear styling',
                                       'glam rock styling',
                                       'avant-garde fashion',
                                       'fetish-inspired fashion details'],
                      'top_type': ['fitted top',
                                   'crop top',
                                   'mesh top',
                                   'lace top',
                                   'halter top',
                                   'tube top',
                                   'corset top',
                                   'lace-trim camisole',
                                   'cropped camisole'],
                      'top_color': ['black',
                                    'white',
                                    'red',
                                    'burgundy',
                                    'pink',
                                    'purple',
                                    'gold',
                                    'silver',
                                    'velvet texture',
                                    'satin sheen',
                                    'lace-textured finish',
                                    'animal print'],
                      'bottom_type': ['mini skirt', 'leather pants', 'skinny jeans', 'flared pants', 'shorts'],
                      'bottom_length': ['very short', 'short', 'long'],
                      'bottom_color': ['black',
                                       'white',
                                       'red',
                                       'burgundy',
                                       'purple',
                                       'gold',
                                       'silver',
                                       'velvet texture',
                                       'satin sheen',
                                       'animal print'],
                      'dress_type': ['bodycon dress',
                                     'mini dress',
                                     'slip dress',
                                     'satin dress',
                                     'asymmetrical dress',
                                     'corset dress'],
                      'dress_color': ['black',
                                      'white',
                                      'red',
                                      'burgundy',
                                      'pink',
                                      'purple',
                                      'gold',
                                      'silver',
                                      'velvet texture',
                                      'satin sheen',
                                      'animal print'],
                      'outerwear': ['blazer', 'biker jacket', 'cropped jacket', 'long coat', 'bolero'],
                      'belt': ['no visible belt', 'chain belt', 'corset belt', 'wide waist belt'],
                      'footwear': ['heels',
                                   'stilettos',
                                   'strappy heels',
                                   'thigh-high boots',
                                   'knee-high boots',
                                   'platform boots'],
                      'footwear_color': ['black',
                                         'white',
                                         'red',
                                         'burgundy',
                                         'gold',
                                         'silver',
                                         'animal print',
                                         'satin sheen'],
                      'hosiery': ['sheer tights',
                                  'opaque tights',
                                  'patterned tights',
                                  'fishnet tights',
                                  'thigh-high stockings',
                                  'bare legs'],
                      'lingerie_type': ['bralette and briefs set',
                                        'lace lingerie set',
                                        'satin lingerie set',
                                        'mesh lingerie set',
                                        'strappy cutout lingerie set',
                                        'bodysuit lingerie'],
                      'lingerie_color': ['black',
                                         'white',
                                         'red',
                                         'burgundy',
                                         'hot pink',
                                         'purple',
                                         'gold',
                                         'silver',
                                         'lace-textured finish',
                                         'satin sheen'],
                      'head_accessory': ['no head accessory', 'jeweled hair pins', 'padded headband', 'veil'],
                      'accessories_scarf': ['no scarf', 'sheer scarf', 'choker scarf'],
                      'accessories_jewelry': ['statement jewelry',
                                              'gold-toned jewelry',
                                              'silver-toned jewelry',
                                              'layered jewelry'],
                      'accessories_necklace': ['no necklace',
                                               'choker necklace',
                                               'layered chain necklace',
                                               'pearl necklace'],
                      'accessories_earrings': ['no earrings',
                                               'hoop earrings',
                                               'drop earrings',
                                               'statement earrings',
                                               'chain earrings'],
                      'accessories_bracelet': ['no bracelet', 'bangle bracelet', 'chain bracelet', 'cuff bracelet'],
                      'accessories_rings': ['no rings', 'multiple rings', 'statement ring', 'stacked rings'],
                      'accessories_glasses': ['no glasses',
                                              'oversized sunglasses',
                                              'cat-eye sunglasses',
                                              'tinted fashion sunglasses',
                                              'sunglasses resting on the head'],
                      'armwear': ['no armwear', 'mesh fingerless sleeves', 'lace arm sleeves'],
                      'accessories_bag': ['no bag', 'clutch bag', 'mini bag', 'chain-strap bag', 'structured handbag']},
 'Gothic / Dark Romantic': {'main_modes': ['dress', 'separates'],
                            'outfit_style': ['dark romantic styling',
                                             'contemporary gothic fashion',
                                             'dark academia style',
                                             'visual kei styling',
                                             'glam rock styling'],
                            'top_type': ['lace top',
                                         'mesh top',
                                         'corset top',
                                         'fitted top',
                                         'blouse',
                                         'lace-trim camisole'],
                            'top_color': ['black',
                                          'charcoal',
                                          'burgundy',
                                          'red',
                                          'purple',
                                          'velvet texture',
                                          'lace-textured finish',
                                          'satin sheen'],
                            'bottom_type': ['mini skirt',
                                            'long skirt',
                                            'leather pants',
                                            'skinny jeans',
                                            'pleated skirt'],
                            'bottom_length': ['very short', 'short', 'knee-length', 'mid-length', 'long'],
                            'bottom_color': ['black',
                                             'charcoal',
                                             'burgundy',
                                             'red',
                                             'purple',
                                             'velvet texture',
                                             'lace-textured finish',
                                             'plaid tartan pattern'],
                            'dress_type': ['gothic dress',
                                           'lace dress',
                                           'corset dress',
                                           'maxi dress',
                                           'mini dress',
                                           'slip dress'],
                            'dress_color': ['black',
                                            'charcoal',
                                            'burgundy',
                                            'red',
                                            'purple',
                                            'velvet texture',
                                            'lace-textured finish'],
                            'outerwear': ['long coat', 'cape', 'biker jacket', 'military coat', 'bolero'],
                            'belt': ['no visible belt', 'corset belt', 'studded belt', 'chain belt'],
                            'footwear': ['platform boots',
                                         'combat boots',
                                         'thigh-high boots',
                                         'knee-high boots',
                                         'heels',
                                         'Mary Janes'],
                            'footwear_color': ['black', 'charcoal', 'burgundy', 'red', 'purple', 'velvet texture'],
                            'hosiery': ['opaque tights',
                                        'patterned tights',
                                        'fishnet tights',
                                        'thigh-high stockings',
                                        'ripped tights',
                                        'opaque thigh-high socks'],
                            'lingerie_type': ['lace lingerie set',
                                              'mesh lingerie set',
                                              'corset lingerie set',
                                              'strappy harness lingerie set',
                                              'bodysuit lingerie'],
                            'lingerie_color': ['black', 'red', 'burgundy', 'purple', 'lace-textured finish'],
                            'head_accessory': ['no head accessory', 'veil', 'hood', 'jeweled hair pins'],
                            'accessories_scarf': ['no scarf', 'choker scarf', 'sheer scarf'],
                            'accessories_jewelry': ['gothic jewelry',
                                                    'silver-toned jewelry',
                                                    'statement jewelry',
                                                    'layered jewelry'],
                            'accessories_necklace': ['no necklace',
                                                     'choker necklace',
                                                     'lace choker',
                                                     'layered chain necklace',
                                                     'pendant necklace'],
                            'accessories_earrings': ['no earrings',
                                                     'cross earrings',
                                                     'chain earrings',
                                                     'ear cuffs',
                                                     'drop earrings'],
                            'accessories_bracelet': ['no bracelet',
                                                     'cuff bracelet',
                                                     'studded bracelet',
                                                     'chain bracelet'],
                            'accessories_rings': ['no rings', 'multiple rings', 'silver rings', 'statement ring'],
                            'accessories_glasses': ['no glasses',
                                                    'small round sunglasses',
                                                    'cat-eye sunglasses',
                                                    'purple-tinted glasses'],
                            'armwear': ['no armwear',
                                        'lace arm sleeves',
                                        'mesh fingerless sleeves',
                                        'detached sleeves'],
                            'accessories_bag': ['no bag', 'chain-strap bag', 'clutch bag', 'shoulder bag']},
 'Emo / Scene / Alt': {'main_modes': ['separates', 'dress'],
                       'outfit_style': ['modern emo styling',
                                        'scene queen styling',
                                        'mall emo styling',
                                        'MySpace-era emo styling',
                                        'alternative Y2K emo styling',
                                        'cute punk scene styling',
                                        'soft grunge styling',
                                        'punk-inspired fashion'],
                       'top_type': ['mesh top',
                                    'graphic baby tee',
                                    'fitted graphic top',
                                    'band tee',
                                    'cropped t-shirt',
                                    'crop top',
                                    'lace-trim camisole',
                                    'cropped camisole',
                                    'tank top'],
                       'top_color': ['black',
                                     'white',
                                     'red',
                                     'pink',
                                     'purple',
                                     'teal',
                                     'green',
                                     'striped pattern',
                                     'plaid tartan pattern',
                                     'animal print',
                                     'heart print',
                                     'lace-textured finish'],
                       'bottom_type': ['mini skirt',
                                       'shorts',
                                       'denim shorts',
                                       'skinny jeans',
                                       'leather pants',
                                       'pleated skirt'],
                       'bottom_length': ['very short', 'short', 'long'],
                       'bottom_color': ['black',
                                        'red',
                                        'pink',
                                        'purple',
                                        'teal',
                                        'green',
                                        'striped pattern',
                                        'plaid tartan pattern',
                                        'animal print'],
                       'dress_type': ['mini dress', 'bodycon dress', 'gothic dress', 'asymmetrical dress'],
                       'dress_color': ['black',
                                       'red',
                                       'pink',
                                       'purple',
                                       'striped pattern',
                                       'plaid tartan pattern',
                                       'animal print'],
                       'outerwear': ['biker jacket', 'cropped jacket', 'denim jacket', 'bomber jacket'],
                       'belt': ['studded belt', 'chain belt', 'utility belt', 'leather belt'],
                       'footwear': ['combat boots',
                                    'platform boots',
                                    'canvas sneakers',
                                    'platform shoes',
                                    'ankle boots'],
                       'footwear_color': ['black',
                                          'white',
                                          'red',
                                          'pink',
                                          'purple',
                                          'teal',
                                          'green',
                                          'striped pattern',
                                          'plaid tartan pattern'],
                       'hosiery': ['fishnet tights',
                                   'striped thigh-high socks',
                                   'mismatched striped socks',
                                   'ripped tights',
                                   'opaque tights',
                                   'patterned tights',
                                   'over-the-knee socks'],
                       'lingerie_type': ['neon modern lingerie set',
                                         'bralette and briefs set',
                                         'mesh lingerie set',
                                         'strappy cutout lingerie set',
                                         'strappy harness lingerie set'],
                       'lingerie_color': ['black',
                                          'hot pink',
                                          'purple',
                                          'teal',
                                          'neon green',
                                          'silver',
                                          'animal print',
                                          'heart print'],
                       'head_accessory': ['no head accessory',
                                          'beanie',
                                          'decorative hair clips',
                                          'decorative barrettes',
                                          'hair beads',
                                          'decorative metal braid and loc cuffs',
                                          'bow hair accessory'],
                       'accessories_scarf': ['no scarf', 'neck ribbon', 'choker scarf'],
                       'accessories_jewelry': ['layered jewelry',
                                               'gothic jewelry',
                                               'silver-toned jewelry',
                                               'statement jewelry'],
                       'accessories_necklace': ['choker necklace',
                                                'layered necklaces',
                                                'lace choker',
                                                'layered chain necklace'],
                       'accessories_earrings': ['cross earrings', 'chain earrings', 'ear cuffs', 'hoop earrings'],
                       'accessories_bracelet': ['stacked bracelets',
                                                'studded bracelet',
                                                'kandi bracelet',
                                                'leather bracelet'],
                       'accessories_rings': ['multiple rings', 'stacked rings', 'silver rings'],
                       'accessories_glasses': ['neon translucent glasses',
                                               'heart-shaped novelty glasses',
                                               'star-shaped novelty glasses',
                                               'oversized scene sunglasses',
                                               'rose-tinted glasses',
                                               'purple-tinted glasses',
                                               'blue-tinted glasses'],
                       'armwear': ['striped arm warmers',
                                   'fishnet arm warmers',
                                   'mesh fingerless sleeves',
                                   'detached sleeves'],
                       'accessories_bag': ['mini bag', 'crossbody bag', 'chain-strap bag', 'backpack']},
 'Sporty / Athleisure': {'main_modes': ['separates'],
                         'outfit_style': ['sporty athleisure style',
                                          'streetwear styling',
                                          'minimalist monochrome style'],
                         'top_type': ['tank top',
                                      'crop top',
                                      'fitted top',
                                      't-shirt',
                                      'cropped t-shirt',
                                      'hoodie',
                                      'polo shirt'],
                         'top_color': ['black',
                                       'white',
                                       'grey',
                                       'charcoal',
                                       'navy',
                                       'blue',
                                       'teal',
                                       'green',
                                       'red',
                                       'pink',
                                       'geometric print'],
                         'bottom_type': ['leggings', 'joggers', 'shorts', 'cargo pants', 'skinny jeans'],
                         'bottom_length': ['very short', 'short', 'knee-length', 'long'],
                         'bottom_color': ['black',
                                          'white',
                                          'grey',
                                          'charcoal',
                                          'navy',
                                          'blue',
                                          'teal',
                                          'green',
                                          'red',
                                          'pink'],
                         'outerwear': ['bomber jacket', 'puffer jacket', 'cropped jacket', 'denim jacket'],
                         'belt': ['no visible belt', 'utility belt'],
                         'footwear': ['sneakers', 'chunky sneakers', 'canvas sneakers', 'ankle boots'],
                         'footwear_color': ['black', 'white', 'grey', 'charcoal', 'navy', 'blue', 'red', 'pink'],
                         'hosiery': ['ankle socks', 'knee-high socks', 'bare legs', 'opaque tights'],
                         'lingerie_type': ['sports bra set', 'sport one-piece swimsuit', 'sport bikini'],
                         'lingerie_color': ['black', 'white', 'grey', 'navy', 'blue', 'teal', 'red', 'pink'],
                         'head_accessory': ['no head accessory', 'baseball cap', 'beanie', 'headband'],
                         'accessories_scarf': ['no scarf', 'knit scarf'],
                         'accessories_jewelry': ['minimal jewelry', 'silver-toned jewelry'],
                         'accessories_necklace': ['no necklace', 'delicate chain necklace'],
                         'accessories_earrings': ['no earrings', 'stud earrings', 'hoop earrings'],
                         'accessories_bracelet': ['no bracelet', 'cuff bracelet'],
                         'accessories_rings': ['no rings', 'single ring'],
                         'accessories_glasses': ['no glasses',
                                                 'sport wraparound sunglasses',
                                                 'mirrored sunglasses',
                                                 'aviator sunglasses'],
                         'armwear': ['no armwear', 'detached sleeves'],
                         'accessories_bag': ['no bag', 'backpack', 'crossbody bag', 'tote bag']},
 'Boho / Festival': {'main_modes': ['separates', 'dress'],
                     'outfit_style': ['boho festival styling', 'bohemian styling', 'romantic lace styling'],
                     'top_type': ['blouse',
                                  'lace top',
                                  'crop top',
                                  'halter top',
                                  'tank top',
                                  'vest top',
                                  'lace-trim camisole'],
                     'top_color': ['white',
                                   'cream',
                                   'beige',
                                   'camel',
                                   'brown',
                                   'olive',
                                   'burgundy',
                                   'silky floral pattern',
                                   'ethnic print',
                                   'linen texture',
                                   'lace-textured finish'],
                     'bottom_type': ['long skirt',
                                     'wide-leg pants',
                                     'flared pants',
                                     'shorts',
                                     'denim shorts',
                                     'mini skirt'],
                     'bottom_length': ['very short', 'short', 'mid-length', 'long'],
                     'bottom_color': ['white',
                                      'cream',
                                      'beige',
                                      'camel',
                                      'brown',
                                      'olive',
                                      'burgundy',
                                      'silky floral pattern',
                                      'ethnic print',
                                      'linen texture'],
                     'dress_type': ['maxi dress', 'wrap dress', 'slip dress', 'midi dress', 'lace dress'],
                     'dress_color': ['white',
                                     'cream',
                                     'beige',
                                     'camel',
                                     'brown',
                                     'olive',
                                     'burgundy',
                                     'silky floral pattern',
                                     'ethnic print',
                                     'linen texture'],
                     'outerwear': ['cardigan', 'denim jacket', 'cape', 'bolero'],
                     'belt': ['no visible belt', 'leather belt', 'wide waist belt', 'chain belt'],
                     'footwear': ['sandals', 'ankle boots', 'chelsea boots', 'platform shoes'],
                     'footwear_color': ['cream', 'beige', 'camel', 'brown', 'olive', 'burgundy', 'ethnic print'],
                     'hosiery': ['bare legs', 'sheer tights', 'ankle socks', 'over-the-knee socks'],
                     'lingerie_type': ['bralette and briefs set',
                                       'lace lingerie set',
                                       'triangle bikini',
                                       'halter bikini'],
                     'lingerie_color': ['white',
                                        'cream',
                                        'brown',
                                        'burgundy',
                                        'silky floral pattern',
                                        'lace-textured finish'],
                     'head_accessory': ['no head accessory',
                                        'headband',
                                        'ribbon headband',
                                        'hair beads',
                                        'decorative metal braid and loc cuffs',
                                        'decorative hair clips'],
                     'accessories_scarf': ['no scarf', 'silk scarf', 'sheer scarf', 'oversized scarf'],
                     'accessories_jewelry': ['layered jewelry', 'gold-toned jewelry', 'statement jewelry'],
                     'accessories_necklace': ['layered necklaces', 'pendant necklace', 'locket necklace'],
                     'accessories_earrings': ['hoop earrings', 'drop earrings', 'statement earrings'],
                     'accessories_bracelet': ['stacked bracelets', 'bangle bracelet', 'leather bracelet'],
                     'accessories_rings': ['multiple rings', 'stacked rings', 'statement ring'],
                     'accessories_glasses': ['no glasses',
                                             'aviator sunglasses',
                                             'rose-tinted glasses',
                                             'tinted fashion sunglasses',
                                             'sunglasses resting on the head'],
                     'armwear': ['no armwear', 'lace arm sleeves'],
                     'accessories_bag': ['shoulder bag', 'crossbody bag', 'tote bag', 'mini bag']},
 'Loungewear / Sleepwear / Boudoir': {'main_modes': ['sleepwear', 'lingerie'],
                                      'outfit_style': ['cozy loungewear styling',
                                                       'boudoir styling',
                                                       'soft feminine styling'],
                                      'lingerie_type': ['bralette and briefs set',
                                                        'lace lingerie set',
                                                        'satin lingerie set',
                                                        'mesh lingerie set',
                                                        'bodysuit lingerie',
                                                        'high-waist lingerie set'],
                                      'lingerie_color': ['black',
                                                         'white',
                                                         'cream',
                                                         'red',
                                                         'burgundy',
                                                         'pink',
                                                         'mauve',
                                                         'satin sheen',
                                                         'lace-textured finish',
                                                         'silky floral pattern'],
                                      'sleepwear_type': ['cute cotton pajama short set',
                                                         'oversized sleep t-shirt',
                                                         'plaid two-piece pajama set',
                                                         'satin two-piece pajama set',
                                                         'button-up pajama set',
                                                         'long-sleeve pajama set',
                                                         'ribbed lounge set',
                                                         'cozy knit loungewear set',
                                                         'tank-and-shorts lounge set',
                                                         'cropped hoodie lounge set',
                                                         'silky camisole sleep set',
                                                         'lace-trim camisole sleep set',
                                                         'minimal textured sexy sleep set',
                                                         'slip nightdress',
                                                         'elegant robe-and-slip sleep set'],
                                      'sleepwear_color': ['black',
                                                          'white',
                                                          'cream',
                                                          'beige',
                                                          'grey',
                                                          'navy',
                                                          'blue',
                                                          'red',
                                                          'burgundy',
                                                          'pink',
                                                          'mauve',
                                                          'purple',
                                                          'silky floral pattern',
                                                          'plaid tartan pattern',
                                                          'ribbed knit texture',
                                                          'velvet texture',
                                                          'satin sheen'],
                                      'outerwear': ['cardigan', 'bolero'],
                                      'belt': ['no visible belt'],
                                      'footwear': ['slippers', 'bare feet'],
                                      'footwear_color': ['black', 'white', 'cream', 'beige', 'pink', 'mauve'],
                                      'hosiery': ['bare legs'],
                                      'head_accessory': ['no head accessory',
                                                         'claw clip',
                                                         'headband',
                                                         'decorative hair clips'],
                                      'accessories_scarf': ['no scarf'],
                                      'accessories_jewelry': ['minimal jewelry', 'delicate jewelry'],
                                      'accessories_necklace': ['no necklace', 'delicate chain necklace'],
                                      'accessories_earrings': ['no earrings', 'stud earrings'],
                                      'accessories_bracelet': ['no bracelet', 'delicate bracelet'],
                                      'accessories_rings': ['no rings', 'single ring'],
                                      'accessories_glasses': ['no glasses', 'thin metal round eyeglasses'],
                                      'armwear': ['no armwear', 'lace arm sleeves'],
                                      'accessories_bag': ['no bag']},
 'Kawaii': {'main_modes': ['separates', 'dress', 'sleepwear'],
            'outfit_style': ['kawaii fashion', 'cute punk scene styling', 'Y2K fashion', 'soft feminine styling'],
            'top_type': ['cute mascot hoodie',
                         'cartoon character sweater',
                         'graphic baby tee',
                         'cropped t-shirt',
                         'crop top',
                         'sweater',
                         'cardigan',
                         'lace-trim camisole'],
            'top_color': ['white',
                          'cream',
                          'pink',
                          'mauve',
                          'purple',
                          'blue',
                          'teal',
                          'heart print',
                          'polka-dot print',
                          'cute cartoon print',
                          'pastel rainbow pattern'],
            'bottom_type': ['mini skirt', 'pleated skirt', 'skater skirt', 'shorts', 'denim shorts'],
            'bottom_length': ['very short', 'short', 'knee-length'],
            'bottom_color': ['white',
                             'cream',
                             'pink',
                             'mauve',
                             'purple',
                             'blue',
                             'teal',
                             'heart print',
                             'polka-dot print',
                             'cute cartoon print',
                             'pastel rainbow pattern'],
            'dress_type': ['mini dress', 'sweater dress', 'lace dress', 'shirt dress'],
            'dress_color': ['white',
                            'cream',
                            'pink',
                            'mauve',
                            'purple',
                            'blue',
                            'heart print',
                            'polka-dot print',
                            'cute cartoon print',
                            'pastel rainbow pattern'],
            'sleepwear_type': ['kawaii print pajama short set',
                               'cute cotton pajama short set',
                               'oversized sleep t-shirt',
                               'tartan footed pajama onesie',
                               'cute animal onesie',
                               'tiger onesie',
                               'bunny onesie',
                               'cropped hoodie lounge set'],
            'sleepwear_color': ['white',
                                'cream',
                                'pink',
                                'mauve',
                                'purple',
                                'blue',
                                'heart print',
                                'plaid tartan pattern',
                                'cute cartoon print',
                                'pastel rainbow pattern'],
            'outerwear': ['cardigan', 'cropped jacket', 'bolero', 'denim jacket'],
            'belt': ['no visible belt', 'chain belt'],
            'footwear': ['Mary Janes', 'platform shoes', 'sneakers', 'canvas sneakers', 'ankle boots'],
            'footwear_color': ['white', 'cream', 'pink', 'mauve', 'purple', 'blue', 'pastel rainbow pattern'],
            'hosiery': ['knee-high socks',
                        'over-the-knee socks',
                        'striped thigh-high socks',
                        'opaque thigh-high socks',
                        'patterned tights',
                        'bare legs'],
            'lingerie_type': ['bralette and briefs set', 'high-waist lingerie set', 'lace lingerie set'],
            'lingerie_color': ['white', 'pink', 'hot pink', 'purple', 'blue', 'heart print', 'lace-textured finish'],
            'head_accessory': ['headband',
                               'padded headband',
                               'decorative hair clips',
                               'decorative barrettes',
                               'pearl hair clips',
                               'bow hair accessory',
                               'ribbon headband'],
            'accessories_scarf': ['no scarf', 'neck ribbon'],
            'accessories_jewelry': ['delicate jewelry', 'pearl jewelry', 'minimal jewelry'],
            'accessories_necklace': ['no necklace', 'soft ribbon choker', 'pearl necklace', 'locket necklace'],
            'accessories_earrings': ['no earrings', 'stud earrings', 'pearl earrings'],
            'accessories_bracelet': ['no bracelet', 'kandi bracelet', 'delicate bracelet'],
            'accessories_rings': ['no rings', 'single ring', 'stacked rings'],
            'accessories_glasses': ['no glasses',
                                    'heart-shaped novelty glasses',
                                    'star-shaped novelty glasses',
                                    'rose-tinted glasses',
                                    'cat-eye eyeglasses'],
            'armwear': ['no armwear', 'striped arm warmers', 'detached sleeves'],
            'accessories_bag': ['mini bag', 'shoulder bag', 'backpack', 'chain-strap bag']}}

CLOTHING_COSPLAY_KEYS = {
    "cosplay_type", "cosplay_color", "cosplay_franchise_western", "cosplay_franchise_asian",
}

# Nail prompts conflict with garments that fully hide the fingers. Keep this
# intentionally textual so self-contained franchise cosplay descriptions are
# covered too, without adding hidden metadata to every costume. Fingerless
# pieces and wrist-only protection remain compatible with visible nails.
FULL_HAND_COVERING_MARKERS = (
    "glove",
    "gloves",
    "mitten",
    "mittens",
    "gauntlet",
    "gauntlets",
)
FULL_HAND_COVERING_EXCLUSIONS = (
    "fingerless glove",
    "fingerless gloves",
    "fingerless mitten",
    "fingerless mittens",
    "wrist gauntlet",
    "wrist gauntlets",
)

# Photographic effects are deliberately uncommon under ordinary Random because
# all three strongly reshape the image. Forced Random still chooses a concrete
# effect every time. Ordinary Random uses 70% clean output and 10% per effect.
OPTICAL_EFFECT_RANDOM_POOL = (
    [None] * 70
    + ["fisheye"] * 10
    + ["infrared false-color"] * 10
    + ["high-contrast duotone"] * 10
)

OUTERWEAR_WEARING_STYLE_RANDOM_POOL = (
    ["Properly worn"] * 60
    + ["Draped over shoulders"] * 15
    + ["Off shoulders at elbows"] * 15
    + ["Carried over one shoulder"] * 10
)

SETTING_SUPPRESSING_ACTION_POSES = {
    "riding a bicycle through the scene, both hands holding the handlebars, body leaning naturally forward, captured in gentle motion",
    "riding a horse, seated securely in the saddle, both hands loosely holding the reins, torso following the horse's movement",
    "seated behind the wheel of a car, both hands placed naturally on the steering wheel, actively driving while glancing toward the camera",
    "riding a moving carousel horse, seated astride the saddle with one hand holding the central pole, surrounding lights and background softened by motion blur",
    "riding a skateboard through the scene, one foot planted on the board, the other just lifted after pushing, arms balancing naturally",
}

BODY_CONTEXT_PORTRAIT_KEYS = {
    "pose", "bottom_type", "dress_type", "sleepwear_type", "cosplay_type",
    "cosplay_franchise_western", "cosplay_franchise_asian", "hosiery", "footwear",
}

CLOSE_FRAMING_FOOTWEAR_SUPPRESSION = {
    "close-up portrait", "headshot portrait", "bust portrait", "half-body portrait",
    "three-quarter portrait",
}

# Ordinary Random footwear is optional even when the requested framing could
# plausibly show it. This keeps a strongly prompt-adherent model from turning an
# off-frame shoe into a belt, bag charm, or floating prop. Manual, Forced Random,
# franchise-authored footwear, and the universal text override bypass this gate.
FOOTWEAR_RANDOM_PRESENCE_PERCENT = {
    "portrait": 10,
    "full-body portrait": 50,
    "full-body glamour portrait": 67,
}
DEFAULT_FOOTWEAR_RANDOM_PRESENCE_PERCENT = 20

# A text override on a main garment driver must also make that garment family
# visible. Merely replacing top_type after Random resolution is insufficient if
# a resolved dress or franchise cosplay still wins the formatter's priority.
MAIN_CLOTHING_OVERRIDE_CONFLICTS = {
    "top_type": {
        "dress_type", "sleepwear_type", "cosplay_type",
        "cosplay_franchise_western", "cosplay_franchise_asian",
    },
    "bottom_type": {
        "dress_type", "sleepwear_type", "cosplay_type",
        "cosplay_franchise_western", "cosplay_franchise_asian",
    },
    "dress_type": {
        "top_type", "bottom_type", "sleepwear_type", "cosplay_type",
        "cosplay_franchise_western", "cosplay_franchise_asian",
    },
    "sleepwear_type": {
        "top_type", "bottom_type", "dress_type", "lingerie_type", "cosplay_type",
        "cosplay_franchise_western", "cosplay_franchise_asian",
    },
    "cosplay_type": {
        "top_type", "bottom_type", "dress_type", "sleepwear_type",
        "cosplay_franchise_western", "cosplay_franchise_asian",
    },
    "cosplay_franchise_western": {
        "top_type", "bottom_type", "dress_type", "sleepwear_type",
        "cosplay_type", "cosplay_franchise_asian",
    },
    "cosplay_franchise_asian": {
        "top_type", "bottom_type", "dress_type", "sleepwear_type",
        "cosplay_type", "cosplay_franchise_western",
    },
}

DEFAULT_LINGERIE_LAYER_POOLS = {
    "separates": [False] * 90 + [True] * 10,
    "dress": [False] * 90 + [True] * 10,
}

ARCHETYPE_LINGERIE_LAYER_POOLS = {
    "Emo / Scene / Alt": [False, True],
}

DEFAULT_ARCHETYPE_LINGERIE_LAYER_POOL = [False] * 90 + [True] * 10

# Compact media presets: strong enough to establish the medium without
# overwhelming the character, styling, pose, and scene descriptors.
MEDIA_TYPE_PRESETS = {
    "studio photograph": {
        "intro": "studio photograph",
        "style": [],
    },
    "photograph": {
        "intro": "photograph",
        "style": [],
    },
    "cinematic still": {
        "intro": "cinematic film still",
        "style": ["moody auteur-cinema lighting", "fine visible film grain", "slightly desaturated palette", "dramatic tonal depth"],
    },
    "polaroid photograph": {
        "intro": "Polaroid instant photograph",
        "style": ["square instant print", "thick white border", "faded film colors", "subtle aged texture"],
    },
    "instant film photo": {
        "intro": "instant film snapshot",
        "style": ["soft instant-film colors", "gentle contrast", "slight exposure imperfections", "tactile print texture"],
    },
    "fashion editorial photograph": {
        "intro": "fashion editorial photograph",
        "style": ["fashion-magazine styling", "polished composition", "controlled editorial lighting"],
    },
    "hand-drawn illustration": {
        "intro": "hand-drawn illustration",
        "style": ["visible hand-drawn linework", "organic line variation", "subtle traditional-media irregularities"],
    },
    "digital illustration": {
        "intro": "digital illustration",
        "style": ["clean digital rendering", "polished edges", "controlled color transitions"],
    },
    "watercolor painting": {
        "intro": "watercolor painting",
        "style": ["translucent washes", "soft pigment blooms", "diffused edges", "textured watercolor paper"],
    },
    "oil painting": {
        "intro": "oil-on-canvas painting",
        "style": ["visible brushwork", "layered pigments", "painterly surface", "rich blended color"],
    },
    "pencil sketch": {
        "intro": "graphite pencil sketch",
        "style": ["visible graphite strokes", "pencil shading", "light cross-hatching", "textured paper"],
    },
    "ink drawing": {
        "intro": "ink drawing",
        "style": ["clean ink linework", "bold black contours", "controlled graphic shading"],
    },
    "anime illustration": {
        "intro": "Japanese anime illustration",
        "style": ["refined manga character design", "clean expressive line art", "polished cel shading"],
    },
    "comic-book illustration": {
        "intro": "comic-book illustration",
        "style": ["bold inked outlines", "graphic shadow shapes", "subtle halftone texture"],
    },
    "3D render": {
        "intro": "stylized animated 3D render",
        "style": ["Pixar-like character design", "rounded expressive forms", "polished materials", "soft cinematic lighting"],
    },
    "pixel art": {
        "intro": "16-bit pixel-art illustration",
        "style": ["clearly visible square pixels", "hard pixel edges", "limited color palette", "sprite-based shading", "no anti-aliasing"],
    },
    "low-poly render": {
        "intro": "strongly stylized low-poly 3D render",
        "style": ["visible polygonal facets", "angular geometry", "flat-shaded surfaces", "sharp planar transitions"],
    },
    "vector illustration": {
        "intro": "minimalist vector illustration",
        "style": ["simple geometric shapes", "crisp smooth outlines", "flat solid color fills", "limited palette", "minimal texture"],
    },
    "mixed-media collage": {
        "intro": "mixed-media collage",
        "style": ["photographic fragments", "torn paper", "printed textures", "painted marks", "visible overlapping edges"],
    },
    "linocut print": {
        "intro": "bold linocut print",
        "style": ["carved graphic linework", "rough hand-cut edges", "limited flat colors", "visible ink texture"],
    },
    "charcoal drawing": {
        "intro": "charcoal-on-paper drawing",
        "style": ["deep black strokes", "smudged shading", "powdery marks", "erased highlights", "monochrome contrast"],
    },
    "papercut illustration": {
        "intro": "layered papercut illustration",
        "style": ["clearly cut paper shapes", "stacked paper layers", "handmade edges", "shallow cast shadows", "tactile paper texture"],
    },
    "pastel drawing": {
        "intro": "chalk pastel drawing",
        "style": ["powdery pigments", "visible pastel strokes", "soft blended edges", "textured paper", "rich matte color"],
    },
}


def load_schema():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


SCHEMA = load_schema()


def indefinite_article(phrase: str) -> str:
    phrase = (phrase or "").strip()
    if not phrase:
        return "a"
    return "an" if phrase[0].lower() in "aeiou" else "a"


def join_phrases(items):
    items = [x for x in items if x]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + ", and " + items[-1] + ""


def ensure_period(text):
    text = (text or "").strip()
    if not text:
        return ""
    if text[-1] in ".!?":
        return text
    return text + "."


def build_sentence(parts):
    parts = [str(x).strip().strip(",") for x in parts if str(x).strip().strip(",")]
    if not parts:
        return ""
    return ensure_period(", ".join(parts))



def stable_choice(seed, namespace, values):
    """Choose deterministically from values using a seed stream unique to one field.

    Each random widget gets its own stable stream, so making another widget fixed
    no longer shifts the random choices that follow it.
    """
    values = list(values or [])
    if not values:
        return None
    normalized_seed = int(seed) & 0xffffffffffffffff
    payload = f"{normalized_seed}:{namespace}".encode("utf-8")
    digest = hashlib.blake2b(payload, digest_size=16).digest()
    index = int.from_bytes(digest, "big") % len(values)
    return values[index]

def is_enabled(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value == 1
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "on", "activated"}
    return False


class CharacterArchitectNode:
    CATEGORY = "prompt"
    DESCRIPTION = "Builds a structured character prompt with independent deterministic randomization, guided clothing families, and compatibility-aware layering. Hover individual controls for their hidden rules."
    FUNCTION = "build_prompt"
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("Prompt", "Face Prompt", "Inspected Value")

    @classmethod
    def INPUT_TYPES(cls):
        required = {}
        for item in SCHEMA["categories"]:
            options = ["None", "Random", "Forced Random"] + item["values"]
            default = item.get("default", "None")
            if default not in options:
                default = "None"
            required[item["key"]] = (
                options,
                {"default": default, "tooltip": CATEGORY_TOOLTIPS.get(item["key"], "")},
            )

        optional = {
            "lock_media_type": ("BOOLEAN", {"default": True, "label_on": "Locked", "label_off": "Unlocked", "tooltip": OPTIONAL_TOOLTIPS["lock_media_type"]}),
            "lock_gender": ("BOOLEAN", {"default": True, "label_on": "Locked", "label_off": "Unlocked", "tooltip": OPTIONAL_TOOLTIPS["lock_gender"]}),
            "lock_content_rating": ("BOOLEAN", {"default": True, "label_on": "Locked", "label_off": "Unlocked", "tooltip": OPTIONAL_TOOLTIPS["lock_content_rating"]}),
            "ethnicity_guidance": ("BOOLEAN", {"default": False, "label_on": "Activated", "label_off": "Deactivated", "tooltip": OPTIONAL_TOOLTIPS["ethnicity_guidance"]}),
            "enhance_realism": ("BOOLEAN", {"default": False, "label_on": "Activated", "label_off": "Deactivated", "tooltip": OPTIONAL_TOOLTIPS["enhance_realism"]}),
            "species_mode": (["Human", "Anthro Furry"], {"default": "Human", "tooltip": OPTIONAL_TOOLTIPS["species_mode"]}),
            "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "tooltip": OPTIONAL_TOOLTIPS["seed"]}),
            "control_after_generate": (["fixed", "increment", "decrement", "randomize"], {"default": "randomize", "tooltip": OPTIONAL_TOOLTIPS["control_after_generate"]}),
            "free_prompt": ("STRING", {"default": "", "multiline": True, "dynamicPrompts": False, "tooltip": OPTIONAL_TOOLTIPS["free_prompt"]}),
            "free_prompt_position": (["After introduction", "After makeup", "At end"], {"default": "After introduction", "tooltip": OPTIONAL_TOOLTIPS["free_prompt_position"]}),
            "override_field": (["None"] + [item["key"] for item in SCHEMA["categories"]], {"default": "None", "tooltip": OPTIONAL_TOOLTIPS["override_field"]}),
            "override_text": ("STRING", {"forceInput": True, "tooltip": OPTIONAL_TOOLTIPS["override_text"]}),
            "inspect_property": (["None"] + [item["key"] for item in SCHEMA["categories"]], {"default": "None", "tooltip": OPTIONAL_TOOLTIPS["inspect_property"]}),
        }
        return {"required": required, "optional": optional}

    def _resolve_values(self, kwargs, seed=0, ethnicity_guidance=False):
        raw = {item["key"]: kwargs.get(item["key"], "None") for item in SCHEMA["categories"]}

        legacy_ethnicity = raw.get("origin_ethnicity")
        if legacy_ethnicity in LEGACY_ETHNICITY_MAP:
            mapped = LEGACY_ETHNICITY_MAP[legacy_ethnicity]
            raw["origin_ethnicity"] = mapped if mapped else "None"

        legacy_portrait_style = raw.get("portrait_style")
        if legacy_portrait_style in LEGACY_PORTRAIT_STYLE_MAP:
            raw["portrait_style"] = LEGACY_PORTRAIT_STYLE_MAP[legacy_portrait_style]

        legacy_effect = raw.get("optical_effect")
        if legacy_effect in LEGACY_PHOTOGRAPHIC_EFFECT_MAP:
            raw["optical_effect"] = LEGACY_PHOTOGRAPHIC_EFFECT_MAP[legacy_effect] or "None"

        for key, value_map in LEGACY_CATEGORY_VALUE_MAPS.items():
            legacy_value = raw.get(key)
            if legacy_value in value_map:
                raw[key] = value_map[legacy_value] or "None"

        if raw.get("hosiery") == "black tights":
            raw["hosiery"] = "opaque tights"
            if raw.get("hosiery_color") in (None, "None"):
                raw["hosiery_color"] = "black"

        schema_by_key = {item["key"]: item for item in SCHEMA["categories"]}

        # Resolve guidance pivots first. Every category uses an independent stable
        # choice derived from the seed, so changing one widget cannot shift the others.
        ethnicity_item = schema_by_key.get("origin_ethnicity")
        selected_ethnicity = raw.get("origin_ethnicity", "None")
        if selected_ethnicity in ("Random", "Forced Random") and ethnicity_item and ethnicity_item["values"]:
            resolved_ethnicity = stable_choice(seed, "origin_ethnicity", ethnicity_item["values"])
        elif selected_ethnicity in (None, "None"):
            resolved_ethnicity = None
        else:
            resolved_ethnicity = selected_ethnicity

        archetype_item = schema_by_key.get("clothing_archetype")
        selected_archetype = raw.get("clothing_archetype", "None")
        if selected_archetype in ("Random", "Forced Random") and archetype_item and archetype_item["values"]:
            resolved_archetype = stable_choice(seed, "clothing_archetype", archetype_item["values"])
        elif selected_archetype in (None, "None"):
            resolved_archetype = None
        else:
            resolved_archetype = selected_archetype
        archetype_config = CLOTHING_ARCHETYPE_CONFIG.get(resolved_archetype, {})

        # The clothing branches are mutually exclusive only for their main garment.
        # Manual selections remain free. With an active archetype, cosplay randoms
        # are suppressed and the chosen main branch stays inside the archetype.
        # Garment types select a clothing family; colors and lengths only modify
        # whichever family wins. Franchise sources are subtypes of one cosplay
        # family, preventing cosplay from receiving three statistical tickets.
        clothing_modes = {
            "separates": ["top_type", "top_color", "bottom_type", "bottom_length", "bottom_color"],
            "dress": ["dress_type", "dress_color"],
            "lingerie": ["lingerie_type", "lingerie_color"],
            "sleepwear": ["sleepwear_type", "sleepwear_color"],
            "cosplay": ["cosplay_type", "cosplay_color", "cosplay_franchise_western", "cosplay_franchise_asian"],
        }
        clothing_mode_drivers = {
            "separates": ["top_type", "bottom_type"],
            "dress": ["dress_type"],
            "lingerie": ["lingerie_type"],
            "sleepwear": ["sleepwear_type"],
            "cosplay": ["cosplay_type", "cosplay_franchise_western", "cosplay_franchise_asian"],
        }
        concrete_modes = [
            mode for mode, keys in clothing_mode_drivers.items()
            if any(raw.get(key) not in (None, "None", "Random", "Forced Random") for key in keys)
        ]
        random_modes = [
            mode for mode, keys in clothing_mode_drivers.items()
            if any(raw.get(key) in ("Random", "Forced Random") for key in keys)
        ]
        forced_modes = [
            mode for mode, keys in clothing_mode_drivers.items()
            if any(raw.get(key) == "Forced Random" for key in keys)
        ]
        if resolved_archetype:
            allowed_main_modes = archetype_config.get("main_modes", ["separates", "dress"])
            candidate_modes = forced_modes or [mode for mode in allowed_main_modes if mode in random_modes]
            chosen_mode = None
            if not concrete_modes and candidate_modes:
                chosen_mode = stable_choice(seed, "__clothing_mode__", candidate_modes)

            main_mode = next(
                (mode for mode in ("cosplay", "dress", "separates", "lingerie", "sleepwear") if mode in concrete_modes),
                chosen_mode,
            )
            lingerie_layer_eligible = main_mode in {"separates", "dress"} or (
                main_mode == "cosplay" and resolved_archetype in {"Casual Everyday", "Emo / Scene / Alt"}
            )
            archetype_layer_pool = ARCHETYPE_LINGERIE_LAYER_POOLS.get(
                resolved_archetype,
                DEFAULT_ARCHETYPE_LINGERIE_LAYER_POOL,
            )
            preserve_random_lingerie = (
                "lingerie" in random_modes
                and lingerie_layer_eligible
                and bool(stable_choice(
                    seed,
                    f"__archetype_lingerie_layer__{resolved_archetype}__{main_mode}",
                    archetype_layer_pool,
                ))
            )
            preserve_forced_lingerie = "lingerie" in forced_modes and bool(concrete_modes)
            for mode, keys in clothing_modes.items():
                if mode == "cosplay":
                    for key in keys:
                        if raw.get(key) == "Random":
                            raw[key] = "None"
                    if mode not in forced_modes:
                        continue
                preserve_lingerie = mode == "lingerie" and (
                    preserve_random_lingerie or preserve_forced_lingerie
                )
                if chosen_mode and mode != chosen_mode and not preserve_lingerie:
                    for key in keys:
                        if raw.get(key) in ("Random", "Forced Random"):
                            raw[key] = "None"
                elif concrete_modes and mode not in concrete_modes and not preserve_lingerie:
                    for key in keys:
                        if raw.get(key) in ("Random", "Forced Random"):
                            raw[key] = "None"
        elif concrete_modes:
            # Explicit garment types beat ordinary Random families. Forced
            # Random remains the deliberate escape hatch and is not suppressed.
            main_mode = next(
                (mode for mode in ("cosplay", "dress", "separates", "lingerie", "sleepwear") if mode in concrete_modes),
                None,
            )
            chance_pool = DEFAULT_LINGERIE_LAYER_POOLS.get(main_mode)
            preserve_default_random_lingerie = (
                "lingerie" in random_modes
                and bool(chance_pool)
                and bool(stable_choice(seed, f"__default_lingerie_layer__{main_mode}", chance_pool))
            )
            for mode, keys in clothing_modes.items():
                preserve_lingerie = mode == "lingerie" and preserve_default_random_lingerie
                if mode not in concrete_modes and not preserve_lingerie:
                    for key in keys:
                        if raw.get(key) == "Random":
                            raw[key] = "None"
        elif len(random_modes) > 1:
            chosen_mode = stable_choice(seed, "__clothing_mode__", forced_modes or random_modes)
            chance_pool = DEFAULT_LINGERIE_LAYER_POOLS.get(chosen_mode)
            preserve_default_random_lingerie = (
                "lingerie" in random_modes
                and bool(chance_pool)
                and bool(stable_choice(seed, f"__default_lingerie_layer__{chosen_mode}", chance_pool))
            )
            for mode, keys in clothing_modes.items():
                preserve_lingerie = mode == "lingerie" and preserve_default_random_lingerie
                if mode != chosen_mode and not preserve_lingerie:
                    for key in keys:
                        if raw.get(key) in ("Random", "Forced Random"):
                            raw[key] = "None"

        # Once cosplay wins as a broad family, choose exactly one source among
        # generic, Western franchise, and Asian franchise.
        cosplay_source_keys = [
            "cosplay_type",
            "cosplay_franchise_western",
            "cosplay_franchise_asian",
        ]
        concrete_cosplay_sources = [
            key for key in cosplay_source_keys
            if raw.get(key) not in (None, "None", "Random", "Forced Random")
        ]
        random_cosplay_sources = [
            key for key in cosplay_source_keys
            if raw.get(key) in ("Random", "Forced Random")
        ]
        forced_cosplay_sources = [
            key for key in cosplay_source_keys if raw.get(key) == "Forced Random"
        ]
        if concrete_cosplay_sources:
            # A manually selected cosplay source is authoritative. Ordinary
            # Random values left on the two sibling source widgets must not
            # resolve behind it and then win merely because franchise outfits
            # are formatted first. Forced Random remains the explicit escape
            # hatch and is intentionally left untouched.
            for key in random_cosplay_sources:
                if raw.get(key) == "Random":
                    raw[key] = "None"
        elif len(random_cosplay_sources) > 1:
            # Weight each source by its number of entries. This gives every
            # individual costume approximately the same probability instead
            # of giving equally sized tickets to differently sized lists.
            cosplay_source_pool = []
            for key in forced_cosplay_sources or random_cosplay_sources:
                source_item = schema_by_key.get(key, {})
                cosplay_source_pool.extend(
                    [key] * max(1, len(source_item.get("values", [])))
                )
            chosen_cosplay_source = stable_choice(
                seed,
                "__cosplay_source__",
                cosplay_source_pool,
            )
            for key in random_cosplay_sources:
                if key != chosen_cosplay_source:
                    raw[key] = "None"

        # A retained random lingerie layer may include swimwear: the prompt's
        # constrained-visibility sentence keeps the underlayer subordinate.
        lingerie_random_is_underlayer = (
            raw.get("lingerie_type") == "Random"
            and any(
                raw.get(key) not in (None, "None")
                for mode, drivers in clothing_mode_drivers.items()
                if mode != "lingerie"
                for key in drivers
            )
        )

        # A cosplay is already a complete outfit description and may contain
        # trousers, shorts, a skirt, or exposed legs. We cannot reliably infer
        # how randomly selected hosiery should be layered with it. Suppress only
        # Random hosiery for cosplay outfits; an explicit manual choice remains
        # untouched and is therefore still available for deliberate styling.
        cosplay_keys = [
            "cosplay_type",
            "cosplay_franchise_western",
            "cosplay_franchise_asian",
        ]
        cosplay_mode_active = any(
            raw.get(key) not in (None, "None") for key in cosplay_keys
        )
        if cosplay_mode_active and raw.get("hosiery") == "Random":
            raw["hosiery"] = "None"

        # Every cosplay source is a self-contained main outfit. Generic
        # costumes suppress random styling and heavy garment additions, while
        # their signature colors and equipment (for example purple platform
        # boots on Padmé). Suppress only random secondary additions. Explicit
        # manual selections remain available for intentional customization.
        generic_cosplay_mode_active = raw.get("cosplay_type") not in (None, "None")
        franchise_mode_active = any(
            raw.get(key) not in (None, "None")
            for key in ("cosplay_franchise_western", "cosplay_franchise_asian")
        )
        franchise_random_suppressed_keys = {
            "outfit_style",
            "outerwear",
            "outerwear_color",
            "belt",
            "belt_color",
            "footwear",
            "footwear_color",
            "head_accessory",
            "accessories_scarf",
            "accessories_jewelry",
            "accessories_necklace",
            "accessories_earrings",
            "accessories_bracelet",
            "accessories_rings",
            "accessories_glasses",
            "armwear",
            "accessories_bag",
            "hosiery_color",
        }
        generic_cosplay_random_suppressed_keys = {
            "outfit_style",
            "outerwear",
            "outerwear_color",
            "belt",
            "belt_color",
            "footwear",
            "footwear_color",
            "hosiery_color",
        }
        if generic_cosplay_mode_active:
            for key in generic_cosplay_random_suppressed_keys:
                if raw.get(key) == "Random":
                    raw[key] = "None"
        if franchise_mode_active:
            for key in franchise_random_suppressed_keys:
                if raw.get(key) == "Random":
                    raw[key] = "None"

        guided_pools = ETHNICITY_RANDOM_POOLS.get(resolved_ethnicity, {}) if ethnicity_guidance else {}
        resolved = {}
        for item in SCHEMA["categories"]:
            key = item["key"]
            if key == "origin_ethnicity":
                resolved[key] = resolved_ethnicity
                continue
            if key == "clothing_archetype":
                resolved[key] = resolved_archetype
                continue

            selected = raw.get(key, "None")
            if (
                key == "eye_color"
                and ethnicity_guidance
                and resolved_ethnicity
                and selected in (None, "None", "Random")
            ):
                resolved[key] = stable_choice(seed, key, guided_pools.get(key, item["values"]))
            elif selected == "Forced Random":
                forced_pool = [
                    value for value in item["values"]
                    if value not in FORCED_RANDOM_EXCLUDED_VALUES
                ]
                resolved[key] = stable_choice(seed, key, forced_pool or item["values"])
            elif franchise_mode_active and key == "outfit_style" and selected in (None, "None", "Random"):
                resolved[key] = None
            elif resolved_archetype and key == "outfit_style" and selected in (None, "None", "Random"):
                resolved[key] = stable_choice(seed, key, archetype_config.get("outfit_style", item["values"]))
            elif selected == "None":
                resolved[key] = None
            elif selected == "Random":
                if key == "optical_effect":
                    resolved[key] = stable_choice(seed, key, OPTICAL_EFFECT_RANDOM_POOL)
                elif key == "outerwear_wearing_style":
                    style_pool = OUTERWEAR_WEARING_STYLE_RANDOM_POOL
                    if resolved.get("outerwear") == "cape":
                        style_pool = [
                            value for value in style_pool
                            if value != "Off shoulders at elbows"
                        ]
                    resolved[key] = stable_choice(seed, key, style_pool)
                elif key == "accessories_glasses":
                    glasses_pool = archetype_config.get(key, item["values"]) if resolved_archetype else item["values"]
                    concrete_glasses = [value for value in glasses_pool if value != "no glasses"]
                    has_glasses = stable_choice(seed, f"{key}__presence__", GLASSES_RANDOM_PRESENCE_POOL)
                    resolved[key] = stable_choice(seed, key, concrete_glasses) if has_glasses and concrete_glasses else "no glasses"
                elif key in {"accessories_bag", "accessories_scarf"}:
                    preferred = archetype_config.get(key, item["values"]) if resolved_archetype else item["values"]
                    absent_value = "no bag" if key == "accessories_bag" else "no scarf"
                    concrete = [value for value in preferred if value != absent_value]
                    presence_pool = BAG_RANDOM_PRESENCE_POOL if key == "accessories_bag" else SCARF_RANDOM_PRESENCE_POOL
                    is_present = stable_choice(seed, f"{key}__presence__", presence_pool)
                    resolved[key] = stable_choice(seed, key, concrete) if is_present and concrete else absent_value
                elif key == "lingerie_type" and lingerie_random_is_underlayer:
                    preferred = archetype_config.get(key, item["values"]) if resolved_archetype else item["values"]
                    resolved[key] = stable_choice(seed, key, preferred)
                elif resolved_archetype and key in CLOTHING_COSPLAY_KEYS:
                    resolved[key] = None
                elif resolved_archetype and key in archetype_config:
                    resolved[key] = stable_choice(seed, key, archetype_config[key])
                elif ethnicity_guidance and resolved_ethnicity and key in ETHNICITY_GUIDED_SUPPRESS_RANDOM:
                    resolved[key] = None
                elif ethnicity_guidance and resolved_ethnicity and key == "skin_finish":
                    resolved[key] = stable_choice(seed, key, NEUTRAL_SKIN_FINISH_POOL)
                elif key in guided_pools:
                    resolved[key] = stable_choice(seed, key, guided_pools[key])
                else:
                    resolved[key] = stable_choice(seed, key, item["values"])
            else:
                resolved[key] = selected

        self._apply_soft_random_coherence(raw, resolved, seed, schema_by_key)

        # These actions already define the physical scene around the subject.
        # Suppress only an ordinary Random setting so a steering wheel, horse,
        # bicycle, carousel, or skateboard is not forced into an incompatible
        # environment. Explicit user intent continues to win.
        if (
            resolved.get("pose") in SETTING_SUPPRESSING_ACTION_POSES
            and raw.get("setting") == "Random"
        ):
            resolved["setting"] = None

        # Ordinary Random nails should never fight a costume that fully covers
        # the hands. Manual nail choices remain authoritative, and Forced Random
        # deliberately keeps its documented rule-bypassing behavior.
        if raw.get("nail_style") == "Random" and self._has_full_hand_covering(resolved):
            resolved["nail_style"] = None

        if raw.get("portrait_style") == "Random" and any(
            resolved.get(key) for key in BODY_CONTEXT_PORTRAIT_KEYS
        ):
            portrait_item = schema_by_key.get("portrait_style")
            weighted_portraits = []
            if portrait_item:
                for value in portrait_item["values"]:
                    weight = 1 if value in {"close-up portrait", "headshot portrait"} else 3
                    weighted_portraits.extend([value] * weight)
            if weighted_portraits:
                resolved["portrait_style"] = stable_choice(
                    seed, "portrait_style__body_context", weighted_portraits
                )

        close_framing = (
            resolved.get("portrait_style") in CLOSE_FRAMING_FOOTWEAR_SUPPRESSION
            or resolved.get("shot_composition") == "tight crop"
        )
        if raw.get("footwear") == "Random":
            keep_footwear = False
            if not close_framing:
                portrait_style = resolved.get("portrait_style")
                percent = FOOTWEAR_RANDOM_PRESENCE_PERCENT.get(
                    portrait_style, DEFAULT_FOOTWEAR_RANDOM_PRESENCE_PERCENT
                )
                keep_footwear = stable_choice(
                    seed, "footwear__framing_presence", [False] * (100 - percent) + [True] * percent
                )
            if not keep_footwear:
                resolved["footwear"] = None
                if raw.get("footwear_color") == "Random":
                    resolved["footwear_color"] = None
        return resolved

    def _apply_soft_random_coherence(self, raw, resolved, seed, schema_by_key):
        """Favor coherent Random combinations without policing explicit intent."""

        # Neckline depth and shape describe the same opening. Guide whichever
        # side is random, but retain ten percent of the old free combinations.
        if stable_choice(seed, "__neckline_compatibility__", NECKLINE_COMPATIBILITY_POOL):
            depth = resolved.get("cleavage_depth")
            neckline_type = resolved.get("cleavage_type")
            if raw.get("cleavage_type") == "Random" and depth in NECKLINE_TYPES_BY_DEPTH:
                resolved["cleavage_type"] = stable_choice(
                    seed, "cleavage_type__compatible", NECKLINE_TYPES_BY_DEPTH[depth]
                )
            elif raw.get("cleavage_depth") == "Random" and neckline_type:
                compatible_depths = [
                    candidate for candidate, types in NECKLINE_TYPES_BY_DEPTH.items()
                    if neckline_type in types
                ]
                if compatible_depths:
                    resolved["cleavage_depth"] = stable_choice(
                        seed, "cleavage_depth__compatible", compatible_depths
                    )

        # Bottom length remains a single visible category. These hidden pools
        # simply prevent ordinary Random from routinely making shorts long or
        # trousers very short; fifteen percent stays intentionally atypical.
        if stable_choice(seed, "__bottom_compatibility__", SOFT_COMPATIBILITY_POOL):
            bottom_type = resolved.get("bottom_type")
            bottom_length = resolved.get("bottom_length")
            if raw.get("bottom_length") == "Random" and bottom_type in BOTTOM_LENGTH_POOLS:
                resolved["bottom_length"] = stable_choice(
                    seed, "bottom_length__compatible", BOTTOM_LENGTH_POOLS[bottom_type]
                )
            elif raw.get("bottom_type") == "Random" and bottom_length:
                compatible_types = [
                    candidate for candidate, lengths in BOTTOM_LENGTH_POOLS.items()
                    if bottom_length in lengths
                ]
                if compatible_types:
                    source_values = schema_by_key.get("bottom_type", {}).get("values", [])
                    compatible_types = [value for value in source_values if value in compatible_types]
                    resolved["bottom_type"] = stable_choice(
                        seed, "bottom_type__compatible", compatible_types
                    )

        self._apply_soft_hair_coherence(raw, resolved, seed, schema_by_key)
        self._apply_soft_photo_coherence(raw, resolved, seed)
        self._apply_cosplay_detail_coherence(raw, resolved)

    def _apply_cosplay_detail_coherence(self, raw, resolved):
        cosplay_text = " ".join(
            str(resolved.get(key) or "")
            for key in ("cosplay_type", "cosplay_franchise_western", "cosplay_franchise_asian")
        ).lower()
        if not cosplay_text.strip():
            return
        padded = f" {re.sub(r'[^a-z0-9]+', ' ', cosplay_text).strip()} "
        has_term = lambda terms: any(f" {term} " in padded for term in terms)

        authored_headwear = has_term({
            "cap", "caps", "hat", "hats", "helmet", "helmets", "hood", "hoods",
            "crown", "crowns", "tiara", "veil", "bonnet", "headpiece", "headdress",
            "halo", "horns", "cat ears", "bunny ears", "animal ears",
        })
        if authored_headwear and raw.get("head_accessory") == "Random":
            resolved["head_accessory"] = None

        structured_upper_garment = has_term({
            "jacket", "jackets", "coat", "coats", "blazer", "blazers", "uniform",
            "uniforms", "robe", "robes", "long sleeved", "sleeves",
        })
        if (
            structured_upper_garment
            and raw.get("cleavage_type") == "Random"
            and resolved.get("cleavage_type") in {"halter neckline", "off-shoulder neckline"}
        ):
            resolved["cleavage_type"] = None

    def _apply_soft_hair_coherence(self, raw, resolved, seed, schema_by_key):
        if not stable_choice(seed, "__hair_compatibility__", HAIR_COMPATIBILITY_POOL):
            return

        style = resolved.get("hair_style")
        cut = resolved.get("hair_cut")
        length = resolved.get("hair_length")
        texture = resolved.get("hair_texture")
        bangs = resolved.get("bangs_style")
        short_lengths = {"cropped hair", "short hair", "chin-length hair"}
        long_lengths = {"medium-long hair", "long hair", "very long hair", "waist-length hair"}
        length_styles = {
            "braided hair", "dreadlocks", "twin braids", "French braid",
            "high ponytail", "low ponytail", "high bun", "low bun", "space buns",
        }

        if style in length_styles and length in short_lengths:
            if raw.get("hair_length") == "Random":
                resolved["hair_length"] = stable_choice(
                    seed, "hair_length__style_compatible",
                    ["shoulder-length hair", "medium-long hair", "long hair", "very long hair"],
                )
                length = resolved["hair_length"]
            elif raw.get("hair_style") == "Random":
                style_values = schema_by_key.get("hair_style", {}).get("values", [])
                resolved["hair_style"] = stable_choice(
                    seed, "hair_style__length_compatible",
                    [value for value in style_values if value not in length_styles],
                )
                style = resolved["hair_style"]

        compact_cuts = {"pixie cut", "fade haircut", "buzz cut", "crew cut"}
        if cut in compact_cuts and length in long_lengths:
            if raw.get("hair_length") == "Random":
                resolved["hair_length"] = stable_choice(
                    seed, "hair_length__cut_compatible", ["cropped hair", "short hair", "chin-length hair"]
                )
                length = resolved["hair_length"]
            elif raw.get("hair_cut") == "Random":
                cut_values = schema_by_key.get("hair_cut", {}).get("values", [])
                resolved["hair_cut"] = stable_choice(
                    seed, "hair_cut__length_compatible",
                    [value for value in cut_values if value not in compact_cuts],
                )

        curly_textures = {"curly", "tightly curled", "coily"}
        if texture in curly_textures and style == "sleek straight styling":
            if raw.get("hair_style") == "Random":
                resolved["hair_style"] = stable_choice(
                    seed, "hair_style__texture_compatible",
                    ["loose hair", "defined curls", "messy textured styling", "braided hair", "dreadlocks", "high ponytail", "low ponytail", "high bun", "low bun"],
                )
            elif raw.get("hair_texture") == "Random":
                resolved["hair_texture"] = stable_choice(
                    seed, "hair_texture__style_compatible", ["straight", "silky straight", "slightly wavy"]
                )

        if bangs == "long face-framing bangs" and length == "cropped hair" and raw.get("bangs_style") == "Random":
            resolved["bangs_style"] = stable_choice(
                seed, "bangs_style__length_compatible",
                ["no bangs", "micro bangs", "straight bangs", "side-swept bangs", "wispy bangs", "choppy bangs"],
            )

        # Loc cuffs are still legal everywhere; braids and locs merely make
        # them more likely instead of turning them into an exclusive pairing.
        if raw.get("head_accessory") == "Random" and resolved.get("hair_style") in {
            "braided hair", "dreadlocks", "twin braids", "French braid"
        }:
            boost_pool = [True] * 20 + [False] * 80
            if stable_choice(seed, "head_accessory__loc_cuff_boost", boost_pool):
                resolved["head_accessory"] = "decorative metal braid and loc cuffs"

    def _apply_soft_photo_coherence(self, raw, resolved, seed):
        if raw.get("lighting_style") != "Random":
            return
        if not stable_choice(seed, "__photo_compatibility__", PHOTO_COMPATIBILITY_POOL):
            return

        effect = resolved.get("optical_effect")
        lens = resolved.get("lens_style")
        lighting = resolved.get("lighting_style")
        harsh_for_duotone = {
            "hard flash", "split lighting", "neon lighting", "colored gel lighting",
            "dramatic chiaroscuro lighting with sculpted highlights and deep shadows",
        }
        colored_for_infrared = {"neon lighting", "colored gel lighting"}
        sculpted_for_lofi = {
            "dramatic studio lighting", "split lighting",
            "dramatic chiaroscuro lighting with sculpted highlights and deep shadows",
            "colored gel lighting",
        }
        conflict = (
            (effect == "high-contrast duotone" and lighting in harsh_for_duotone)
            or (effect == "infrared false-color" and lighting in colored_for_infrared)
            or (lens in {"disposable camera look", "cheap digital camera aesthetic"} and lighting in sculpted_for_lofi)
        )
        if conflict:
            resolved["lighting_style"] = stable_choice(
                seed, "lighting_style__photo_compatible", SIMPLE_PHOTO_LIGHTING
            )

    def _has_full_hand_covering(self, data):
        handwear_sources = (
            data.get("armwear"),
            data.get("cosplay_type"),
            data.get("cosplay_franchise_western"),
            data.get("cosplay_franchise_asian"),
        )
        for value in handwear_sources:
            if not value:
                continue
            normalized = str(value).casefold()
            for exclusion in FULL_HAND_COVERING_EXCLUSIONS:
                normalized = normalized.replace(exclusion, "")
            if any(marker in normalized for marker in FULL_HAND_COVERING_MARKERS):
                return True
        return False

    def _combine_color(self, data, item_key, color_key):
        item = data.get(item_key)
        color = data.get(color_key)
        if not item:
            return None
        if item in {"bare feet", "bare legs", "no visible belt"}:
            return item
        return f"{color} {item}" if color else item

    def _combine_bottom(self, data):
        bottom_type = data.get("bottom_type")
        if not bottom_type:
            return None
        bottom_length = data.get("bottom_length")
        # An explicit length overrides built-in skirt length words, avoiding
        # phrases such as "long long skirt" or "mid-length mini skirt".
        if bottom_length and bottom_type in {"mini skirt", "long skirt"}:
            bottom_type = "skirt"
        parts = [bottom_length, data.get("bottom_color"), bottom_type]
        return " ".join(part for part in parts if part)

    def _format_clothing(self, data):
        outfit_style = data.get("outfit_style")

        cosplay = self._combine_color(data, "cosplay_type", "cosplay_color")
        franchise_cosplay = data.get("cosplay_franchise_western") or data.get("cosplay_franchise_asian")
        dress = self._combine_color(data, "dress_type", "dress_color")
        lingerie = self._combine_color(data, "lingerie_type", "lingerie_color")
        sleepwear = self._combine_color(data, "sleepwear_type", "sleepwear_color")
        top = self._combine_color(data, "top_type", "top_color")
        bottom = self._combine_bottom(data)
        footwear = self._combine_color(data, "footwear", "footwear_color")
        outerwear = self._combine_color(data, "outerwear", "outerwear_color")
        outerwear_phrase = outerwear.replace(" layer", "") if outerwear else None
        outerwear_type = data.get("outerwear")
        outerwear_wearing_style = data.get("outerwear_wearing_style") or "Properly worn"
        belt = self._combine_color(data, "belt", "belt_color")
        hosiery = self._combine_color(data, "hosiery", "hosiery_color")
        scarf = data.get("accessories_scarf")

        hosiery_layered_under_bottom = bool(bottom and hosiery and hosiery != "bare legs")
        if hosiery_layered_under_bottom:
            bottom_length = data.get("bottom_length")
            if bottom_length == "mid-length":
                hosiery = f"partially visible {hosiery}"
            elif bottom_length == "long":
                hosiery = f"mostly concealed {hosiery}"
            bottom = f"{bottom} layered over {hosiery}"

        main_clothing_mode = None
        main_items = []

        if franchise_cosplay:
            main_clothing_mode = "franchise_cosplay"
            normalized = franchise_cosplay
            if normalized.startswith("A ") or normalized.startswith("An "):
                normalized = normalized[0].lower() + normalized[1:]
            main_items.append(normalized)
        elif cosplay:
            main_clothing_mode = "cosplay"
            main_items.append(cosplay)
        elif dress:
            main_clothing_mode = "dress"
            main_items.append(dress)
        elif top or bottom:
            main_clothing_mode = "separates"
            if top:
                main_items.append(top)
            if bottom:
                main_items.append(bottom)
        elif lingerie:
            main_clothing_mode = "lingerie"
            main_items.append(lingerie)
        elif sleepwear:
            main_clothing_mode = "sleepwear"
            main_items.append(sleepwear)

        extra_items = []
        if belt and belt != "no visible belt":
            extra_items.append(belt)
        if footwear:
            extra_items.append(footwear)
        if hosiery and not hosiery_layered_under_bottom:
            extra_items.append(hosiery)
        if scarf and scarf != "no scarf":
            extra_items.append(scarf)

        clauses = []
        standalone_sentences = []
        if outfit_style:
            clauses.append(f"styled in {outfit_style}")
        if main_items:
            clauses.append("wearing " + join_phrases(main_items + extra_items))
        elif extra_items:
            clauses.append("wearing " + join_phrases(extra_items))

        layered_outer = main_clothing_mode in {"separates", "dress", "cosplay", "franchise_cosplay", "sleepwear"}
        layered_lingerie = layered_outer and bool(lingerie) and main_clothing_mode != "lingerie"

        if layered_lingerie:
            archetype = data.get("clothing_archetype")
            if archetype == "Emo / Scene / Alt":
                clauses.append(f"with {lingerie} visibly layered beneath the clothes")
            elif archetype == "Casual Everyday":
                clauses.append(f"with {lingerie} subtly peeking from beneath the clothes")
            else:
                lingerie_phrase = lingerie if "bra straps" in lingerie else f"{indefinite_article(lingerie)} {lingerie}"
                standalone_sentences.append(
                    "Through the small parts that protrude from the clothing, "
                    f"one can guess {lingerie_phrase} beneath the clothes"
                )
        if outerwear_phrase:
            over_outfit = " over the outfit" if main_clothing_mode else ""
            if outerwear_type == "cape" and outerwear_wearing_style == "Properly worn":
                cape_fall = "over the outfit" if main_clothing_mode else "down the back"
                standalone_sentences.append(
                    f"The subject also wears {indefinite_article(outerwear_phrase)} {outerwear_phrase}{over_outfit}. "
                    f"The cape is fastened securely around both shoulders and hangs evenly {cape_fall}"
                )
            elif outerwear_type == "cape" and outerwear_wearing_style == "Draped over shoulders":
                standalone_sentences.append(
                    f"The subject also has {indefinite_article(outerwear_phrase)} {outerwear_phrase} draped evenly "
                    "over both shoulders and hanging freely down the back"
                )
            elif outerwear_type == "cape" and outerwear_wearing_style == "Off shoulders at elbows":
                standalone_sentences.append(
                    f"The subject also wears {indefinite_article(outerwear_phrase)} {outerwear_phrase} deliberately "
                    "slipped low from both shoulders and gathered symmetrically around the upper arms"
                )
            elif outerwear_wearing_style == "Draped over shoulders":
                standalone_sentences.append(
                    f"The subject also has {indefinite_article(outerwear_phrase)} {outerwear_phrase} draped evenly "
                    "over both shoulders like a cape, with both arms outside its sleeves"
                )
            elif outerwear_wearing_style == "Off shoulders at elbows":
                standalone_sentences.append(
                    f"The subject also wears {indefinite_article(outerwear_phrase)} {outerwear_phrase} deliberately "
                    "slipped off both shoulders, with its sleeves gathered symmetrically around the elbows"
                )
            elif outerwear_wearing_style == "Carried over one shoulder":
                standalone_sentences.append(
                    f"The subject carries {indefinite_article(outerwear_phrase)} {outerwear_phrase} casually over "
                    "one shoulder instead of wearing it"
                )
            else:
                standalone_sentences.append(
                    f"The subject also wears {indefinite_article(outerwear_phrase)} {outerwear_phrase}{over_outfit}. "
                    f"The {outerwear_type} is worn conventionally, fully covering both shoulders, with both arms "
                    "completely inside its sleeves"
                )

        return clauses, standalone_sentences

    def _format_accessories(self, data):
        wear_keys = [
            "head_accessory", "accessories_glasses", "armwear", "accessories_jewelry", "accessories_necklace",
            "accessories_earrings", "accessories_bracelet", "accessories_rings"
        ]
        carry_keys = ["accessories_bag"]
        excluded = {"no head accessory", "no glasses", "no armwear", "no necklace", "no earrings", "no bracelet", "no rings", "no bag"}
        wear_items = [data[k] for k in wear_keys if data.get(k) and data[k] not in excluded]
        carry_items = [data[k] for k in carry_keys if data.get(k) and data[k] not in excluded]
        return wear_items, carry_items

    def _collect_hair_descriptors(self, data):
        descriptors = []
        hair_adjectives = [value for value in [data.get("hair_texture"), data.get("hair_color")] if value]
        if hair_adjectives:
            descriptors.append(" ".join(hair_adjectives + ["hair"]))
        for key in ["hair_style", "hair_cut", "hair_length", "bangs_style"]:
            value = data.get(key)
            if value:
                descriptors.append(value)
        return descriptors

    def _media_preset(self, media_type):
        preset = MEDIA_TYPE_PRESETS.get(media_type, {})
        intro = preset.get("intro") or media_type or "image"
        style = list(preset.get("style") or [])
        return intro, style

    def _media_intro_with_effect(self, data):
        media_type = data.get("media_type") or "image"
        media_intro, media_style = self._media_preset(media_type)
        effect = data.get("optical_effect")
        if effect:
            phrase = f'"{effect}" {media_intro}'
            article_basis = effect
        else:
            phrase = media_intro
            article_basis = media_intro
        return phrase, media_style, indefinite_article(article_basis).capitalize()

    def _resolve_species_subject(self, gender, species_mode):
        species_mode = species_mode if species_mode in SPECIES_MODE_SUBJECT_MAP else "Human"
        subject_map = SPECIES_MODE_SUBJECT_MAP.get(species_mode, SPECIES_MODE_SUBJECT_MAP["Human"])
        subject_gender = subject_map.get(gender, gender or "person")
        if species_mode == "Anthro Furry":
            booster = list(ANTHRO_FURRY_PREFIX)
        else:
            booster = []
        return subject_gender, booster

    def _ethnicity_descriptor(self, data, ethnicity_guidance=False):
        ethnicity = data.get("origin_ethnicity")
        if not ethnicity:
            return None
        if ethnicity_guidance:
            template = ETHNICITY_PROMPTS.get(ethnicity, ethnicity)
            return template.format(eye_color=data.get("eye_color") or "brown")
        return ethnicity

    def _build_full_prompt(self, data, free_prompt="", free_prompt_position="After introduction", enhance_realism=False, species_mode="Human", ethnicity_guidance=False):
        media_intro, media_style, media_article = self._media_intro_with_effect(data)
        portrait_style = data.get("portrait_style") or "portrait"
        gender = data.get("gender") or "person"
        age = data.get("origin_age")
        subject_gender, species_prefix = self._resolve_species_subject(gender, species_mode)

        subject = f"{age} {subject_gender}" if age else subject_gender
        intro = f"{media_article} {media_intro}, {portrait_style} of {indefinite_article(subject)} {subject}"

        intro_descriptors = []
        portrait_descriptors = []
        post_makeup_descriptors = []
        final_descriptors = []

        ethnicity_descriptor = self._ethnicity_descriptor(data, ethnicity_guidance=ethnicity_guidance)
        if ethnicity_descriptor:
            intro_descriptors.append(ethnicity_descriptor)

        content_rating = data.get("content_rating")
        if content_rating:
            intro_descriptors.append(CONTENT_RATING_MAP.get(content_rating, content_rating))

        pose = data.get("pose")
        if pose:
            intro_descriptors.append(pose)

        portrait_order = [
            ("body_type", "{value}"),
            ("body_physique", "{value}"),
            ("body_feminine_curves", "{value}"),
            ("body_hair", "{value}"),
            ("bust", "{value}"),
            ("cleavage_depth", "{value}"),
            ("cleavage_type", "{value}"),
            ("butt_shape", "{value}"),
            ("thigh_shape", "{value}"),
            ("skin_finish", "{value}"),
            ("expression", "{value}"),
            ("eye_expression", "{value} gaze"),
            ("face_shape", "{value} face"),
            ("jawline", "{value}"),
            ("chin_shape", "{value}"),
            ("eye_shape", "{value} eyes"),
            ("eye_color", "{value} eyes"),
            ("eyelashes", "{value}"),
            ("eyebrows", "{value}"),
            ("nose_shape", "{value}"),
            ("lip_shape", "{value}"),
            ("facial_hair", "{value}"),
            ("makeup_eye", "{value}"),
            ("makeup_lips", "{value}"),
            ("nail_style", "{value}"),
            ("tattoo_style", "{value}"),
            ("makeup_complexion", "{value}"),
        ]

        for key, template in portrait_order:
            if key == "eye_color" and ethnicity_guidance and data.get("origin_ethnicity"):
                continue
            value = data.get(key)
            if value:
                portrait_descriptors.append(template.format(value=value))

        portrait_descriptors.extend(self._collect_hair_descriptors(data))

        clothing_clauses, clothing_sentences = self._format_clothing(data)
        wear_accessories, carry_accessories = self._format_accessories(data)
        if clothing_clauses:
            post_makeup_descriptors.append("This subject is " + ", ".join(clothing_clauses))
        post_makeup_descriptors.extend(clothing_sentences)
        if wear_accessories:
            post_makeup_descriptors.append("This subject is wearing " + join_phrases(wear_accessories))
        if carry_accessories:
            post_makeup_descriptors.append("This subject is carrying " + join_phrases(carry_accessories))

        for key, template in [
            ("pose_mood", "{value}"),
            ("setting", "{value}"),
            ("lens_style", "{value}"),
            ("shot_composition", "{value}"),
            ("camera_direction", "{value}"),
            ("lighting_style", "{value}"),
        ]:
            value = data.get(key)
            if value:
                final_descriptors.append(template.format(value=value))

        first_sentence_parts = [intro]
        if species_prefix:
            first_sentence_parts.extend(species_prefix)
        first_sentence_parts.extend(media_style)
        if free_prompt and free_prompt_position == "After introduction":
            first_sentence_parts.append(free_prompt)
        first_sentence_parts.extend(intro_descriptors)
        first_sentence_parts.extend(portrait_descriptors)
        if free_prompt and free_prompt_position == "After makeup":
            first_sentence_parts.append(free_prompt)

        sentences = []
        first_sentence = build_sentence(first_sentence_parts)
        if first_sentence:
            sentences.append(first_sentence)

        for clause in post_makeup_descriptors:
            sentences.append(ensure_period(clause))

        final_sentence = build_sentence(final_descriptors)
        if final_sentence:
            sentences.append(final_sentence)

        if free_prompt and free_prompt_position == "At end":
            sentences.append(ensure_period(free_prompt))
        if enhance_realism:
            sentences.append(ensure_period(ENHANCE_REALISM_SUFFIX))
        return " ".join(sentence for sentence in sentences if sentence).strip()

    def _build_face_prompt(self, data, species_mode="Human", ethnicity_guidance=False):
        media_intro, media_style, media_article = self._media_intro_with_effect(data)
        gender = data.get("gender") or "person"
        age = data.get("origin_age")
        subject_gender, _species_prefix = self._resolve_species_subject(gender, species_mode)
        subject = f"{age} {subject_gender}" if age else subject_gender
        intro = f"{media_article} {media_intro} of {indefinite_article(subject)} {subject}"

        parts = [intro]
        parts.extend(media_style)
        ethnicity_descriptor = self._ethnicity_descriptor(data, ethnicity_guidance=ethnicity_guidance)
        if ethnicity_descriptor:
            parts.append(ethnicity_descriptor)
        skip_values = {"no head accessory", "no glasses", "no scarf", "no earrings"}

        face_order = [
            ("expression", "{value}"),
            ("eye_expression", "{value} gaze"),
            ("face_shape", "{value} face"),
            ("jawline", "{value}"),
            ("chin_shape", "{value}"),
            ("eye_shape", "{value} eyes"),
            ("eye_color", "{value} eyes"),
            ("eyelashes", "{value}"),
            ("eyebrows", "{value}"),
            ("nose_shape", "{value}"),
            ("lip_shape", "{value}"),
            ("facial_hair", "{value}"),
            ("makeup_eye", "{value}"),
            ("makeup_lips", "{value}"),
            ("head_accessory", "{value}"),
            ("accessories_glasses", "{value}"),
            ("accessories_earrings", "{value}"),
            ("accessories_scarf", "{value}"),
            ("makeup_complexion", "{value}"),
            ("lighting_style", "{value}"),
        ]

        for key, template in face_order:
            if key == "eye_color" and ethnicity_guidance and data.get("origin_ethnicity"):
                continue
            value = data.get(key)
            if value and value not in skip_values:
                parts.append(template.format(value=value))

        parts.extend(self._collect_hair_descriptors(data))

        return ", ".join(part for part in parts if part).strip()

    def build_prompt(self, free_prompt="", free_prompt_position="After introduction", ethnicity_guidance=False, enhance_realism=False, species_mode="Human", seed=0, control_after_generate="randomize", override_field="None", override_text="", inspect_property="None", **kwargs):
        ethnicity_guidance = is_enabled(ethnicity_guidance)
        data = self._resolve_values(kwargs, seed=seed, ethnicity_guidance=ethnicity_guidance)
        override_text = (override_text or "").strip().strip(",")
        valid_fields = {item["key"] for item in SCHEMA["categories"]}
        if override_field in valid_fields and override_text:
            # Applied after every random, guidance, compatibility, and framing
            # rule: a connected string is the user's final authority.
            for conflicting_field in MAIN_CLOTHING_OVERRIDE_CONFLICTS.get(override_field, ()):
                data[conflicting_field] = None
            data[override_field] = override_text
        free_prompt = (free_prompt or "").strip().strip(",")
        enhance_realism = is_enabled(enhance_realism)

        # Backward compatibility: some older workflows may still pass the former
        # furry_enhancer field through kwargs or restoration logic. Map it into
        # the new species_mode concept when species_mode is not already explicit.
        if species_mode not in {"Human", "Anthro Furry"}:
            legacy_furry = kwargs.get("furry_enhancer", None)
            if isinstance(species_mode, bool) or isinstance(species_mode, (int, float)) or isinstance(species_mode, str):
                if is_enabled(species_mode) or is_enabled(legacy_furry):
                    species_mode = "Anthro Furry"
                else:
                    species_mode = "Human"
            else:
                species_mode = "Human"

        full_prompt = self._build_full_prompt(data, free_prompt=free_prompt, free_prompt_position=free_prompt_position, enhance_realism=enhance_realism, species_mode=species_mode, ethnicity_guidance=ethnicity_guidance)
        face_prompt = self._build_face_prompt(data, species_mode=species_mode, ethnicity_guidance=ethnicity_guidance)
        inspected_value = ""
        if inspect_property in valid_fields:
            value = data.get(inspect_property)
            inspected_value = "" if value is None else str(value)
        return (full_prompt, face_prompt, inspected_value)
