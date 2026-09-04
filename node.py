import hashlib
import json
import re
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "data" / "categories.json"

CONTENT_RATING_SENTENCES = {
    "normal": "The subject is presented with a neutral, non-sexualized, non-explicit treatment.",
    "glamour/sexy/explicit": "The subject is presented with a glamorous, sexualized, explicit treatment.",
}

NATURAL_REALISM_SUFFIX = "Captured as a spontaneous real-life photograph, casual and unstaged, with natural body language, ordinary environmental details, believable lighting falloff, realistic camera exposure, subtle sensor texture, imperfect but plausible composition, restrained post-processing, authentic skin, hair and fabric detail, and the quiet visual randomness of an actual moment."
DIRECTED_REALISM_SUFFIX = "Captured as a believable real-life photograph with intentional visual direction, plausible body language, coherent environmental detail, believable lighting falloff, realistic camera exposure, subtle sensor texture, controlled but natural composition, restrained post-processing, and authentic skin, hair and fabric detail."
CREATURE_REALISM_SUFFIX = "Captured as a tangible real-world creature, with physically plausible nonhuman anatomy, coherent material response to light, believable interaction between its body, clothing, and environment, realistic camera exposure, subtle sensor texture, restrained post-processing, and imperfect but plausible composition."
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


# Identity Forge compatibility is intentionally data-driven. Character Architect
# does not try to identify a blob, centaur, robot, or any other morphology from a
# library of creature names. It reads the exact anatomy phrases supplied in the
# connected JSON and applies a small fixed grammar around those phrases.
IDENTITY_SPECIES_GROUP = "Species & Anatomy"
IDENTITY_SLOT_ORDER = (
    "head", "eyes", "integument", "arms", "hands", "legs_feet", "tail", "wings", "extras",
)

IDENTITY_TO_CA_FIELD = {
    "age": "origin_age",
    "body_type": "body_type",
    "fitness_level": "body_physique",
    "bust": "bust",
    "face_shape": "face_shape",
    "jawline": "jawline",
    "chin": "chin_shape",
    "eye_shape": "eye_shape",
    "eye_color": "eye_color",
    "eyebrows": "eyebrows",
    "nose": "nose_shape",
    "lips": "lip_shape",
    "hair_color": "hair_color",
    "hair_length": "hair_length",
    "hair_texture": "hair_texture",
    "hair_style": "hair_style",
    "facial_hair": "facial_hair",
    "hair_accessory": "head_accessory",
    "expression": "expression",
    "pose": "pose",
    "location": "setting",
    "location_setting": "setting",
    "lighting": "lighting_style",
    "shot_type": "portrait_style",
    "mood": "pose_mood",
    "composition": "shot_composition",
    "bag": "accessories_bag",
    "accessories": "accessories_jewelry",
    "footwear": "footwear",
    "earrings": "accessories_earrings",
    "necklace": "accessories_necklace",
    "other_jewelry": "accessories_jewelry",
    "nails": "nail_style",
    "rings": "accessories_rings",
    "bracelet": "accessories_bracelet",
    "eye_makeup": "makeup_eye",
    "lashes": "eyelashes",
    "lips_makeup": "makeup_lips",
    "skin_finish": "makeup_complexion",
}

IDENTITY_FIELD_GROUP = {
    "age": "Demographics", "ethnicity": "Demographics", "gender": "Demographics",
    "body_type": "Body", "bust": "Body", "fitness_level": "Body", "height": "Body",
    "posture": "Body", "shoulder_width": "Body", "skin_tone": "Body",
    "complexion": "Face", "eye_color": "Face", "eye_shape": "Face",
    "eyebrows": "Face", "face_shape": "Face", "freckles_density": "Face",
    "skin_details": "Face", "facial_hair": "Hair", "hair_accessory": "Hair",
    "hair_color": "Hair", "hair_highlights": "Hair", "hair_length": "Hair",
    "hair_part": "Hair", "hair_style": "Hair", "hair_texture": "Hair",
    "blush": "Makeup", "contour": "Makeup", "eye_makeup": "Makeup",
    "eyeliner": "Makeup", "highlight": "Makeup", "lashes": "Makeup",
    "lips_makeup": "Makeup", "makeup_style": "Makeup", "skin_finish": "Makeup",
    "bracelet": "Jewelry & Nails", "earrings": "Jewelry & Nails",
    "nails": "Jewelry & Nails", "necklace": "Jewelry & Nails",
    "piercings": "Jewelry & Nails", "rings": "Jewelry & Nails",
    "accessories": "Clothing", "bag": "Clothing", "outfit_description": "Clothing",
    "expression": "Setting & Shot",
    "held_item": "Setting & Shot", "lighting": "Setting & Shot",
    "location": "Setting & Shot", "location_setting": "Setting & Shot",
    "mood": "Setting & Shot", "pose": "Setting & Shot", "shot_type": "Setting & Shot",
    "composition": "Setting & Shot",
}

IDENTITY_GROUP_CA_FIELDS = {
    "Demographics": {"origin_age", "origin_ethnicity"},
    "Body": {
        "body_archetype", "body_type", "body_physique", "body_feminine_curves", "body_hair", "skin_finish", "bust",
        "cleavage_depth", "cleavage_type", "butt_shape", "thigh_shape",
        "body_detail_1", "body_detail_2", "body_detail_3",
    },
    "Face": {
        "face_shape", "jawline", "chin_shape", "eye_shape", "eye_color", "eyebrows", "nose_shape",
        "lip_shape", "expression", "eye_expression",
    },
    "Hair": {
        "hair_color", "hair_texture", "hair_style", "hair_cut", "hair_length", "bangs_style", "facial_hair",
    },
    "Makeup": {"eyelashes", "makeup_eye", "makeup_complexion", "makeup_lips"},
    "Jewelry & Nails": {
        "nail_style", "accessories_jewelry", "accessories_necklace", "accessories_earrings",
        "accessories_bracelet", "accessories_rings",
    },
    "Clothing": {
        "clothing_archetype", "top_type", "top_color", "bottom_type", "bottom_length",
        "bottom_color", "lingerie_type", "lingerie_color", "sleepwear_type", "sleepwear_color",
        "cosplay_type", "cosplay_franchise_western", "cosplay_franchise_asian", "cosplay_color",
        "hosiery", "hosiery_color", "dress_type", "dress_color", "outerwear", "outerwear_color",
        "outerwear_wearing_style", "belt", "belt_color", "footwear", "footwear_color",
        "accessories_bag",
    },
    "Setting & Shot": {
        "composition_archetype", "portrait_style", "capture_style", "setting", "scene_scenario", "lens_style", "shot_composition", "pose_mood", "pose",
        "camera_direction", "head_direction", "camera_angle", "lighting_style", "optical_effect",
    },
}

# These fields are human-anatomy assertions. In an Anthropomorphic/Feral creature
# branch, ordinary Random values are removed. A manual choice, Forced Random, or
# universal text override remains authoritative and can deliberately reintroduce one.
CREATURE_HUMAN_ANATOMY_FIELDS = set().union(
    IDENTITY_GROUP_CA_FIELDS["Demographics"],
    IDENTITY_GROUP_CA_FIELDS["Body"],
    IDENTITY_GROUP_CA_FIELDS["Face"],
    IDENTITY_GROUP_CA_FIELDS["Hair"],
    IDENTITY_GROUP_CA_FIELDS["Makeup"],
)
CREATURE_HUMAN_ANATOMY_FIELDS.discard("origin_age")

# Ordinary Random values in these fields assume human organs or a conventional
# humanoid silhouette. A leading creature therefore starts without them. JSON,
# manual selections, Forced Random, and the universal override can still add
# them deliberately.
CREATURE_ORGAN_DEPENDENT_FIELDS = {
    "tattoo_style", "nail_style", "head_accessory", "accessories_scarf",
    "accessories_jewelry", "accessories_necklace", "accessories_earrings",
    "accessories_bracelet", "accessories_rings", "accessories_glasses",
    "armwear", "accessories_bag", "footwear", "footwear_color",
}

IDENTITY_MAIN_CLOTHING_FIELDS = {
    "top_type", "bottom_type", "dress_type", "lingerie_type", "sleepwear_type",
    "cosplay_type", "cosplay_franchise_western", "cosplay_franchise_asian",
}
IDENTITY_OUTFIT_RANDOM_CLEAR_FIELDS = {
    *IDENTITY_MAIN_CLOTHING_FIELDS,
    "top_color", "bottom_length", "bottom_color", "lingerie_color", "sleepwear_color",
    "cosplay_color", "dress_color", "belt", "belt_color", "footwear", "footwear_color",
    "hosiery", "hosiery_color", "outerwear", "outerwear_color", "outerwear_wearing_style",
}

# Unmapped Identity Forge fields still have deterministic, compact prose. These
# templates describe the supplied value; they never infer new creature anatomy.
IDENTITY_EXTRA_TEMPLATES = {
    "skin_tone": "{value} skin",
    "height": "{value}",
    "waist": "{value} waist",
    "hips": "{value} hips",
    "shoulder_width": "{value} shoulders",
    "neck_length": "{value} neck",
    "posture": "{value} posture",
    "forehead": "{value} forehead",
    "cheekbones": "{value} cheekbones",
    "complexion": "{value} complexion",
    "skin_details": "{value}",
    "freckles_density": "{value}",
    "smile_type": "{value}",
    "hair_part": "{value}",
    "hair_highlights": "{value}",
    "makeup_style": "{value}",
    "eyebrow_makeup": "{value}",
    "eyeliner": "{value}",
    "contour": "{value}",
    "highlight": "{value}",
    "blush": "{value}",
    "piercings": "{value}",
    "watch_type": "{value}",
    "season": "{value}",
    "clothing_color": "{value}",
    "clothing_pattern": "{value}",
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
    "bedroom selfie": "portrait",
    "full-body glamour portrait": "full-body portrait",
    "editorial portrait": "portrait",
    "cinematic portrait": "portrait",
    "fashion portrait": "portrait",
    "beauty portrait": "portrait",
    "street-style portrait": "portrait",
    "environmental portrait": "portrait",
    "candid portrait": "portrait",
    "dramatic portrait": "portrait",
    "spontaneous handheld selfie": "portrait",
}

LEGACY_CAPTURE_STYLE_BY_PORTRAIT = {
    "full-body glamour portrait": "glamour",
    "editorial portrait": "editorial",
    "cinematic portrait": "cinematic",
    "fashion portrait": "fashion",
    "beauty portrait": "beauty",
    "street-style portrait": "street-style",
    "environmental portrait": "environmental",
    "candid portrait": "candid",
    "dramatic portrait": "dramatic",
    "spontaneous handheld selfie": "candid",
    "bedroom selfie": "candid",
}

LEGACY_PHOTOGRAPHIC_EFFECT_MAP = {
    "fisheye optical distortion": "fisheye",
    "Petzval swirling bokeh": None,
    "split-diopter depth effect": None,
}

LEGACY_CATEGORY_VALUE_MAPS = {
    "content_rating": {
        "glamour": "glamour/sexy/explicit",
        "sexy": "glamour/sexy/explicit",
        "explicit": "glamour/sexy/explicit",
        "glamour / sexy / explicit": "glamour/sexy/explicit",
    },
    "dress_type": {
        "contemporary djellaba, a full-length loose hooded robe": "contemporary djellaba",
        "contemporary kaftan dress with long flowing sleeves": "contemporary kaftan",
        "salwar kameez ensemble with a long tunic and straight trousers": "salwar kameez ensemble",
        "kurta and flowing trouser ensemble": "kurta and trouser ensemble",
        "contemporary sari draped over a fitted blouse": "contemporary sari",
        "embroidered anarkali dress with a long flared silhouette": "Anarkali suit",
        "kebaya blouse with a coordinated batik sarong": "kebaya and batik sarong ensemble",
        "baju kurung ensemble with a long tunic and ankle-length skirt": "baju kurung ensemble",
        "ao dai tunic over flowing trousers": "ao dai ensemble",
        "West African boubou robe over a matching underdress": "West African boubou ensemble",
        "modern qipao dress with a mandarin collar and side slits": "modern qipao",
    },
    "body_type": {
        "very petite": "very short", "petite": "short", "short compact": "short", "compact": "short",
        "lanky": "tall", "tall slender": "tall", "tall curvy": "tall", "statuesque": "tall",
        "slim": "average height", "slender": "average height", "average": "average height",
        "voluptuous": "average height", "plus-size": "average height", "stocky": "average height",
        "broad-built": "average height", "androgynous": "average height",
    },
    "body_physique": {
        "soft physique": "soft untrained physique", "wiry physique": "toned physique",
        "lean masculine physique": "athletic physique", "broad-shouldered physique": "muscular physique",
        "very muscular physique": "heavily muscular physique", "powerfully muscular physique": "heavily muscular physique",
        "heavy muscular physique": "heavily muscular physique", "dance-athletic physique": "athletic physique",
        "plush physique": "plump physique",
    },
    "body_feminine_curves": {
        "flat silhouette": "almost no curves", "boyish silhouette": "straight silhouette",
        "androgynous build": "androgynous silhouette", "gentle curves": "subtle curves",
        "moderate curves": "balanced curves",
        "pronounced curves": "pronounced hourglass silhouette", "gentle hourglass silhouette": "soft hourglass silhouette",
        "curvy silhouette": "pronounced hourglass silhouette", "pear silhouette": "pear-shaped silhouette",
        "top heavy silhouette": "top-heavy silhouette", "narrow hips": "narrow-hip silhouette",
        "wide hips": "wide-hip silhouette", "short-legged proportions": "short-legged proportions",
        "long-legged proportions": "long-legged proportions",
        "pronounced inward lumbar curve with a deeply arched lower-back silhouette": "pronounced lumbar lordosis, with a deeply concave lower back, the abdomen projecting forward, and the pelvis tilted so the buttocks project prominently backward",
    },
    "lens_style": {
        "smartphone camera look": None,
    },
    "lighting_style": {
        "candlelit ambiance": None,
    },
    "camera_direction": {
        "back view": "rear three-quarter view",
        "facing camera": "front-facing view",
        "three-quarter angle": "three-quarter view",
        "looking down toward camera": "front-facing view",
        "looking upward": "front-facing view",
        "front-facing symmetrical view": "front-facing view",
        "head tilted toward camera": "front-facing view",
        "slight sideways glance": "three-quarter view",
        "high-angle view": "front-facing view",
        "low-angle view": "front-facing view",
        "pronounced high-angle view, with the camera positioned above the subject": "front-facing view",
        "pronounced low-angle view, with the camera positioned below the subject": "front-facing view",
        "rear three-quarter view with the subject looking back over one shoulder": "rear three-quarter view",
    },
    "camera_angle": {
        "high-angle view": "from a pronounced high angle, with the camera positioned above the subject",
        "low-angle view": "from a pronounced low angle, with the camera positioned below the subject",
        "pronounced high-angle view, with the camera positioned above the subject": "from a pronounced high angle, with the camera positioned above the subject",
        "pronounced low-angle view, with the camera positioned below the subject": "from a pronounced low angle, with the camera positioned below the subject",
    },
    "head_direction": {
        "looking down toward camera": "looking downward",
        "looking downward toward the camera": "looking downward",
        "looking upward": "looking upward",
        "head tilted toward camera": "head tilted slightly",
        "slight sideways glance": "glancing slightly to one side",
        "rear three-quarter view with the subject looking back over one shoulder": "looking back over one shoulder",
    },
    "shot_composition": {
        "clean studio composition": "clean precisely organized composition",
        "tight crop": None,
        "wide framing": None,
    },
    "pose": {
        "low side squat, one heel raised, torso upright": "low side squat, torso upright",
        "standing with the back partly turned, looking over one shoulder, hips shifted softly to one side": "standing with the weight shifted softly onto one hip",
        "standing in a three-quarter pose, one hand in the hair, hips turned away": "standing with one hand in the hair and the weight shifted onto one hip",
        "leaning back against a wall, one knee bent, hips angled slightly, relaxed sensual posture": "leaning back against a wall with one knee bent and the hips angled slightly",
        "sitting sideways on a stool, upper body twisting toward the camera, one hand braced behind": "seated on the edge of a stool with one hand braced behind",
        "on hands and knees, back mostly straight, head turned toward the camera, natural elegant body line": "on hands and knees with the back mostly straight",
        "on hands and knees viewed from a rear three-quarter angle, hips angled toward the camera, looking back over one shoulder": "on hands and knees with the weight shifted onto one arm",
        "on hands and knees with one knee drawn forward between the hands, torso turned slightly toward the camera": "on hands and knees with one knee drawn forward between the hands and the torso gently twisted",
        "kneeling with forearms resting on the floor, hips raised, back gently curved, head turned toward the camera": "kneeling with forearms resting on the floor, hips raised, and the back gently curved",
        "riding a bicycle through the scene, both hands holding the handlebars, body leaning naturally forward, captured in gentle motion": "riding a bicycle with both hands holding the handlebars and the body leaning naturally forward",
        "seated behind the wheel of a car, both hands placed naturally on the steering wheel, actively driving while glancing toward the camera": "seated behind the wheel of a car with both hands placed naturally on the steering wheel while actively driving",
        "riding a moving carousel horse, seated astride the saddle with one hand holding the central pole, surrounding lights and background softened by motion blur": "riding a moving carousel horse, seated astride the saddle with one hand holding the central pole",
        "raising one hand in a friendly wave toward someone off-frame": "raising one hand in a friendly wave",
        "on hands and knees with the back mostly straight and the head raised naturally": "on hands and knees with the back mostly straight",
        "on hands and knees with a gentle arch through the lower back, shoulders lowered, chin slightly raised": "on hands and knees with a gentle arch through the lower back and the shoulders lowered",
        "kneeling with forearms resting on the floor, hips raised, back gently curved, and head raised naturally": "kneeling with forearms resting on the floor, hips raised, and the back gently curved",
    },
    "pose_mood": {
        "relaxed pose": "relaxed attitude",
        "confident pose": "confident attitude",
        "playful pose": "playful attitude",
        "seductive pose": "seductive attitude",
        "elegant pose": "elegant bearing",
        "guarded pose": "guarded attitude",
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

# Eye Focus controls the subject's visual target, independently from the angle
# of the head and the emotional quality of the gaze.  These phrases are already
# anatomically anchored so the final prompt can place them next to camera
# geometry without relying on a vague "looking at camera" fallback.
EYE_FOCUS_VALUES = [
    "eyes focused directly on the camera",
    "eyes focused just past the camera",
    "eyes focused on a nearby person",
    "eyes focused on a nearby object",
    "eyes focused on the object held in the hands",
    "eyes focused into the distance",
    "eyes focused toward the subject's left",
    "eyes focused toward the subject's right",
]

# Composition Archetypes are coherent, variable recipes built exclusively from
# vocabulary exposed by the regular widgets.  Repeated values are deliberate
# weights.  The archetype name itself never enters the prompt.
COMPOSITION_ARCHETYPE_VALUES = [
    "Direct Headshot",
    "Three-Quarter Close Portrait",
    "Strict Profile Portrait",
    "High-Angle Intimate Portrait",
    "Low-Angle Iconic Portrait",
    "Rear Look-Back Portrait",
    "Relaxed Hip-Shift Standing",
    "Hand-in-Hair Standing",
    "Arms-Raised Standing",
    "Wall-Leaning Portrait",
    "Forward-Leaning Portrait",
    "Folded-Arms Portrait",
    "Hands-in-Pockets Standing",
    "Hands-Behind-Back Standing",
    "Friendly Hand Gesture",
    "Formal Salute",
    "Cross-Legged Seated",
    "Chair-Edge Forward Lean",
    "Knee-Drawn-Up Seated",
    "Side Stool Portrait",
    "Low Open Seated",
    "Balanced Low Squat",
    "Compact Squat",
    "Grounded Crouch",
    "Side Squat",
    "Elegant Heel-Sit",
    "One-Knee Kneel",
    "Upright Open-Elbow Kneel",
    "Forward-Leaning Kneel",
    "All-Fours Neutral",
    "All-Fours Twist",
    "Arched Floor Pose",
    "Playful Prone",
    "Side S-Curve Reclining",
    "Open Supine",
    "Head-Supported Side Recline",
    "Asymmetric Supine",
    "Prone Forearm Portrait",
    "Curled Side Recline",
    "Bent-Knee Supine",
    "Dynamic Movement",
    "Handheld Selfie",
    "Focused Handheld Object",
    "Writing in Hand",
    "Casual Sip",
    "Social Candid",
    "Attentive Observer",
    "Crowd Reaction",
    "Waiting Candid",
    "Social Exchange",
]

COMPOSITION_ARCHETYPE_CONTROL_FIELDS = {
    "portrait_style", "pose", "camera_direction", "head_direction",
    "eye_focus", "camera_angle", "shot_composition",
}

EYE_LEVEL_ANGLE = "at eye level"
LOW_ANGLE = "from a pronounced low angle, with the camera positioned below the subject"
WORM_EYE_ANGLE = "from an extreme worm's-eye angle at ground level, with the camera looking sharply upward"
HIGH_ANGLE = "from a pronounced high angle, with the camera positioned above the subject"
OVERHEAD_ANGLE = "from an overhead bird's-eye angle, with the camera looking straight down"

DIRECT_EYE_FOCUS = "eyes focused directly on the camera"
PAST_CAMERA_FOCUS = "eyes focused just past the camera"
NEARBY_PERSON_FOCUS = "eyes focused on a nearby person"
NEARBY_OBJECT_FOCUS = "eyes focused on a nearby object"
HELD_OBJECT_FOCUS = "eyes focused on the object held in the hands"
DISTANCE_FOCUS = "eyes focused into the distance"
LEFT_FOCUS = "eyes focused toward the subject's left"
RIGHT_FOCUS = "eyes focused toward the subject's right"

# Seventy percent direct camera focus in neutral recipes keeps camera-facing
# eyes dominant across the complete archetype catalogue.  Context-dependent
# recipes below deliberately replace it when the action has a clear target.
CAMERA_DOMINANT_FOCUS = (
    [DIRECT_EYE_FOCUS] * 7
    + [PAST_CAMERA_FOCUS] * 2
    + [DISTANCE_FOCUS]
)
CAMERA_OR_SOCIAL_FOCUS = (
    [DIRECT_EYE_FOCUS] * 5
    + [PAST_CAMERA_FOCUS] * 2
    + [NEARBY_PERSON_FOCUS] * 2
    + [DISTANCE_FOCUS]
)
PROFILE_FOCUS = [DISTANCE_FOCUS] * 4 + [LEFT_FOCUS] * 2 + [RIGHT_FOCUS] * 2 + [PAST_CAMERA_FOCUS]
REAR_CAMERA_FOCUS = [DIRECT_EYE_FOCUS] * 7 + [PAST_CAMERA_FOCUS] * 3


def _composition_profile(*, pose, framing, camera, head, focus, angle, composition):
    return {
        "pose": list(pose),
        "portrait_style": list(framing),
        "camera_direction": list(camera),
        "head_direction": list(head),
        "eye_focus": list(focus),
        "camera_angle": list(angle),
        "shot_composition": list(composition),
    }


COMPOSITION_ARCHETYPE_CONFIG = {
    "Direct Headshot": _composition_profile(
        pose=[None],
        framing=["close-up portrait", "headshot portrait", "headshot portrait", "bust portrait"],
        camera=["front-facing view"] * 4 + ["three-quarter view"],
        head=["head held level"] * 4 + ["head tilted slightly"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 6 + [HIGH_ANGLE, LOW_ANGLE],
        composition=["centered composition"] * 3 + ["symmetrical composition"] * 2 + ["clean precisely organized composition", "editorial magazine composition"],
    ),
    "Three-Quarter Close Portrait": _composition_profile(
        pose=[None, "standing with one hand in the hair and the weight shifted onto one hip", "adjusting one sleeve with the opposite hand"],
        framing=["close-up portrait", "bust portrait", "bust portrait", "half-body portrait"],
        camera=["three-quarter view"] * 4 + ["front-facing view"],
        head=["head held level"] * 3 + ["head tilted slightly"] * 2 + ["glancing slightly to one side"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 6 + [HIGH_ANGLE, LOW_ANGLE],
        composition=["rule-of-thirds composition"] * 3 + ["editorial magazine composition"] * 2 + ["clean precisely organized composition", "candid off-center framing"],
    ),
    "Strict Profile Portrait": _composition_profile(
        pose=[None],
        framing=["close-up portrait", "headshot portrait", "bust portrait"],
        camera=["profile view"],
        head=["head held level"] * 3 + ["looking upward", "looking downward", "glancing slightly to one side"],
        focus=PROFILE_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 6 + [HIGH_ANGLE, LOW_ANGLE],
        composition=["negative-space composition"] * 4 + ["rule-of-thirds composition"] * 2 + ["candid off-center framing"],
    ),
    "High-Angle Intimate Portrait": _composition_profile(
        pose=[None, "standing with one hand in the hair and the weight shifted onto one hip"],
        framing=["close-up portrait", "headshot portrait", "bust portrait"],
        camera=["front-facing view"] * 3 + ["three-quarter view"] * 2,
        head=["looking upward"] * 4 + ["head held level", "head tilted slightly"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[HIGH_ANGLE] * 5 + [OVERHEAD_ANGLE],
        composition=["subject placed low in frame"] * 3 + ["centered composition"] * 2 + ["rule-of-thirds composition", "clean precisely organized composition"],
    ),
    "Low-Angle Iconic Portrait": _composition_profile(
        pose=[None, "standing naturally with both arms folded across the chest", "standing with both hands loosely clasped behind the back"],
        framing=["bust portrait", "half-body portrait", "half-body portrait", "three-quarter portrait"],
        camera=["front-facing view"] * 3 + ["three-quarter view"] * 2,
        head=["looking downward"] * 4 + ["head held level", "head tilted slightly"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[LOW_ANGLE] * 5 + [WORM_EYE_ANGLE],
        composition=["subject placed high in frame"] * 3 + ["centered composition"] * 2 + ["symmetrical composition", "editorial magazine composition"],
    ),
    "Rear Look-Back Portrait": _composition_profile(
        pose=["standing with the weight shifted softly onto one hip", "standing with both hands loosely clasped behind the back", "leaning back against a wall with one knee bent"],
        framing=["bust portrait", "half-body portrait", "three-quarter portrait"],
        camera=["rear three-quarter view"],
        head=["looking back over one shoulder"],
        focus=REAR_CAMERA_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 6 + [LOW_ANGLE, HIGH_ANGLE],
        composition=["rule-of-thirds composition"] * 3 + ["candid off-center framing"] * 2 + ["negative-space composition", "editorial magazine composition"],
    ),
    "Relaxed Hip-Shift Standing": _composition_profile(
        pose=["standing with the weight shifted softly onto one hip"],
        framing=["half-body portrait", "three-quarter portrait", "three-quarter portrait", "full-body portrait"],
        camera=["front-facing view"] * 3 + ["three-quarter view"] * 4 + ["profile view"],
        head=["head held level"] * 4 + ["head tilted slightly"] * 2 + ["glancing slightly to one side"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 6 + [LOW_ANGLE, HIGH_ANGLE],
        composition=["rule-of-thirds composition"] * 3 + ["editorial magazine composition"] * 2 + ["candid off-center framing", "negative-space composition"],
    ),
    "Hand-in-Hair Standing": _composition_profile(
        pose=["standing with one hand in the hair and the weight shifted onto one hip"],
        framing=["half-body portrait", "three-quarter portrait", "three-quarter portrait", "full-body portrait"],
        camera=["front-facing view"] * 3 + ["three-quarter view"] * 4,
        head=["head held level"] * 3 + ["head tilted slightly"] * 2 + ["glancing slightly to one side"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 6 + [LOW_ANGLE, HIGH_ANGLE],
        composition=["editorial magazine composition"] * 3 + ["rule-of-thirds composition"] * 2 + ["negative-space composition", "clean precisely organized composition"],
    ),
    "Arms-Raised Standing": _composition_profile(
        pose=["standing with both arms raised, wrists loosely crossed"],
        framing=["three-quarter portrait", "full-body portrait", "full-body portrait"],
        camera=["front-facing view"] * 4 + ["three-quarter view"] * 3,
        head=["head held level"] * 3 + ["looking upward"] * 2 + ["head tilted slightly"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 5 + [LOW_ANGLE] * 2 + [HIGH_ANGLE],
        composition=["centered composition"] * 2 + ["symmetrical composition"] * 2 + ["dynamic diagonal composition"] * 2 + ["editorial magazine composition"],
    ),
    "Wall-Leaning Portrait": _composition_profile(
        pose=["leaning back against a wall with one knee bent"],
        framing=["half-body portrait", "three-quarter portrait", "full-body portrait"],
        camera=["three-quarter view"] * 4 + ["profile view"] * 3 + ["front-facing view"],
        head=["head held level"] * 3 + ["head tilted slightly", "glancing slightly to one side", "looking downward"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 6 + [LOW_ANGLE, HIGH_ANGLE],
        composition=["rule-of-thirds composition"] * 3 + ["candid off-center framing"] * 2 + ["negative-space composition"] * 2,
    ),
    "Forward-Leaning Portrait": _composition_profile(
        pose=["bending forward with both hands resting above the knees"],
        framing=["half-body portrait", "three-quarter portrait", "three-quarter portrait"],
        camera=["front-facing view"] * 4 + ["three-quarter view"] * 3,
        head=["head held level"] * 3 + ["looking upward"] * 2 + ["head tilted slightly"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 5 + [HIGH_ANGLE] * 2 + [LOW_ANGLE],
        composition=["centered composition"] * 2 + ["rule-of-thirds composition"] * 3 + ["editorial magazine composition", "candid off-center framing"],
    ),
    "Folded-Arms Portrait": _composition_profile(
        pose=["standing naturally with both arms folded across the chest"],
        framing=["half-body portrait", "three-quarter portrait", "three-quarter portrait", "full-body portrait"],
        camera=["front-facing view"] * 4 + ["three-quarter view"] * 3,
        head=["head held level"] * 4 + ["head tilted slightly", "glancing slightly to one side"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 6 + [LOW_ANGLE, HIGH_ANGLE],
        composition=["centered composition"] * 2 + ["clean precisely organized composition"] * 2 + ["editorial magazine composition"] * 2 + ["rule-of-thirds composition"],
    ),
    "Hands-in-Pockets Standing": _composition_profile(
        pose=["standing casually with both hands resting in the pockets"],
        framing=["three-quarter portrait", "three-quarter portrait", "full-body portrait"],
        camera=["three-quarter view"] * 4 + ["front-facing view"] * 3 + ["profile view"],
        head=["head held level"] * 3 + ["glancing slightly to one side"] * 2 + ["head tilted slightly"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 7 + [LOW_ANGLE, HIGH_ANGLE],
        composition=["candid off-center framing"] * 3 + ["rule-of-thirds composition"] * 3 + ["negative-space composition"],
    ),
    "Hands-Behind-Back Standing": _composition_profile(
        pose=["standing with both hands loosely clasped behind the back"],
        framing=["three-quarter portrait", "full-body portrait", "full-body portrait"],
        camera=["front-facing view"] * 3 + ["three-quarter view"] * 3 + ["profile view"],
        head=["head held level"] * 4 + ["head tilted slightly", "glancing slightly to one side"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 7 + [LOW_ANGLE, HIGH_ANGLE],
        composition=["clean precisely organized composition"] * 2 + ["symmetrical composition"] * 2 + ["rule-of-thirds composition"] * 2 + ["editorial magazine composition"],
    ),
    "Friendly Hand Gesture": _composition_profile(
        pose=[
            "raising one hand in a friendly wave",
            "giving a cheerful thumbs-up with one hand",
            "raising both shoulders in a light shrug, palms turned upward",
            "adjusting one sleeve with the opposite hand",
        ],
        framing=["half-body portrait", "half-body portrait", "three-quarter portrait"],
        camera=["front-facing view"] * 5 + ["three-quarter view"] * 3,
        head=["head held level"] * 4 + ["head tilted slightly"] * 2 + ["glancing slightly to one side"],
        focus=CAMERA_OR_SOCIAL_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 8 + [LOW_ANGLE, HIGH_ANGLE],
        composition=["candid off-center framing"] * 3 + ["rule-of-thirds composition"] * 3 + ["centered composition"],
    ),
    "Formal Salute": _composition_profile(
        pose=["standing at attention with one hand raised in a formal military salute"],
        framing=["half-body portrait", "three-quarter portrait", "full-body portrait"],
        camera=["front-facing view"] * 5 + ["three-quarter view"] * 2,
        head=["head held level"],
        focus=[DIRECT_EYE_FOCUS] * 6 + [DISTANCE_FOCUS] * 2 + [PAST_CAMERA_FOCUS],
        angle=[EYE_LEVEL_ANGLE] * 7 + [LOW_ANGLE] * 2,
        composition=["centered composition"] * 3 + ["symmetrical composition"] * 3 + ["clean precisely organized composition"],
    ),
    "Cross-Legged Seated": _composition_profile(
        pose=["seated upright with legs crossed, one hand resting on the upper knee"],
        framing=["three-quarter portrait", "full-body portrait", "full-body portrait"],
        camera=["front-facing view"] * 3 + ["three-quarter view"] * 4,
        head=["head held level"] * 3 + ["head tilted slightly"] * 2 + ["glancing slightly to one side"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 6 + [HIGH_ANGLE] * 2 + [LOW_ANGLE],
        composition=["editorial magazine composition"] * 3 + ["rule-of-thirds composition"] * 2 + ["centered composition", "clean precisely organized composition"],
    ),
    "Chair-Edge Forward Lean": _composition_profile(
        pose=["perched on the edge of a chair, knees together, torso leaning forward slightly, hands resting on the thighs"],
        framing=["half-body portrait", "three-quarter portrait", "full-body portrait"],
        camera=["front-facing view"] * 4 + ["three-quarter view"] * 3,
        head=["head held level"] * 3 + ["looking upward"] * 2 + ["head tilted slightly"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 5 + [HIGH_ANGLE] * 3,
        composition=["centered composition"] * 2 + ["rule-of-thirds composition"] * 3 + ["subject placed low in frame", "editorial magazine composition"],
    ),
    "Knee-Drawn-Up Seated": _composition_profile(
        pose=["seated with one knee raised toward the chest, arms loosely wrapped around the leg"],
        framing=["three-quarter portrait", "full-body portrait"],
        camera=["three-quarter view"] * 4 + ["profile view"] * 2 + ["front-facing view"],
        head=["head tilted slightly"] * 3 + ["looking downward"] * 2 + ["head held level"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 5 + [HIGH_ANGLE] * 3,
        composition=["candid off-center framing"] * 2 + ["negative-space composition"] * 2 + ["rule-of-thirds composition"] * 2 + ["editorial magazine composition"],
    ),
    "Side Stool Portrait": _composition_profile(
        pose=["seated on the edge of a stool with one hand braced behind"],
        framing=["half-body portrait", "three-quarter portrait", "three-quarter portrait"],
        camera=["three-quarter view"] * 4 + ["profile view"] * 2 + ["front-facing view"],
        head=["head held level"] * 2 + ["head tilted slightly"] * 2 + ["glancing slightly to one side"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 6 + [HIGH_ANGLE, LOW_ANGLE],
        composition=["rule-of-thirds composition"] * 3 + ["editorial magazine composition"] * 2 + ["candid off-center framing", "negative-space composition"],
    ),
    "Low Open Seated": _composition_profile(
        pose=["sitting low with knees comfortably apart, elbows resting on the thighs, shoulders slightly forward"],
        framing=["three-quarter portrait", "full-body portrait", "full-body portrait"],
        camera=["front-facing view"] * 4 + ["three-quarter view"] * 3,
        head=["head held level"] * 4 + ["head tilted slightly", "looking upward"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 6 + [LOW_ANGLE] * 2 + [HIGH_ANGLE],
        composition=["centered composition"] * 3 + ["clean precisely organized composition"] * 2 + ["rule-of-thirds composition", "subject placed high in frame"],
    ),
    "Balanced Low Squat": _composition_profile(
        pose=["balanced in a low squat, elbows resting loosely on the thighs, torso upright"],
        framing=["three-quarter portrait", "full-body portrait", "full-body portrait"],
        camera=["front-facing view"] * 3 + ["three-quarter view"] * 4,
        head=["head held level"] * 3 + ["looking upward"] * 2 + ["head tilted slightly"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 5 + [HIGH_ANGLE] * 2 + [LOW_ANGLE],
        composition=["centered composition"] * 2 + ["rule-of-thirds composition"] * 3 + ["editorial magazine composition", "dynamic diagonal composition"],
    ),
    "Compact Squat": _composition_profile(
        pose=["compact low squat, arms wrapped around the knees, shoulders slightly rounded"],
        framing=["three-quarter portrait", "full-body portrait"],
        camera=["front-facing view"] * 3 + ["three-quarter view"] * 3 + ["profile view"] * 2,
        head=["head tilted slightly"] * 2 + ["looking downward"] * 2 + ["head held level"] * 2,
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 4 + [HIGH_ANGLE] * 3 + [LOW_ANGLE],
        composition=["centered composition"] * 2 + ["negative-space composition"] * 2 + ["rule-of-thirds composition"] * 2 + ["candid off-center framing"],
    ),
    "Grounded Crouch": _composition_profile(
        pose=["low crouching pose, one hand planted on the floor, the other resting on the thigh"],
        framing=["full-body portrait"],
        camera=["three-quarter view"] * 4 + ["profile view"] * 3,
        head=["head held level"] * 2 + ["looking upward"] * 2 + ["glancing slightly to one side"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 4 + [LOW_ANGLE] * 3 + [HIGH_ANGLE],
        composition=["dynamic diagonal composition"] * 4 + ["rule-of-thirds composition"] * 2 + ["candid off-center framing"],
    ),
    "Side Squat": _composition_profile(
        pose=["low side squat, torso upright"],
        framing=["three-quarter portrait", "full-body portrait", "full-body portrait"],
        camera=["profile view"] * 5 + ["three-quarter view"] * 3,
        head=["head held level"] * 2 + ["glancing slightly to one side"] * 2 + ["head tilted slightly"],
        focus=[DIRECT_EYE_FOCUS] * 4 + [PAST_CAMERA_FOCUS] * 2 + [DISTANCE_FOCUS] * 2 + [LEFT_FOCUS, RIGHT_FOCUS],
        angle=[EYE_LEVEL_ANGLE] * 5 + [HIGH_ANGLE] * 2 + [LOW_ANGLE],
        composition=["rule-of-thirds composition"] * 3 + ["negative-space composition"] * 3 + ["dynamic diagonal composition"],
    ),
    "Elegant Heel-Sit": _composition_profile(
        pose=["kneeling with hips resting on the heels, hands placed on the thighs, upright elegant posture"],
        framing=["three-quarter portrait", "full-body portrait", "full-body portrait"],
        camera=["front-facing view"] * 4 + ["three-quarter view"] * 3,
        head=["head held level"] * 4 + ["head tilted slightly"] * 2,
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 5 + [HIGH_ANGLE] * 2 + [LOW_ANGLE],
        composition=["centered composition"] * 3 + ["symmetrical composition"] * 2 + ["editorial magazine composition", "rule-of-thirds composition"],
    ),
    "One-Knee Kneel": _composition_profile(
        pose=["kneeling on one knee with the other knee raised, forearm resting across the raised thigh"],
        framing=["full-body portrait", "full-body portrait", "three-quarter portrait"],
        camera=["front-facing view"] * 2 + ["three-quarter view"] * 4 + ["profile view"],
        head=["head held level"] * 3 + ["looking upward"] * 2 + ["head tilted slightly"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 5 + [LOW_ANGLE] * 2 + [HIGH_ANGLE],
        composition=["rule-of-thirds composition"] * 3 + ["dynamic diagonal composition"] * 2 + ["editorial magazine composition", "centered composition"],
    ),
    "Upright Open-Elbow Kneel": _composition_profile(
        pose=["kneeling upright with both hands behind the head, elbows open, hips shifted slightly to one side"],
        framing=["three-quarter portrait", "full-body portrait", "full-body portrait"],
        camera=["front-facing view"] * 4 + ["three-quarter view"] * 3,
        head=["head held level"] * 3 + ["head tilted slightly"] * 2 + ["looking upward"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 5 + [LOW_ANGLE] * 2 + [HIGH_ANGLE],
        composition=["centered composition"] * 2 + ["editorial magazine composition"] * 3 + ["symmetrical composition", "dynamic diagonal composition"],
    ),
    "Forward-Leaning Kneel": _composition_profile(
        pose=["kneeling and leaning forward, palms resting on the floor in front"],
        framing=["three-quarter portrait", "full-body portrait"],
        camera=["three-quarter view"] * 4 + ["profile view"] * 3,
        head=["looking downward"] * 3 + ["head held level"] * 2 + ["head tilted slightly"],
        focus=[DIRECT_EYE_FOCUS] * 5 + [PAST_CAMERA_FOCUS] * 2 + [NEARBY_OBJECT_FOCUS] * 2 + [DISTANCE_FOCUS],
        angle=[EYE_LEVEL_ANGLE] * 4 + [HIGH_ANGLE] * 3 + [LOW_ANGLE],
        composition=["rule-of-thirds composition"] * 3 + ["dynamic diagonal composition"] * 2 + ["negative-space composition", "candid off-center framing"],
    ),
    "All-Fours Neutral": _composition_profile(
        pose=["on hands and knees with the back mostly straight"],
        framing=["full-body portrait", "full-body portrait", "three-quarter portrait"],
        camera=["profile view"] * 4 + ["three-quarter view"] * 4,
        head=["head held level"] * 3 + ["looking upward"] * 2 + ["head tilted slightly"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 5 + [HIGH_ANGLE] * 3,
        composition=["rule-of-thirds composition"] * 3 + ["dynamic diagonal composition"] * 2 + ["candid off-center framing", "negative-space composition"],
    ),
    "All-Fours Twist": _composition_profile(
        pose=[
            "on hands and knees with the weight shifted onto one arm",
            "on hands and knees with one knee drawn forward between the hands and the torso gently twisted",
        ],
        framing=["three-quarter portrait", "full-body portrait", "full-body portrait"],
        camera=["rear three-quarter view"] * 4 + ["three-quarter view"] * 3 + ["profile view"],
        head=["looking back over one shoulder"] * 4 + ["glancing slightly to one side"] * 2 + ["head held level"],
        focus=REAR_CAMERA_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 5 + [HIGH_ANGLE] * 3,
        composition=["dynamic diagonal composition"] * 3 + ["candid off-center framing"] * 2 + ["rule-of-thirds composition"] * 2,
    ),
    "Arched Floor Pose": _composition_profile(
        pose=[
            "on hands and knees with a gentle arch through the lower back and the shoulders lowered",
            "kneeling with forearms resting on the floor, hips raised, and the back gently curved",
        ],
        framing=["full-body portrait", "full-body portrait", "three-quarter portrait"],
        camera=["profile view"] * 4 + ["rear three-quarter view"] * 3 + ["three-quarter view"],
        head=["head held level"] * 2 + ["looking upward"] * 2 + ["looking back over one shoulder"] * 2,
        focus=[DIRECT_EYE_FOCUS] * 6 + [PAST_CAMERA_FOCUS] * 2 + [DISTANCE_FOCUS],
        angle=[EYE_LEVEL_ANGLE] * 5 + [HIGH_ANGLE] * 2 + [LOW_ANGLE],
        composition=["dynamic diagonal composition"] * 3 + ["rule-of-thirds composition"] * 3 + ["candid off-center framing"],
    ),
    "Playful Prone": _composition_profile(
        pose=["lying on the stomach, upper body lifted on the elbows, both lower legs raised behind"],
        framing=["three-quarter portrait", "full-body portrait", "full-body portrait"],
        camera=["three-quarter view"] * 4 + ["profile view"] * 3,
        head=["head held level"] * 2 + ["looking upward"] * 2 + ["head tilted slightly"] * 2,
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[HIGH_ANGLE] * 4 + [EYE_LEVEL_ANGLE] * 3 + [OVERHEAD_ANGLE],
        composition=["dynamic diagonal composition"] * 3 + ["rule-of-thirds composition"] * 3 + ["candid off-center framing"],
    ),
    "Side S-Curve Reclining": _composition_profile(
        pose=["reclining on one side in a gentle S-curve, upper body supported by one forearm, upper knee drawn forward"],
        framing=["three-quarter portrait", "full-body portrait", "full-body portrait"],
        camera=["profile view"] * 4 + ["three-quarter view"] * 4,
        head=["head held level"] * 2 + ["head tilted slightly"] * 3 + ["glancing slightly to one side"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[HIGH_ANGLE] * 4 + [EYE_LEVEL_ANGLE] * 3 + [OVERHEAD_ANGLE],
        composition=["dynamic diagonal composition"] * 3 + ["rule-of-thirds composition"] * 2 + ["negative-space composition"] * 2,
    ),
    "Open Supine": _composition_profile(
        pose=["lying on the back with the legs comfortably spread apart and the arms resting naturally"],
        framing=["full-body portrait"],
        camera=["front-facing view"] * 3 + ["three-quarter view"] * 2,
        head=["head held level"] * 3 + ["head tilted slightly"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[OVERHEAD_ANGLE] * 5 + [HIGH_ANGLE] * 3,
        composition=["centered composition"] * 3 + ["symmetrical composition"] * 2 + ["dynamic diagonal composition"] * 2,
    ),
    "Head-Supported Side Recline": _composition_profile(
        pose=["lying on the side with the head supported by one hand and the legs relaxed"],
        framing=["three-quarter portrait", "full-body portrait", "full-body portrait"],
        camera=["profile view"] * 4 + ["three-quarter view"] * 4,
        head=["head tilted slightly"] * 4 + ["head held level"] * 2,
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[HIGH_ANGLE] * 4 + [EYE_LEVEL_ANGLE] * 3 + [OVERHEAD_ANGLE],
        composition=["rule-of-thirds composition"] * 3 + ["negative-space composition"] * 2 + ["editorial magazine composition"] * 2,
    ),
    "Asymmetric Supine": _composition_profile(
        pose=["lying on the back with one knee bent and the other leg extended"],
        framing=["full-body portrait"],
        camera=["front-facing view"] * 3 + ["three-quarter view"] * 3,
        head=["head held level"] * 3 + ["head tilted slightly", "glancing slightly to one side"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[HIGH_ANGLE] * 4 + [OVERHEAD_ANGLE] * 4,
        composition=["dynamic diagonal composition"] * 3 + ["editorial magazine composition"] * 2 + ["centered composition", "rule-of-thirds composition"],
    ),
    "Prone Forearm Portrait": _composition_profile(
        pose=["lying on the stomach with the upper body gently raised on the forearms"],
        framing=["half-body portrait", "three-quarter portrait", "full-body portrait"],
        camera=["front-facing view"] * 2 + ["three-quarter view"] * 4 + ["profile view"] * 2,
        head=["head held level"] * 3 + ["looking upward"] * 2 + ["head tilted slightly"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 4 + [HIGH_ANGLE] * 4,
        composition=["rule-of-thirds composition"] * 3 + ["editorial magazine composition"] * 2 + ["negative-space composition", "candid off-center framing"],
    ),
    "Curled Side Recline": _composition_profile(
        pose=["lying curled slightly on one side with the knees loosely drawn upward"],
        framing=["three-quarter portrait", "full-body portrait"],
        camera=["profile view"] * 5 + ["three-quarter view"] * 3,
        head=["looking downward"] * 3 + ["head tilted slightly"] * 2 + ["head held level"],
        focus=[DIRECT_EYE_FOCUS] * 5 + [PAST_CAMERA_FOCUS] * 2 + [DISTANCE_FOCUS] * 2,
        angle=[HIGH_ANGLE] * 4 + [OVERHEAD_ANGLE] * 2 + [EYE_LEVEL_ANGLE] * 2,
        composition=["negative-space composition"] * 3 + ["candid off-center framing"] * 2 + ["rule-of-thirds composition"] * 2,
    ),
    "Bent-Knee Supine": _composition_profile(
        pose=["reclining on the back with both knees bent and the feet resting on the supporting surface"],
        framing=["full-body portrait"],
        camera=["front-facing view"] * 3 + ["three-quarter view"] * 2,
        head=["head held level"] * 3 + ["head tilted slightly"],
        focus=CAMERA_DOMINANT_FOCUS,
        angle=[OVERHEAD_ANGLE] * 5 + [HIGH_ANGLE] * 3,
        composition=["centered composition"] * 3 + ["symmetrical composition"] * 2 + ["dynamic diagonal composition"] * 2,
    ),
    "Dynamic Movement": _composition_profile(
        pose=["caught mid-spin while dancing, torso and arms turning dynamically", "dancing casually among a small surrounding crowd"],
        framing=["three-quarter portrait", "full-body portrait", "full-body portrait"],
        camera=["three-quarter view"] * 4 + ["profile view"] * 3 + ["rear three-quarter view"],
        head=["head held level"] * 2 + ["glancing slightly to one side"] * 3 + ["head tilted slightly"],
        focus=[DIRECT_EYE_FOCUS] * 4 + [PAST_CAMERA_FOCUS] * 2 + [DISTANCE_FOCUS] * 3 + [NEARBY_PERSON_FOCUS],
        angle=[EYE_LEVEL_ANGLE] * 5 + [LOW_ANGLE] * 2 + [HIGH_ANGLE],
        composition=["dynamic diagonal composition"] * 5 + ["candid off-center framing"] * 2 + ["rule-of-thirds composition"],
    ),
    "Handheld Selfie": _composition_profile(
        pose=["taking a selfie with one arm extended, holding a smartphone at arm's length with its front camera aimed toward the subject, looking into the phone's camera"],
        framing=["bust portrait", "half-body portrait", "three-quarter portrait"],
        camera=["front-facing view"] * 5 + ["three-quarter view"],
        head=["head held level"] * 3 + ["head tilted slightly"] * 2,
        focus=[DIRECT_EYE_FOCUS],
        angle=[EYE_LEVEL_ANGLE] * 4 + [HIGH_ANGLE] * 2,
        composition=["centered composition"] * 2 + ["candid off-center framing"] * 3 + ["rule-of-thirds composition"],
    ),
    "Focused Handheld Object": _composition_profile(
        pose=[
            "holding a game controller with both hands, absorbed in an ongoing game",
            "reading a folded newspaper held naturally in both hands, absorbed in the article",
            "holding an unfolded paper map and tracing a route with one finger",
            "examining a small instant photograph held delicately between the fingers",
        ],
        framing=["half-body portrait", "three-quarter portrait", "three-quarter portrait"],
        camera=["front-facing view"] * 3 + ["three-quarter view"] * 4 + ["profile view"],
        head=["looking downward"] * 5 + ["head held level", "head tilted slightly"],
        focus=[HELD_OBJECT_FOCUS] * 8 + [DIRECT_EYE_FOCUS, PAST_CAMERA_FOCUS],
        angle=[EYE_LEVEL_ANGLE] * 5 + [HIGH_ANGLE] * 3,
        composition=["rule-of-thirds composition"] * 3 + ["clean precisely organized composition"] * 2 + ["candid off-center framing", "editorial magazine composition"],
    ),
    "Writing in Hand": _composition_profile(
        pose=["writing a quick note in a small pocket notebook, pausing briefly in thought"],
        framing=["half-body portrait", "three-quarter portrait"],
        camera=["three-quarter view"] * 5 + ["profile view"] * 2 + ["front-facing view"],
        head=["looking downward"] * 5 + ["head tilted slightly", "head held level"],
        focus=[HELD_OBJECT_FOCUS] * 8 + [DIRECT_EYE_FOCUS, PAST_CAMERA_FOCUS],
        angle=[EYE_LEVEL_ANGLE] * 4 + [HIGH_ANGLE] * 4,
        composition=["rule-of-thirds composition"] * 3 + ["negative-space composition"] * 2 + ["clean precisely organized composition", "candid off-center framing"],
    ),
    "Casual Sip": _composition_profile(
        pose=["taking a casual sip from a takeaway cup, holding it loosely near the face"],
        framing=["bust portrait", "half-body portrait", "three-quarter portrait"],
        camera=["front-facing view"] * 3 + ["three-quarter view"] * 4,
        head=["head held level"] * 3 + ["head tilted slightly"] * 2 + ["glancing slightly to one side"],
        focus=CAMERA_OR_SOCIAL_FOCUS,
        angle=[EYE_LEVEL_ANGLE] * 7 + [HIGH_ANGLE, LOW_ANGLE],
        composition=["candid off-center framing"] * 3 + ["rule-of-thirds composition"] * 3 + ["centered composition"],
    ),
    "Social Candid": _composition_profile(
        pose=["laughing during a lively group conversation", "posing naturally while friends gather loosely nearby"],
        framing=["half-body portrait", "three-quarter portrait", "full-body portrait"],
        camera=["three-quarter view"] * 4 + ["profile view"] * 2 + ["front-facing view"] * 2,
        head=["glancing slightly to one side"] * 3 + ["head held level"] * 2 + ["head tilted slightly"],
        focus=[NEARBY_PERSON_FOCUS] * 5 + [DIRECT_EYE_FOCUS] * 3 + [PAST_CAMERA_FOCUS] * 2,
        angle=[EYE_LEVEL_ANGLE] * 8 + [HIGH_ANGLE, LOW_ANGLE],
        composition=["candid off-center framing"] * 4 + ["rule-of-thirds composition"] * 3 + ["negative-space composition"],
    ),
    "Attentive Observer": _composition_profile(
        pose=[
            "listening intently to a speech, visibly moved, among a small crowd of fellow listeners",
            "watching a nearby performance with absorbed fascination",
            "reading a posted notice alongside several curious onlookers",
        ],
        framing=["half-body portrait", "three-quarter portrait", "full-body portrait"],
        camera=["three-quarter view"] * 4 + ["profile view"] * 3 + ["front-facing view"],
        head=["glancing slightly to one side"] * 3 + ["looking upward"] * 2 + ["head held level"],
        focus=[NEARBY_PERSON_FOCUS] * 3 + [NEARBY_OBJECT_FOCUS] * 3 + [DISTANCE_FOCUS] * 2 + [DIRECT_EYE_FOCUS] * 2,
        angle=[EYE_LEVEL_ANGLE] * 8 + [HIGH_ANGLE, LOW_ANGLE],
        composition=["negative-space composition"] * 3 + ["rule-of-thirds composition"] * 3 + ["candid off-center framing"] * 2,
    ),
    "Crowd Reaction": _composition_profile(
        pose=[
            "applauding enthusiastically among a gathered audience",
            "joining a spontaneous group cheer with one arm raised",
            "reacting with surprise as the surrounding crowd turns toward the same event",
        ],
        framing=["three-quarter portrait", "full-body portrait", "full-body portrait"],
        camera=["front-facing view"] * 3 + ["three-quarter view"] * 4 + ["profile view"],
        head=["head held level"] * 2 + ["looking upward"] * 2 + ["glancing slightly to one side"] * 2,
        focus=[DIRECT_EYE_FOCUS] * 4 + [NEARBY_PERSON_FOCUS] * 3 + [DISTANCE_FOCUS] * 2 + [PAST_CAMERA_FOCUS],
        angle=[EYE_LEVEL_ANGLE] * 6 + [LOW_ANGLE] * 2 + [HIGH_ANGLE],
        composition=["dynamic diagonal composition"] * 4 + ["candid off-center framing"] * 2 + ["rule-of-thirds composition"] * 2,
    ),
    "Waiting Candid": _composition_profile(
        pose=["waiting patiently in a loose queue, casually observing the surroundings"],
        framing=["half-body portrait", "three-quarter portrait", "full-body portrait"],
        camera=["three-quarter view"] * 4 + ["profile view"] * 3 + ["front-facing view"],
        head=["glancing slightly to one side"] * 3 + ["head held level"] * 2 + ["head tilted slightly"],
        focus=[DIRECT_EYE_FOCUS] * 5 + [PAST_CAMERA_FOCUS] * 2 + [DISTANCE_FOCUS] * 2 + [NEARBY_PERSON_FOCUS],
        angle=[EYE_LEVEL_ANGLE] * 8 + [HIGH_ANGLE, LOW_ANGLE],
        composition=["candid off-center framing"] * 4 + ["negative-space composition"] * 2 + ["rule-of-thirds composition"] * 2,
    ),
    "Social Exchange": _composition_profile(
        pose=[
            "reaching forward with one arm to grasp another person's offered hand just outside the frame",
            "sharing a celebratory toast within a small gathering",
        ],
        framing=["three-quarter portrait", "three-quarter portrait", "full-body portrait"],
        camera=["three-quarter view"] * 5 + ["profile view"] * 2 + ["front-facing view"],
        head=["glancing slightly to one side"] * 4 + ["head held level"] * 2,
        focus=[NEARBY_PERSON_FOCUS] * 6 + [DIRECT_EYE_FOCUS] * 3 + [PAST_CAMERA_FOCUS],
        angle=[EYE_LEVEL_ANGLE] * 8 + [HIGH_ANGLE, LOW_ANGLE],
        composition=["rule-of-thirds composition"] * 3 + ["candid off-center framing"] * 3 + ["dynamic diagonal composition"],
    ),
}

MOUTH_EXPRESSION_VALUES = [
    "relaxed closed lips",
    "slightly parted lips",
    "open mouth",
    "lips puckered for a kiss",
    "lips pursed while blowing a kiss",
    "tongue extended straight forward",
    "tongue peeking from one corner of the mouth",
    "lower lip gently caught between the teeth",
    "upper lip curled in a snarl",
    "teeth bared in a snarl",
]

MOUTH_EXPRESSION_POOLS = {
    "neutral expression": ["relaxed closed lips", "slightly parted lips"],
    "calm expression": ["relaxed closed lips", "slightly parted lips"],
    "soft smile": ["relaxed closed lips", "slightly parted lips"],
    "warm smile": ["relaxed closed lips", "slightly parted lips"],
    "subtle smile": ["relaxed closed lips", "slightly parted lips"],
    "broad smile": ["slightly parted lips", "open mouth"],
    "serious expression": ["relaxed closed lips", "slightly parted lips"],
    "confident expression": ["relaxed closed lips", "slightly parted lips", "lower lip gently caught between the teeth"],
    "mysterious expression": ["relaxed closed lips", "slightly parted lips"],
    "playful expression": ["lips puckered for a kiss", "lips pursed while blowing a kiss", "tongue peeking from one corner of the mouth", "lower lip gently caught between the teeth"],
    "dreamy expression": ["relaxed closed lips", "slightly parted lips"],
    "melancholic expression": ["relaxed closed lips", "slightly parted lips"],
    "surprised expression": ["open mouth"],
    "concerned expression": ["slightly parted lips", "relaxed closed lips"],
    "determined expression": ["relaxed closed lips", "upper lip curled in a snarl"],
    "sensual expression": ["slightly parted lips", "lips puckered for a kiss", "lower lip gently caught between the teeth"],
    "shy expression": ["relaxed closed lips", "slightly parted lips"],
    "joyful expression": ["slightly parted lips", "open mouth"],
    "pensive expression": ["relaxed closed lips", "slightly parted lips"],
    "defiant expression": ["relaxed closed lips", "upper lip curled in a snarl", "teeth bared in a snarl", "tongue extended straight forward"],
}

# A compact, human-readable palette syntax gives every existing color slot an
# arbitrary text escape hatch without adding a second widget beside every
# dropdown.  Example: "top=fuchsia; hosiery=salmon pink; hair=teal".
CUSTOM_COLOR_TARGETS = {
    "eyes": "eye_color", "eye": "eye_color", "eye_color": "eye_color",
    "hair": "hair_color", "hair_color": "hair_color",
    "top": "top_color", "top_color": "top_color",
    "bottom": "bottom_color", "bottom_color": "bottom_color",
    "lingerie": "lingerie_color", "swimwear": "lingerie_color", "lingerie_color": "lingerie_color",
    "sleepwear": "sleepwear_color", "sleepwear_color": "sleepwear_color",
    "cosplay": "cosplay_color", "cosplay_color": "cosplay_color",
    "hosiery": "hosiery_color", "tights": "hosiery_color", "stockings": "hosiery_color", "hosiery_color": "hosiery_color",
    "dress": "dress_color", "dress_color": "dress_color",
    "outerwear": "outerwear_color", "jacket": "outerwear_color", "coat": "outerwear_color", "outerwear_color": "outerwear_color",
    "belt": "belt_color", "belt_color": "belt_color",
    "footwear": "footwear_color", "shoes": "footwear_color", "boots": "footwear_color", "footwear_color": "footwear_color",
}

# A reference-face caption is intentionally parsed into the node's existing
# fields instead of being appended as an opaque prose block. This preserves the
# established sentence order, Face Prompt, Pre-gen hair-only boundary, and
# per-field inspection. Manual / Forced Random choices stay above this layer;
# Identity Forge, broad external subject additions, and ordinary Random stay
# below it. The universal one-field override is applied later and remains the
# final authority.
FACE_HAIR_OVERRIDE_FIELDS = (
    "face_shape", "jawline", "chin_shape", "eye_shape", "eye_color",
    "eyelashes", "eyebrows", "nose_shape", "lip_shape", "facial_hair",
    "hair_color", "hair_texture", "hair_style", "hair_cut", "hair_length",
    "bangs_style",
)
FACE_HAIR_OVERRIDE_ALIASES = {
    "face": "face_shape",
    "face_shape": "face_shape",
    "jaw": "jawline",
    "jaw_line": "jawline",
    "jawline": "jawline",
    "chin": "chin_shape",
    "chin_shape": "chin_shape",
    "eyes": "eye_shape",
    "eye_shape": "eye_shape",
    "eye_colour": "eye_color",
    "eye_color": "eye_color",
    "eye_lashes": "eyelashes",
    "eyelashes": "eyelashes",
    "eye_brows": "eyebrows",
    "eyebrows": "eyebrows",
    "nose": "nose_shape",
    "nose_shape": "nose_shape",
    "lips": "lip_shape",
    "lip_shape": "lip_shape",
    "facial_hair": "facial_hair",
    "hair_colour": "hair_color",
    "hair_color": "hair_color",
    "hair_texture": "hair_texture",
    "hair_style": "hair_style",
    "hairstyle": "hair_style",
    "hair_cut": "hair_cut",
    "haircut": "hair_cut",
    "hair_length": "hair_length",
    "bangs": "bangs_style",
    "bangs_style": "bangs_style",
    "fringe": "bangs_style",
}
FACE_HAIR_ABSENT_VALUES = {
    "", "none", "null", "n/a", "na", "not applicable", "not visible",
    "unknown", "absent", "no facial hair",
}

SUBJECT_WILDCARD_CLEAR_FIELDS = set().union(
    IDENTITY_GROUP_CA_FIELDS["Demographics"],
    IDENTITY_GROUP_CA_FIELDS["Body"],
    IDENTITY_GROUP_CA_FIELDS["Face"],
    IDENTITY_GROUP_CA_FIELDS["Hair"],
    IDENTITY_GROUP_CA_FIELDS["Makeup"],
    {"gender", "tattoo_style", "nail_style"},
)

PHOTOGRAPHY_WILDCARD_CLEAR_FIELDS = {
    "media_type", "composition_archetype", "portrait_style", "capture_style", "camera_direction",
    "head_direction", "camera_angle", "shot_composition", "lens_style",
    "lighting_style", "optical_effect",
}

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
    "Japanese-inspired super-high-waisted wide-leg trousers with a broad extended waistband and deep pleats": ["mid-length", "long", "long"],
    "drop-crotch sarouel harem pants": ["mid-length", "long", "long"],
    "high-waisted performance leggings with wide sheer lace side panels": ["long"],
    "cutout athletic leggings with large sheer mesh panels": ["long"],
    "loose flowing wide-leg halter jumpsuit": ["long"],
    "sleek figure-hugging flared jumpsuit": ["long"],
    "pencil skirt": ["knee-length", "mid-length"],
    "A-line skirt": ["short", "knee-length", "mid-length"],
    "bias-cut satin midi skirt": ["mid-length"],
    "denim skirt": ["very short", "short", "knee-length"],
    "cigarette trousers": ["mid-length", "long"],
    "straight-leg trousers": ["mid-length", "long", "long"],
    "culottes": ["knee-length", "mid-length"],
    "tailored shorts": ["short", "knee-length"],
    "capri pants": ["mid-length"],
    "tennis skirt": ["very short", "short"],
    "tapered technical cargo pants": ["mid-length", "long", "long"],
    "asymmetrical layered skirt": ["short", "knee-length", "mid-length", "long"],
    "patent leather pants": ["mid-length", "long"],
}

# Hosiery needs different wording under trousers than it does with skirts,
# dresses, or short bottoms. This remains an internal semantic family: it does
# not add a widget and therefore cannot move or invalidate serialized values.
TROUSER_BOTTOM_TYPES = {
    "jeans", "skinny jeans", "trousers", "wide-leg pants", "flared pants",
    "cargo pants", "leggings", "joggers", "leather pants", "cigarette trousers",
    "straight-leg trousers", "culottes", "capri pants", "tapered technical cargo pants",
    "patent leather pants",
    "Japanese-inspired super-high-waisted wide-leg trousers with a broad extended waistband and deep pleats",
    "drop-crotch sarouel harem pants",
    "high-waisted performance leggings with wide sheer lace side panels",
    "cutout athletic leggings with large sheer mesh panels",
}

FULL_BODY_ONE_PIECE_BOTTOM_TYPES = {
    "loose flowing wide-leg halter jumpsuit",
    "sleek figure-hugging flared jumpsuit",
}

# Complete outfits whose lower half behaves like full-length trousers.  They
# need the same hosiery layering grammar as trousers even though the public
# schema stores them under Dress / complete outfit rather than Bottom.
FULL_LEG_COMPLETE_OUTFIT_TYPES = {
    "denim overalls",
    "utility boiler suit",
    "tailored trouser suit",
    "salwar kameez ensemble",
    "kurta and trouser ensemble",
    "Anarkali suit",
    "ao dai ensemble",
}

# This garment contains its defining color in its name. Ignoring Dress color for
# it avoids contradictory phrases such as "pink classic little black dress".
FIXED_COLOR_GARMENTS = {"classic little black dress"}

BODY_HEIGHT_CLASSIC_RANDOM_POOL = [
    "very short", "short", "average height", "tall", "very tall",
]

BODY_ARCHETYPE_VALUES = [
    "Petite Thin Arched",
    "Petite Straight Slim",
    "Petite Soft Curvy",
    "Petite Full Hourglass",
    "Delicate Slender",
    "Tall Slender",
    "Long-Legged Slim",
    "Soft Natural",
    "Soft Feminine",
    "Girl Next Door",
    "Slim Wide-Hip",
    "Soft Pear",
    "Soft Hourglass",
    "Compact Full Hourglass",
    "Top-Heavy Curvy",
    "Plush Curvy",
    "Full Soft Hourglass",
    "Full Pear",
    "Plus-Size Soft",
    "Obese Soft",
    "Obese Pear",
    "Obese Hourglass",
    "Straight Androgynous",
    "Stocky Broad",
    "Lean Athletic",
    "Powerfully Muscular",
]

BODY_DETAIL_VALUES = [
    "compact torso",
    "long torso",
    "fine-boned narrow frame",
    "very narrow defined waist",
    "straight narrow waist with minimal waist-to-hip contrast",
    "soft broad waist",
    "very wide rounded hips",
    "narrow hips",
    "very thin delicate upper arms",
    "soft full upper arms",
    "slender upper arms",
    "flat lower abdomen",
    "soft rounded abdomen",
    "prominent abdomen",
    "gentle inward lumbar curve",
    "pronounced inward lumbar curve",
    "short-legged proportions",
    "long-legged proportions",
    "very full bust with pronounced forward projection",
    "slender neck and delicate shoulder line",
]

BODY_DETAIL_AXES = {
    "compact torso": "torso",
    "long torso": "torso",
    "fine-boned narrow frame": "frame",
    "very narrow defined waist": "waist",
    "straight narrow waist with minimal waist-to-hip contrast": "waist",
    "soft broad waist": "waist",
    "very wide rounded hips": "hips",
    "narrow hips": "hips",
    "very thin delicate upper arms": "upper_arms",
    "soft full upper arms": "upper_arms",
    "slender upper arms": "upper_arms",
    "flat lower abdomen": "abdomen",
    "soft rounded abdomen": "abdomen",
    "prominent abdomen": "abdomen",
    "gentle inward lumbar curve": "lumbar_curve",
    "pronounced inward lumbar curve": "lumbar_curve",
    "short-legged proportions": "leg_proportion",
    "long-legged proportions": "leg_proportion",
    "very full bust with pronounced forward projection": "bust_projection",
    "slender neck and delicate shoulder line": "neck_shoulders",
}

BODY_DETAIL_KEYS = ("body_detail_1", "body_detail_2", "body_detail_3")
BODY_ARCHETYPE_CONTROL_FIELDS = {
    "body_type", "body_physique", "body_feminine_curves", "bust",
    "butt_shape", "thigh_shape", *BODY_DETAIL_KEYS,
}

# Body archetypes contain only pools of phrases exposed by the regular widgets.
# They are recipes, never hidden prompt vocabulary. Repeated values are deliberate
# weights, while Body Detail axes prevent ordinary/archetype Random contradictions.
BODY_ARCHETYPE_CONFIG = {
    "Petite Thin Arched": {
        "body_type": ["very short", "short", "short"],
        "body_physique": ["naturally extremely slender, fine-boned underweight physique", "extremely underweight physique", "very slim physique"],
        "body_feminine_curves": ["almost no curves", "straight silhouette", "subtle curves"],
        "bust": ["flat chest", "very small bust", "small bust"],
        "butt_shape": ["flat glute shape", "small rounded glutes"],
        "thigh_shape": ["extremely slender straight legs with narrow thighs and calves", "very slim thighs", "narrow thighs"],
        "body_details": ["compact torso", "fine-boned narrow frame", "very thin delicate upper arms", "gentle inward lumbar curve", "pronounced inward lumbar curve"],
    },
    "Petite Straight Slim": {
        "body_type": ["very short", "short", "short"],
        "body_physique": ["naturally extremely slender, fine-boned underweight physique", "naturally extremely slender, fine-boned underweight physique", "extremely underweight physique"],
        "body_feminine_curves": ["almost no curves", "almost no curves", "straight silhouette"],
        "bust": ["flat chest", "flat chest", "very small bust"],
        "butt_shape": ["flat glute shape"],
        "thigh_shape": ["extremely slender straight legs with narrow thighs and calves", "extremely slender straight legs with narrow thighs and calves", "very slim thighs"],
        "body_details": ["fine-boned narrow frame", "very thin delicate upper arms", "straight narrow waist with minimal waist-to-hip contrast"],
    },
    "Petite Soft Curvy": {
        "body_type": ["very short", "short", "short"],
        "body_physique": ["soft untrained physique", "average physique", "plump physique"],
        "body_feminine_curves": ["balanced curves", "soft curves", "soft hourglass silhouette"],
        "bust": ["medium bust", "full bust", "large bust"],
        "butt_shape": ["soft rounded glutes", "full rounded glutes", "heart-shaped glutes"],
        "thigh_shape": ["soft thighs", "curvy thighs", "full thighs", "soft thick thighs"],
        "body_details": ["compact torso", "very narrow defined waist", "very wide rounded hips", "soft full upper arms", "soft rounded abdomen"],
    },
    "Petite Full Hourglass": {
        "body_type": ["very short", "short", "short"],
        "body_physique": ["soft untrained physique", "plump physique", "plus-size physique"],
        "body_feminine_curves": ["very pronounced curves", "pronounced hourglass silhouette"],
        "bust": ["large bust", "very large bust", "very full projected bust"],
        "butt_shape": ["full rounded glutes", "prominent glute shape", "heart-shaped glutes"],
        "thigh_shape": ["full thighs", "thick thighs", "soft thick thighs", "very thick soft thighs"],
        "body_details": ["compact torso", "very narrow defined waist", "very wide rounded hips", "soft full upper arms", "short-legged proportions"],
    },
    "Delicate Slender": {
        "body_type": ["short", "average height"],
        "body_physique": ["very slim physique", "slim physique"],
        "body_feminine_curves": ["almost no curves", "straight silhouette", "subtle curves"],
        "bust": ["flat chest", "very small bust", "small bust"],
        "butt_shape": ["flat glute shape", "small rounded glutes"],
        "thigh_shape": ["very slim thighs", "slim thighs", "narrow thighs"],
        "body_details": ["fine-boned narrow frame", "very thin delicate upper arms", "flat lower abdomen", "narrow hips", "long torso"],
    },
    "Tall Slender": {
        "body_type": ["tall", "tall", "very tall"],
        "body_physique": ["very slim physique", "slim physique"],
        "body_feminine_curves": ["straight silhouette", "subtle curves"],
        "bust": ["very small bust", "small bust", "medium bust"],
        "butt_shape": ["flat glute shape", "small rounded glutes", "lifted glute shape"],
        "thigh_shape": ["very slim thighs", "slim thighs", "long toned thighs"],
        "body_details": ["long torso", "long-legged proportions", "slender upper arms", "flat lower abdomen", "narrow hips"],
    },
    "Long-Legged Slim": {
        "body_type": ["average height", "tall", "tall"],
        "body_physique": ["slim physique", "lightly toned physique", "toned physique"],
        "body_feminine_curves": ["straight silhouette", "subtle curves", "balanced curves"],
        "bust": ["small bust", "medium bust"],
        "butt_shape": ["small rounded glutes", "lifted glute shape"],
        "thigh_shape": ["slim thighs", "long toned thighs"],
        "body_details": ["long-legged proportions", "flat lower abdomen", "slender upper arms", "very narrow defined waist", "narrow hips"],
    },
    "Soft Natural": {
        "body_type": ["short", "average height", "average height", "tall"],
        "body_physique": ["soft untrained physique", "average physique"],
        "body_feminine_curves": ["balanced curves", "soft curves"],
        "bust": ["medium bust", "full bust"],
        "butt_shape": ["soft rounded glutes", "full rounded glutes"],
        "thigh_shape": ["soft thighs", "curvy thighs", "full thighs"],
        "body_details": ["soft rounded abdomen", "soft full upper arms", "gentle inward lumbar curve", "compact torso", "long torso"],
    },
    "Soft Feminine": {
        "body_type": ["short", "average height", "average height"],
        "body_physique": ["soft untrained physique", "average physique"],
        "body_feminine_curves": ["soft curves", "balanced curves", "soft hourglass silhouette"],
        "bust": ["medium bust", "full bust", "large bust"],
        "butt_shape": ["soft rounded glutes", "heart-shaped glutes", "full rounded glutes"],
        "thigh_shape": ["soft thighs", "curvy thighs", "full thighs"],
        "body_details": ["very narrow defined waist", "soft full upper arms", "soft rounded abdomen", "gentle inward lumbar curve", "very wide rounded hips"],
    },
    "Girl Next Door": {
        "body_type": ["average height", "average height", "average height", "short", "tall"],
        "body_physique": ["slim physique", "slim physique", "slim physique", "soft untrained physique"],
        "body_feminine_curves": ["soft hourglass silhouette", "soft hourglass silhouette", "balanced curves"],
        "bust": ["full rounded bust with natural forward projection", "full rounded bust with natural forward projection", "full bust"],
        "butt_shape": ["prominent rounded glutes", "prominent rounded glutes", "full rounded glutes", "heart-shaped glutes"],
        "thigh_shape": ["slim thighs", "slim thighs", "narrow thighs"],
        "body_details": ["very narrow defined waist", "slender upper arms", "slender neck and delicate shoulder line"],
    },
    "Slim Wide-Hip": {
        "body_type": ["average height", "tall"],
        "body_physique": ["very slim physique", "slim physique"],
        "body_feminine_curves": ["wide-hip silhouette", "pear-shaped silhouette", "balanced curves"],
        "bust": ["very small bust", "small bust", "medium bust"],
        "butt_shape": ["broad glute shape", "full rounded glutes", "prominent glute shape"],
        "thigh_shape": ["curvy thighs", "full thighs", "soft thick thighs"],
        "body_details": ["very wide rounded hips", "very narrow defined waist", "long-legged proportions", "flat lower abdomen", "slender upper arms"],
    },
    "Soft Pear": {
        "body_type": ["short", "average height", "average height"],
        "body_physique": ["soft untrained physique", "plump physique"],
        "body_feminine_curves": ["pear-shaped silhouette", "wide-hip silhouette"],
        "bust": ["small bust", "medium bust", "full bust"],
        "butt_shape": ["broad glute shape", "full rounded glutes", "prominent glute shape"],
        "thigh_shape": ["full thighs", "soft thick thighs", "very thick soft thighs"],
        "body_details": ["very wide rounded hips", "soft rounded abdomen", "soft full upper arms", "soft broad waist", "short-legged proportions"],
    },
    "Soft Hourglass": {
        "body_type": ["short", "average height", "average height"],
        "body_physique": ["soft untrained physique", "average physique", "plump physique"],
        "body_feminine_curves": ["soft hourglass silhouette", "balanced curves", "soft curves"],
        "bust": ["full bust", "large bust", "generous bust"],
        "butt_shape": ["soft rounded glutes", "full rounded glutes", "heart-shaped glutes"],
        "thigh_shape": ["curvy thighs", "full thighs", "soft thick thighs"],
        "body_details": ["very narrow defined waist", "very wide rounded hips", "soft rounded abdomen", "gentle inward lumbar curve", "soft full upper arms"],
    },
    "Compact Full Hourglass": {
        "body_type": ["short", "average height", "average height"],
        "body_physique": ["soft untrained physique"],
        "body_feminine_curves": ["very pronounced curves", "pronounced hourglass silhouette"],
        "bust": ["very large bust", "generous bust", "very full projected bust", "very full projected bust"],
        "butt_shape": ["full rounded glutes", "prominent glute shape", "heart-shaped glutes"],
        "thigh_shape": ["full thighs", "soft thick thighs", "soft thick thighs", "very thick soft thighs"],
        "body_details": ["compact torso", "very narrow defined waist", "very wide rounded hips"],
    },
    "Top-Heavy Curvy": {
        "body_type": ["short", "average height", "average height"],
        "body_physique": ["soft untrained physique", "plump physique"],
        "body_feminine_curves": ["top-heavy silhouette", "very pronounced curves"],
        "bust": ["large bust", "very large bust", "huge breasts", "very full projected bust"],
        "butt_shape": ["small rounded glutes", "soft rounded glutes", "lifted glute shape"],
        "thigh_shape": ["soft thighs", "curvy thighs", "full thighs"],
        "body_details": ["compact torso", "narrow hips", "very narrow defined waist", "soft full upper arms", "soft rounded abdomen"],
    },
    "Plush Curvy": {
        "body_type": ["short", "average height", "average height"],
        "body_physique": ["plump physique", "plus-size physique"],
        "body_feminine_curves": ["very pronounced curves", "soft curves", "balanced curves"],
        "bust": ["large bust", "generous bust", "heavy breasts"],
        "butt_shape": ["full rounded glutes", "broad glute shape", "prominent glute shape"],
        "thigh_shape": ["full thighs", "thick thighs", "soft thick thighs"],
        "body_details": ["soft rounded abdomen", "soft full upper arms", "very wide rounded hips", "soft broad waist", "short-legged proportions"],
    },
    "Full Soft Hourglass": {
        "body_type": ["short", "average height", "average height"],
        "body_physique": ["plump physique", "plus-size physique", "overweight physique"],
        "body_feminine_curves": ["soft hourglass silhouette", "pronounced hourglass silhouette", "very pronounced curves"],
        "bust": ["generous bust", "heavy breasts", "very full projected bust"],
        "butt_shape": ["full rounded glutes", "prominent glute shape", "heart-shaped glutes"],
        "thigh_shape": ["thick thighs", "soft thick thighs", "very thick soft thighs"],
        "body_details": ["very narrow defined waist", "very wide rounded hips", "soft rounded abdomen", "soft full upper arms", "short-legged proportions"],
    },
    "Full Pear": {
        "body_type": ["short", "average height", "average height"],
        "body_physique": ["plump physique", "plus-size physique", "overweight physique"],
        "body_feminine_curves": ["pear-shaped silhouette", "wide-hip silhouette"],
        "bust": ["medium bust", "full bust", "large bust"],
        "butt_shape": ["broad glute shape", "full rounded glutes", "prominent glute shape"],
        "thigh_shape": ["thick thighs", "soft thick thighs", "very thick soft thighs"],
        "body_details": ["very wide rounded hips", "soft rounded abdomen", "soft broad waist", "soft full upper arms", "short-legged proportions"],
    },
    "Plus-Size Soft": {
        "body_type": ["short", "average height", "average height", "tall"],
        "body_physique": ["plus-size physique", "overweight physique"],
        "body_feminine_curves": ["soft curves", "balanced curves", "wide-hip silhouette"],
        "bust": ["full bust", "generous bust", "heavy breasts"],
        "butt_shape": ["broad glute shape", "full rounded glutes"],
        "thigh_shape": ["full thighs", "thick thighs", "soft thick thighs"],
        "body_details": ["soft broad waist", "soft rounded abdomen", "soft full upper arms", "very wide rounded hips", "short-legged proportions"],
    },
    "Obese Soft": {
        "body_type": ["short", "average height", "average height", "tall"],
        "body_physique": ["obese physique"],
        "body_feminine_curves": ["soft curves", "balanced curves", "straight silhouette"],
        "bust": ["heavy breasts", "huge breasts", "generous bust"],
        "butt_shape": ["broad glute shape", "full rounded glutes", "prominent glute shape"],
        "thigh_shape": ["thick thighs", "soft thick thighs", "very thick soft thighs"],
        "body_details": ["prominent abdomen", "soft broad waist", "soft full upper arms", "short-legged proportions", "very wide rounded hips"],
    },
    "Obese Pear": {
        "body_type": ["short", "average height", "average height"],
        "body_physique": ["obese physique"],
        "body_feminine_curves": ["pear-shaped silhouette", "wide-hip silhouette"],
        "bust": ["full bust", "large bust", "heavy breasts"],
        "butt_shape": ["broad glute shape", "prominent glute shape", "full rounded glutes"],
        "thigh_shape": ["soft thick thighs", "very thick soft thighs", "thick thighs"],
        "body_details": ["very wide rounded hips", "prominent abdomen", "soft full upper arms", "soft broad waist", "short-legged proportions"],
    },
    "Obese Hourglass": {
        "body_type": ["short", "average height", "average height"],
        "body_physique": ["obese physique"],
        "body_feminine_curves": ["pronounced hourglass silhouette", "very pronounced curves"],
        "bust": ["huge breasts", "heavy breasts", "very full projected bust"],
        "butt_shape": ["full rounded glutes", "prominent glute shape", "heart-shaped glutes"],
        "thigh_shape": ["soft thick thighs", "very thick soft thighs", "thick thighs"],
        "body_details": ["very narrow defined waist", "very wide rounded hips", "prominent abdomen", "soft full upper arms", "short-legged proportions"],
    },
    "Straight Androgynous": {
        "body_type": ["short", "average height", "tall"],
        "body_physique": ["slim physique", "average physique", "toned physique"],
        "body_feminine_curves": ["straight silhouette", "androgynous silhouette", "almost no curves"],
        "bust": ["flat chest", "very small bust", "small bust"],
        "butt_shape": ["flat glute shape", "square glute shape", "small rounded glutes"],
        "thigh_shape": ["narrow thighs", "slim thighs", "long toned thighs"],
        "body_details": ["narrow hips", "flat lower abdomen", "slender upper arms", "long torso", "long-legged proportions"],
    },
    "Stocky Broad": {
        "body_type": ["short", "average height", "average height"],
        "body_physique": ["soft untrained physique", "average physique", "muscular physique"],
        "body_feminine_curves": ["straight silhouette", "androgynous silhouette", "almost no curves"],
        "bust": ["flat chest", "medium bust"],
        "butt_shape": ["square glute shape", "broad glute shape", "athletic glute shape"],
        "thigh_shape": ["thick thighs", "powerful thighs", "muscular thighs"],
        "body_details": ["compact torso", "soft broad waist", "short-legged proportions", "soft full upper arms", "flat lower abdomen"],
    },
    "Lean Athletic": {
        "body_type": ["average height", "tall", "tall"],
        "body_physique": ["lightly toned physique", "toned physique", "athletic physique"],
        "body_feminine_curves": ["straight silhouette", "subtle curves", "balanced curves"],
        "bust": ["small bust", "medium bust"],
        "butt_shape": ["lifted glute shape", "athletic glute shape"],
        "thigh_shape": ["long toned thighs", "muscular thighs", "powerful thighs"],
        "body_details": ["flat lower abdomen", "long-legged proportions", "slender upper arms", "gentle inward lumbar curve", "long torso"],
    },
    "Powerfully Muscular": {
        "body_type": ["average height", "tall", "very tall"],
        "body_physique": ["muscular physique", "heavily muscular physique", "heavily muscular physique"],
        "body_feminine_curves": ["straight silhouette", "almost no curves", "balanced curves"],
        "bust": ["flat chest", "medium bust"],
        "butt_shape": ["athletic glute shape", "lifted glute shape", "square glute shape"],
        "thigh_shape": ["muscular thighs", "powerful thighs", "thick thighs"],
        "body_details": ["flat lower abdomen", "long torso", "long-legged proportions", "compact torso"],
    },
}

DEFAULT_CLOTHING_MODE_WEIGHTS = {
    "separates": 4,
    "dress": 4,
    "lingerie": 5,
    "sleepwear": 4,
    "cosplay": 5,
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
    "content_rating": "Controls presentation intensity with two concrete outcomes: normal produces a neutral, non-sexualized, non-explicit treatment; glamour/sexy/explicit produces a glamorous, sexualized, explicit treatment. It is included in both Prompt and Pre-gen Text.",
    "gender": "Defines the subject wording. It never hides or forbids body, clothing, makeup, or facial-hair choices.",
    "composition_archetype": "Optional coherent composition recipe. It coordinates framing, pose, horizontal camera direction, head direction, eye focus, vertical camera angle, and frame placement while preserving manual and Forced Random choices. A manual archetype suppresses an ordinary Random Scene scenario; a manual or Forced Random scenario remains authoritative.",
    "portrait_style": "Controls only subject framing, from close-up to full body. Under ordinary Random it adapts to the visibility required by a random pose. Manual and Forced Random framing remain free.",
    "capture_style": "Controls photographic treatment independently from framing. Selfie is now an explicit Pose action, so Capture style no longer silently overrides camera geometry.",
    "scene_scenario": "Rare complete action-and-setting unit. None keeps the classic Pose + Setting path. Ordinary Random selects a scenario ten percent of the time and otherwise keeps Pose + Setting. Forced Random guarantees a scenario. A manually selected scenario replaces Pose and Setting; camera, framing, lighting, and styling remain independent.",
    "setting": "Adds a contextual environment. Ordinary Random is suppressed when a bicycle, horse, car, carousel, or skateboard pose already supplies its own scene context. Manual choices, Forced Random, and text override remain authoritative.",
    "lens_style": "Adds optical and depth-of-field characteristics after the scene description. Ordinary Random only softens a few known harsh lens/lighting collisions; 20% remain deliberately wild.",
    "shot_composition": "Controls placement inside the frame, not camera height. Ordinary Random follows Capture style and avoids placing the subject high with a high camera, or low with a low camera. Manual and Forced Random remain free.",
    "pose_mood": "Adds attitude or emotional bearing without duplicating the concrete body position.",
    "pose": "Controls body mechanics and only keeps an orientation when that orientation is intrinsic to the pose, such as a side squat. Ordinary Random then coordinates with Camera direction; explicit combinations remain authoritative. Vehicle actions suppress only an ordinary Random setting.",
    "camera_direction": "Controls the horizontal relationship between camera and subject. Ordinary Random follows intrinsically side-oriented poses and favors readable views for gestures or movement; manual and Forced Random choices remain unrestricted.",
    "head_direction": "Controls the head orientation independently from body pose, camera height, and Eye Focus. Looking downward no longer implies looking toward the camera.",
    "camera_angle": "Controls only camera height: eye level, low angle, worm's-eye, high angle, or overhead bird's-eye. Ordinary Random keeps it distinct from subject placement in the frame and reserves extreme angles for occasional variation; manual and Forced Random remain unrestricted.",
    "lighting_style": "Describes the light independently from the setting. Ordinary Random softens a few known clashes with duotone, infrared, disposable, and cheap-digital treatments while preserving a 20% wild-card share.",
    "optical_effect": "Opt-in photographic treatment placed before Media type for stronger adherence. Protected from global random buttons; manual Random yields no effect 70% of the time, while Forced Random always selects an effect.",
    "origin_age": "Adds an adult age range near the subject introduction.",
    "origin_ethnicity": "The resolved broad category is included in Pre-gen Text. With Ethnicity guidance enabled, Full Prompt additionally receives the detailed phenotype anchor and weighted eye, hair, and skin pools; that detailed guidance stays out of Pre-gen.",
    "body_archetype": "Optional coherent body recipe. It fills only body controls left on None or ordinary Random. Manual selections and Forced Random remain authoritative, and every phrase an archetype can produce is also available in the regular body widgets.",
    "body_type": "Height only. Ordinary Random excludes the exceptional 'a person with dwarfism' and 'a person of giant stature' values. Forced Random includes the complete list, and a manual choice always remains authoritative. Height is written separately from physique, so short + obese or tall + extremely underweight remains unambiguous.",
    "body_physique": "Weight, softness, fitness, or muscular development, independently weighted by broad families under ordinary Random. Forced Random remains uniform across concrete choices.",
    "body_feminine_curves": "Curve intensity and broad silhouette independently from height and weight. Leg proportions and lumbar curvature now live in Body Detail, with legacy workflows migrated automatically. It is never restricted by gender.",
    "body_hair": "Protected from one-click randomization because explicit presence or absence strongly changes the result. Manual Random and Forced Random remain available.",
    "skin_finish": "Protected from one-click randomization. Ethnicity guidance may use a neutral compatible pool when this field is manually set to Random.",
    "bust": "Independent morphological descriptor; no gender or content-rating restriction is applied.",
    "cleavage_depth": "Works with Cleavage type and clothing. When either neckline field is on ordinary Random, compatible depth/type pairs are favored 90% of the time; manual and Forced Random choices stay free.",
    "cleavage_type": "Neckline shape combined with Neckline depth. Ordinary Random favors coherent pairs; halter and off-shoulder are also suppressed when a complete cosplay already specifies a structured jacket, coat, blazer, uniform, or robe. Manual and Forced Random remain free.",
    "butt_shape": "Independent lower-body descriptor; combines with Body type, physique, curves, and thighs.",
    "thigh_shape": "Independent thigh descriptor; combines with the other body controls.",
    "body_detail_1": "Optional morphological refinement. Ordinary Random and Body Archetype avoid contradictory axes across the three detail slots; manual and Forced Random choices remain authoritative.",
    "body_detail_2": "Second refinement using the same complete Body Detail vocabulary and precedence rules.",
    "body_detail_3": "Third refinement using the same complete Body Detail vocabulary and precedence rules.",
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
    "clothing_archetype": "Guides clothing fields left on Random with concrete compatible garments. Manual choices are never overwritten; cosplay is not selected automatically by archetypes.",
    "top_type": "A concrete top activates the separates family. When a full-body jumpsuit is drawn, an ordinary Random top is suppressed; a manual or Forced Random top remains authoritative and is described as worn over the jumpsuit.",
    "top_color": "Colors modify an active top; a color alone does not activate the separates family.",
    "bottom_type": "A concrete bottom activates the separates family, including full-body jumpsuits. An ordinary Random jumpsuit suppresses an ordinary Random top; a manual or Forced Random top is retained and worn over it. Ordinary Random also softly favors a workable garment length.",
    "bottom_length": "Controls leg coverage. Ordinary Random uses hidden type-compatible pools; manual and Forced Random lengths remain unrestricted. Mid-length trousers show hosiery below their hems; long trousers confine it to the ankles. Skirts, dresses, and short bottoms describe hosiery normally.",
    "bottom_color": "Colors modify an active bottom; a color alone does not activate the separates family.",
    "lingerie_type": "Can be the main outfit or a rare underlayer. Ordinary/Casual/most archetype Random layering is 10%; Emo is 50%; Forced Random is always honored. Under cosplay, automatic layering is limited to Casual and Emo.",
    "lingerie_color": "Colors the selected lingerie or swimwear. A color alone does not activate lingerie.",
    "sleepwear_type": "A complete main garment family. When selected, ordinary Random dress, separates, lingerie, and cosplay families are suppressed.",
    "sleepwear_color": "Colors active sleepwear; a color alone does not activate it.",
    "cosplay_type": "Complete generic costume. Its source draw is weighted for fair per-costume probability. Ordinary Random hosiery, outerwear, belts, and footwear are suppressed; manual choices, Forced Random, and text override remain available.",
    "cosplay_franchise_western": "Complete Western franchise outfit. All cosplay sources share one family and are weighted for fair per-costume probability.",
    "cosplay_franchise_asian": "Complete Asian franchise outfit. All cosplay sources share one family and are weighted for fair per-costume probability.",
    "cosplay_color": "Applies only to generic cosplay. Franchise costumes keep their authored colors unless you make an explicit manual color choice elsewhere.",
    "hosiery": "With skirts, dresses, and short bottoms, hosiery is described normally. Mid-length trousers show it below the trouser hems; long trousers use the deliberately compact ankle-only wording validated in image tests. Ordinary Random is suppressed under cosplay; manual and Forced Random remain valid.",
    "hosiery_color": "Colors active hosiery and follows the same garment-length wording. Every cosplay suppresses ordinary Random hosiery and its color; manual and Forced Random remain valid.",
    "dress_type": "A concrete dress activates the dress family and suppresses competing ordinary Random main garments.",
    "dress_color": "Colors an active dress; a color alone does not activate the dress family.",
    "outerwear": "An optional layer placed over the resolved main outfit. Ordinary Random is suppressed for every cosplay; manual, Forced Random, and override remain available.",
    "outerwear_color": "Colors active outerwear. Every cosplay neutralizes ordinary Random outerwear and its color unless explicitly forced or selected.",
    "outerwear_wearing_style": "Controls how active outerwear is worn. New nodes start on None; an active outerwear without a selected style is worn conventionally. Ordinary Random favors conventional wear, while Forced Random gives every supported position an equal chance.",
    "belt": "An optional accessory layer. Ordinary Random is suppressed for every cosplay; manual, Forced Random, and override remain available.",
    "belt_color": "Colors an active belt. Every cosplay suppresses an ordinary Random belt and its color; manual and Forced Random choices remain valid.",
    "footwear": "Optional footwear. Ordinary Random estimates whether feet are likely to appear from pose, framing, and vertical camera angle; visible hosiery adds a small coherence bonus. Close-up and headshot suppress it, low angles strongly reduce it, while high and worm's-eye views favor it. Manual, Forced Random, franchise-authored footwear, and text override remain valid.",
    "footwear_color": "Colors active footwear. When visibility-aware Random footwear is omitted, its Random color is removed atomically. Manual footwear/colors, Forced Random, and text override remain valid.",
    "head_accessory": "Optional hair/head item. Ordinary Random is suppressed when a complete cosplay already specifies headwear; manual and Forced Random can deliberately layer both. Loc cuffs remain possible everywhere and receive a gentle boost with dreadlocks and braids.",
    "accessories_scarf": "Protected from one-click randomization. When deliberately left on ordinary Random, a scarf appears about 30% of the time; Forced Random always adds one.",
    "accessories_jewelry": "General jewelry fallback. With specific necklace, earrings, bracelet, or rings, gold/silver tone becomes a compatible material modifier and other broad jewelry labels stand down to prevent merged objects.",
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
    "lock_content_rating": "Protects Content rating from global randomization. Content rating is outside every local section randomizer.",
    "ethnicity_guidance": "When activated, facial anatomy uses a strong anchor; Eye color on None or Random uses its weighted ethnicity pool. Forced Random and manual values deliberately override guidance.",
    "enhance_realism": "Appends a realism suffix about plausible lighting, exposure, texture, composition, and natural photographic imperfections.",
    "species_mode": "Anthro Furry adds a furry subject prefix. It does not remove human-oriented clothing or morphology controls.",
    "enforce_portrait_framing": "When activated, Pre-gen Text becomes one minimal introductory sentence containing only media type, resolved portrait/capture style, age, simple ethnicity category, gender, and any fundamental nonhuman subject type. This lets a close framing establish the first-pass composition before clothing and body detail are introduced later.",
    "seed": "Every Random field has its own deterministic stream derived from this seed. Fixing one field no longer changes unrelated random fields.",
    "control_after_generate": "ComfyUI seed behavior after each run. Use fixed to preserve all resolved Random choices while editing selected fields.",
    "free_prompt": "Free text inserted at the selected position without changing any structured category.",
    "free_prompt_position": "Places Free prompt after the introduction, after makeup, or at the very end.",
    "override_field": "Selects the structured property replaced by Override text. A non-empty connected string has absolute priority over manual choices, Forced Random, guidance, archetypes, probabilities, and compatibility rules. Overriding a main garment type also clears competing main garment families so the text is guaranteed to appear.",
    "override_text": "Connect one STRING here. When non-empty, it replaces the property selected by Override field exactly as written.",
    "identity_forge_json": "Optional JSON from Identity Forge Archetype, Cosplayer, Creature, or Modifier. Character Architect keeps its own interface and rendering order while importing the preset. Archetype/Cosplayer identity remains anchored even when manual clothing replaces the imported outfit. Manual choices and Forced Random stay above imported JSON; ordinary Random stays below it. Creature anatomy activates the nonhuman-safe renderer.",
    "inspect_property": "Selects one resolved property to expose through Inspected Value for overlays, comparisons, and statistics. It reports the final value after every rule and override.",
    "eye_focus": "Controls what the eyes are actually focused on, independently from Head direction and gaze mood. Manual and Forced Random choices are authoritative; ordinary Random favors the active action when it clearly involves a person or held object.",
    "mouth_expression": "Adds a concrete mouth action independently from the general facial expression. Ordinary Random uses a compatible pool; manual and Forced Random combinations remain unrestricted.",
    "setting_text_override": "Optional exact text replacing Setting and Scene scenario. Connect or paste a description produced from a reference image by ComfyUI Generate Text; Character Architect itself loads no vision model and adds no dependency.",
    "pose_text_override": "Optional exact text replacing Pose and Scene scenario while preserving Setting. It can receive a pose description generated from a reference image without adding a vision-model dependency to Character Architect.",
    "face_hair_text_override": "Optional structured face-reference description from Generate Text. Use semicolon-separated key=value pairs for the supported Face and Hair fields. Manual and Forced Random selections remain authoritative per field; this input then leads over Identity Forge, Subject wildcard, and ordinary Random. A valid description suspends the indivisible Subject wildcard and detailed Ethnicity Guidance, while preserving the simple origin category. Face traits stay out of Pre-gen; resolved hair remains included.",
    "custom_color_overrides": "Arbitrary color replacements using target=value pairs separated by semicolons or new lines. Example: top=fuchsia; hosiery=salmon pink; hair=teal. Clothing colors modify only an active garment.",
    "wildcard_subject": "Optional expanded wildcard text replacing the node's subject identity and appearance blocks. Supply already-expanded text or connect a wildcard processor; Character Architect does not require or bundle a wildcard engine.",
    "wildcard_clothing": "Optional expanded wildcard text replacing the node's Clothes and Shoes block. Standalone accessories remain available unless the supplied text includes them.",
    "wildcard_pose": "Optional expanded wildcard text replacing Pose and Scene scenario while preserving the node's Setting.",
    "wildcard_setting": "Optional expanded wildcard text replacing Setting and Scene scenario while preserving the node's Pose.",
    "wildcard_photography": "Optional expanded wildcard text replacing Media type, framing, camera, composition, lens, lighting, and optical-effect controls.",
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

# Concrete clothing replaces the former abstract Outfit Style signal. Every
# phrase used by an archetype is also inserted into the matching manual widget,
# so ordinary Full Random and manual selection share exactly the same vocabulary.
CLOTHING_SCHEMA_ADDITIONS = {
    "clothing_archetype": ["Regional Everyday / Formalwear"],
    "top_type": [
        "silk blouse", "tie-neck silk blouse", "puff-sleeve blouse", "peplum top",
        "turtleneck top", "off-shoulder top", "fitted bodysuit top", "sweater vest",
        "Breton striped top", "multi-pocket technical vest", "sculptural asymmetric top",
        "ruffled high-collar blouse", "ornate brocade corset top", "embroidered huipil blouse",
        "guayabera shirt",
    ],
    "bottom_type": [
        "pencil skirt", "A-line skirt", "bias-cut satin midi skirt", "denim skirt",
        "cigarette trousers", "straight-leg trousers", "culottes", "tailored shorts",
        "capri pants", "tennis skirt", "tapered technical cargo pants",
        "asymmetrical layered skirt", "patent leather pants",
    ],
    "dress_type": [
        "classic little black dress", "classic sheath dress", "cocktail dress",
        "fit-and-flare dress", "tea dress", "summer sundress", "blazer dress",
        "denim dress", "tailored trouser suit", "classic skirt suit", "denim overalls",
        "utility boiler suit", "short romper", "architectural cutout dress",
        "metallic mini dress",
        "contemporary djellaba",
        "contemporary kaftan",
        "salwar kameez ensemble",
        "kurta and trouser ensemble",
        "contemporary sari",
        "Anarkali suit",
        "kebaya and batik sarong ensemble",
        "baju kurung ensemble",
        "ao dai ensemble",
        "West African boubou ensemble",
        "modern qipao",
    ],
    "outerwear": [
        "pea coat", "duffle coat", "parka", "raincoat", "cropped tweed jacket",
        "varsity jacket", "utility field jacket", "shearling jacket", "faux-fur coat",
        "long wool coat", "cropped technical shell jacket",
        "sharp-shouldered cropped blazer", "tailored military jacket",
        "contemporary haori-style jacket", "mandarin-collar frog-button jacket",
    ],
    "footwear": [
        "ballet flats", "classic pumps", "kitten heels", "mules", "espadrilles",
        "cowboy boots", "riding boots", "rain boots",
        "extreme platform stiletto heels with very tall heels and thick platform soles, Pleaser-style",
    ],
}

REGIONAL_COMPLETE_OUTFITS = CLOTHING_SCHEMA_ADDITIONS["dress_type"][-11:]

# Short, readable widget labels expand into compact visual definitions. These
# descriptions contain only the construction cues that help the image model
# distinguish each garment; they deliberately avoid encyclopedic background.
CULTURAL_GARMENT_EXPANSIONS = {
    "contemporary djellaba": "contemporary North African djellaba, a loose ankle-length hooded robe with long sleeves and a clean front opening",
    "contemporary kaftan": "contemporary kaftan with a loose floor-length silhouette, wide flowing sleeves, a defined neckline, and restrained decorative trim",
    "salwar kameez ensemble": "South Asian salwar kameez ensemble with a long side-slit tunic, loose tapered salwar trousers, and a matching shoulder-draped dupatta",
    "kurta and trouser ensemble": "South Asian kurta ensemble with a straight knee-length side-slit tunic worn over loose flowing trousers",
    "contemporary sari": "contemporary South Asian sari, long draped fabric wrapped into a floor-length skirt and pleated over one shoulder above a fitted blouse",
    "Anarkali suit": "South Asian Anarkali suit with a fitted embroidered bodice, long flared panelled kurta, slim churidar trousers, and a matching shoulder-draped dupatta",
    "kebaya and batik sarong ensemble": "Southeast Asian kebaya ensemble with a fitted embroidered front-opening blouse over a coordinated ankle-length batik sarong",
    "baju kurung ensemble": "Malay baju kurung ensemble with a loose long-sleeved thigh-length tunic over a coordinated ankle-length straight skirt",
    "ao dai ensemble": "Vietnamese ao dai ensemble with a high-collared fitted long tunic, waist-high side slits, and loose flowing trousers",
    "West African boubou ensemble": "West African boubou ensemble with a wide flowing embroidered robe, broad sleeves, and a coordinated full-length underdress",
    "modern qipao": "modern qipao with a fitted column silhouette, high mandarin collar, diagonal frog closures, and side slits",
    "embroidered huipil blouse": "embroidered huipil blouse with a loose square-cut silhouette, straight neckline, short wide sleeves, and geometric woven panels",
    "guayabera shirt": "guayabera shirt with four front patch pockets, vertical pleated panels, straight hem, and short sleeves",
    "contemporary haori-style jacket": "contemporary haori-style jacket with a straight open front, broad rectangular sleeves, and a hip-length boxy silhouette",
    "mandarin-collar frog-button jacket": "mandarin-collar frog-button jacket with a straight structured cut, stand collar, and symmetrical knotted front closures",
}

CLOTHING_ARCHETYPE_ENRICHMENTS = {
    "Classy Chic": {
        "top_type": ["silk blouse", "tie-neck silk blouse", "peplum top", "turtleneck top", "sweater vest", "Breton striped top"],
        "bottom_type": ["pencil skirt", "A-line skirt", "bias-cut satin midi skirt", "cigarette trousers", "straight-leg trousers", "culottes"],
        "dress_type": ["classic little black dress", "classic sheath dress", "cocktail dress", "fit-and-flare dress", "tea dress", "blazer dress", "tailored trouser suit", "classic skirt suit"],
        "outerwear": ["pea coat", "cropped tweed jacket", "long wool coat"],
        "footwear": ["ballet flats", "classic pumps", "kitten heels", "mules", "riding boots"],
    },
    "Casual Everyday": {
        "top_type": ["puff-sleeve blouse", "turtleneck top", "off-shoulder top", "fitted bodysuit top", "sweater vest", "Breton striped top"],
        "bottom_type": ["A-line skirt", "denim skirt", "straight-leg trousers", "culottes", "tailored shorts", "capri pants", "tennis skirt"],
        "dress_type": ["fit-and-flare dress", "tea dress", "summer sundress", "denim dress", "denim overalls", "utility boiler suit", "short romper"],
        "outerwear": ["parka", "raincoat", "varsity jacket", "utility field jacket", "shearling jacket"],
        "footwear": ["ballet flats", "mules", "espadrilles", "cowboy boots", "rain boots"],
    },
    "Streetwear": {
        "top_type": ["multi-pocket technical vest", "fitted bodysuit top"],
        "bottom_type": ["tapered technical cargo pants", "patent leather pants"],
        "outerwear": ["cropped technical shell jacket", "varsity jacket", "utility field jacket", "sharp-shouldered cropped blazer"],
    },
    "Romantic / Feminine Soft": {
        "top_type": ["silk blouse", "tie-neck silk blouse", "puff-sleeve blouse", "peplum top", "off-shoulder top"],
        "bottom_type": ["A-line skirt", "bias-cut satin midi skirt", "tennis skirt"],
        "dress_type": ["cocktail dress", "fit-and-flare dress", "tea dress", "summer sundress"],
        "footwear": ["ballet flats", "kitten heels", "espadrilles"],
    },
    "Glam / Night Out": {
        "top_type": ["sculptural asymmetric top", "fitted bodysuit top"],
        "bottom_type": ["pencil skirt", "patent leather pants"],
        "dress_type": ["classic little black dress", "cocktail dress", "blazer dress", "architectural cutout dress", "metallic mini dress"],
        "outerwear": ["sharp-shouldered cropped blazer", "faux-fur coat"],
        "footwear": ["classic pumps", "mules", "extreme platform stiletto heels with very tall heels and thick platform soles, Pleaser-style"],
    },
    "Gothic / Dark Romantic": {
        "top_type": ["ruffled high-collar blouse", "ornate brocade corset top", "sculptural asymmetric top"],
        "bottom_type": ["pencil skirt", "asymmetrical layered skirt", "patent leather pants"],
        "dress_type": ["architectural cutout dress", "classic little black dress"],
        "outerwear": ["tailored military jacket", "faux-fur coat", "sharp-shouldered cropped blazer"],
        "footwear": ["extreme platform stiletto heels with very tall heels and thick platform soles, Pleaser-style"],
    },
    "Emo / Scene / Alt": {
        "top_type": ["ruffled high-collar blouse", "ornate brocade corset top", "sculptural asymmetric top"],
        "bottom_type": ["asymmetrical layered skirt", "patent leather pants", "tapered technical cargo pants"],
        "outerwear": ["tailored military jacket", "sharp-shouldered cropped blazer"],
        "footwear": ["extreme platform stiletto heels with very tall heels and thick platform soles, Pleaser-style"],
    },
    "Sporty / Athleisure": {
        "top_type": ["fitted bodysuit top", "sweater vest"],
        "bottom_type": ["tennis skirt", "capri pants", "tailored shorts"],
        "dress_type": ["utility boiler suit", "short romper"],
        "outerwear": ["varsity jacket", "raincoat", "utility field jacket"],
    },
    "Boho / Festival": {
        "top_type": ["puff-sleeve blouse", "off-shoulder top", "embroidered huipil blouse"],
        "bottom_type": ["A-line skirt", "bias-cut satin midi skirt", "culottes"],
        "dress_type": ["fit-and-flare dress", "tea dress", "summer sundress"],
        "outerwear": ["shearling jacket"],
        "footwear": ["espadrilles", "cowboy boots"],
    },
    "Kawaii": {
        "top_type": ["puff-sleeve blouse", "peplum top", "sweater vest", "off-shoulder top"],
        "bottom_type": ["A-line skirt", "tennis skirt"],
        "dress_type": ["fit-and-flare dress", "tea dress"],
        "outerwear": ["cropped tweed jacket"],
        "footwear": ["ballet flats", "kitten heels"],
    },
}

CLOTHING_ARCHETYPE_CONFIG["Regional Everyday / Formalwear"] = {
    "main_modes": ["dress"],
    "dress_type": list(REGIONAL_COMPLETE_OUTFITS),
    "dress_color": [
        "black", "white", "cream", "beige", "camel", "brown", "navy", "blue",
        "teal", "green", "olive", "red", "burgundy", "pink", "purple", "gold",
        "silver", "silky floral pattern", "geometric print", "linen texture",
    ],
    # Keep the complete regional garment indivisible. Random secondary garments
    # stand down instead of producing cross-cultural composites.
    "outerwear": [None],
    "belt": ["no visible belt"],
    "footwear": ["sandals", "loafers", "ballet flats"],
    "footwear_color": ["black", "white", "cream", "beige", "camel", "brown", "gold", "silver"],
    "hosiery": ["bare legs"],
    "lingerie_type": ["simple bralette underlayer"],
    "lingerie_color": ["black", "white", "cream"],
    "head_accessory": ["no head accessory"],
    "accessories_scarf": ["no scarf"],
    "accessories_bag": ["no bag", "handbag", "clutch bag"],
}

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
# they strongly reshape the image. Forced Random still chooses a concrete
# effect every time. Ordinary Random keeps seventy percent clean output.
OPTICAL_EFFECT_RANDOM_POOL = (
    [None] * 70
    + ["fisheye"] * 8
    + ["infrared false-color"] * 8
    + ["high-contrast duotone"] * 7
    + ["selective-color monochrome"] * 7
)

BODY_PHYSIQUE_RANDOM_FAMILIES = (
    ["underweight"] * 11 + ["ordinary"] * 14 + ["heavy"] * 11 + ["muscular"] * 4
)
BODY_PHYSIQUE_RANDOM_VALUES = {
    "underweight": [
        "naturally extremely slender, fine-boned underweight physique",
        "extremely underweight physique",
        "very slim physique",
        "slim physique",
    ],
    "ordinary": ["soft untrained physique", "average physique", "lightly toned physique", "toned physique"],
    "heavy": ["plump physique", "plus-size physique", "overweight physique", "obese physique"],
    "muscular": ["athletic physique", "muscular physique", "heavily muscular physique"],
}

OUTERWEAR_WEARING_STYLE_RANDOM_POOL = (
    ["Properly worn"] * 60
    + ["Draped over shoulders"] * 15
    + ["Off shoulders at elbows"] * 15
    + ["Carried over one shoulder"] * 10
)

BICYCLE_SCENARIO = "riding a full-size road bicycle along a real cycle path, seated on the saddle with both hands on the handlebars, feet placed on the pedals, and the body leaning naturally forward"
HORSE_SCENARIO = "riding a full-size horse in an open equestrian arena, seated securely in a fitted saddle with both feet in the stirrups, both hands loosely holding the reins, and the torso following the horse's movement"
CAR_DRIVING_SCENARIO = "seated correctly in the driver's seat inside a full-size production passenger car with a conventional enclosed cabin, visible dashboard, windshield, doors, and an empty front passenger seat, both hands naturally on the steering wheel while driving along a real road"
CAROUSEL_SCENARIO = "riding a full-size decorative carousel horse on a working amusement-park carousel, seated astride the saddle with one hand holding the central pole as the surrounding platform turns"
SKATEBOARD_SCENARIO = "riding a skateboard through a real urban skatepark, one foot planted on the board, the other just lifted after pushing, arms balancing naturally among ramps and painted concrete"

LEGACY_ACTION_POSE_TO_SCENARIO = {
    "riding a bicycle with both hands holding the handlebars and the body leaning naturally forward": BICYCLE_SCENARIO,
    "riding a horse, seated securely in the saddle, both hands loosely holding the reins, torso following the horse's movement": HORSE_SCENARIO,
    "seated behind the wheel of a car with both hands placed naturally on the steering wheel while actively driving": CAR_DRIVING_SCENARIO,
    "riding a moving carousel horse, seated astride the saddle with one hand holding the central pole": CAROUSEL_SCENARIO,
    "riding a skateboard through the scene, one foot planted on the board, the other just lifted after pushing, arms balancing naturally": SKATEBOARD_SCENARIO,
}

VEHICLE_OR_MOUNT_SCENARIOS = {
    BICYCLE_SCENARIO, HORSE_SCENARIO, CAR_DRIVING_SCENARIO, CAROUSEL_SCENARIO, SKATEBOARD_SCENARIO,
}

SELFIE_CAPTURE_STYLE = "spontaneous handheld selfie"
SELFIE_POSE = (
    "taking a selfie with one arm extended, holding a smartphone at arm's length with its front camera "
    "aimed toward the subject, looking into the phone's camera"
)

# Framing and pose are separate controls, but their ordinary Random values
# should agree about how much of the body must be visible. Explicit and Forced
# Random selections remain deliberately unconstrained.
CLOSE_FRAMINGS = {"close-up portrait", "headshot portrait"}
BUST_FRAMINGS = CLOSE_FRAMINGS | {"bust portrait"}
UPPER_BODY_POSES = {
    "standing with the weight shifted softly onto one hip",
    "standing with one hand in the hair and the weight shifted onto one hip",
    "leaning back against a wall with one knee bent",
    "standing at attention with one hand raised in a formal military salute",
    "raising one hand in a friendly wave",
    "standing naturally with both arms folded across the chest",
    "standing casually with both hands resting in the pockets",
    "standing with both hands loosely clasped behind the back",
    "giving a cheerful thumbs-up with one hand",
    "raising both shoulders in a light shrug, palms turned upward",
    "adjusting one sleeve with the opposite hand",
}
FULL_SCENE_POSES = {
    "balanced in a low squat, elbows resting loosely on the thighs, torso upright",
    "compact low squat, arms wrapped around the knees, shoulders slightly rounded",
    "low crouching pose, one hand planted on the floor, the other resting on the thigh",
    "low side squat, torso upright",
    "kneeling with hips resting on the heels, hands placed on the thighs, upright elegant posture",
    "kneeling on one knee with the other knee raised, forearm resting across the raised thigh",
    "kneeling upright with both hands behind the head, elbows open, hips shifted slightly to one side",
    "kneeling and leaning forward, palms resting on the floor in front",
    "on hands and knees with the back mostly straight",
    "on hands and knees with the weight shifted onto one arm",
    "on hands and knees with a gentle arch through the lower back and the shoulders lowered",
    "on hands and knees with one knee drawn forward between the hands and the torso gently twisted",
    "kneeling with forearms resting on the floor, hips raised, and the back gently curved",
    "lying on the stomach, upper body lifted on the elbows, both lower legs raised behind",
    "reclining on one side in a gentle S-curve, upper body supported by one forearm, upper knee drawn forward",
    "lying on the back with the legs comfortably spread apart and the arms resting naturally",
    "lying on the side with the head supported by one hand and the legs relaxed",
    "lying on the back with one knee bent and the other leg extended",
    "lying on the stomach with the upper body gently raised on the forearms",
    "lying curled slightly on one side with the knees loosely drawn upward",
    "reclining on the back with both knees bent and the feet resting on the supporting surface",
    "caught mid-spin while dancing, torso and arms turning dynamically",
}

MID_BODY_POSES = UPPER_BODY_POSES | {
    "bending forward with both hands resting above the knees",
    "seated upright with legs crossed, one hand resting on the upper knee",
    "perched on the edge of a chair, knees together, torso leaning forward slightly, hands resting on the thighs",
    "seated with one knee raised toward the chest, arms loosely wrapped around the leg",
    "seated on the edge of a stool with one hand braced behind",
    "sitting low with knees comfortably apart, elbows resting on the thighs, shoulders slightly forward",
    SELFIE_POSE,
    "holding a game controller with both hands, absorbed in an ongoing game",
    "listening intently to a speech, visibly moved, among a small crowd of fellow listeners",
    "applauding enthusiastically among a gathered audience",
    "laughing during a lively group conversation",
    "waiting patiently in a loose queue, casually observing the surroundings",
    "joining a spontaneous group cheer with one arm raised",
    "dancing casually among a small surrounding crowd",
    "watching a nearby performance with absorbed fascination",
    "reading a posted notice alongside several curious onlookers",
    "reacting with surprise as the surrounding crowd turns toward the same event",
    "sharing a celebratory toast within a small gathering",
    "posing naturally while friends gather loosely nearby",
    "shaking a hand extended from the edge of the frame",
    "reading a folded newspaper held naturally in both hands, absorbed in the article",
    "writing a quick note in a small pocket notebook, pausing briefly in thought",
    "holding an unfolded paper map and tracing a route with one finger",
    "taking a casual sip from a takeaway cup, holding it loosely near the face",
    "examining a small instant photograph held delicately between the fingers",
}

# Horizontal direction remains a distinct creative axis, but its ordinary
# Random distribution should still let a readable gesture be seen. These are
# weighted preferences only: every explicit or Forced Random direction remains
# legal, including rear views and unusual vertical angles.
FRONT_READABLE_POSES = {
    "standing at attention with one hand raised in a formal military salute",
    "raising one hand in a friendly wave",
    "standing naturally with both arms folded across the chest",
    "giving a cheerful thumbs-up with one hand",
    "raising both shoulders in a light shrug, palms turned upward",
    "adjusting one sleeve with the opposite hand",
    SELFIE_POSE,
    "holding a game controller with both hands, absorbed in an ongoing game",
    "reading a folded newspaper held naturally in both hands, absorbed in the article",
}
KINETIC_SCENE_POSES = {
    "caught mid-spin while dancing, torso and arms turning dynamically",
    "joining a spontaneous group cheer with one arm raised",
    "dancing casually among a small surrounding crowd",
}
SIDE_ORIENTED_POSES = {
    "low side squat, torso upright",
    "reclining on one side in a gentle S-curve, upper body supported by one forearm, upper knee drawn forward",
    "lying on the side with the head supported by one hand and the legs relaxed",
    "lying curled slightly on one side with the knees loosely drawn upward",
}
DEFAULT_RANDOM_CAMERA_DIRECTIONS = (
    ["front-facing view"] * 4
    + ["three-quarter view"] * 4
    + ["profile view"] * 2
    + ["rear three-quarter view"] * 2
)
FRONT_READABLE_CAMERA_DIRECTIONS = (
    ["front-facing view"] * 5
    + ["three-quarter view"] * 4
    + ["profile view"]
)
KINETIC_CAMERA_DIRECTIONS = (
    ["front-facing view"] * 2
    + ["three-quarter view"] * 4
    + ["profile view"] * 3
    + ["rear three-quarter view"]
)
SIDE_ORIENTED_CAMERA_DIRECTIONS = (
    ["profile view"] * 5
    + ["three-quarter view"] * 3
    + ["rear three-quarter view"]
)
CAR_SCENARIO_CAMERA_DIRECTIONS = (
    ["front-facing view"] * 3
    + ["three-quarter view"] * 5
    + ["profile view"] * 2
)
VEHICLE_MOUNT_RANDOM_FRAMING_POOL = (
    ["three-quarter portrait"] * 2 + ["full-body portrait"] * 3
)
DEFAULT_RANDOM_CAMERA_ANGLES = (
    ["at eye level"] * 6
    + ["from a pronounced low angle, with the camera positioned below the subject"] * 2
    + ["from a pronounced high angle, with the camera positioned above the subject"] * 2
    + ["from an extreme worm's-eye angle at ground level, with the camera looking sharply upward"]
    + ["from an overhead bird's-eye angle, with the camera looking straight down"]
)
VEHICLE_MOUNT_RANDOM_CAMERA_ANGLES = (
    ["at eye level"] * 6
    + ["from a pronounced low angle, with the camera positioned below the subject"]
    + ["from a pronounced high angle, with the camera positioned above the subject"]
)
CLOSE_RANDOM_CAMERA_ANGLES = (
    ["at eye level"] * 6
    + ["from a pronounced low angle, with the camera positioned below the subject"]
    + ["from a pronounced high angle, with the camera positioned above the subject"] * 2
)
HIGH_CAMERA_ANGLES = {
    "from a pronounced high angle, with the camera positioned above the subject",
    "from an overhead bird's-eye angle, with the camera looking straight down",
}
LOW_CAMERA_ANGLES = {
    "from a pronounced low angle, with the camera positioned below the subject",
    "from an extreme worm's-eye angle at ground level, with the camera looking sharply upward",
}
HIGH_FRAME_PLACEMENT = "subject placed high in frame"
LOW_FRAME_PLACEMENT = "subject placed low in frame"
CAPTURE_FRAMING_POOLS = {
    "beauty": ["close-up portrait", "headshot portrait", "bust portrait", "bust portrait", "half-body portrait"],
    "glamour": ["bust portrait", "half-body portrait", "half-body portrait", "three-quarter portrait", "three-quarter portrait", "full-body portrait"],
    "editorial": ["bust portrait", "half-body portrait", "three-quarter portrait", "three-quarter portrait", "full-body portrait"],
    "fashion": ["bust portrait", "half-body portrait", "three-quarter portrait", "three-quarter portrait", "full-body portrait"],
    "cinematic": ["close-up portrait", "bust portrait", "half-body portrait", "three-quarter portrait", "full-body portrait", "full-body portrait"],
    "street-style": ["half-body portrait", "three-quarter portrait", "three-quarter portrait", "full-body portrait", "full-body portrait"],
    "environmental": ["half-body portrait", "three-quarter portrait", "full-body portrait", "full-body portrait"],
    "candid": ["bust portrait", "half-body portrait", "three-quarter portrait", "full-body portrait"],
    "dramatic": ["close-up portrait", "bust portrait", "half-body portrait", "three-quarter portrait", "full-body portrait"],
}
DEFAULT_RANDOM_FRAMING_POOL = [
    "portrait", "bust portrait", "half-body portrait", "half-body portrait",
    "three-quarter portrait", "three-quarter portrait", "full-body portrait",
]

NATURAL_CAPTURE_STYLES = {"street-style", "environmental", "candid"}
CAPTURE_COMPOSITION_POOLS = {
    "street-style": [
        "rule-of-thirds composition", "negative-space composition", "dynamic diagonal composition",
        "subject placed high in frame", "subject placed low in frame", "candid off-center framing",
    ],
    "environmental": [
        "rule-of-thirds composition", "negative-space composition", "subject placed high in frame",
        "subject placed low in frame", "candid off-center framing", "centered composition",
    ],
    "candid": [
        "rule-of-thirds composition", "dynamic diagonal composition", "subject placed high in frame",
        "subject placed low in frame", "candid off-center framing",
    ],
    "cinematic": [
        "rule-of-thirds composition", "negative-space composition", "dynamic diagonal composition",
        "subject placed high in frame", "subject placed low in frame", "symmetrical composition",
    ],
    "glamour": [
        "centered composition", "symmetrical composition", "rule-of-thirds composition",
        "negative-space composition", "clean precisely organized composition", "editorial magazine composition",
    ],
    "editorial": [
        "centered composition", "symmetrical composition", "rule-of-thirds composition",
        "negative-space composition", "dynamic diagonal composition", "clean precisely organized composition",
        "editorial magazine composition",
    ],
    "fashion": [
        "centered composition", "symmetrical composition", "rule-of-thirds composition",
        "dynamic diagonal composition", "clean precisely organized composition", "editorial magazine composition",
    ],
    "beauty": [
        "centered composition", "symmetrical composition", "rule-of-thirds composition",
        "negative-space composition", "clean precisely organized composition", "editorial magazine composition",
    ],
    "dramatic": [
        "centered composition", "symmetrical composition", "negative-space composition",
        "dynamic diagonal composition", "subject placed high in frame", "subject placed low in frame",
    ],
}
CAPTURE_LENS_POOLS = {
    "street-style": ["35mm documentary lens look", "50mm standard lens look", "wide-angle perspective", "vintage lens rendering", "disposable camera look", "cheap digital camera aesthetic"],
    "environmental": ["35mm documentary lens look", "50mm standard lens look", "wide-angle perspective", "vintage lens rendering", "anamorphic lens look"],
    "candid": ["35mm documentary lens look", "50mm standard lens look", "85mm portrait lens look", "vintage lens rendering", "disposable camera look", "cheap digital camera aesthetic"],
    "beauty": ["50mm standard lens look", "85mm portrait lens look", "macro-detail lens look", "soft-focus lens look"],
}
NATURAL_CAPTURE_LIGHTING = [
    "window light", "golden-hour light", "overcast daylight", "direct flash", "hard flash",
    "backlit glow", "rim lighting", "neon lighting", "subdued low-key lighting with deep natural shadows",
]

# V4 environment metadata is explicit rather than inferred from words such as
# "inside". Ordinary Random uses these families to choose physically coherent
# lighting and grammar; manual and Forced Random selections remain untouched.
OUTDOOR_OR_SEMIOPEN_SETTINGS = {
    "on a chic café terrace with passing pedestrians and gentle city bustle",
    "on a lively city street with storefront reflections, distant traffic, and pedestrian movement",
    "on a high rooftop with layered skyline architecture and gentle urban haze",
    "in a narrow neon-lined alley with reflective pavement and distant nightlife movement",
    "along a seaside promenade with railings, distant walkers, and an open coastal horizon",
    "on a windswept beach with rolling surf, dunes, and sparse distant figures",
    "in a misty forest clearing with layered trees, undergrowth, and atmospheric depth",
    "in an overgrown garden with stone paths, dense greenery, and distant architecture",
    "at a weathered desert roadside stop with open horizon and passing vehicle traces",
    "in open countryside with layered fields, distant paths, and gentle background movement",
    "in a university courtyard with layered architecture, greenery, and passing students",
    "in an open town square with surrounding facades and diffuse pedestrian activity",
    "along a narrow old-town street with textured walls, balconies, and distant passersby",
    "on a rain-slicked boulevard with layered reflections, traffic haze, and urban movement",
    "outside a rural roadside station with weathered signs, open landscape, and passing vehicles",
    "on a mountain lodge terrace with timber architecture, distant peaks, and relaxed activity",
    "beside a quiet lakeside dock with wooded depth and subtle distant movement",
    "along a rugged rocky coastline with layered cliffs, sea mist, and open horizon",
    "in an autumn park with textured foliage, winding paths, and scattered distant walkers",
    "along a snowy village street with warm windows, layered rooftops, and sparse activity",
    "inside a botanical courtyard with stone arcades, abundant greenery, and quiet movement",
    "at a lively fairground with colorful structures, distant visitors, and playful atmospheric depth",
    "beside a rooftop pool with city views, lounge furniture, and relaxed background activity",
    "at a tropical resort pool with lush greenery, reflective water, and distant guests",
    "on a pedestrian bridge with structural lines, city depth, and passing figures",
    "along a Mediterranean harbor quay with moored boats, weathered stone, waterfront buildings, and open sea depth",
    "in a broad brutalist civic plaza with monumental concrete forms, geometric steps, and sparse pedestrian movement",
    "beneath an elevated railway with repeating steel supports, layered street activity, and deep urban perspective",
    "along an urban canal embankment with stone walls, footbridges, waterside paths, and passing cyclists",
    "at a suburban gas station with fuel pumps, a small convenience building, parked vehicles, and roadside depth",
    "on a vineyard terrace with ordered vine rows, low stone walls, distant hills, and open agricultural depth",
    "inside a dense bamboo grove with tall repeating stalks, filtered daylight, leaf litter, and winding natural paths",
    "along a rocky canyon trail with layered sandstone walls, uneven ground, sparse vegetation, and distant depth",
    "on a vast salt flat with pale textured ground, a low uninterrupted horizon, and subtle distant reflections",
    "along a wetland boardwalk with reed beds, shallow reflective water, open sky, and distant birdlife",
    "at an eerie abandoned amusement park with rusting rides, peeling paint, cracked pavement, encroaching weeds, and empty urbex depth",
}

DAYLIT_INTERIOR_SETTINGS = {
    "in a refined luxury hotel lobby with polished surfaces and quiet guest movement",
    "inside a contemporary apartment with lived-in details and open-plan architectural depth",
    "in a minimalist loft with industrial windows, textured walls, and sparse modern furniture",
    "inside an elegant dressing room with garment racks, mirrors, and scattered styling tools",
    "inside a grand staircase hall with sweeping lines, ornate architecture, and distant visitors",
    "in a spacious contemporary gallery with abstract artworks and quiet background visitors",
    "inside a humid glass greenhouse with dense varied foliage and layered botanical depth",
    "in a historic flower conservatory with ironwork, winding paths, and seasonal vegetation",
    "inside a lived-in bedroom with rumpled fabrics, personal details, and natural clutter",
    "in a faded retro motel room with roadside atmosphere beyond the windows",
    "inside a tall-shelved library with quiet reading areas and subtle background movement",
    "inside a curated boutique showroom with mirrors, display areas, and spacious retail depth",
    "inside a modern office lobby with clean architecture and diffuse professional activity",
    "inside a busy train-station concourse with layered signage and flowing distant commuters",
    "inside a spacious airport terminal with glass architecture and distant travelers in motion",
    "inside a lively shopping arcade with layered storefronts, reflections, and casual foot traffic",
    "in a vintage theater foyer with decorative architecture and softly gathering guests",
    "in an art-deco ballroom with geometric ornament, open floor space, and distant guests",
    "inside a converted industrial warehouse with raw textures, open space, and scattered activity",
    "inside a cozy attic room with sloped ceilings, layered belongings, and intimate depth",
    "inside a neighborhood laundromat with repeating machines, reflective surfaces, and casual activity",
    "inside an independent record shop with crowded shelves, posters, and browsing visitors",
    "inside a grand hotel suite with layered rooms, rich textiles, and understated luxury",
    "inside a small neighborhood café with varied seating, window reflections, and quiet conversation",
    "inside an old railway carriage with worn textures, narrow depth, and seated travelers",
    "inside a spacious artist studio with large windows, easels, canvases, worktables, and layered creative clutter",
    "inside a working ceramics studio with pottery wheels, clay-covered tables, drying shelves, and finished vessels",
    "inside a grand natural-history museum hall with large specimen displays, stone architecture, and scattered visitors",
    "inside a professional vehicle workshop with full-size cars, hydraulic lifts, tool cabinets, and open service bays",
    "inside a bright dance rehearsal studio with sprung flooring, mirrored walls, high windows, and open practice space",
    "inside a working bakery with flour-dusted counters, cooling racks, ovens, and active preparation areas",
    "inside a public gymnasium with court markings, retractable bleachers, sports equipment, and broad overhead structure",
    "inside a large working farm barn with timber framing, stacked hay, agricultural tools, and open daylight from wide doors",
    "inside a textile workshop with cutting tables, fabric rolls, sewing stations, and hanging work in progress",
    "beside a public indoor swimming pool with tiled deck, lane markings, high windows, and reflective aquatic depth",
    "inside a vast aircraft hangar with full-size aircraft, maintenance platforms, equipment carts, and daylight through broad doors",
    "inside a commercial airplane passenger cabin with aligned seat rows, overhead luggage bins, oval windows, and a visible central aisle",
}

ENCLOSED_INTERIOR_SETTINGS = {
    "in a working professional photo studio with neutral backdrops and subtle production activity",
    "on a spacious fashion editorial set with modular scenery and layered production depth",
    "backstage at a fashion show among clothing racks and softly blurred staff movement",
    "inside an intimate bar with dark wood booths and indistinct background patrons",
    "inside an intimate room with layered fabrics and a quiet domestic atmosphere",
    "in a refined velvet lounge with curved seating, rich textures, and discreet activity",
    "inside a futuristic corridor with repeating structures, reflective materials, and distant silhouettes",
    "on a surreal theatrical set with oversized abstract forms and shifting visual textures",
    "on an urban subway platform with repeating lines and indistinct passenger movement",
    "inside a crowded nightclub with layered silhouettes, reflective surfaces, and energetic atmosphere",
    "along a quiet hotel corridor with repeating doors, soft textures, and distant movement",
    "inside a stylish restaurant with layered tables and discreet background conversation",
    "inside a late-night convenience store with stocked aisles and quiet background customers",
    "inside a retro video arcade with glowing machines and indistinct background players",
    "inside an aquarium tunnel with curved transparent walls, moving marine life, blue ambient light, and visitors in the distance",
    "in the open central aisle of a vintage cinema auditorium with upholstered seat rows, decorative walls, and a distant screen",
    "at a bowling-lane approach area with polished lanes, ball returns, scoring displays, and neighboring players",
    "inside an underground parking garage with concrete columns, painted bay markings, parked cars, and layered artificial light",
    "inside a spacious supermarket aisle with stocked shelves, shopping carts, overhead signs, and distant customers",
    "inside a music rehearsal room with instrument stands, amplifiers, acoustic panels, and loosely arranged equipment",
    "inside an observatory dome with a large telescope, curved mechanical structure, control equipment, and a partly open roof slit",
    "inside an archival reading room with long tables, document stands, storage cabinets, and quiet researchers",
    "inside a modern laboratory with glassware, analytical equipment, illuminated workbenches, and controlled technical order",
    "inside a professional radio studio with broadcast microphones, acoustic panels, mixing equipment, and a window into the control room",
    "inside a martial-arts dojo with padded flooring, simple training equipment, open practice space, and restrained wooden details",
    "inside a spacious Art Deco elevator with wood-and-brass wall panels, illuminated controls, a patterned floor, and closed sliding doors",
    "beside an indoor karting circuit with tire barriers, painted track markings, parked go-karts, and a broad industrial roof",
    "inside a spacious hospital treatment room with diagnostic monitors, articulated medical equipment, stainless carts, and clinical workstations in the background",
}

OUTDOOR_OR_SEMIOPEN_SCENARIOS = {
    "waiting on a train platform beside luggage, watching arriving passengers board",
    "bargaining with a market vendor at a busy open-air stall",
    "ordering from a busy street-food stall amid waiting customers",
    "inspecting an unusual object at a flea-market stall",
    "waiting at a bus stop among commuters watching approaching traffic",
    "relaxing at a rooftop gathering among a small group and distant city lights",
    BICYCLE_SCENARIO,
    HORSE_SCENARIO,
    CAROUSEL_SCENARIO,
    SKATEBOARD_SCENARIO,
}

DAYLIT_INTERIOR_SCENARIOS = {
    "standing at an airport baggage carousel, watching luggage pass",
    CAR_DRIVING_SCENARIO,
}

ENCLOSED_INTERIOR_SCENARIOS = {
    "seated at a casino gaming table, playing a hand of poker with an expression blending mischief and concentration",
    "standing at a retro arcade cabinet, hands on the controls and absorbed in a fast-paced game",
    "singing into a microphone in a karaoke bar, reacting to a small lively audience",
    "ordering at a busy café counter while staff prepare drinks behind the counter",
    "studying at a library table among open books, notes, and quiet nearby readers",
    "browsing a vinyl record in an independent record shop, carefully examining its sleeve",
    "dancing on a crowded party floor among moving guests and shifting lights",
    "seated in a tattoo studio, ready for an upcoming tattoo session, while a tattoo artist stands nearby holding a tattoo machine and preparing to begin, before any tattooing has started",
    "examining an artwork in a gallery among quiet visitors",
    "folding fresh laundry inside a neighborhood laundromat",
    "seated in a diner booth, engaged in lively conversation with companions",
    "singing into a studio microphone during rehearsal while the band remains nearby",
    "following through after releasing a bowling ball and watching it travel down the lane",
    "waiting backstage before a performance, sharing a mirror with other performers",
    "seated in a hair salon while a stylist works, with mirrors and quiet activity around them",
    "assembling a handmade object at a community workshop among other participants",
}

EXTERIOR_NATURAL_LIGHTING = {"golden-hour light", "overcast daylight"}
WINDOW_DEPENDENT_LIGHTING = {"window light"}


def environment_family(setting=None, scenario=None):
    if scenario:
        if scenario in OUTDOOR_OR_SEMIOPEN_SCENARIOS:
            return "outdoor"
        if scenario in DAYLIT_INTERIOR_SCENARIOS:
            return "daylit_interior"
        if scenario in ENCLOSED_INTERIOR_SCENARIOS:
            return "enclosed_interior"
    if setting in OUTDOOR_OR_SEMIOPEN_SETTINGS:
        return "outdoor"
    if setting in DAYLIT_INTERIOR_SETTINGS:
        return "daylit_interior"
    if setting in ENCLOSED_INTERIOR_SETTINGS:
        return "enclosed_interior"
    return "unknown"


def lighting_is_compatible(family, lighting):
    if family == "enclosed_interior":
        return lighting not in EXTERIOR_NATURAL_LIGHTING | WINDOW_DEPENDENT_LIGHTING
    if family == "outdoor":
        return lighting not in WINDOW_DEPENDENT_LIGHTING
    return True

BODY_CONTEXT_PORTRAIT_KEYS = {
    "pose", "bottom_type", "dress_type", "sleepwear_type", "cosplay_type",
    "cosplay_franchise_western", "cosplay_franchise_asian", "hosiery", "footwear",
}

# Ordinary Random footwear follows the probable visibility of feet rather than
# treating the broad word "portrait" as a crop. Pose supplies the strongest body
# clue, framing supplies the fallback, and vertical camera angle then modifies
# the result. This still leaves occasional model freedom, while preferring a
# completed outfit over accidental socks-only styling. Manual, Forced Random,
# franchise-authored footwear, and the universal text override bypass this gate.
FOOTWEAR_HARD_SUPPRESSION_FRAMINGS = {"close-up portrait", "headshot portrait"}
FOOTWEAR_FRAMING_PRESENCE_PERCENT = {
    "portrait": 60,
    "bust portrait": 15,
    "half-body portrait": 50,
    "three-quarter portrait": 75,
    "full-body portrait": 95,
}
DEFAULT_FOOTWEAR_RANDOM_PRESENCE_PERCENT = 60

FOOTWEAR_HIGH_VISIBILITY_POSES = {
    "balanced in a low squat, elbows resting loosely on the thighs, torso upright",
    "compact low squat, arms wrapped around the knees, shoulders slightly rounded",
    "low crouching pose, one hand planted on the floor, the other resting on the thigh",
    "low side squat, torso upright",
    "kneeling and leaning forward, palms resting on the floor in front",
    "on hands and knees with the back mostly straight",
    "on hands and knees with the weight shifted onto one arm",
    "on hands and knees with a gentle arch through the lower back and the shoulders lowered",
    "on hands and knees with one knee drawn forward between the hands and the torso gently twisted",
    "kneeling with forearms resting on the floor, hips raised, and the back gently curved",
    "lying on the stomach, upper body lifted on the elbows, both lower legs raised behind",
    "reclining on one side in a gentle S-curve, upper body supported by one forearm, upper knee drawn forward",
    "lying on the back with the legs comfortably spread apart and the arms resting naturally",
    "lying on the side with the head supported by one hand and the legs relaxed",
    "lying on the back with one knee bent and the other leg extended",
    "lying on the stomach with the upper body gently raised on the forearms",
    "lying curled slightly on one side with the knees loosely drawn upward",
    "reclining on the back with both knees bent and the feet resting on the supporting surface",
}

FOOTWEAR_MEDIUM_VISIBILITY_POSES = {
    "bending forward with both hands resting above the knees",
    "seated upright with legs crossed, one hand resting on the upper knee",
    "perched on the edge of a chair, knees together, torso leaning forward slightly, hands resting on the thighs",
    "seated with one knee raised toward the chest, arms loosely wrapped around the leg",
    "seated on the edge of a stool with one hand braced behind",
    "sitting low with knees comfortably apart, elbows resting on the thighs, shoulders slightly forward",
    "kneeling with hips resting on the heels, hands placed on the thighs, upright elegant posture",
    "kneeling on one knee with the other knee raised, forearm resting across the raised thigh",
    "kneeling upright with both hands behind the head, elbows open, hips shifted slightly to one side",
    "caught mid-spin while dancing, torso and arms turning dynamically",
}

FOOTWEAR_LOW_VISIBILITY_POSES = set()

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


def _insert_unique(values, additions, after=None):
    result = [value for value in values if value not in additions]
    index = result.index(after) + 1 if after in result else len(result)
    result[index:index] = list(additions)
    return result


def _extend_clothing_schema(schema):
    """Replace abstract styling with concrete, manually reachable garments."""
    categories = schema.setdefault("categories", [])
    # Preserve old workflow positions in the frontend migration map, but remove
    # the obsolete backend widget and therefore all prompt influence.
    categories[:] = [item for item in categories if item.get("key") != "outfit_style"]
    by_key = {item.get("key"): item for item in categories}

    for key, additions in CLOTHING_SCHEMA_ADDITIONS.items():
        item = by_key.get(key)
        if not item:
            continue
        item["values"] = _insert_unique(item.get("values", []), additions)

    dress = by_key.get("dress_type")
    if dress:
        dress["label"] = "Dress / complete outfit"

    # Outfit Style pools are intentionally discarded. Their former ideas now
    # materialize through visible concrete garments in the relevant recipes.
    for config in CLOTHING_ARCHETYPE_CONFIG.values():
        config.pop("outfit_style", None)
    for archetype, additions_by_field in CLOTHING_ARCHETYPE_ENRICHMENTS.items():
        config = CLOTHING_ARCHETYPE_CONFIG.get(archetype)
        if not config:
            continue
        for key, additions in additions_by_field.items():
            config[key] = _insert_unique(config.get(key, []), additions)
    return schema


def _extend_body_morphology_schema(schema):
    """Add the V3 body model without requiring a replacement categories.json."""
    categories = schema.setdefault("categories", [])
    by_key = {item.get("key"): item for item in categories}

    curves = by_key.get("body_feminine_curves")
    if curves:
        curves["label"] = "Body feminine curves / Body shape"
        legacy_details = {
            "short-legged proportions",
            "long-legged proportions",
            "pronounced inward lumbar curve with a deeply arched lower-back silhouette",
            "pronounced lumbar lordosis, with a deeply concave lower back, the abdomen projecting forward, and the pelvis tilted so the buttocks project prominently backward",
        }
        curves["values"] = [value for value in curves.get("values", []) if value not in legacy_details]
        curves["values"] = _insert_unique(
            curves["values"],
            ["soft curves", "very pronounced curves"],
            after="balanced curves",
        )

    bust = by_key.get("bust")
    if bust:
        bust["values"] = _insert_unique(
            bust.get("values", []), ["very full projected bust"], after="very large bust"
        )
        bust["values"] = _insert_unique(
            bust["values"],
            ["full rounded bust with natural forward projection"],
            after="full bust",
        )

    butt = by_key.get("butt_shape")
    if butt:
        butt["values"] = _insert_unique(
            butt.get("values", []), ["prominent rounded glutes"], after="soft rounded glutes"
        )

    physique = by_key.get("body_physique")
    if physique:
        physique["values"] = _insert_unique(
            physique.get("values", []),
            ["naturally extremely slender, fine-boned underweight physique"],
            after="extremely underweight physique",
        )

    thighs = by_key.get("thigh_shape")
    if thighs:
        thighs["values"] = _insert_unique(
            thighs.get("values", []),
            ["extremely slender straight legs with narrow thighs and calves"],
            after="very slim thighs",
        )
        thighs["values"] = _insert_unique(
            thighs["values"],
            ["soft thick thighs", "very thick soft thighs"],
            after="full thighs",
        )

    body_archetype = by_key.get("body_archetype")
    if body_archetype:
        body_archetype["values"] = list(BODY_ARCHETYPE_VALUES)
    else:
        insert_at = next(
            (index for index, item in enumerate(categories) if item.get("key") == "body_type"),
            len(categories),
        )
        categories.insert(insert_at, {
            "key": "body_archetype",
            "label": "Body Archetype",
            "default": "None",
            "values": list(BODY_ARCHETYPE_VALUES),
        })

    by_key = {item.get("key"): item for item in categories}
    insert_at = next(
        (index + 1 for index, item in enumerate(categories) if item.get("key") == "thigh_shape"),
        len(categories),
    )
    for offset, detail_key in enumerate(BODY_DETAIL_KEYS):
        detail = by_key.get(detail_key)
        if detail:
            detail["values"] = list(BODY_DETAIL_VALUES)
            continue
        categories.insert(insert_at + offset, {
            "key": detail_key,
            "label": f"Body Detail {offset + 1}",
            "default": "None",
            "values": list(BODY_DETAIL_VALUES),
        })
    return schema


def _extend_composition_archetype_schema(schema):
    categories = schema["categories"]
    existing = next(
        (item for item in categories if item.get("key") == "composition_archetype"),
        None,
    )
    if existing:
        existing["values"] = list(COMPOSITION_ARCHETYPE_VALUES)
        return schema
    insert_at = next(
        (index for index, item in enumerate(categories) if item.get("key") == "portrait_style"),
        0,
    )
    categories.insert(insert_at, {
        "key": "composition_archetype",
        "label": "Composition Archetype",
        "default": "None",
        "values": list(COMPOSITION_ARCHETYPE_VALUES),
    })
    return schema


def load_schema():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
    schema = _extend_clothing_schema(schema)
    schema = _extend_body_morphology_schema(schema)
    return _extend_composition_archetype_schema(schema)


SCHEMA = load_schema()


def _validate_composition_archetypes():
    by_key = {item["key"]: item for item in SCHEMA["categories"]}
    if len(COMPOSITION_ARCHETYPE_VALUES) != 50:
        raise RuntimeError("Composition Archetype catalogue must contain exactly 50 entries")
    if set(COMPOSITION_ARCHETYPE_VALUES) != set(COMPOSITION_ARCHETYPE_CONFIG):
        raise RuntimeError("Composition Archetype names and configuration keys do not match")

    allowed_by_field = {
        key: set(by_key[key]["values"])
        for key in COMPOSITION_ARCHETYPE_CONTROL_FIELDS
        if key != "eye_focus"
    }
    allowed_by_field["eye_focus"] = set(EYE_FOCUS_VALUES)
    allowed_by_field["pose"].add(None)
    covered_poses = set()
    for archetype, config in COMPOSITION_ARCHETYPE_CONFIG.items():
        if set(config) != COMPOSITION_ARCHETYPE_CONTROL_FIELDS:
            raise RuntimeError(f"Incomplete Composition Archetype profile: {archetype}")
        for field, values in config.items():
            if not values:
                raise RuntimeError(f"Empty {field} pool in Composition Archetype: {archetype}")
            unknown = set(values) - allowed_by_field[field]
            if unknown:
                raise RuntimeError(
                    f"Hidden vocabulary in Composition Archetype {archetype}/{field}: {sorted(unknown)!r}"
                )
        covered_poses.update(value for value in config["pose"] if value)
    missing_poses = set(by_key["pose"]["values"]) - covered_poses
    if missing_poses:
        raise RuntimeError(f"Composition Archetypes do not cover Pose values: {sorted(missing_poses)!r}")


_validate_composition_archetypes()


def _validate_environment_metadata():
    by_key = {item["key"]: item for item in SCHEMA["categories"]}
    setting_values = set(by_key["setting"]["values"])
    scenario_values = set(by_key["scene_scenario"]["values"])
    setting_groups = (
        OUTDOOR_OR_SEMIOPEN_SETTINGS,
        DAYLIT_INTERIOR_SETTINGS,
        ENCLOSED_INTERIOR_SETTINGS,
    )
    scenario_groups = (
        OUTDOOR_OR_SEMIOPEN_SCENARIOS,
        DAYLIT_INTERIOR_SCENARIOS,
        ENCLOSED_INTERIOR_SCENARIOS,
    )
    classified_settings = set().union(*setting_groups)
    classified_scenarios = set().union(*scenario_groups)
    if classified_settings != setting_values:
        raise RuntimeError(
            "Environment metadata mismatch for Setting: "
            f"missing={sorted(setting_values - classified_settings)!r}, "
            f"unknown={sorted(classified_settings - setting_values)!r}"
        )
    if classified_scenarios != scenario_values:
        raise RuntimeError(
            "Environment metadata mismatch for Scene scenario: "
            f"missing={sorted(scenario_values - classified_scenarios)!r}, "
            f"unknown={sorted(classified_scenarios - scenario_values)!r}"
        )
    if sum(len(group) for group in setting_groups) != len(classified_settings):
        raise RuntimeError("A Setting belongs to more than one environment family")
    if sum(len(group) for group in scenario_groups) != len(classified_scenarios):
        raise RuntimeError("A Scene scenario belongs to more than one environment family")


_validate_environment_metadata()


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


def deduplicate_hair_descriptors(items):
    """Remove only true wording duplicates while preserving distinct hair traits."""
    output = []
    positions = {}
    for value in items:
        if not value:
            continue
        normalized = re.sub(r"\bhair\b", "", str(value).lower())
        normalized = re.sub(r"[^a-z0-9]+", " ", normalized).strip()
        if normalized in positions:
            index = positions[normalized]
            # Prefer the self-contained wording (for example
            # "shoulder-length hair" over the imported shorthand
            # "shoulder-length") without moving it in the sentence.
            if re.search(r"\bhair\b", str(value), flags=re.IGNORECASE) and not re.search(
                r"\bhair\b", str(output[index]), flags=re.IGNORECASE
            ):
                output[index] = value
            continue
        positions[normalized] = len(output)
        output.append(value)
    return output


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
    DESCRIPTION = "A character prompt builder with high ethnicity adherence for Krea 2, deterministic conflict-aware randomization, and optional Identity Forge JSON compatibility."
    FUNCTION = "build_prompt"
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("Prompt", "Face Prompt", "Inspected Value", "Pre-gen Text")

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
            "enforce_portrait_framing": ("BOOLEAN", {"default": False, "label_on": "Activated", "label_off": "Deactivated", "tooltip": OPTIONAL_TOOLTIPS["enforce_portrait_framing"]}),
            "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "tooltip": OPTIONAL_TOOLTIPS["seed"]}),
            "control_after_generate": (["fixed", "increment", "decrement", "randomize"], {"default": "randomize", "tooltip": OPTIONAL_TOOLTIPS["control_after_generate"]}),
            "free_prompt": ("STRING", {"default": "", "multiline": True, "dynamicPrompts": False, "tooltip": OPTIONAL_TOOLTIPS["free_prompt"]}),
            "free_prompt_position": (["After introduction", "After makeup", "At end"], {"default": "After introduction", "tooltip": OPTIONAL_TOOLTIPS["free_prompt_position"]}),
            "override_field": (["None"] + [item["key"] for item in SCHEMA["categories"]], {"default": "None", "tooltip": OPTIONAL_TOOLTIPS["override_field"]}),
            "override_text": ("STRING", {"forceInput": True, "tooltip": OPTIONAL_TOOLTIPS["override_text"]}),
            "identity_forge_json": ("STRING", {"forceInput": True, "tooltip": OPTIONAL_TOOLTIPS["identity_forge_json"]}),
            "inspect_property": (["None"] + [item["key"] for item in SCHEMA["categories"]], {"default": "None", "tooltip": OPTIONAL_TOOLTIPS["inspect_property"]}),
            "eye_focus": (["None", "Random", "Forced Random"] + EYE_FOCUS_VALUES, {"default": "None", "tooltip": OPTIONAL_TOOLTIPS["eye_focus"]}),
            "mouth_expression": (["None", "Random", "Forced Random"] + MOUTH_EXPRESSION_VALUES, {"default": "None", "tooltip": OPTIONAL_TOOLTIPS["mouth_expression"]}),
            "setting_text_override": ("STRING", {"default": "", "multiline": True, "dynamicPrompts": False, "tooltip": OPTIONAL_TOOLTIPS["setting_text_override"]}),
            "pose_text_override": ("STRING", {"default": "", "multiline": True, "dynamicPrompts": False, "tooltip": OPTIONAL_TOOLTIPS["pose_text_override"]}),
            "face_hair_text_override": ("STRING", {"default": "", "multiline": True, "dynamicPrompts": False, "tooltip": OPTIONAL_TOOLTIPS["face_hair_text_override"]}),
            "custom_color_overrides": ("STRING", {"default": "", "multiline": True, "dynamicPrompts": False, "tooltip": OPTIONAL_TOOLTIPS["custom_color_overrides"]}),
            "wildcard_subject": ("STRING", {"default": "", "multiline": False, "dynamicPrompts": True, "tooltip": OPTIONAL_TOOLTIPS["wildcard_subject"]}),
            "wildcard_clothing": ("STRING", {"default": "", "multiline": False, "dynamicPrompts": True, "tooltip": OPTIONAL_TOOLTIPS["wildcard_clothing"]}),
            "wildcard_pose": ("STRING", {"default": "", "multiline": False, "dynamicPrompts": True, "tooltip": OPTIONAL_TOOLTIPS["wildcard_pose"]}),
            "wildcard_setting": ("STRING", {"default": "", "multiline": False, "dynamicPrompts": True, "tooltip": OPTIONAL_TOOLTIPS["wildcard_setting"]}),
            "wildcard_photography": ("STRING", {"default": "", "multiline": False, "dynamicPrompts": True, "tooltip": OPTIONAL_TOOLTIPS["wildcard_photography"]}),
        }
        return {"required": required, "optional": optional}

    def _resolve_values(self, kwargs, seed=0, ethnicity_guidance=False, eye_focus="None"):
        raw = {item["key"]: kwargs.get(item["key"], "None") for item in SCHEMA["categories"]}

        legacy_selfie = (
            raw.get("capture_style") == SELFIE_CAPTURE_STYLE
            or raw.get("portrait_style") in {"spontaneous handheld selfie", "bedroom selfie"}
        )

        legacy_ethnicity = raw.get("origin_ethnicity")
        if legacy_ethnicity in LEGACY_ETHNICITY_MAP:
            mapped = LEGACY_ETHNICITY_MAP[legacy_ethnicity]
            raw["origin_ethnicity"] = mapped if mapped else "None"

        legacy_portrait_style = raw.get("portrait_style")
        if raw.get("capture_style") in (None, "None") and legacy_portrait_style in LEGACY_CAPTURE_STYLE_BY_PORTRAIT:
            raw["capture_style"] = LEGACY_CAPTURE_STYLE_BY_PORTRAIT[legacy_portrait_style]
        if legacy_portrait_style in LEGACY_PORTRAIT_STYLE_MAP:
            raw["portrait_style"] = LEGACY_PORTRAIT_STYLE_MAP[legacy_portrait_style]
        if legacy_selfie:
            raw["capture_style"] = "candid"
            if raw.get("pose") in (None, "None", "Random"):
                raw["pose"] = SELFIE_POSE

        # Five context-dependent actions used to live in Pose. Preserve old
        # workflows by migrating them into the enriched Scene scenario form,
        # where the required vehicle, mount, or activity environment is explicit.
        legacy_action_scenario = LEGACY_ACTION_POSE_TO_SCENARIO.get(raw.get("pose"))
        if legacy_action_scenario and raw.get("scene_scenario") in (None, "None", "Random"):
            raw["scene_scenario"] = legacy_action_scenario
            raw["pose"] = "None"

        # Ordinary Random scenario is intentionally subordinate to a deliberate
        # Pose, Setting, or Composition Archetype. Forced Random and manual
        # scenarios remain authoritative.
        if raw.get("scene_scenario") == "Random" and any(
            self._is_authoritative_selection(raw.get(key)) for key in ("pose", "setting")
        ):
            raw["scene_scenario"] = "None"
        if (
            raw.get("scene_scenario") == "Random"
            and self._is_authoritative_selection(raw.get("composition_archetype"))
        ):
            raw["scene_scenario"] = "None"

        # V20 and older mixed height, weight, and silhouette in Body type. Move
        # the old semantic information into the new independent controls before
        # applying the simple value aliases below.
        old_body_type = raw.get("body_type")
        if raw.get("body_physique") in (None, "None"):
            physique_from_old_type = {
                "slim": "slim physique", "slender": "slim physique", "lanky": "very slim physique",
                "voluptuous": "plump physique", "plus-size": "plus-size physique",
                "stocky": "soft untrained physique", "broad-built": "muscular physique",
            }.get(old_body_type)
            if physique_from_old_type:
                raw["body_physique"] = physique_from_old_type
        if raw.get("body_feminine_curves") in (None, "None"):
            curves_from_old_type = {
                "voluptuous": "pronounced hourglass silhouette",
                "tall curvy": "pronounced hourglass silhouette",
                "androgynous": "androgynous silhouette",
            }.get(old_body_type)
            if curves_from_old_type:
                raw["body_feminine_curves"] = curves_from_old_type

        # Leg proportions and lumbar curvature used to occupy Body curves (and,
        # in older releases, Body type). Move them into the first free Body
        # Detail slot while leaving every newer explicit detail untouched.
        legacy_body_detail = {
            "short-legged": "short-legged proportions",
            "short-legged proportions": "short-legged proportions",
            "long-legged": "long-legged proportions",
            "long-legged proportions": "long-legged proportions",
            "pronounced inward lumbar curve with a deeply arched lower-back silhouette": "pronounced inward lumbar curve",
            "pronounced lumbar lordosis, with a deeply concave lower back, the abdomen projecting forward, and the pelvis tilted so the buttocks project prominently backward": "pronounced inward lumbar curve",
        }.get(raw.get("body_feminine_curves"))
        if not legacy_body_detail:
            legacy_body_detail = {
                "short-legged": "short-legged proportions",
                "short-legged proportions": "short-legged proportions",
                "long-legged": "long-legged proportions",
                "long-legged proportions": "long-legged proportions",
            }.get(old_body_type)
        if legacy_body_detail:
            for detail_key in BODY_DETAIL_KEYS:
                if raw.get(detail_key) in (None, "None"):
                    raw[detail_key] = legacy_body_detail
                    break
            if raw.get("body_feminine_curves") in {
                "short-legged proportions",
                "long-legged proportions",
                "pronounced inward lumbar curve with a deeply arched lower-back silhouette",
                "pronounced lumbar lordosis, with a deeply concave lower back, the abdomen projecting forward, and the pelvis tilted so the buttocks project prominently backward",
            }:
                raw["body_feminine_curves"] = "None"

        # Preserve the spatial intent formerly buried inside legacy Pose and
        # Camera direction values. These cross-field migrations run only when
        # the new dedicated axis has not already been selected.
        legacy_pose = raw.get("pose")
        if raw.get("camera_direction") in (None, "None"):
            if legacy_pose == "on hands and knees viewed from a rear three-quarter angle, hips angled toward the camera, looking back over one shoulder":
                raw["camera_direction"] = "rear three-quarter view"
            elif legacy_pose in {
                "standing with the back partly turned, looking over one shoulder, hips shifted softly to one side",
                "standing in a three-quarter pose, one hand in the hair, hips turned away",
                "sitting sideways on a stool, upper body twisting toward the camera, one hand braced behind",
            }:
                raw["camera_direction"] = "three-quarter view"
        if raw.get("head_direction") in (None, "None"):
            if legacy_pose in {
                "standing with the back partly turned, looking over one shoulder, hips shifted softly to one side",
                "on hands and knees viewed from a rear three-quarter angle, hips angled toward the camera, looking back over one shoulder",
            }:
                raw["head_direction"] = "looking back over one shoulder"
            elif "toward the camera" in str(legacy_pose or ""):
                raw["head_direction"] = "head held level"

        legacy_camera_direction = raw.get("camera_direction")
        if raw.get("head_direction") in (None, "None"):
            raw["head_direction"] = LEGACY_CATEGORY_VALUE_MAPS["head_direction"].get(legacy_camera_direction, raw.get("head_direction"))
        if raw.get("camera_angle") in (None, "None"):
            raw["camera_angle"] = LEGACY_CATEGORY_VALUE_MAPS["camera_angle"].get(legacy_camera_direction, raw.get("camera_angle"))
        if legacy_camera_direction == "front-facing symmetrical view" and raw.get("shot_composition") in (None, "None", "Random"):
            raw["shot_composition"] = "symmetrical composition"
        legacy_composition = raw.get("shot_composition")
        if legacy_composition == "tight crop" and raw.get("portrait_style") in (None, "None", "Random", "portrait"):
            raw["portrait_style"] = "close-up portrait"
        elif legacy_composition == "wide framing" and raw.get("portrait_style") in (None, "None", "Random", "portrait"):
            raw["portrait_style"] = "full-body portrait"

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

        body_archetype_item = schema_by_key.get("body_archetype")
        selected_body_archetype = raw.get("body_archetype", "None")
        if selected_body_archetype in ("Random", "Forced Random") and body_archetype_item and body_archetype_item["values"]:
            resolved_body_archetype = stable_choice(
                seed, "body_archetype", body_archetype_item["values"]
            )
        elif selected_body_archetype in (None, "None"):
            resolved_body_archetype = None
        else:
            resolved_body_archetype = selected_body_archetype
        body_archetype_config = BODY_ARCHETYPE_CONFIG.get(resolved_body_archetype, {})

        composition_archetype_item = schema_by_key.get("composition_archetype")
        selected_composition_archetype = raw.get("composition_archetype", "None")
        if (
            selected_composition_archetype in ("Random", "Forced Random")
            and composition_archetype_item
            and composition_archetype_item["values"]
        ):
            resolved_composition_archetype = stable_choice(
                seed,
                "composition_archetype",
                composition_archetype_item["values"],
            )
        elif selected_composition_archetype in (None, "None"):
            resolved_composition_archetype = None
        else:
            resolved_composition_archetype = selected_composition_archetype

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
            if forced_modes:
                mode_pool = forced_modes
            else:
                mode_pool = [
                    mode
                    for mode in random_modes
                    for _ in range(DEFAULT_CLOTHING_MODE_WEIGHTS.get(mode, 1))
                ]
            chosen_mode = stable_choice(seed, "__clothing_mode__", mode_pool)
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
        # costumes suppress random heavy garment additions, while
        # their signature colors and equipment (for example purple platform
        # boots on Padmé). Suppress only random secondary additions. Explicit
        # manual selections remain available for intentional customization.
        generic_cosplay_mode_active = raw.get("cosplay_type") not in (None, "None")
        franchise_mode_active = any(
            raw.get(key) not in (None, "None")
            for key in ("cosplay_franchise_western", "cosplay_franchise_asian")
        )
        franchise_random_suppressed_keys = {
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
            if key == "body_archetype":
                resolved[key] = resolved_body_archetype
                continue
            if key == "composition_archetype":
                resolved[key] = resolved_composition_archetype
                continue
            if key == "clothing_archetype":
                resolved[key] = resolved_archetype
                continue
            if key in BODY_DETAIL_KEYS:
                # The three shared-vocabulary slots are resolved together after
                # the generic pass so ordinary/archetype Random can avoid using
                # two contradictory values from the same morphological axis.
                resolved[key] = None
                continue

            selected = raw.get(key, "None")
            if key == "scene_scenario" and selected == "Random":
                # Scene scenario is an alternative branch, not an always-on
                # master layer. An ordinary Random draw chooses a complete
                # scenario ten percent of the time and otherwise keeps the
                # classic Pose + Setting pair.
                use_scenario = stable_choice(
                    seed,
                    "scene_scenario__branch__",
                    [False] * 9 + [True],
                )
                resolved[key] = stable_choice(seed, key, item["values"]) if use_scenario else None
            elif (
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
            elif (
                resolved_body_archetype
                and key in BODY_ARCHETYPE_CONTROL_FIELDS
                and key in body_archetype_config
                and selected in (None, "None", "Random")
            ):
                resolved[key] = stable_choice(seed, key, body_archetype_config[key])
            elif selected == "None":
                resolved[key] = None
            elif selected == "Random":
                if key == "optical_effect":
                    resolved[key] = stable_choice(seed, key, OPTICAL_EFFECT_RANDOM_POOL)
                elif key == "body_type":
                    resolved[key] = stable_choice(seed, key, BODY_HEIGHT_CLASSIC_RANDOM_POOL)
                elif key == "body_physique":
                    family = stable_choice(seed, f"{key}__family__", BODY_PHYSIQUE_RANDOM_FAMILIES)
                    resolved[key] = stable_choice(seed, key, BODY_PHYSIQUE_RANDOM_VALUES[family])
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

        self._resolve_body_details(
            raw,
            resolved,
            seed,
            schema_by_key,
            body_archetype_config,
        )

        # A scenario is a complete action/environment unit. It deliberately
        # replaces the two independent axes instead of stacking three scenes.
        # Apply this before geometry coherence so a discarded random Pose does
        # not silently steer camera choices for the winning scenario branch.
        if resolved.get("scene_scenario"):
            resolved["pose"] = None
            resolved["setting"] = None

        # Full-body jumpsuits are complete base garments. Ordinary Random tops
        # stand down; manual and Forced Random tops remain deliberate layers.
        if (
            resolved.get("bottom_type") in FULL_BODY_ONE_PIECE_BOTTOM_TYPES
            and raw.get("top_type") == "Random"
        ):
            resolved["top_type"] = None
            if raw.get("top_color") == "Random":
                resolved["top_color"] = None

        self._apply_soft_random_coherence(raw, resolved, seed, schema_by_key)
        self._apply_scene_geometry_coherence(raw, resolved, seed, schema_by_key)

        # A complete Scene scenario has its own action and geometry grammar.
        # Otherwise the Composition Archetype replaces only None/ordinary
        # Random fields after the classic coherence pass, so Capture style can
        # still guide independent lens and lighting choices without redrawing
        # the archetype's final composition.
        if resolved.get("scene_scenario"):
            resolved["composition_archetype"] = None
        elif resolved_composition_archetype:
            self._apply_composition_archetype(
                raw,
                resolved,
                seed,
                selected_eye_focus=eye_focus,
            )

        # Ordinary Random nails should never fight a costume that fully covers
        # the hands. Manual nail choices remain authoritative, and Forced Random
        # deliberately keeps its documented rule-bypassing behavior.
        if raw.get("nail_style") == "Random" and self._has_full_hand_covering(resolved):
            resolved["nail_style"] = None

        if raw.get("footwear") == "Random":
            percent = self._footwear_random_presence_percent(resolved)
            keep_footwear = stable_choice(
                seed, "footwear__visibility_presence", [False] * (100 - percent) + [True] * percent
            ) if percent else False
            if not keep_footwear:
                resolved["footwear"] = None
                if raw.get("footwear_color") == "Random":
                    resolved["footwear_color"] = None
        self._apply_environment_lighting_coherence(raw, resolved, seed, schema_by_key)
        return resolved

    @staticmethod
    def _resolve_body_details(raw, resolved, seed, schema_by_key, archetype_config):
        """Resolve the shared detail slots with explicit precedence and soft coherence."""
        source_values = schema_by_key.get("body_detail_1", {}).get("values", BODY_DETAIL_VALUES)
        used_values = set()
        used_axes = set()

        # Manual and Forced Random are resolved first and never rewritten.
        # Forced Random intentionally draws without conflict filtering.
        for key in BODY_DETAIL_KEYS:
            selected = raw.get(key, "None")
            if selected == "Forced Random":
                value = stable_choice(seed, key, source_values)
            elif selected not in (None, "None", "Random"):
                value = selected
            else:
                continue
            resolved[key] = value
            if value:
                used_values.add(value)
                axis = BODY_DETAIL_AXES.get(value)
                if axis:
                    used_axes.add(axis)

        archetype_pool = list(archetype_config.get("body_details", []))
        for key in BODY_DETAIL_KEYS:
            selected = raw.get(key, "None")
            if selected not in (None, "None", "Random"):
                continue

            preferred = archetype_pool if archetype_pool else []
            candidates = [
                value for value in preferred
                if value not in used_values
                and BODY_DETAIL_AXES.get(value) not in used_axes
            ]
            if not candidates and selected == "Random":
                # Ordinary Random remains able to reach every manually exposed
                # detail, even when no archetype candidate survives the occupied axes.
                candidates = [
                    value for value in source_values
                    if value not in used_values
                    and BODY_DETAIL_AXES.get(value) not in used_axes
                ]
            value = stable_choice(seed, f"{key}__coherent", candidates) if candidates else None
            resolved[key] = value
            if value:
                used_values.add(value)
                axis = BODY_DETAIL_AXES.get(value)
                if axis:
                    used_axes.add(axis)

    @staticmethod
    def _footwear_random_presence_percent(resolved):
        framing = resolved.get("portrait_style")
        if framing in FOOTWEAR_HARD_SUPPRESSION_FRAMINGS:
            return 0

        percent = FOOTWEAR_FRAMING_PRESENCE_PERCENT.get(
            framing, DEFAULT_FOOTWEAR_RANDOM_PRESENCE_PERCENT
        )
        pose = resolved.get("pose")
        if pose in FOOTWEAR_HIGH_VISIBILITY_POSES:
            percent = max(percent, 90)
        elif pose in FOOTWEAR_MEDIUM_VISIBILITY_POSES:
            percent = max(percent, 70)
        elif pose in FOOTWEAR_LOW_VISIBILITY_POSES:
            percent = min(percent, 10)

        hosiery = resolved.get("hosiery")
        if hosiery and hosiery != "bare legs":
            percent = min(98, percent + 5)

        angle = resolved.get("camera_angle")
        if angle == "from a pronounced low angle, with the camera positioned below the subject":
            percent = min(percent, 8)
        elif angle == "from an extreme worm's-eye angle at ground level, with the camera looking sharply upward":
            percent = max(percent, 90)
        elif angle == "from a pronounced high angle, with the camera positioned above the subject":
            percent = min(98, percent + 20)
        elif angle == "from an overhead bird's-eye angle, with the camera looking straight down":
            percent = max(percent, 90)
        return max(0, min(100, percent))

    def _apply_composition_archetype(self, raw, resolved, seed, selected_eye_focus="None"):
        """Resolve one coherent composition recipe around authoritative anchors.

        Manual and Forced Random values are anchors.  Only None and ordinary
        Random fields are supplied by the archetype.  Reconciliation may redraw
        another archetype-owned field, but never an explicit one.
        """

        archetype = resolved.get("composition_archetype")
        config = COMPOSITION_ARCHETYPE_CONFIG.get(archetype)
        if not config:
            return

        selected_by_field = {
            field: selected_eye_focus if field == "eye_focus" else raw.get(field, "None")
            for field in COMPOSITION_ARCHETYPE_CONTROL_FIELDS
        }
        owned = {
            field
            for field, selected in selected_by_field.items()
            if selected in (None, "None", "Random")
        }

        # Eye Focus is an optional widget resolved later in the public build
        # path.  Materialize an authoritative value here as an anchor so the
        # archetype can already orient an owned head around it.
        if "eye_focus" not in owned:
            if selected_eye_focus == "Forced Random":
                resolved["eye_focus"] = stable_choice(
                    seed, "eye_focus__forced", EYE_FOCUS_VALUES
                )
            elif selected_eye_focus not in (None, "", "None", "Random"):
                resolved["eye_focus"] = selected_eye_focus

        for field in (
            "pose", "portrait_style", "camera_direction", "camera_angle",
            "shot_composition", "head_direction", "eye_focus",
        ):
            if field in owned:
                resolved[field] = stable_choice(
                    seed,
                    f"composition_archetype__{archetype}__{field}",
                    config[field],
                )

        # An explicit pose becomes the mechanical anchor.  If the archetype
        # owns framing, keep enough of the body visible for that pose.
        pose = resolved.get("pose")
        framing = resolved.get("portrait_style")
        if "portrait_style" in owned:
            if pose in FULL_SCENE_POSES:
                compatible = [
                    value for value in config["portrait_style"]
                    if value in {"three-quarter portrait", "full-body portrait"}
                ] or ["three-quarter portrait", "full-body portrait", "full-body portrait"]
                resolved["portrait_style"] = stable_choice(
                    seed, f"composition_archetype__{archetype}__pose_visible_framing", compatible
                )
            elif pose in UPPER_BODY_POSES:
                compatible = [
                    value for value in config["portrait_style"]
                    if value in {"bust portrait", "half-body portrait", "three-quarter portrait"}
                ] or ["bust portrait", "half-body portrait", "three-quarter portrait"]
                resolved["portrait_style"] = stable_choice(
                    seed, f"composition_archetype__{archetype}__upper_body_framing", compatible
                )
            elif pose in MID_BODY_POSES:
                compatible = [
                    value for value in config["portrait_style"]
                    if value in {"half-body portrait", "three-quarter portrait", "full-body portrait"}
                ] or ["half-body portrait", "three-quarter portrait", "full-body portrait"]
                resolved["portrait_style"] = stable_choice(
                    seed, f"composition_archetype__{archetype}__mid_body_framing", compatible
                )

        # Conversely, an explicit close crop prevents an archetype-owned pose
        # from injecting invisible lower-body mechanics.
        framing = resolved.get("portrait_style")
        if "pose" in owned and "portrait_style" not in owned:
            if framing in CLOSE_FRAMINGS:
                resolved["pose"] = None
            elif framing == "bust portrait" and resolved.get("pose") not in UPPER_BODY_POSES:
                compatible = [value for value in config["pose"] if value in UPPER_BODY_POSES]
                resolved["pose"] = stable_choice(
                    seed, f"composition_archetype__{archetype}__bust_pose", compatible
                ) if compatible else None

        # An explicit horizontal view guides an archetype-owned pose.  A
        # front-facing manual camera should not receive an intrinsically
        # side-oriented floor pose merely because of the selected family.
        direction = resolved.get("camera_direction")
        if (
            "pose" in owned
            and "camera_direction" not in owned
            and direction == "front-facing view"
            and resolved.get("pose") in SIDE_ORIENTED_POSES
        ):
            compatible = [value for value in config["pose"] if value not in SIDE_ORIENTED_POSES]
            resolved["pose"] = stable_choice(
                seed, f"composition_archetype__{archetype}__front_readable_pose", compatible
            ) if compatible else None

        # Camera height and placement are independent axes, but pulling both in
        # the same vertical direction is a known hard conflict.  Redraw only an
        # archetype-owned side of the pair.
        angle = resolved.get("camera_angle")
        placement = resolved.get("shot_composition")
        conflict = (
            (angle in HIGH_CAMERA_ANGLES and placement == HIGH_FRAME_PLACEMENT)
            or (angle in LOW_CAMERA_ANGLES and placement == LOW_FRAME_PLACEMENT)
        )
        if conflict and "shot_composition" in owned:
            incompatible = HIGH_FRAME_PLACEMENT if angle in HIGH_CAMERA_ANGLES else LOW_FRAME_PLACEMENT
            compatible = [value for value in config["shot_composition"] if value != incompatible]
            resolved["shot_composition"] = stable_choice(
                seed, f"composition_archetype__{archetype}__vertical_placement", compatible
            )
        elif conflict and "camera_angle" in owned:
            incompatible_angles = HIGH_CAMERA_ANGLES if placement == HIGH_FRAME_PLACEMENT else LOW_CAMERA_ANGLES
            compatible = [value for value in config["camera_angle"] if value not in incompatible_angles]
            resolved["camera_angle"] = stable_choice(
                seed, f"composition_archetype__{archetype}__vertical_angle", compatible
            ) if compatible else EYE_LEVEL_ANGLE

        # Rear views require a head turn before the eyes can engage the camera.
        # If the head is explicit and does not turn back, an archetype-owned
        # focus yields instead of rewriting that explicit anatomy.
        direction = resolved.get("camera_direction")
        focus = resolved.get("eye_focus")
        near_camera = focus in {DIRECT_EYE_FOCUS, PAST_CAMERA_FOCUS}
        if direction == "rear three-quarter view" and near_camera:
            if "head_direction" in owned:
                resolved["head_direction"] = "looking back over one shoulder"
            elif resolved.get("head_direction") != "looking back over one shoulder" and "eye_focus" in owned:
                resolved["eye_focus"] = stable_choice(
                    seed,
                    f"composition_archetype__{archetype}__rear_away_focus",
                    [DISTANCE_FOCUS, LEFT_FOCUS, RIGHT_FOCUS],
                )
        elif direction != "rear three-quarter view" and resolved.get("head_direction") == "looking back over one shoulder" and "head_direction" in owned:
            compatible = [value for value in config["head_direction"] if value != "looking back over one shoulder"]
            resolved["head_direction"] = stable_choice(
                seed, f"composition_archetype__{archetype}__forward_head", compatible
            ) if compatible else "head held level"

        # Direct camera focus finally binds head pitch to an elevated or lowered
        # camera.  This is relational: looking downward remains fully legal at
        # eye level when selected explicitly, and no historical "toward camera"
        # suffix is reconstructed.
        if (
            resolved.get("eye_focus") == DIRECT_EYE_FOCUS
            and resolved.get("camera_direction") != "rear three-quarter view"
            and "head_direction" in owned
        ):
            angle = resolved.get("camera_angle")
            if angle in HIGH_CAMERA_ANGLES:
                resolved["head_direction"] = "looking upward"
            elif angle in LOW_CAMERA_ANGLES:
                resolved["head_direction"] = "looking downward"

        resolved["_composition_archetype_owned_fields"] = owned

    def _apply_scene_geometry_coherence(self, raw, resolved, seed, schema_by_key):
        """Normalize the independent axes of a randomly staged photograph.

        Pose owns body mechanics; Camera direction owns horizontal orientation;
        Camera angle owns vertical viewpoint; Shot composition owns placement.
        This pass only alters ordinary Random values. Manual choices, Forced
        Random, imported authoritative values, and text overrides stay free.
        """

        capture_style = resolved.get("capture_style")
        scenario = resolved.get("scene_scenario")

        # Framing is selected jointly from photographic intent and the amount
        # of body required by the pose. This prevents a full-scene action from
        # blindly overwhelming every other compositional intention.
        pose = resolved.get("pose")
        if raw.get("portrait_style") == "Random":
            capture_pool = CAPTURE_FRAMING_POOLS.get(capture_style, DEFAULT_RANDOM_FRAMING_POOL)
            if scenario in VEHICLE_OR_MOUNT_SCENARIOS:
                allowed = {"three-quarter portrait", "full-body portrait"}
                fallback = VEHICLE_MOUNT_RANDOM_FRAMING_POOL
            elif pose in FULL_SCENE_POSES:
                allowed = {"three-quarter portrait", "full-body portrait"}
                fallback = ["three-quarter portrait", "full-body portrait", "full-body portrait"]
            elif pose in UPPER_BODY_POSES:
                allowed = {"bust portrait", "half-body portrait", "three-quarter portrait"}
                fallback = ["bust portrait", "half-body portrait", "three-quarter portrait"]
            elif pose in MID_BODY_POSES:
                allowed = {"half-body portrait", "three-quarter portrait", "full-body portrait"}
                fallback = ["half-body portrait", "three-quarter portrait", "full-body portrait"]
            else:
                allowed = set(capture_pool)
                fallback = capture_pool
            framing_pool = [value for value in capture_pool if value in allowed] or fallback
            resolved["portrait_style"] = stable_choice(seed, "portrait_style__pose_compatible", framing_pool)

        framing = resolved.get("portrait_style")
        if raw.get("portrait_style") == "Random" and raw.get("pose") == "Random":
            if framing in CLOSE_FRAMINGS:
                resolved["pose"] = None
            elif framing == "bust portrait" and resolved.get("pose") not in UPPER_BODY_POSES:
                source_poses = schema_by_key.get("pose", {}).get("values", [])
                compatible = [value for value in source_poses if value in UPPER_BODY_POSES]
                resolved["pose"] = stable_choice(seed, "pose__random_bust_compatible", compatible) if compatible else None

        # Close framing cannot usefully communicate a complex lower-body
        # action. When the user fixed that framing and left Pose on ordinary
        # Random, omit the pose and let expression/head direction carry it.
        if raw.get("portrait_style") != "Random" and framing in CLOSE_FRAMINGS and raw.get("pose") == "Random":
            resolved["pose"] = None
        elif raw.get("portrait_style") != "Random" and framing == "bust portrait" and raw.get("pose") == "Random":
            source_poses = schema_by_key.get("pose", {}).get("values", [])
            compatible = [value for value in source_poses if value in UPPER_BODY_POSES]
            resolved["pose"] = stable_choice(seed, "pose__bust_compatible", compatible) if compatible else None

        # A side-defined pose already owns the body's horizontal orientation.
        # If Camera direction is explicit and incompatible, redraw only an
        # ordinary-Random pose; two explicit choices remain authoritative.
        explicit_horizontal = resolved.get("camera_direction")
        if (
            raw.get("pose") == "Random"
            and raw.get("camera_direction") != "Random"
            and resolved.get("pose") in SIDE_ORIENTED_POSES
            and explicit_horizontal in {"front-facing view", "back view"}
        ):
            source_poses = schema_by_key.get("pose", {}).get("values", [])
            compatible = [value for value in source_poses if value not in SIDE_ORIENTED_POSES]
            resolved["pose"] = stable_choice(seed, "pose__horizontal_compatible", compatible) if compatible else None

        # Capture style describes photographic intent. Ordinary Random
        # composition, lens, and (for natural captures) lighting are redrawn
        # from a compatible family. This is a preference system, not a ban.
        composition_pool = CAPTURE_COMPOSITION_POOLS.get(capture_style)
        if raw.get("shot_composition") == "Random" and composition_pool:
            resolved["shot_composition"] = stable_choice(
                seed, "shot_composition__capture_compatible", composition_pool
            )
        lens_pool = CAPTURE_LENS_POOLS.get(capture_style)
        if raw.get("lens_style") == "Random" and lens_pool:
            resolved["lens_style"] = stable_choice(seed, "lens_style__capture_compatible", lens_pool)
        if raw.get("lighting_style") == "Random" and capture_style in NATURAL_CAPTURE_STYLES:
            resolved["lighting_style"] = stable_choice(
                seed, "lighting_style__capture_compatible", NATURAL_CAPTURE_LIGHTING
            )

        # Ordinary Random uses weighted, pose-aware horizontal directions. A
        # salute, wave, or thumbs-up should normally remain readable, while
        # locomotion still benefits from profile and three-quarter views.
        if raw.get("camera_direction") == "Random":
            pose = resolved.get("pose")
            if scenario == CAR_DRIVING_SCENARIO:
                direction_pool = CAR_SCENARIO_CAMERA_DIRECTIONS
            elif scenario in VEHICLE_OR_MOUNT_SCENARIOS:
                direction_pool = KINETIC_CAMERA_DIRECTIONS
            elif pose in SIDE_ORIENTED_POSES:
                direction_pool = SIDE_ORIENTED_CAMERA_DIRECTIONS
            elif pose in FRONT_READABLE_POSES:
                direction_pool = FRONT_READABLE_CAMERA_DIRECTIONS
            elif pose in KINETIC_SCENE_POSES:
                direction_pool = KINETIC_CAMERA_DIRECTIONS
            else:
                direction_pool = DEFAULT_RANDOM_CAMERA_DIRECTIONS
            resolved["camera_direction"] = stable_choice(
                seed, "camera_direction__pose_compatible", direction_pool
            )

        # Eye level is the neutral random baseline. Extreme worm's-eye and
        # bird's-eye shots stay present, but no longer occupy forty percent of
        # the random output; close portraits and selfies avoid them entirely.
        if raw.get("camera_angle") == "Random":
            if scenario in VEHICLE_OR_MOUNT_SCENARIOS:
                angle_pool = VEHICLE_MOUNT_RANDOM_CAMERA_ANGLES
            elif framing in BUST_FRAMINGS:
                angle_pool = CLOSE_RANDOM_CAMERA_ANGLES
            else:
                angle_pool = DEFAULT_RANDOM_CAMERA_ANGLES
            placement = resolved.get("shot_composition")
            if placement == HIGH_FRAME_PLACEMENT:
                angle_pool = [value for value in angle_pool if value not in HIGH_CAMERA_ANGLES]
            elif placement == LOW_FRAME_PLACEMENT:
                angle_pool = [value for value in angle_pool if value not in LOW_CAMERA_ANGLES]
            resolved["camera_angle"] = stable_choice(
                seed, "camera_angle__framing_compatible", angle_pool
            )

        # Frame placement is not a second camera angle. Keep an ordinary
        # Random placement from pulling vertically against the final angle.
        angle = resolved.get("camera_angle")
        placement = resolved.get("shot_composition")
        vertical_conflict = (
            (angle in HIGH_CAMERA_ANGLES and placement == HIGH_FRAME_PLACEMENT)
            or (angle in LOW_CAMERA_ANGLES and placement == LOW_FRAME_PLACEMENT)
        )
        if raw.get("shot_composition") == "Random" and vertical_conflict:
            source = composition_pool or schema_by_key.get("shot_composition", {}).get("values", [])
            incompatible = HIGH_FRAME_PLACEMENT if angle in HIGH_CAMERA_ANGLES else LOW_FRAME_PLACEMENT
            compatible = [value for value in source if value != incompatible]
            if compatible:
                resolved["shot_composition"] = stable_choice(
                    seed, "shot_composition__vertical_compatible", compatible
                )

        # Ordinary Random head direction follows the final horizontal view.
        # Vertical angle remains independent, so rear three-quarter + low angle
        # and looking-back + worm's-eye combinations remain fully possible.
        horizontal = resolved.get("camera_direction")
        if raw.get("head_direction") == "Random":
            if horizontal == "back view":
                resolved["head_direction"] = None
            elif horizontal == "rear three-quarter view":
                resolved["head_direction"] = stable_choice(
                    seed,
                    "head_direction__rear_compatible",
                    ["looking back over one shoulder"] * 3 + ["head held level", "glancing slightly to one side"],
                )
            elif resolved.get("head_direction") == "looking back over one shoulder":
                resolved["head_direction"] = stable_choice(
                    seed,
                    "head_direction__forward_compatible",
                    ["head held level", "head tilted slightly", "looking upward", "looking downward", "glancing slightly to one side"],
                )

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

    def _apply_environment_lighting_coherence(self, raw, resolved, seed, schema_by_key):
        """Bind ordinary Random light and environment without touching authority."""
        lighting = resolved.get("lighting_style")
        lighting_raw = raw.get("lighting_style")
        scenario = resolved.get("scene_scenario")
        setting = resolved.get("setting")

        if lighting_raw == "Random":
            family = environment_family(setting=setting, scenario=scenario)
            if lighting_is_compatible(family, lighting):
                return
            source = schema_by_key.get("lighting_style", {}).get("values", [])
            compatible = [value for value in source if lighting_is_compatible(family, value)]
            if compatible:
                resolved["lighting_style"] = stable_choice(
                    seed,
                    f"lighting_style__environment__{family}",
                    compatible,
                )
            return

        # A manual or Forced Random light guides an ordinary Random environment.
        # Two manual/Forced selections deliberately remain untouched.
        if not lighting:
            return
        if scenario and raw.get("scene_scenario") == "Random":
            source = schema_by_key.get("scene_scenario", {}).get("values", [])
            compatible = [
                value for value in source
                if lighting_is_compatible(environment_family(scenario=value), lighting)
            ]
            if compatible:
                resolved["scene_scenario"] = stable_choice(
                    seed, "scene_scenario__lighting_compatible", compatible
                )
            return
        if not scenario and raw.get("setting") == "Random":
            source = schema_by_key.get("setting", {}).get("values", [])
            compatible = [
                value for value in source
                if lighting_is_compatible(environment_family(setting=value), lighting)
            ]
            if compatible:
                resolved["setting"] = stable_choice(
                    seed, "setting__lighting_compatible", compatible
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
        if item in FIXED_COLOR_GARMENTS:
            return item
        expanded_item = CULTURAL_GARMENT_EXPANSIONS.get(item, item)
        # Preserve the garment's short cut explicitly. Text-generation refiners
        # otherwise tend to simplify "pajama short set" to the length-neutral
        # "pajama set", which can turn the shorts into long pajama trousers.
        expanded_item = re.sub(
            r"\bpajama short set\b",
            "pajama set with short pajama shorts",
            expanded_item,
            flags=re.IGNORECASE,
        )
        return f"{color} {expanded_item}" if color else expanded_item

    def _combine_bottom(self, data):
        bottom_type = data.get("bottom_type")
        if not bottom_type:
            return None
        bottom_length = data.get("bottom_length")
        if bottom_type in FULL_BODY_ONE_PIECE_BOTTOM_TYPES:
            bottom_length = None
        # An explicit length overrides built-in skirt length words, avoiding
        # phrases such as "long long skirt" or "mid-length mini skirt".
        if bottom_length and bottom_type in {"mini skirt", "long skirt"}:
            bottom_type = "skirt"
        parts = [bottom_length, data.get("bottom_color"), bottom_type]
        return " ".join(part for part in parts if part)

    @staticmethod
    def _is_authoritative_selection(raw_value):
        """Manual and Forced Random values sit above imported JSON.

        Plain Random and None are deliberately non-authoritative: an Identity Forge
        preset may replace them without changing any unrelated deterministic stream.
        """
        return raw_value not in (None, "", "None", "Random")

    @staticmethod
    def _parse_identity_forge_json(raw_json):
        raw_json = (raw_json or "").strip()
        if not raw_json:
            return {}
        try:
            document = json.loads(raw_json)
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            print(f"[CharacterArchitect] Ignoring malformed Identity Forge JSON: {exc}")
            return {}
        if not isinstance(document, dict):
            print("[CharacterArchitect] Ignoring Identity Forge JSON that is not an object.")
            return {}

        meta = document.get("_meta") if isinstance(document.get("_meta"), dict) else {}
        modifiers = document.get("_modifiers") if isinstance(document.get("_modifiers"), dict) else {}
        groups = {}
        for group_name, group_values in document.items():
            if group_name.startswith("_") or not isinstance(group_values, dict):
                continue
            normalized = {}
            group_modifier = modifiers.get(group_name)
            for field, value in group_values.items():
                if not isinstance(value, (str, int, float)):
                    continue
                value = str(value).strip()
                if not value or value == "None":
                    continue
                descriptor = modifiers.get(field) or group_modifier
                if isinstance(descriptor, str) and descriptor.strip():
                    value = f"{descriptor.strip()} {value}"
                normalized[field] = value
            if normalized:
                groups[group_name] = normalized

        slots = groups.get(IDENTITY_SPECIES_GROUP, {})
        # A generic JSON input never activates the creature renderer. Both an
        # explicit creature marker and actual anatomy are required. Archetype,
        # Cosplayer, and Modifier documents therefore stay on the human path.
        is_creature = bool(meta.get("creature_of") and slots)
        return {
            "meta": dict(meta),
            "groups": groups,
            "slots": dict(slots),
            "is_creature": is_creature,
            "modifiers": dict(modifiers),
        }

    @staticmethod
    def _identity_age(value):
        value = str(value or "").strip()
        return f"{value}-year-old" if value.isdigit() else value

    @staticmethod
    def _identity_extra(field, value):
        template = IDENTITY_EXTRA_TEMPLATES.get(field, "{value}")
        return template.format(value=value)

    def _apply_identity_forge(self, data, identity, raw_values):
        """Merge an Identity Forge document without changing CA's manual priority."""
        if not identity:
            return data

        meta = identity.get("meta", {})
        groups = {
            group_name: dict(group_values)
            for group_name, group_values in (identity.get("groups") or {}).items()
        }
        modifiers = identity.get("modifiers") or {}

        # Per-gender Archetype variants live in _meta rather than the normal
        # field groups. Character Architect's own Gender control selects the
        # branch; Identity Forge's gender metadata never takes authority back.
        gender = data.get("gender")
        variant_key = None
        if gender in {"woman", "transgender woman"}:
            variant_key = "Female"
        elif gender in {"man", "transgender man"}:
            variant_key = "Male"
        variants = meta.get("variants") if isinstance(meta.get("variants"), dict) else {}
        variant_fields = variants.get(variant_key) if variant_key else None
        if isinstance(variant_fields, dict):
            for source_field, value in variant_fields.items():
                if not isinstance(value, (str, int, float)):
                    continue
                value = str(value).strip()
                if not value or value == "None":
                    continue
                group_name = IDENTITY_FIELD_GROUP.get(source_field, "Other")
                descriptor = modifiers.get(source_field) or modifiers.get(group_name)
                if isinstance(descriptor, str) and descriptor.strip():
                    value = f"{descriptor.strip()} {value}"
                groups.setdefault(group_name, {})[source_field] = value
        explicit_fields = {
            key for key, value in raw_values.items() if self._is_authoritative_selection(value)
        }
        data["_explicit_fields"] = explicit_fields
        data["_identity_meta"] = meta
        data["_identity_slots"] = identity.get("slots", {})
        data["_identity_is_creature"] = bool(identity.get("is_creature"))
        cosplay_of = str(meta.get("cosplay_of") or "").strip()
        character_archetype = str(meta.get("archetype") or "").strip()
        if cosplay_of and cosplay_of not in {"None", "Random"}:
            data["_identity_anchor"] = f"The subject is portrayed as {cosplay_of}."
        elif character_archetype and character_archetype not in {"None", "Random"}:
            data["_identity_anchor"] = (
                f"The subject embodies the {character_archetype} character archetype."
            )
        identity_applied_fields = set()

        suppress_groups = set(meta.get("suppress_groups") or [])
        suppress_fields = set(meta.get("suppress_fields") or [])
        if meta.get("covers_face"):
            suppress_groups.update({"Face", "Hair", "Makeup"})
        if meta.get("covers_hair"):
            suppress_groups.add("Hair")
        if meta.get("covers_body"):
            suppress_groups.update({"Body", "Jewelry & Nails"})

        # A leading nonhuman form must not silently inherit a randomized human
        # face/body/hair. Explicit CA choices remain possible by design.
        form = str(meta.get("form") or "")
        leading_creature = identity.get("is_creature") and form in {"Anthropomorphic", "Feral"}
        if leading_creature:
            for field in CREATURE_HUMAN_ANATOMY_FIELDS:
                if field not in explicit_fields:
                    data[field] = None
            if "pose" not in explicit_fields:
                data["pose"] = None

        for group_name in suppress_groups:
            for field in IDENTITY_GROUP_CA_FIELDS.get(group_name, ()):
                if field not in explicit_fields:
                    data[field] = None
        for source_field in suppress_fields:
            target_field = IDENTITY_TO_CA_FIELD.get(source_field)
            if target_field and target_field not in explicit_fields:
                data[target_field] = None

        extras = {group: [] for group in groups if group != IDENTITY_SPECIES_GROUP}
        for group_name, fields in groups.items():
            if group_name == IDENTITY_SPECIES_GROUP or group_name in suppress_groups:
                continue
            for source_field, value in fields.items():
                if source_field in {"gender", "outfit_description", "held_item"}:
                    continue
                if source_field == "ethnicity":
                    if "origin_ethnicity" not in explicit_fields:
                        extras.setdefault(group_name, []).append(value)
                    continue
                target_field = IDENTITY_TO_CA_FIELD.get(source_field)
                if target_field:
                    if target_field not in explicit_fields:
                        data[target_field] = self._identity_age(value) if source_field == "age" else value
                        identity_applied_fields.add(target_field)
                else:
                    extras.setdefault(group_name, []).append(self._identity_extra(source_field, value))

        clothing = groups.get("Clothing", {})
        imported_outfit = clothing.get("outfit_description")
        explicit_main = bool(explicit_fields & IDENTITY_MAIN_CLOTHING_FIELDS)
        if imported_outfit and "Clothing" not in suppress_groups and not explicit_main:
            data["_identity_outfit"] = imported_outfit
            for field in IDENTITY_OUTFIT_RANDOM_CLEAR_FIELDS:
                if field not in explicit_fields:
                    data[field] = None

        held_item = groups.get("Setting & Shot", {}).get("held_item")
        if held_item and "Setting & Shot" not in suppress_groups:
            data["_identity_held_item"] = held_item

        data["_identity_extras"] = {group: values for group, values in extras.items() if values}
        data["_identity_applied_fields"] = identity_applied_fields
        return data

    @staticmethod
    def _creature_presentation(gender):
        if gender in {"woman", "transgender woman"}:
            return "feminine"
        if gender in {"man", "transgender man"}:
            return "masculine"
        if gender in {"androgynous femboy", "androgynous tomboy"}:
            return "androgynous"
        return ""

    @staticmethod
    def _creature_grammar(gender):
        if gender in {"woman", "transgender woman"}:
            return {"subject": "She", "possessive": "her", "has": "has"}
        if gender in {"man", "transgender man"}:
            return {"subject": "He", "possessive": "his", "has": "has"}
        if gender in {"androgynous femboy", "androgynous tomboy"}:
            return {"subject": "They", "possessive": "their", "has": "have"}
        return {"subject": "It", "possessive": "its", "has": "has"}

    @staticmethod
    def _without_article(value):
        return re.sub(r"^(?:a|an|the)\s+", "", str(value or "").strip(), flags=re.IGNORECASE)

    @staticmethod
    def _lingerie_as_panels(lingerie):
        phrase = str(lingerie or "").strip()
        if not phrase:
            return ""
        replacements = (
            (r"\blingerie set\b", "lingerie-inspired panels"),
            (r"\bclassic two-piece bikini\b", "two-piece swimwear-inspired panels"),
            (r"\btwo-piece swimsuit bikini\b", "two-piece swimwear-inspired panels"),
            (r"\btwo-piece bikini\b", "two-piece swimwear-inspired panels"),
            (r"\bone-piece swimsuit\b", "one-piece swimwear-inspired panel"),
        )
        for pattern, replacement in replacements:
            updated = re.sub(pattern, replacement, phrase, flags=re.IGNORECASE)
            if updated != phrase:
                return updated
        return f"{phrase}-inspired panels"

    def _format_clothing(self, data, include_scarf=True):
        identity_outfit = data.get("_identity_outfit")

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
        scarf = data.get("accessories_scarf") if include_scarf else None

        hosiery_integrated_with_trousers = False
        footwear_integrated_with_trousers = False
        bottom_type = data.get("bottom_type")
        bottom_length = data.get("bottom_length")
        effective_trouser_length = bottom_length
        if bottom_type in TROUSER_BOTTOM_TYPES and not effective_trouser_length:
            effective_trouser_length = (
                "mid-length" if bottom_type in {"culottes", "capri pants"} else "long"
            )
        dress_type = data.get("dress_type")
        higher_priority_outfit = bool(identity_outfit or franchise_cosplay or cosplay)
        bottom_is_active = bool(bottom) and not higher_priority_outfit and not dress
        dress_is_active = bool(dress) and not higher_priority_outfit
        if (
            bottom_is_active
            and hosiery
            and hosiery != "bare legs"
            and bottom_type in TROUSER_BOTTOM_TYPES
        ):
            if effective_trouser_length == "mid-length":
                bottom = f"{bottom}, with {hosiery} worn underneath and visible below the trouser hems"
                hosiery_integrated_with_trousers = True
            elif effective_trouser_length == "long":
                if footwear:
                    bottom = (
                        f"{bottom}, with {hosiery} worn fully underneath the trousers "
                        f"and visible only in the narrow gap between the trouser hems and {footwear}"
                    )
                    footwear_integrated_with_trousers = True
                else:
                    bottom = (
                        f"{bottom}, with {hosiery} worn fully underneath the trousers "
                        "and visible only in a narrow band below the trouser hems at the ankles"
                    )
                hosiery_integrated_with_trousers = True
        elif (
            bottom_is_active
            and hosiery
            and hosiery != "bare legs"
            and bottom_type in FULL_BODY_ONE_PIECE_BOTTOM_TYPES
        ):
            if footwear:
                bottom = (
                    f"{bottom}, with {hosiery} worn fully underneath its trouser legs "
                    f"and visible only in the narrow gap between the cuffs and {footwear}"
                )
                footwear_integrated_with_trousers = True
            else:
                bottom = (
                    f"{bottom}, with {hosiery} worn fully underneath its trouser legs "
                    "and visible only in a narrow band below the cuffs at the ankles"
                )
            hosiery_integrated_with_trousers = True
        elif (
            dress_is_active
            and hosiery
            and hosiery != "bare legs"
            and dress_type in FULL_LEG_COMPLETE_OUTFIT_TYPES
        ):
            if footwear:
                dress = (
                    f"{dress}, with {hosiery} worn fully underneath its trouser legs "
                    f"and visible only in the narrow gap between the cuffs and {footwear}"
                )
                footwear_integrated_with_trousers = True
            else:
                dress = (
                    f"{dress}, with {hosiery} worn fully underneath its trouser legs "
                    "and visible only in a narrow band below the cuffs at the ankles"
                )
            hosiery_integrated_with_trousers = True

        main_clothing_mode = None
        main_items = []

        if identity_outfit:
            main_clothing_mode = "identity_outfit"
            main_items.append(identity_outfit)
        elif franchise_cosplay:
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
            if bottom_type in FULL_BODY_ONE_PIECE_BOTTOM_TYPES and bottom:
                main_items.append(bottom)
                if top:
                    main_items.append(f"{top} worn over the one-piece outfit")
            else:
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
        if footwear and not footwear_integrated_with_trousers:
            extra_items.append(footwear)
        if hosiery and not hosiery_integrated_with_trousers:
            extra_items.append(hosiery)
        if scarf and scarf != "no scarf":
            extra_items.append(scarf)

        clauses = []
        lingerie_sentences = []
        if main_items:
            clauses.append("wearing " + join_phrases(main_items + extra_items))
        elif extra_items:
            clauses.append("wearing " + join_phrases(extra_items))

        layered_outer = main_clothing_mode in {"separates", "dress", "cosplay", "franchise_cosplay", "identity_outfit", "sleepwear"}
        layered_lingerie = layered_outer and bool(lingerie) and main_clothing_mode != "lingerie"

        if layered_lingerie:
            archetype = data.get("clothing_archetype")
            if archetype == "Emo / Scene / Alt":
                clauses.append(f"with {lingerie} visibly layered beneath the clothes")
            elif archetype == "Casual Everyday":
                clauses.append(f"with {lingerie} subtly peeking from beneath the clothes")
            else:
                lingerie_phrase = lingerie if "bra straps" in lingerie else f"{indefinite_article(lingerie)} {lingerie}"
                lingerie_sentences.append(
                    "Through the small parts that protrude from the clothing, "
                    f"one can guess {lingerie_phrase} beneath the clothes"
                )

        outfit_sentence = "This subject is " + ", ".join(clauses) if clauses else None
        outerwear_sentences = []
        beneath_outfit_sentence = None
        if outerwear_phrase:
            over_outfit = " over the outfit" if main_clothing_mode else ""
            if outerwear_type == "cape" and outerwear_wearing_style == "Properly worn":
                cape_fall = "over the outfit" if main_clothing_mode else "down the back"
                outerwear_sentences.append(
                    f"The subject wears {indefinite_article(outerwear_phrase)} {outerwear_phrase}{over_outfit}. "
                    f"The cape is fastened securely around both shoulders and hangs evenly {cape_fall}"
                )
            elif outerwear_type == "cape" and outerwear_wearing_style == "Draped over shoulders":
                outerwear_sentences.append(
                    f"The subject has {indefinite_article(outerwear_phrase)} {outerwear_phrase} draped evenly "
                    "over both shoulders and hanging freely down the back"
                )
            elif outerwear_type == "cape" and outerwear_wearing_style == "Off shoulders at elbows":
                outerwear_sentences.append(
                    f"The subject wears {indefinite_article(outerwear_phrase)} {outerwear_phrase} deliberately "
                    "slipped low from both shoulders and gathered symmetrically around the upper arms"
                )
            elif outerwear_wearing_style == "Draped over shoulders":
                outerwear_sentences.append(
                    f"The subject has {indefinite_article(outerwear_phrase)} {outerwear_phrase} draped evenly "
                    "over both shoulders like a cape, with both arms outside its sleeves"
                )
            elif outerwear_wearing_style == "Off shoulders at elbows":
                outerwear_sentences.append(
                    f"The subject wears {indefinite_article(outerwear_phrase)} {outerwear_phrase} deliberately "
                    "slipped off both shoulders, with its sleeves gathered symmetrically around the elbows"
                )
            elif outerwear_wearing_style == "Carried over one shoulder":
                outerwear_sentences.append(
                    f"The subject carries {indefinite_article(outerwear_phrase)} {outerwear_phrase} casually over "
                    "one shoulder instead of wearing it"
                )
            else:
                outerwear_sentences.append(
                    f"The subject wears {indefinite_article(outerwear_phrase)} {outerwear_phrase}{over_outfit}. "
                    f"The {outerwear_type} is worn conventionally, fully covering both shoulders, with both arms "
                    "completely inside its sleeves"
                )

            if outfit_sentence and outerwear_wearing_style != "Carried over one shoulder":
                if outerwear_wearing_style == "Draped over shoulders":
                    visibility = "visible through the open front and wherever naturally uncovered"
                    outerwear_reference = f"draped {outerwear_type}"
                elif outerwear_wearing_style == "Off shoulders at elbows":
                    outerwear_reference = f"lowered {outerwear_type}"
                    visibility = None
                else:
                    visibility = "visible only where naturally exposed"
                    outerwear_reference = outerwear_type
                beneath_outfit_sentence = f"Beneath the {outerwear_reference}, the subject is {', '.join(clauses)}"
                if visibility:
                    beneath_outfit_sentence += f", {visibility}"

        if outerwear_phrase and outerwear_wearing_style != "Carried over one shoulder":
            ordered_sentences = list(outerwear_sentences)
            if beneath_outfit_sentence:
                ordered_sentences.append(beneath_outfit_sentence)
            ordered_sentences.extend(lingerie_sentences)
        else:
            ordered_sentences = []
            if outfit_sentence:
                ordered_sentences.append(outfit_sentence)
            ordered_sentences.extend(lingerie_sentences)
            ordered_sentences.extend(outerwear_sentences)

        return ordered_sentences

    @staticmethod
    def _format_jewelry(data):
        """Keep jewelry compact while binding every specific piece to its slot."""
        general = data.get("accessories_jewelry")
        tone = general if general in {"gold-toned jewelry", "silver-toned jewelry"} else None
        tone_adjective = tone.removesuffix(" jewelry") if tone else None
        excluded = {"no necklace", "no earrings", "no bracelet", "no rings"}
        necklace = data.get("accessories_necklace")
        earrings = data.get("accessories_earrings")
        bracelet = data.get("accessories_bracelet")
        rings = data.get("accessories_rings")
        specifics = [value for value in (necklace, earrings, bracelet, rings) if value and value not in excluded]
        if not specifics:
            return general

        material_markers = {"gold", "silver", "pearl", "ribbon", "lace", "leather", "kandi"}

        def toned(value):
            if not tone_adjective or any(marker in value.lower() for marker in material_markers):
                return value
            return f"{tone_adjective} {value}"

        clauses = []
        if necklace and necklace not in excluded:
            if necklace == "soft ribbon choker":
                clauses.append("a plain pendant-free soft ribbon choker around the neck")
            elif necklace == "lace choker":
                clauses.append("a plain pendant-free lace choker around the neck")
            else:
                value = toned(necklace)
                article = "" if value == "layered necklaces" else f"{indefinite_article(value)} "
                clauses.append(f"{article}{value} around the neck")
        if earrings and earrings not in excluded:
            if earrings == "cross earrings":
                value = toned("cross-shaped earrings")
                clauses.append(f"small {value} on the ears")
            else:
                clauses.append(f"{toned(earrings)} on the ears")
        if bracelet and bracelet not in excluded:
            clauses.append(f"{toned(bracelet)} at the wrists")
        if rings and rings not in excluded:
            clauses.append(f"{toned(rings)} on the fingers")
        return join_phrases(clauses)

    def _format_accessories(self, data):
        wear_keys = ["head_accessory", "accessories_glasses", "armwear"]
        carry_keys = ["accessories_bag"]
        excluded = {"no head accessory", "no glasses", "no armwear", "no necklace", "no earrings", "no bracelet", "no rings", "no bag"}
        wear_items = [data[k] for k in wear_keys if data.get(k) and data[k] not in excluded]
        jewelry = self._format_jewelry(data)
        if jewelry:
            wear_items.append(jewelry)
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
        return deduplicate_hair_descriptors(descriptors)

    def _media_preset(self, media_type):
        preset = MEDIA_TYPE_PRESETS.get(media_type, {})
        intro = preset.get("intro") or media_type or "image"
        style = list(preset.get("style") or [])
        return intro, style

    def _media_intro_with_effect(self, data):
        media_type = data.get("media_type") or "image"
        media_intro, media_style = self._media_preset(media_type)
        effect = data.get("optical_effect")
        if effect == "selective-color monochrome":
            phrase = f"selectively colorized monochrome {media_intro}"
            article_basis = "selectively"
        elif effect:
            phrase = f'"{effect}" {media_intro}'
            article_basis = effect
        else:
            phrase = media_intro
            article_basis = media_intro
        return phrase, media_style, indefinite_article(article_basis).capitalize()

    @staticmethod
    def _portrait_phrase(data):
        """Combine independent framing and capture treatment without duplication."""
        framing = data.get("portrait_style") or "portrait"
        capture = data.get("capture_style")
        if not capture:
            return framing
        if framing == "portrait":
            return f"{capture} portrait"
        framing_prefix = framing.removesuffix(" portrait")
        return f"{framing_prefix} {capture} portrait"

    @staticmethod
    def _appearance_sentences(portrait_descriptors):
        """Give personal appearance its own semantic clause.

        The opening sentence is reserved for identity and scene geometry; this
        prevents makeup, nails, tattoos, and hair from appearing as loose
        fragments immediately after a long pose.
        """
        descriptors = [value for value in portrait_descriptors if value]
        if not descriptors:
            return []
        return [ensure_period("The subject has " + join_phrases(descriptors))]

    @staticmethod
    def _format_body_and_appearance(data, ethnicity_guidance=False, identity_extras=None):
        """Render human morphology as readable semantic clauses."""
        identity_extras = identity_extras or {}
        height = data.get("body_type")
        body = []
        for key in (
            "body_physique", "body_feminine_curves", "body_hair",
            "bust", "cleavage_depth", "cleavage_type", "butt_shape", "thigh_shape",
            "body_detail_1", "body_detail_2", "body_detail_3",
        ):
            if data.get(key):
                body.append(data[key])
        body.extend(identity_extras.get("Body", []))

        face = []
        for key, template in [
            ("skin_finish", "{value}"),
            ("expression", "{value}"),
            ("mouth_expression", "{value}"),
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
        ]:
            if key == "eye_color" and ethnicity_guidance and data.get("origin_ethnicity"):
                continue
            value = data.get(key)
            if value:
                face.append(template.format(value=value))
        face.extend(identity_extras.get("Face", []))

        hair = []
        hair_adjectives = [value for value in (data.get("hair_texture"), data.get("hair_color")) if value]
        if hair_adjectives:
            hair.append(" ".join(hair_adjectives + ["hair"]))
        for key in ("hair_style", "hair_cut", "hair_length", "bangs_style"):
            if data.get(key):
                hair.append(data[key])
        hair.extend(identity_extras.get("Hair", []))
        hair = deduplicate_hair_descriptors(hair)

        sentences = []
        if height:
            if height == "person with dwarfism":
                height_clause = "The subject is a person with dwarfism"
            elif height == "average height":
                height_clause = "The subject is of average height"
            else:
                height_clause = f"The subject is {height}"
            if body:
                height_clause += ", with " + join_phrases(body)
            sentences.append(ensure_period(height_clause))
        elif body:
            sentences.append(ensure_period("The subject has " + join_phrases(body)))
        if face:
            sentences.append(ensure_period("Facial features include " + join_phrases(face)))
        if hair:
            sentences.append(ensure_period("The subject has " + join_phrases(hair)))
        return sentences

    @staticmethod
    def _format_styling_details(data, identity_extras=None):
        identity_extras = identity_extras or {}
        styling = []
        for key in ("makeup_eye", "makeup_lips", "makeup_complexion", "nail_style", "tattoo_style"):
            if data.get(key):
                styling.append(data[key])
        styling.extend(identity_extras.get("Makeup", []))
        return ensure_period("Styling details include " + join_phrases(styling)) if styling else ""

    @staticmethod
    def _lighting_clause(data):
        lighting = data.get("lighting_style")
        if not lighting:
            return None
        family = environment_family(
            setting=data.get("setting"),
            scenario=data.get("scene_scenario"),
        )
        if family in {"daylit_interior", "enclosed_interior"}:
            if lighting == "overcast daylight":
                return "lit by soft diffuse overcast daylight"
            if lighting == "golden-hour light":
                return "lit by warm golden-hour daylight"
            return f"lit by {lighting}"
        return f"under {lighting}"

    @staticmethod
    def _format_scene_sentences(data, extra_descriptors=None):
        """Keep action, environment, camera geometry, and optics together."""
        scenario = data.get("scene_scenario")
        pose = data.get("pose")
        attitude = data.get("pose_mood")
        setting = data.get("setting")
        subject_scene = f"The subject is {scenario}" if scenario else (f"The subject is {pose}" if pose else "The subject is shown")
        if attitude:
            if attitude.endswith(("energy", "composure")):
                subject_scene += f", with {attitude}"
            else:
                subject_scene += f", with {indefinite_article(attitude)} {attitude}"
        if setting and not scenario:
            subject_scene += f", {setting}"
        if data.get("head_direction"):
            head = data["head_direction"]
            if head.startswith("head "):
                subject_scene += f", with the subject's {head}"
            else:
                subject_scene += f", while {head}"
        if data.get("eye_focus"):
            subject_scene += f", with their {data['eye_focus']}"
        for descriptor in extra_descriptors or []:
            if descriptor:
                subject_scene += f", {descriptor}"

        camera_scene = []
        if data.get("camera_direction"):
            direction = data["camera_direction"]
            camera_scene.append(f"{indefinite_article(direction)} {direction}")
        if data.get("camera_angle"):
            camera_scene.append(f"photographed {data['camera_angle']}")
        if data.get("shot_composition"):
            camera_scene.append(f"framed with {data['shot_composition']}")
        if data.get("lens_style"):
            lens = data["lens_style"]
            camera_scene.append(f"with {indefinite_article(lens)} {lens}")
        lighting_clause = CharacterArchitectNode._lighting_clause(data)
        if lighting_clause:
            camera_scene.append(lighting_clause)

        sentences = []
        if scenario or pose or attitude or setting or data.get("head_direction") or data.get("eye_focus") or (extra_descriptors or []):
            sentences.append(ensure_period(subject_scene))
        if camera_scene:
            sentences.append(ensure_period("The image uses " + ", ".join(camera_scene)))
        return sentences

    @staticmethod
    def _realism_suffix(data):
        """Match the realism epilogue to natural versus directed capture intent."""
        directed = {"glamour", "editorial", "cinematic", "fashion", "beauty", "dramatic"}
        return DIRECTED_REALISM_SUFFIX if data.get("capture_style") in directed else NATURAL_REALISM_SUFFIX

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
        portrait_style = self._portrait_phrase(data)
        gender = data.get("gender") or "person"
        age = data.get("origin_age")
        subject_gender, species_prefix = self._resolve_species_subject(gender, species_mode)

        subject = f"{age} {subject_gender}" if age else subject_gender
        intro = f"{media_article} {media_intro}, {portrait_style} of {indefinite_article(subject)} {subject}"

        identity_descriptors = []
        post_makeup_descriptors = []
        final_descriptors = []
        identity_extras = data.get("_identity_extras") or {}

        ethnicity_descriptor = self._ethnicity_descriptor(data, ethnicity_guidance=ethnicity_guidance)
        if ethnicity_descriptor:
            identity_descriptors.append(ethnicity_descriptor)
        identity_descriptors.extend(identity_extras.get("Demographics", []))

        external_clothing = data.get("_external_clothing_text")
        clothing_sentences = (
            ["This subject is wearing " + external_clothing]
            if external_clothing
            else self._format_clothing(data)
        )
        wear_accessories, carry_accessories = self._format_accessories(data)
        post_makeup_descriptors.extend(clothing_sentences)
        if wear_accessories:
            post_makeup_descriptors.append("This subject is wearing " + join_phrases(wear_accessories))
        if carry_accessories:
            post_makeup_descriptors.append("This subject is carrying " + join_phrases(carry_accessories))
        if identity_extras.get("Jewelry & Nails"):
            post_makeup_descriptors.append(
                "This subject is wearing " + join_phrases(identity_extras["Jewelry & Nails"])
            )
        if identity_extras.get("Clothing"):
            post_makeup_descriptors.append(
                "This subject also has " + join_phrases(identity_extras["Clothing"])
            )
        if data.get("_identity_held_item"):
            post_makeup_descriptors.append(f"This subject is holding {data['_identity_held_item']}")
        subtle_slots = data.get("_identity_slots") or {}
        if subtle_slots and (data.get("_identity_meta") or {}).get("form") == "Subtle":
            anatomy = [subtle_slots.get(slot) for slot in IDENTITY_SLOT_ORDER if subtle_slots.get(slot)]
            if anatomy:
                post_makeup_descriptors.append("This subject also has " + join_phrases(anatomy))

        final_descriptors.extend(identity_extras.get("Setting & Shot", []))

        first_sentence_parts = [intro]
        if species_prefix:
            first_sentence_parts.extend(species_prefix)
        first_sentence_parts.extend(media_style)
        if free_prompt and free_prompt_position == "After introduction":
            first_sentence_parts.append(free_prompt)
        first_sentence_parts.extend(identity_descriptors)
        sentences = []
        first_sentence = build_sentence(first_sentence_parts)
        if first_sentence:
            sentences.append(first_sentence)
        if data.get("_identity_anchor"):
            sentences.append(ensure_period(data["_identity_anchor"]))
        content_rating_sentence = CONTENT_RATING_SENTENCES.get(data.get("content_rating"))
        if content_rating_sentence:
            sentences.append(content_rating_sentence)
        if data.get("_external_subject_text"):
            sentences.append(ensure_period("The subject is described as " + data["_external_subject_text"]))

        # Scene geometry follows the identity introduction immediately. A long
        # body, hair, clothing, or accessory inventory must not bury the pose
        # and camera instructions at the end of the prompt.
        sentences.extend(self._format_scene_sentences(data, final_descriptors))
        if data.get("_external_photography_text"):
            sentences.append(ensure_period("Photographic description: " + data["_external_photography_text"]))

        sentences.extend(self._format_body_and_appearance(
            data,
            ethnicity_guidance=ethnicity_guidance,
            identity_extras=identity_extras,
        ))

        for clause in post_makeup_descriptors:
            sentences.append(ensure_period(clause))

        styling_sentence = self._format_styling_details(data, identity_extras)
        if styling_sentence:
            sentences.append(styling_sentence)
        if free_prompt and free_prompt_position == "After makeup":
            sentences.append(ensure_period(free_prompt))

        if free_prompt and free_prompt_position == "At end":
            sentences.append(ensure_period(free_prompt))
        if enhance_realism:
            sentences.append(ensure_period(self._realism_suffix(data)))
        return " ".join(sentence for sentence in sentences if sentence).strip()

    def _build_pre_gen_prompt(
        self,
        data,
        free_prompt="",
        free_prompt_position="After introduction",
        enhance_realism=False,
        species_mode="Human",
        creature=False,
        enforce_portrait_framing=False,
    ):
        """Build the body-and-scene companion prompt from the resolved draw.

        This deliberately omits detailed ethnicity guidance, face, makeup, body
        hair, accessories, and the realism epilogue. It keeps the photographic
        introduction, subject kind, scene/camera controls, complete structural
        morphology, scalp-hair description, resolved clothing, simple ethnicity
        category, content rating, and free text. Enforced portrait framing reduces
        this to the minimal identity-and-framing introduction.
        """
        media_intro, media_style, media_article = self._media_intro_with_effect(data)
        portrait_style = self._portrait_phrase(data)
        ethnicity = data.get("origin_ethnicity")

        if is_enabled(enforce_portrait_framing):
            # Composition lock deliberately ignores optical effects and every
            # downstream block. Only the resolved media/framing introduction
            # survives, plus the fundamental creature type when applicable.
            minimal_media_intro, _ = self._media_preset(data.get("media_type") or "image")
            minimal_media_article = indefinite_article(minimal_media_intro).capitalize()
            if creature:
                minimal_subject = self._creature_subject(data, include_size=False)
            else:
                gender = data.get("gender") or "person"
                minimal_subject, _ = self._resolve_species_subject(gender, species_mode)
            minimal_subject = " ".join(
                str(value).strip()
                for value in (data.get("origin_age"), ethnicity, minimal_subject)
                if value
            )
            return ensure_period(
                f"{minimal_media_article} {minimal_media_intro}, {portrait_style} "
                f"of {indefinite_article(minimal_subject)} {minimal_subject}"
            )

        if creature:
            subject = self._creature_subject(data)
            age = data.get("origin_age")
            subject = " ".join(str(value).strip() for value in (age, ethnicity, subject) if value)
            first_parts = [
                f"{media_article} {media_intro}",
                f"{portrait_style} of {indefinite_article(subject)} {subject}",
            ]
        else:
            gender = data.get("gender") or "person"
            age = data.get("origin_age")
            subject_gender, species_prefix = self._resolve_species_subject(gender, species_mode)
            subject = " ".join(
                str(value).strip() for value in (age, ethnicity, subject_gender) if value
            )
            first_parts = [
                f"{media_article} {media_intro}, {portrait_style} of {indefinite_article(subject)} {subject}"
            ]
            first_parts.extend(species_prefix)

        first_parts.extend(media_style)
        if free_prompt and free_prompt_position == "After introduction":
            first_parts.append(free_prompt)
        sentences = [build_sentence(first_parts)]
        if data.get("_identity_anchor"):
            sentences.append(ensure_period(data["_identity_anchor"]))
        content_rating_sentence = CONTENT_RATING_SENTENCES.get(data.get("content_rating"))
        if content_rating_sentence:
            sentences.append(content_rating_sentence)
        if data.get("_external_subject_text"):
            sentences.append(ensure_period("The subject is described as " + data["_external_subject_text"]))
        scene_extras = (data.get("_identity_extras") or {}).get("Setting & Shot", [])
        sentences.extend(self._format_scene_sentences(data, scene_extras))
        if data.get("_external_photography_text"):
            sentences.append(ensure_period("Photographic description: " + data["_external_photography_text"]))

        # Reuse the exact resolved morphology from the main prompt. Body
        # Archetype itself is not rendered: only its reproducible components are.
        height = data.get("body_type")
        body = [value for value in (
            data.get("body_physique"),
            data.get("body_feminine_curves"),
            data.get("bust"),
            data.get("butt_shape"),
            data.get("thigh_shape"),
            data.get("body_detail_1"),
            data.get("body_detail_2"),
            data.get("body_detail_3"),
        ) if value]
        if height:
            if height == "person with dwarfism":
                height_clause = "The subject is a person with dwarfism"
            elif height == "average height":
                height_clause = "The subject is of average height"
            else:
                height_clause = f"The subject is {height}"
            if body:
                height_clause += ", with " + join_phrases(body)
            sentences.append(ensure_period(height_clause))
        elif body:
            sentences.append(ensure_period("The subject has " + join_phrases(body)))

        hair = self._collect_hair_descriptors(data)
        if hair:
            sentences.append(ensure_period("The subject has " + join_phrases(hair)))

        # Pre-gen has no makeup block. "After makeup" therefore maps to the
        # same structural boundary: immediately before the resolved clothing.
        if free_prompt and free_prompt_position == "After makeup":
            sentences.append(ensure_period(free_prompt))

        # Clothing is structural during Pre-gen: beginning from a dressed body
        # avoids asking later diffusion steps to cover already-established skin.
        # The scarf is an accessory in this node and therefore stays excluded.
        if data.get("_external_clothing_text"):
            sentences.append(ensure_period("This subject is wearing " + data["_external_clothing_text"]))
        else:
            sentences.extend(
                ensure_period(sentence)
                for sentence in self._format_clothing(data, include_scarf=False)
            )

        if free_prompt and free_prompt_position == "At end":
            sentences.append(ensure_period(free_prompt))

        return " ".join(sentence for sentence in sentences if sentence).strip()

    def _creature_subject(self, data, include_size=True):
        meta = data.get("_identity_meta") or {}
        creature_name = str(meta.get("creature_of") or "creature").strip()
        form = str(meta.get("form") or "Anthropomorphic")
        creature_class = str(meta.get("creature_class") or "")
        if form == "Feral":
            core = f"monstrous {creature_name}" if creature_class in {"Monsters", "Aliens"} else creature_name
        else:
            core = f"anthropomorphic {creature_name} hybrid"
        presentation = self._creature_presentation(data.get("gender"))
        size = str(meta.get("size") or "").strip() if include_size else ""
        return " ".join(part for part in (size, presentation, core) if part)

    def _creature_main_clothing(self, data, grammar):
        """Return one anatomy-safe garment phrase using fixed bridge templates."""
        slots = data.get("_identity_slots") or {}
        body_anchor = self._without_article(slots.get("integument"))
        lower_anchor = self._without_article(slots.get("legs_feet"))
        possessive = grammar["possessive"]

        identity_outfit = data.get("_identity_outfit")
        franchise_cosplay = data.get("cosplay_franchise_western") or data.get("cosplay_franchise_asian")
        cosplay = self._combine_color(data, "cosplay_type", "cosplay_color")
        dress = self._combine_color(data, "dress_type", "dress_color")
        lingerie = self._combine_color(data, "lingerie_type", "lingerie_color")
        sleepwear = self._combine_color(data, "sleepwear_type", "sleepwear_color")
        top = self._combine_color(data, "top_type", "top_color")
        bottom = self._combine_bottom(data)

        if identity_outfit:
            phrase = identity_outfit
            mode = "identity_outfit"
        elif franchise_cosplay:
            phrase = franchise_cosplay
            mode = "franchise_cosplay"
        elif cosplay:
            phrase = cosplay
            mode = "cosplay"
        elif dress:
            phrase = dress
            mode = "dress"
        elif top or bottom:
            adapted = []
            if data.get("bottom_type") in FULL_BODY_ONE_PIECE_BOTTOM_TYPES and bottom:
                adapted.append(
                    f"{bottom}, adapted to {possessive} {body_anchor}" if body_anchor else bottom
                )
                if top:
                    top_phrase = f"{top} worn over the one-piece outfit"
                    adapted.append(
                        f"{top_phrase}, fitted around {possessive} {body_anchor}"
                        if body_anchor else top_phrase
                    )
            else:
                if top:
                    adapted.append(
                        f"{top} fitted around {possessive} {body_anchor}" if body_anchor else top
                    )
                if bottom:
                    adapted.append(
                        f"{bottom} fitted over the lower portion of {possessive} {lower_anchor}"
                        if lower_anchor else bottom
                    )
            return join_phrases(adapted), "separates"
        elif lingerie:
            panels = self._lingerie_as_panels(lingerie)
            phrase = f"{panels} wrapped around {possessive} {body_anchor}" if body_anchor else panels
            return phrase, "lingerie"
        elif sleepwear:
            phrase = sleepwear
            mode = "sleepwear"
        else:
            return "", None

        if body_anchor:
            phrase = f"{phrase}, adapted to {possessive} {body_anchor}"
        return phrase, mode

    def _format_creature_clothing(self, data, grammar):
        slots = data.get("_identity_slots") or {}
        body_anchor = self._without_article(slots.get("integument"))
        arm_anchor = self._without_article(slots.get("arms"))
        lower_anchor = self._without_article(slots.get("legs_feet"))
        possessive = grammar["possessive"]

        main_phrase, main_mode = self._creature_main_clothing(data, grammar)
        hosiery = self._combine_color(data, "hosiery", "hosiery_color")
        if hosiery == "bare legs":
            hosiery = None
        if hosiery and lower_anchor:
            hosiery = f"{hosiery} fitted over the lower portion of {possessive} {lower_anchor}"

        belt = self._combine_color(data, "belt", "belt_color")
        if belt == "no visible belt":
            belt = None
        if belt and body_anchor:
            belt = f"{belt} fitted around {possessive} {body_anchor}"

        footwear = self._combine_color(data, "footwear", "footwear_color")
        if footwear == "bare feet":
            footwear = None
        scarf = data.get("accessories_scarf")
        if scarf == "no scarf":
            scarf = None

        extras = [item for item in (belt, footwear, scarf) if item]
        if hosiery:
            if main_phrase:
                main_phrase = f"{main_phrase}, with {hosiery}"
            else:
                main_phrase = hosiery
        if extras:
            main_phrase = join_phrases([main_phrase] + extras) if main_phrase else join_phrases(extras)

        clauses = []
        if main_phrase:
            clauses.append(f"wearing {main_phrase}")

        outfit_sentence = "This subject is " + ", ".join(clauses) if clauses else None
        sentences = []

        outerwear = self._combine_color(data, "outerwear", "outerwear_color")
        if outerwear:
            outerwear = outerwear.replace(" layer", "")
            outerwear_type = data.get("outerwear") or "outerwear"
            wearing_style = data.get("outerwear_wearing_style") or "Properly worn"
            over_outfit = " over the outfit" if main_mode else ""
            article = indefinite_article(outerwear)
            if wearing_style == "Draped over shoulders":
                sentence = f"The subject also has {article} {outerwear} draped instead of conventionally worn"
                if body_anchor:
                    sentence += f" around {possessive} {body_anchor}"
            elif wearing_style == "Off shoulders at elbows":
                sentence = f"The subject also wears {article} {outerwear} slipped low instead of conventionally worn"
                if arm_anchor:
                    sentence += f" around {possessive} {arm_anchor}"
            elif wearing_style == "Carried over one shoulder":
                sentence = f"The subject carries {article} {outerwear} instead of wearing it"
            else:
                sentence = f"The subject wears {article} {outerwear}{over_outfit}"
                if body_anchor:
                    sentence += f", adapted to {possessive} {body_anchor}"
                if arm_anchor:
                    sentence += f", with its sleeves fitted around {possessive} {arm_anchor}"
            if wearing_style == "Carried over one shoulder":
                if outfit_sentence:
                    sentences.append(outfit_sentence)
                sentences.append(sentence)
            else:
                sentences.append(sentence)
                if outfit_sentence:
                    if wearing_style == "Draped over shoulders":
                        visibility = "visible through the open front and wherever naturally uncovered"
                        outerwear_reference = f"draped {outerwear_type}"
                    elif wearing_style == "Off shoulders at elbows":
                        outerwear_reference = f"lowered {outerwear_type}"
                        visibility = None
                    else:
                        visibility = "visible only where naturally exposed"
                        outerwear_reference = outerwear_type
                    beneath = f"Beneath the {outerwear_reference}, the subject is {', '.join(clauses)}"
                    if visibility:
                        beneath += f", {visibility}"
                    sentences.append(beneath)
        elif outfit_sentence:
            sentences.append(outfit_sentence)
        return sentences

    def _creature_explicit_descriptors(self, data, ethnicity_guidance=False):
        descriptors = []
        ethnicity = self._ethnicity_descriptor(data, ethnicity_guidance=ethnicity_guidance)
        if ethnicity:
            descriptors.append(ethnicity)
        order = [
            ("body_type", "{value}"), ("body_physique", "{value}"),
            ("body_feminine_curves", "{value}"), ("body_hair", "{value}"),
            ("bust", "{value}"), ("cleavage_depth", "{value}"),
            ("cleavage_type", "{value}"), ("butt_shape", "{value}"),
            ("thigh_shape", "{value}"), ("body_detail_1", "{value}"),
            ("body_detail_2", "{value}"), ("body_detail_3", "{value}"),
            ("skin_finish", "{value}"),
            ("expression", "{value}"), ("mouth_expression", "{value}"), ("eye_expression", "{value} gaze"),
            ("face_shape", "{value} face"), ("jawline", "{value}"),
            ("chin_shape", "{value}"), ("eye_shape", "{value} eyes"),
            ("eye_color", "{value} eyes"), ("eyelashes", "{value}"),
            ("eyebrows", "{value}"), ("nose_shape", "{value}"),
            ("lip_shape", "{value}"), ("facial_hair", "{value}"),
            ("makeup_eye", "{value}"), ("makeup_lips", "{value}"),
            ("nail_style", "{value}"), ("tattoo_style", "{value}"),
            ("makeup_complexion", "{value}"),
        ]
        for field, template in order:
            if field == "eye_color" and ethnicity_guidance and data.get("origin_ethnicity"):
                continue
            value = data.get(field)
            if value:
                descriptors.append(template.format(value=value))
        descriptors.extend(self._collect_hair_descriptors(data))
        extras = data.get("_identity_extras") or {}
        for group_name in ("Demographics", "Body", "Face", "Hair", "Makeup"):
            descriptors.extend(extras.get(group_name, []))
        return descriptors

    def _build_creature_prompt(self, data, free_prompt="", free_prompt_position="After introduction", enhance_realism=False, ethnicity_guidance=False):
        media_intro, media_style, media_article = self._media_intro_with_effect(data)
        portrait_style = self._portrait_phrase(data)
        grammar = self._creature_grammar(data.get("gender"))
        subject = self._creature_subject(data)
        age = data.get("origin_age")
        subject_with_age = f"{age} {subject}" if age else subject

        first_parts = [
            f"{media_article} {media_intro}",
            f"{portrait_style} of {indefinite_article(subject_with_age)} {subject_with_age}",
        ]
        first_parts.extend(media_style)
        sentences = [build_sentence(first_parts)]
        if data.get("_identity_anchor"):
            sentences.append(ensure_period(data["_identity_anchor"]))
        content_rating_sentence = CONTENT_RATING_SENTENCES.get(data.get("content_rating"))
        if content_rating_sentence:
            sentences.append(content_rating_sentence)
        if data.get("_external_subject_text"):
            sentences.append(ensure_period("The subject is described as " + data["_external_subject_text"]))

        slots = data.get("_identity_slots") or {}
        anatomy = [slots.get(slot) for slot in IDENTITY_SLOT_ORDER if slots.get(slot)]
        if anatomy:
            sentences.append(ensure_period(f"{grammar['subject']} {grammar['has']} {join_phrases(anatomy)}"))

        if free_prompt and free_prompt_position == "After introduction":
            sentences.append(ensure_period(free_prompt))

        explicit_descriptors = self._creature_explicit_descriptors(data, ethnicity_guidance=ethnicity_guidance)
        if explicit_descriptors:
            sentences.append(build_sentence(explicit_descriptors))
        if free_prompt and free_prompt_position == "After makeup":
            sentences.append(ensure_period(free_prompt))

        sentences.extend(self._format_scene_sentences(
            data,
            (data.get("_identity_extras") or {}).get("Setting & Shot", []),
        ))
        if data.get("_external_photography_text"):
            sentences.append(ensure_period("Photographic description: " + data["_external_photography_text"]))

        if data.get("_external_clothing_text"):
            sentences.append(ensure_period("This subject is wearing " + data["_external_clothing_text"]))
        else:
            sentences.extend(ensure_period(sentence) for sentence in self._format_creature_clothing(data, grammar))

        wear_accessories, carry_accessories = self._format_accessories(data)
        if wear_accessories:
            sentences.append(ensure_period("This subject is wearing " + join_phrases(wear_accessories)))
        if carry_accessories:
            sentences.append(ensure_period("This subject is carrying " + join_phrases(carry_accessories)))
        if (data.get("_identity_extras") or {}).get("Jewelry & Nails"):
            sentences.append(ensure_period(
                "This subject is wearing " + join_phrases(data["_identity_extras"]["Jewelry & Nails"])
            ))
        if data.get("_identity_held_item"):
            sentences.append(ensure_period(f"This subject is holding {data['_identity_held_item']}"))

        if free_prompt and free_prompt_position == "At end":
            sentences.append(ensure_period(free_prompt))
        if enhance_realism:
            sentences.append(ensure_period(CREATURE_REALISM_SUFFIX))
        return " ".join(sentence for sentence in sentences if sentence).strip()

    def _build_creature_face_prompt(self, data):
        if data.get("_external_subject_text"):
            parts = [data["_external_subject_text"]]
            if data.get("eye_focus"):
                parts.append(data["eye_focus"])
            if data.get("_external_photography_text"):
                parts.append(data["_external_photography_text"])
            return ", ".join(part for part in parts if part).strip()

        media_intro, media_style, media_article = self._media_intro_with_effect(data)
        subject = self._creature_subject(data)
        age = data.get("origin_age")
        if age:
            subject = f"{age} {subject}"
        parts = [f"{media_article} {media_intro} of {indefinite_article(subject)} {subject}"]
        parts.extend(media_style)
        slots = data.get("_identity_slots") or {}
        for slot in ("head", "eyes", "integument", "extras"):
            if slots.get(slot):
                parts.append(slots[slot])
        if data.get("lighting_style"):
            parts.append(data["lighting_style"])
        if data.get("eye_focus"):
            parts.append(data["eye_focus"])
        return ", ".join(part for part in parts if part).strip()

    def _build_face_prompt(self, data, species_mode="Human", ethnicity_guidance=False):
        if data.get("_external_subject_text"):
            parts = [data["_external_subject_text"]]
            if data.get("eye_focus"):
                parts.append(data["eye_focus"])
            if data.get("_external_photography_text"):
                parts.append(data["_external_photography_text"])
            return ", ".join(part for part in parts if part).strip()

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
            ("mouth_expression", "{value}"),
            ("eye_expression", "{value} gaze"),
            ("eye_focus", "{value}"),
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

    @staticmethod
    def _external_text(value):
        return str(value or "").strip().strip(",")

    @staticmethod
    def _parse_custom_color_overrides(text):
        overrides = {}
        for entry in re.split(r"[;\n\r]+", str(text or "")):
            entry = entry.strip()
            if not entry:
                continue
            match = re.match(r"^\s*([^:=]+?)\s*[:=]\s*(.+?)\s*$", entry)
            if not match:
                continue
            raw_target, raw_value = match.groups()
            target = re.sub(r"[\s-]+", "_", raw_target.strip().casefold())
            field = CUSTOM_COLOR_TARGETS.get(target)
            value = raw_value.strip().strip(",")
            if field and value:
                overrides[field] = value
        return overrides

    @staticmethod
    def _parse_face_hair_text_override(text):
        """Parse a compact Generate Text result into existing structured fields.

        Returning ``None`` means that no recognized pair was supplied and the
        node must keep its normal behavior. A dictionary containing explicit
        ``None`` values is valid: for example ``facial_hair=none`` deliberately
        prevents a lower-priority random or imported beard from reappearing.
        """
        raw_text = str(text or "").strip()
        if not raw_text:
            return None

        # Generate Text occasionally wraps a requested one-line record in a
        # Markdown fence. Removing the fence tokens is deterministic and does
        # not reinterpret any visual description.
        raw_text = re.sub(r"^\s*```(?:text|txt|json)?\s*", "", raw_text, flags=re.IGNORECASE)
        raw_text = re.sub(r"\s*```\s*$", "", raw_text)
        parsed = {}
        for entry in re.split(r"[;\n\r]+", raw_text):
            entry = re.sub(r"^\s*[-*•]+\s*", "", entry).strip()
            if not entry:
                continue
            match = re.match(r"^\s*([^:=]+?)\s*[:=]\s*(.*?)\s*$", entry)
            if not match:
                continue
            raw_key, raw_value = match.groups()
            normalized_key = re.sub(r"[^a-z0-9]+", "_", raw_key.lower()).strip("_")
            field = FACE_HAIR_OVERRIDE_ALIASES.get(normalized_key)
            if not field:
                continue
            value = re.sub(r"\s+", " ", raw_value).strip().strip("`\"'").strip(" .,;")
            if value.lower() in FACE_HAIR_ABSENT_VALUES:
                value = None
            parsed[field] = value
        return parsed if parsed else None

    def _apply_face_hair_text_override(self, data, parsed_values, raw_values):
        """Apply the reference face between authored choices and added sources.

        Per-field manual and Forced Random selections retain their normal
        authority. Every other covered field is cleared first, then populated
        from the reference description when present. This makes omissions
        meaningful and prevents lower Identity Forge or Random values from
        silently contradicting the image.
        """
        if parsed_values is None:
            return data

        applied_fields = set()
        for field in FACE_HAIR_OVERRIDE_FIELDS:
            if self._is_authoritative_selection(raw_values.get(field)):
                continue
            data[field] = parsed_values.get(field)
            applied_fields.add(field)

        # Identity Forge may carry unmapped hair-part/highlight prose. It cannot
        # be reconciled field by field with the reference and therefore yields
        # with the rest of the lower-priority Hair source. Non-hair Face extras
        # such as complexion or freckles remain independent.
        (data.get("_identity_extras") or {}).pop("Hair", None)
        imported_fields = data.get("_identity_applied_fields")
        if isinstance(imported_fields, set):
            imported_fields.difference_update(applied_fields)
        data["_face_hair_override_active"] = True
        data["_face_hair_override_fields"] = applied_fields
        return data

    @staticmethod
    def _eye_focus_pool(data):
        action = " ".join(str(data.get(key) or "") for key in ("scene_scenario", "pose")).casefold()
        held_object_markers = (
            "reading", "newspaper", "book", "phone", "smartphone", "clipboard",
            "camera", "letter", "menu", "map", "object held", "holding",
        )
        social_markers = (
            "conversation", "companions", "speaking", "talking", "greeting",
            "handshake", "interview", "small group", "another person",
        )
        travel_markers = (
            "driving", "bicycle", "cycling", "skateboard", "horse", "walking",
            "running", "moving through", "crossing",
        )
        if any(marker in action for marker in held_object_markers):
            return [
                "eyes focused on the object held in the hands",
                "eyes focused on the object held in the hands",
                "eyes focused on the object held in the hands",
                "eyes focused on a nearby object",
            ]
        if any(marker in action for marker in social_markers):
            return [
                "eyes focused on a nearby person",
                "eyes focused on a nearby person",
                "eyes focused just past the camera",
            ]
        if any(marker in action for marker in travel_markers):
            return [
                "eyes focused into the distance",
                "eyes focused into the distance",
                "eyes focused on a nearby object",
            ]
        return [
            "eyes focused directly on the camera",
            "eyes focused directly on the camera",
            "eyes focused just past the camera",
            "eyes focused on a nearby person",
            "eyes focused on a nearby object",
            "eyes focused into the distance",
            "eyes focused toward the subject's left",
            "eyes focused toward the subject's right",
        ]

    def _apply_custom_inputs(
        self,
        data,
        *,
        seed,
        eye_focus="None",
        mouth_expression="None",
        setting_text_override="",
        pose_text_override="",
        custom_color_overrides="",
        wildcard_subject="",
        wildcard_clothing="",
        wildcard_pose="",
        wildcard_setting="",
        wildcard_photography="",
    ):
        explicit = data.setdefault("_explicit_fields", set())

        for field, value in self._parse_custom_color_overrides(custom_color_overrides).items():
            data[field] = value
            explicit.add(field)

        subject_text = self._external_text(wildcard_subject)
        clothing_text = self._external_text(wildcard_clothing)
        photography_text = self._external_text(wildcard_photography)
        final_pose_text = self._external_text(pose_text_override) or self._external_text(wildcard_pose)
        final_setting_text = self._external_text(setting_text_override) or self._external_text(wildcard_setting)

        if subject_text:
            for field in SUBJECT_WILDCARD_CLEAR_FIELDS:
                data[field] = None
            extras = data.get("_identity_extras") or {}
            for group in ("Demographics", "Body", "Face", "Hair", "Makeup"):
                extras.pop(group, None)
            data["_identity_slots"] = {}
            data["_identity_is_creature"] = False
            data.pop("_identity_anchor", None)
            data["_external_subject_text"] = subject_text

        if clothing_text:
            for field in IDENTITY_OUTFIT_RANDOM_CLEAR_FIELDS | {"clothing_archetype"}:
                data[field] = None
            data.pop("_identity_outfit", None)
            (data.get("_identity_extras") or {}).pop("Clothing", None)
            data["_external_clothing_text"] = clothing_text

        if photography_text:
            for field in PHOTOGRAPHY_WILDCARD_CLEAR_FIELDS:
                data[field] = None
            data["_external_photography_text"] = photography_text

        if final_pose_text:
            data["scene_scenario"] = None
            data["pose"] = final_pose_text
            explicit.add("pose")
        if final_setting_text:
            data["scene_scenario"] = None
            data["setting"] = final_setting_text
            explicit.add("setting")

        selected_focus = self._external_text(eye_focus)
        archetype_focus = data.get("eye_focus")
        focus_is_explicit = False
        if selected_focus == "Forced Random":
            selected_focus = stable_choice(seed, "eye_focus__forced", EYE_FOCUS_VALUES)
            focus_is_explicit = True
        elif selected_focus == "Random":
            selected_focus = archetype_focus or stable_choice(seed, "eye_focus", self._eye_focus_pool(data))
        elif selected_focus in ("", "None"):
            selected_focus = archetype_focus
        else:
            focus_is_explicit = True
        if selected_focus:
            data["eye_focus"] = selected_focus
            if focus_is_explicit:
                explicit.add("eye_focus")

        selected_mouth = self._external_text(mouth_expression)
        if selected_mouth == "Random":
            pool = MOUTH_EXPRESSION_POOLS.get(data.get("expression"), MOUTH_EXPRESSION_VALUES)
            selected_mouth = stable_choice(seed, "mouth_expression", pool)
        elif selected_mouth == "Forced Random":
            selected_mouth = stable_choice(seed, "mouth_expression__forced", MOUTH_EXPRESSION_VALUES)
        elif selected_mouth in ("", "None"):
            selected_mouth = None
        if selected_mouth and not subject_text:
            data["mouth_expression"] = selected_mouth
            explicit.add("mouth_expression")

        return data

    def build_prompt(
        self,
        free_prompt="",
        free_prompt_position="After introduction",
        ethnicity_guidance=False,
        enhance_realism=False,
        species_mode="Human",
        enforce_portrait_framing=False,
        seed=0,
        control_after_generate="randomize",
        override_field="None",
        override_text="",
        identity_forge_json="",
        inspect_property="None",
        eye_focus="None",
        mouth_expression="None",
        setting_text_override="",
        pose_text_override="",
        face_hair_text_override="",
        custom_color_overrides="",
        wildcard_subject="",
        wildcard_clothing="",
        wildcard_pose="",
        wildcard_setting="",
        wildcard_photography="",
        **kwargs,
    ):
        ethnicity_guidance = is_enabled(ethnicity_guidance)
        raw_values = {item["key"]: kwargs.get(item["key"], "None") for item in SCHEMA["categories"]}
        resolution_kwargs = dict(kwargs)
        if any(self._external_text(value) for value in (
            setting_text_override, pose_text_override, wildcard_pose, wildcard_setting,
        )) or (
            override_field in {"pose", "setting"} and self._external_text(override_text)
        ):
            # A complete Scene scenario would otherwise clear Pose and Setting
            # before these category-specific external inputs can replace it.
            resolution_kwargs["scene_scenario"] = "None"

        # Free-form Pose and Photography sources are authoritative but cannot be
        # classified safely by this deterministic node.  Suspend the complete
        # recipe rather than pretending to understand their geometry.  A Setting
        # source alone remains fully compatible with Composition Archetype.
        composition_external_override = (
            any(self._external_text(value) for value in (
                pose_text_override, wildcard_pose, wildcard_photography,
            ))
            or (
                override_field in COMPOSITION_ARCHETYPE_CONTROL_FIELDS
                and self._external_text(override_text)
            )
        )
        if composition_external_override:
            resolution_kwargs["composition_archetype"] = "None"

        data = self._resolve_values(
            resolution_kwargs,
            seed=seed,
            ethnicity_guidance=ethnicity_guidance,
            eye_focus=eye_focus,
        )
        identity = self._parse_identity_forge_json(identity_forge_json)
        if identity:
            data = self._apply_identity_forge(data, identity, raw_values)
            if (
                raw_values.get("scene_scenario") == "Random"
                and {"pose", "setting"} & set(data.get("_identity_applied_fields") or ())
                ):
                # Imported authored context outranks only the optional ordinary
                # Random scenario branch. Manual and Forced Random scenarios
                # have already declared stronger intent and remain untouched.
                data["scene_scenario"] = None

        parsed_face_hair = self._parse_face_hair_text_override(face_hair_text_override)

        data = self._apply_custom_inputs(
            data,
            seed=seed,
            eye_focus=eye_focus,
            mouth_expression=mouth_expression,
            setting_text_override=setting_text_override,
            pose_text_override=pose_text_override,
            custom_color_overrides=custom_color_overrides,
            # Subject wildcard is an indivisible identity/appearance sentence.
            # A valid structured face source outranks it, so retaining both
            # would leave contradictory face or hair phrases in the prompt.
            wildcard_subject="" if parsed_face_hair is not None else wildcard_subject,
            wildcard_clothing=wildcard_clothing,
            wildcard_pose=wildcard_pose,
            wildcard_setting=wildcard_setting,
            wildcard_photography=wildcard_photography,
        )
        data = self._apply_face_hair_text_override(data, parsed_face_hair, raw_values)

        override_text = (override_text or "").strip().strip(",")
        valid_fields = {item["key"] for item in SCHEMA["categories"]}
        if override_field in valid_fields and override_text:
            # Applied after every random, guidance, compatibility, and framing
            # rule: a connected string is the user's final authority.
            for conflicting_field in MAIN_CLOTHING_OVERRIDE_CONFLICTS.get(override_field, ()):
                data[conflicting_field] = None
            if override_field in IDENTITY_MAIN_CLOTHING_FIELDS:
                data.pop("_identity_outfit", None)
            data[override_field] = override_text
            data.setdefault("_explicit_fields", set()).add(override_field)
            if override_field in {"pose", "setting"}:
                data["scene_scenario"] = None
            if override_field in SUBJECT_WILDCARD_CLEAR_FIELDS:
                data.pop("_external_subject_text", None)
            if override_field in IDENTITY_OUTFIT_RANDOM_CLEAR_FIELDS | {"clothing_archetype"}:
                data.pop("_external_clothing_text", None)
            if override_field in PHOTOGRAPHY_WILDCARD_CLEAR_FIELDS:
                data.pop("_external_photography_text", None)
        free_prompt = (free_prompt or "").strip().strip(",")
        enhance_realism = is_enabled(enhance_realism)
        effective_ethnicity_guidance = bool(
            ethnicity_guidance and not data.get("_face_hair_override_active")
        )

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

        identity_meta = data.get("_identity_meta") or {}
        leading_creature = bool(
            data.get("_identity_is_creature")
            and str(identity_meta.get("form") or "") in {"Anthropomorphic", "Feral"}
        )
        if leading_creature:
            explicit_fields = data.get("_explicit_fields") or set()
            imported_fields = data.get("_identity_applied_fields") or set()
            for field in CREATURE_ORGAN_DEPENDENT_FIELDS:
                if field not in explicit_fields and field not in imported_fields:
                    data[field] = None
            full_prompt = self._build_creature_prompt(
                data,
                free_prompt=free_prompt,
                free_prompt_position=free_prompt_position,
                enhance_realism=enhance_realism,
                ethnicity_guidance=effective_ethnicity_guidance,
            )
            face_prompt = self._build_creature_face_prompt(data)
        else:
            full_prompt = self._build_full_prompt(data, free_prompt=free_prompt, free_prompt_position=free_prompt_position, enhance_realism=enhance_realism, species_mode=species_mode, ethnicity_guidance=effective_ethnicity_guidance)
            face_prompt = self._build_face_prompt(data, species_mode=species_mode, ethnicity_guidance=effective_ethnicity_guidance)
        pre_gen_text = self._build_pre_gen_prompt(
            data,
            free_prompt=free_prompt,
            free_prompt_position=free_prompt_position,
            enhance_realism=enhance_realism,
            species_mode=species_mode,
            creature=leading_creature,
            enforce_portrait_framing=enforce_portrait_framing,
        )
        inspected_value = ""
        if inspect_property in valid_fields:
            value = data.get(inspect_property)
            inspected_value = "" if value is None else str(value)
        # Keep the three historical output indexes untouched.  Pre-gen Text is
        # appended so existing workflow links continue to target the same data.
        return (full_prompt, face_prompt, inspected_value, pre_gen_text)
