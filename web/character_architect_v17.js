// Character Architect frontend schema v17 / public v2.1.1.
import { app } from "../../scripts/app.js";

const RANDOM_PROTECTED_KEYS = new Set(["body_hair", "facial_hair", "skin_finish", "makeup_complexion", "accessories_scarf", "free_prompt_position", "clothing_archetype", "optical_effect", "override_field", "inspect_property"]);
const GLOBAL_PIVOT_KEYS = new Set(["ethnicity_guidance", "enhance_realism"]);
const ETHNICITY_GUIDED_RANDOM_KEYS = new Set([
    "face_shape", "jawline", "chin_shape", "eye_shape", "eye_color", "eyebrows",
    "nose_shape", "lip_shape", "hair_color", "hair_texture", "skin_finish",
]);
const DRESS_KEYS = ["dress_type", "dress_color"];
const SEPARATES_KEYS = ["top_type", "top_color", "bottom_type", "bottom_length", "bottom_color"];
const LINGERIE_KEYS = ["lingerie_type", "lingerie_color"];
const SLEEPWEAR_KEYS = ["sleepwear_type", "sleepwear_color"];
const COSPLAY_KEYS = ["cosplay_type", "cosplay_color"];
const FRANCHISE_WESTERN_KEYS = ["cosplay_franchise_western"];
const FRANCHISE_ASIAN_KEYS = ["cosplay_franchise_asian"];
const PRIMARY_CLOTHING_KEYS = [
    ...DRESS_KEYS,
    ...SEPARATES_KEYS,
    ...LINGERIE_KEYS,
    ...SLEEPWEAR_KEYS,
    ...COSPLAY_KEYS,
    ...FRANCHISE_WESTERN_KEYS,
    ...FRANCHISE_ASIAN_KEYS,
];
const BODY_CONTEXT_PORTRAIT_KEYS = new Set([
    "pose", "bottom_type", "dress_type", "sleepwear_type", "cosplay_type",
    "cosplay_franchise_western", "cosplay_franchise_asian", "hosiery", "footwear",
]);
const CLOSE_FRAMING_FOOTWEAR_SUPPRESSION = new Set([
    "close-up portrait", "headshot portrait", "bust portrait", "half-body portrait", "three-quarter portrait",
]);
const FOOTWEAR_RANDOM_PRESENCE_PERCENT = new Map([
    ["portrait", 10],
    ["full-body portrait", 50],
    ["full-body glamour portrait", 67],
]);
const DEFAULT_FOOTWEAR_RANDOM_PRESENCE_PERCENT = 20;
const BOTTOM_LENGTH_POOLS = new Map([
    ["jeans", ["mid-length", "long", "long"]],
    ["skinny jeans", ["mid-length", "long", "long"]],
    ["trousers", ["knee-length", "mid-length", "long", "long"]],
    ["wide-leg pants", ["mid-length", "long", "long"]],
    ["flared pants", ["long"]],
    ["cargo pants", ["knee-length", "mid-length", "long", "long"]],
    ["shorts", ["very short", "short", "short", "knee-length"]],
    ["denim shorts", ["very short", "short", "short", "knee-length"]],
    ["mini skirt", ["very short", "short"]],
    ["pleated skirt", ["very short", "short", "knee-length", "mid-length", "long"]],
    ["skater skirt", ["very short", "short", "knee-length", "mid-length"]],
    ["leggings", ["knee-length", "mid-length", "long", "long"]],
    ["joggers", ["mid-length", "long", "long"]],
    ["leather pants", ["mid-length", "long", "long"]],
    ["long skirt", ["mid-length", "long", "long"]],
]);
const NECKLINE_TYPES_BY_DEPTH = new Map([
    ["high neckline", ["crew neck", "halter neckline"]],
    ["modest neckline", ["crew neck", "scoop neck", "square neckline", "halter neckline"]],
    ["open neckline", ["scoop neck", "V-neck", "sweetheart neckline", "square neckline", "off-shoulder neckline", "halter neckline"]],
    ["low neckline", ["scoop neck", "V-neck", "sweetheart neckline", "square neckline", "off-shoulder neckline", "halter neckline", "plunging neckline"]],
    ["deep neckline", ["V-neck", "sweetheart neckline", "off-shoulder neckline", "plunging neckline"]],
]);
const SIMPLE_PHOTO_LIGHTING = [
    "soft studio lighting", "window light", "golden-hour light", "overcast daylight",
    "backlit glow", "rim lighting", "subdued low-key lighting with deep natural shadows",
];

// ComfyUI stores widget values positionally. The node is visually reordered below,
// so serialization must always use this backend/schema order rather than node.widgets order.
// Exact order used by the public v1.0 line. Keep it intact for migration.
const V15_CANONICAL_WIDGET_ORDER = [
    "media_type", "gender", "content_rating", "portrait_style", "setting", "lens_style", "shot_composition",
    "pose_mood", "pose", "camera_direction", "lighting_style", "optical_effect", "origin_age", "origin_ethnicity", "body_type",
    "body_physique", "body_feminine_curves", "body_hair", "skin_finish", "bust", "cleavage_depth",
    "cleavage_type", "butt_shape", "thigh_shape", "expression", "eye_expression", "face_shape", "jawline",
    "chin_shape", "eye_shape", "eye_color", "eyelashes", "eyebrows", "nose_shape", "lip_shape",
    "facial_hair", "hair_color", "hair_texture", "hair_style", "hair_cut", "hair_length", "bangs_style",
    "tattoo_style", "makeup_eye", "makeup_complexion", "makeup_lips", "nail_style", "clothing_archetype", "outfit_style",
    "top_type", "top_color", "bottom_type", "bottom_length", "bottom_color", "lingerie_type",
    "lingerie_color", "sleepwear_type", "sleepwear_color", "cosplay_type", "cosplay_franchise_western",
    "cosplay_franchise_asian", "cosplay_color", "hosiery", "hosiery_color", "dress_type", "dress_color", "outerwear", "outerwear_color", "belt", "belt_color",
    "footwear", "footwear_color", "head_accessory", "accessories_scarf", "accessories_jewelry",
    "accessories_necklace", "accessories_earrings", "accessories_bracelet", "accessories_rings",
    "accessories_glasses", "armwear", "accessories_bag", "lock_media_type", "lock_gender",
    "lock_content_rating", "ethnicity_guidance", "enhance_realism", "species_mode", "enforce_single_subject",
    "seed", "control_after_generate", "free_prompt", "free_prompt_position",
];

const CANONICAL_WIDGET_ORDER = V15_CANONICAL_WIDGET_ORDER.filter(
    (name) => name !== "enforce_single_subject",
);
CANONICAL_WIDGET_ORDER.splice(
    CANONICAL_WIDGET_ORDER.indexOf("outerwear_color") + 1,
    0,
    "outerwear_wearing_style",
);
CANONICAL_WIDGET_ORDER.push("override_field", "inspect_property");

// Exact canonical order used before hosiery, outerwear, and belt colors were
// added. Its 90 positional values restore by name before new defaults apply.
const PRE_SECONDARY_GARMENT_COLORS_CANONICAL_WIDGET_ORDER = V15_CANONICAL_WIDGET_ORDER.filter(
    (name) => !["hosiery_color", "outerwear_color", "belt_color"].includes(name),
);

// Exact canonical order used immediately before optical_effect was added.
// Workflows saved by that release contain 89 positional values; restoring them
// by this map prevents every later widget from shifting by one position.
const PRE_OPTICAL_EFFECT_CANONICAL_WIDGET_ORDER = PRE_SECONDARY_GARMENT_COLORS_CANONICAL_WIDGET_ORDER.filter(
    (name) => name !== "optical_effect",
);

// Exact canonical order used by v8, before clothing_archetype was introduced.
const V8_CANONICAL_WIDGET_ORDER = [
    "media_type", "gender", "content_rating", "portrait_style", "setting", "lens_style", "shot_composition",
    "pose_mood", "pose", "camera_direction", "lighting_style", "origin_age", "origin_ethnicity", "body_type",
    "body_physique", "body_feminine_curves", "body_hair", "skin_finish", "bust", "cleavage_depth",
    "cleavage_type", "butt_shape", "thigh_shape", "expression", "eye_expression", "face_shape", "jawline",
    "chin_shape", "eye_shape", "eye_color", "eyelashes", "eyebrows", "nose_shape", "lip_shape",
    "facial_hair", "hair_color", "hair_texture", "hair_style", "hair_cut", "hair_length", "bangs_style",
    "tattoo_style", "makeup_eye", "makeup_complexion", "makeup_lips", "nail_style", "outfit_style",
    "top_type", "top_color", "bottom_type", "bottom_length", "bottom_color", "lingerie_type",
    "lingerie_color", "sleepwear_type", "sleepwear_color", "cosplay_type", "cosplay_franchise_western",
    "cosplay_franchise_asian", "cosplay_color", "hosiery", "dress_type", "dress_color", "outerwear", "belt",
    "footwear", "footwear_color", "head_accessory", "accessories_scarf", "accessories_jewelry",
    "accessories_necklace", "accessories_earrings", "accessories_bracelet", "accessories_rings",
    "accessories_glasses", "armwear", "accessories_bag", "lock_media_type", "lock_gender",
    "lock_content_rating", "ethnicity_guidance", "enhance_realism", "species_mode", "enforce_single_subject",
    "seed", "control_after_generate", "free_prompt", "free_prompt_position",
];

// Exact canonical order used by v7, before pose, bottom_length, and
// ethnicity_guidance were introduced.
const V7_CANONICAL_WIDGET_ORDER = [
    "media_type", "gender", "content_rating", "portrait_style", "setting", "lens_style", "shot_composition",
    "pose_mood", "camera_direction", "lighting_style", "origin_age", "origin_ethnicity", "body_type",
    "body_physique", "body_feminine_curves", "body_hair", "skin_finish", "bust", "cleavage_depth",
    "cleavage_type", "butt_shape", "thigh_shape", "expression", "eye_expression", "face_shape", "jawline",
    "chin_shape", "eye_shape", "eye_color", "eyelashes", "eyebrows", "nose_shape", "lip_shape",
    "facial_hair", "hair_color", "hair_texture", "hair_style", "hair_cut", "hair_length", "bangs_style",
    "tattoo_style", "makeup_eye", "makeup_complexion", "makeup_lips", "nail_style", "outfit_style",
    "top_type", "top_color", "bottom_type", "bottom_color", "lingerie_type", "lingerie_color",
    "sleepwear_type", "sleepwear_color", "cosplay_type", "cosplay_franchise_western",
    "cosplay_franchise_asian", "cosplay_color", "hosiery", "dress_type", "dress_color", "outerwear", "belt",
    "footwear", "footwear_color", "head_accessory", "accessories_scarf", "accessories_jewelry",
    "accessories_necklace", "accessories_earrings", "accessories_bracelet", "accessories_rings",
    "accessories_glasses", "armwear", "accessories_bag", "lock_media_type", "lock_gender",
    "lock_content_rating", "enhance_realism", "species_mode", "enforce_single_subject", "seed",
    "control_after_generate", "free_prompt", "free_prompt_position",
];

// Canonical order used by the release immediately before sleepwear fields.
const PRE_SLEEPWEAR_CANONICAL_WIDGET_ORDER = V7_CANONICAL_WIDGET_ORDER.filter(
    (name) => !SLEEPWEAR_KEYS.includes(name),
);

// Older canonical releases predate both sleepwear and the former furry enhancer field.
const PRE_FURRY_PRE_SLEEPWEAR_CANONICAL_WIDGET_ORDER = V7_CANONICAL_WIDGET_ORDER.filter(
    (name) => !SLEEPWEAR_KEYS.includes(name) && name !== "species_mode",
);

// Very early canonical release, before the optional single-subject trigger.
const PRE_SINGLE_SUBJECT_CANONICAL_WIDGET_ORDER = V7_CANONICAL_WIDGET_ORDER.filter(
    (name) => !SLEEPWEAR_KEYS.includes(name)
        && name !== "species_mode"
        && name !== "enforce_single_subject",
);

// Previous releases serialized the visually reordered widgets. This map repairs those
// workflows once, then future saves use CANONICAL_WIDGET_ORDER.
const LEGACY_VISUAL_WIDGET_ORDER = [
    "media_type", "lock_media_type", "gender", "lock_gender", "content_rating",
    "lock_content_rating", "enhance_realism", "species_mode", "seed", "control_after_generate",
    "portrait_style", "setting", "lens_style", "shot_composition", "pose_mood",
    "camera_direction", "lighting_style", "origin_age", "origin_ethnicity", "body_type",
    "body_physique", "body_feminine_curves", "skin_finish", "bust", "cleavage_depth",
    "cleavage_type", "butt_shape", "thigh_shape", "body_hair", "expression", "eye_expression",
    "face_shape", "jawline", "chin_shape", "eye_shape", "eye_color", "eyelashes", "eyebrows",
    "nose_shape", "lip_shape", "facial_hair", "hair_color", "hair_texture", "hair_style",
    "hair_cut", "hair_length", "bangs_style", "tattoo_style", "makeup_eye",
    "makeup_complexion", "makeup_lips", "nail_style", "outfit_style", "top_type", "top_color",
    "bottom_type", "bottom_color", "lingerie_type", "lingerie_color", "cosplay_type",
    "cosplay_color", "cosplay_franchise_western", "cosplay_franchise_asian", "hosiery",
    "dress_type", "dress_color", "outerwear", "belt", "footwear", "footwear_color",
    "head_accessory", "accessories_scarf", "accessories_jewelry", "accessories_necklace",
    "accessories_earrings", "accessories_bracelet", "accessories_rings", "accessories_glasses", "armwear", "accessories_bag",
    "free_prompt", "free_prompt_position",
];

const GROUPS = [
    { id: "all", label: "ALL CATEGORIES", keys: "*" },
    {
        id: "composition",
        label: "COMPOSITION",
        keys: ["portrait_style", "setting", "lens_style", "shot_composition", "pose_mood", "pose", "camera_direction", "lighting_style", "optical_effect"],
    },
    {
        id: "body",
        label: "BODY",
        keys: ["origin_age", "origin_ethnicity", "body_type", "body_physique", "body_feminine_curves"],
    },
    {
        id: "body_specific",
        label: "BODY SPECIFIC",
        keys: ["bust", "cleavage_depth", "cleavage_type", "butt_shape", "thigh_shape", "body_hair", "skin_finish"],
    },
    {
        id: "face",
        label: "FACE",
        keys: ["expression", "eye_expression", "face_shape", "jawline", "chin_shape", "eye_shape", "eye_color", "eyelashes", "eyebrows", "nose_shape", "lip_shape", "facial_hair"],
    },
    {
        id: "hair",
        label: "HAIR",
        keys: ["hair_color", "hair_texture", "hair_style", "hair_cut", "hair_length", "bangs_style"],
    },
    {
        id: "tattoos_makeup",
        label: "TATTOOS / MAKE-UP",
        keys: ["tattoo_style", "makeup_eye", "makeup_lips", "nail_style", "makeup_complexion"],
    },
    {
        id: "clothes_shoes",
        label: "CLOTHES, SLEEPWEAR, COSPLAY AND SHOES",
        keys: [
            "clothing_archetype", "outfit_style", "top_type", "top_color", "bottom_type", "bottom_length", "bottom_color",
            "lingerie_type", "lingerie_color", "sleepwear_type", "sleepwear_color", "cosplay_type", "cosplay_color",
            "cosplay_franchise_western", "cosplay_franchise_asian", "hosiery", "hosiery_color",
            "dress_type", "dress_color", "outerwear", "outerwear_color", "outerwear_wearing_style", "belt", "belt_color", "footwear", "footwear_color",
        ],
    },
    {
        id: "accessories",
        label: "ACCESSORIES",
        keys: ["head_accessory", "accessories_glasses", "armwear", "accessories_jewelry", "accessories_necklace", "accessories_earrings", "accessories_bracelet", "accessories_rings", "accessories_bag", "accessories_scarf"],
    },
    {
        id: "override_inspection",
        label: "OVERRIDE AND INSPECTION",
        keys: ["override_field", "inspect_property"],
    },
];

const SECTION_TOOLTIPS = {
    all: "Global controls affect every unlocked category. Pivot locks protect Media type, Gender, and Content rating; protected fields and the seed are not overwritten. RANDOMIZE ALL ONCE creates manual concrete choices, so those choices intentionally override guidance rules.",
    composition: "Image-level controls: framing, environment, pose, camera, lighting, and optical treatment. Ordinary Random softens only a few known harsh photographic collisions and preserves 20% wild combinations. Optical Effect is written before Media type.",
    body: "General identity, stature, weight, fitness, and curves. Body type and Body physique are independent so combinations such as very petite + plump remain possible.",
    body_specific: "Detailed morphology, body hair, and skin. Ordinary Random favors compatible neckline depth/type pairs 90% of the time. Body hair and skin finish stay protected from one-click randomization.",
    face: "Facial structure and expression. Ethnicity Guidance can constrain compatible Random traits; explicit manual values always win.",
    hair: "Hair color, texture, style, cut, length, and bangs remain combinable. Ordinary Random softens only the clearest structural clashes 75% of the time, preserving experimental undercuts and mixed constructions.",
    tattoos_makeup: "Independent tattoo, makeup, and nail controls. Random nails are silently removed when full hand-covering gloves are detected.",
    clothes_shoes: "Main garment families are mutually exclusive for ordinary Random. Hidden bottom-length pools favor workable pairs 85% of the time without banning unusual combinations. Cosplay protection, manual choices, Forced Random, and override retain their established priority.",
    accessories: "Optional additions guided by clothing archetypes. Ordinary Random presence is 33% for glasses and 40% for bags. Scarves remain protected from one-click randomization; when deliberately set to Random they appear about 30% of the time.",
    override_inspection: "A connected Override text replaces the selected field after every other rule. Inspect property exposes one final resolved value through the dedicated output for overlays, comparisons, and statistics.",
};

function getLockStore(node) {
    if (!node.properties) node.properties = {};
    if (!node.properties.cpf_group_locks) node.properties.cpf_group_locks = {};
    return node.properties.cpf_group_locks;
}

function isGroupLocked(node, groupId) {
    if (!groupId || groupId === "all") return false;
    return !!getLockStore(node)[groupId];
}

function setGroupLocked(node, groupId, locked) {
    if (!groupId || groupId === "all") return;
    getLockStore(node)[groupId] = !!locked;
    node.setDirtyCanvas(true, true);
    app.graph.setDirtyCanvas(true, true);
}

function toggleGroupLocked(node, groupId) {
    setGroupLocked(node, groupId, !isGroupLocked(node, groupId));
}

function getLockedGroupKeySet(node) {
    const keySet = new Set();
    for (const group of GROUPS) {
        if (group.id !== "all" && isGroupLocked(node, group.id)) {
            for (const key of group.keys) keySet.add(key);
        }
    }
    return keySet;
}

function concreteValues(widget) {
    const values = widget?.options?.values;
    if (!Array.isArray(values)) return [];
    return values.filter(
        (value) => value !== "None" && value !== "Random" && value !== "Forced Random"
    );
}

function setWidgetValue(widget, value) {
    if (!widget) return false;
    widget.value = value;
    widget.callback?.(value, app.canvas, widget.node, widget);
    return true;
}

function chooseVisibleRandomValue(widget) {
    const values = concreteValues(widget);
    if (!values.length) return false;
    if (widget.name === "optical_effect" && Math.random() < 0.70) {
        setWidgetValue(widget, "None");
        return true;
    }
    if (widget.name === "accessories_glasses") {
        if (Math.random() < 0.67) {
            setWidgetValue(widget, "no glasses");
            return true;
        }
        const glasses = values.filter((value) => value !== "no glasses");
        if (!glasses.length) return setWidgetValue(widget, "no glasses");
        setWidgetValue(widget, glasses[Math.floor(Math.random() * glasses.length)]);
        return true;
    }
    if (widget.name === "accessories_bag" || widget.name === "accessories_scarf") {
        const isBag = widget.name === "accessories_bag";
        const absentValue = isBag ? "no bag" : "no scarf";
        const presenceChance = isBag ? 0.40 : 0.30;
        if (Math.random() >= presenceChance) return setWidgetValue(widget, absentValue);
        const presentValues = values.filter((value) => value !== absentValue);
        if (!presentValues.length) return setWidgetValue(widget, absentValue);
        return setWidgetValue(widget, presentValues[Math.floor(Math.random() * presentValues.length)]);
    }
    if (widget.name === "outerwear_wearing_style") {
        const outerwear = widget.node ? widgetMap(widget.node).get("outerwear")?.value : null;
        if (outerwear === "cape") {
            const capeChoices = [
                ...Array(60).fill("Properly worn"),
                ...Array(15).fill("Draped over shoulders"),
                ...Array(10).fill("Carried over one shoulder"),
            ];
            return setWidgetValue(widget, capeChoices[Math.floor(Math.random() * capeChoices.length)]);
        }
        const roll = Math.random();
        let choice = "Properly worn";
        if (roll >= 0.60 && roll < 0.75) choice = "Draped over shoulders";
        else if (roll >= 0.75 && roll < 0.90) choice = "Off shoulders at elbows";
        else if (roll >= 0.90) choice = "Carried over one shoulder";
        return setWidgetValue(widget, choice);
    }
    if (widget.name === "portrait_style" && hasBodyVisibilityPressure(widget.node)) {
        const weighted = [];
        for (const value of values) {
            const weight = ["close-up portrait", "headshot portrait"].includes(value) ? 1 : 3;
            for (let index = 0; index < weight; index += 1) weighted.push(value);
        }
        return setWidgetValue(widget, weighted[Math.floor(Math.random() * weighted.length)]);
    }
    let candidates = values;
    if (values.length > 1 && values.includes(widget.value)) {
        candidates = values.filter((value) => value !== widget.value);
    }
    const chosen = candidates[Math.floor(Math.random() * candidates.length)];
    setWidgetValue(widget, chosen);
    return true;
}

function chooseFrom(values) {
    return values[Math.floor(Math.random() * values.length)];
}

function applySoftRandomCoherenceOnce(node, keySet, lockedGroupKeys) {
    const byName = widgetMap(node);
    const randomized = (key) => keySet ? keySet.has(key) : !lockedGroupKeys.has(key);

    if (Math.random() < 0.90) {
        const depthWidget = byName.get("cleavage_depth");
        const typeWidget = byName.get("cleavage_type");
        const compatibleTypes = NECKLINE_TYPES_BY_DEPTH.get(depthWidget?.value);
        if (randomized("cleavage_type") && compatibleTypes?.length) {
            setWidgetValue(typeWidget, chooseFrom(compatibleTypes));
        } else if (randomized("cleavage_depth") && typeWidget?.value) {
            const compatibleDepths = [...NECKLINE_TYPES_BY_DEPTH.entries()]
                .filter(([, types]) => types.includes(typeWidget.value))
                .map(([depth]) => depth);
            if (compatibleDepths.length) setWidgetValue(depthWidget, chooseFrom(compatibleDepths));
        }
    }

    if (Math.random() < 0.85) {
        const typeWidget = byName.get("bottom_type");
        const lengthWidget = byName.get("bottom_length");
        const compatibleLengths = BOTTOM_LENGTH_POOLS.get(typeWidget?.value);
        if (randomized("bottom_length") && compatibleLengths?.length) {
            setWidgetValue(lengthWidget, chooseFrom(compatibleLengths));
        } else if (randomized("bottom_type") && lengthWidget?.value) {
            const compatibleTypes = [...BOTTOM_LENGTH_POOLS.entries()]
                .filter(([, lengths]) => lengths.includes(lengthWidget.value))
                .map(([type]) => type);
            if (compatibleTypes.length) setWidgetValue(typeWidget, chooseFrom(compatibleTypes));
        }
    }

    if (Math.random() < 0.75) applySoftHairCoherenceOnce(byName, randomized);
    if (Math.random() < 0.80) applySoftPhotoCoherenceOnce(byName, randomized);
    applyCosplayDetailCoherenceOnce(byName, randomized);
}

function applyCosplayDetailCoherenceOnce(byName, randomized) {
    const cosplayText = ["cosplay_type", "cosplay_franchise_western", "cosplay_franchise_asian"]
        .map((key) => byName.get(key)?.value)
        .filter((value) => value && value !== "None" && value !== "Random" && value !== "Forced Random")
        .join(" ")
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, " ")
        .trim();
    if (!cosplayText) return;
    const padded = ` ${cosplayText} `;
    const hasTerm = (terms) => terms.some((term) => padded.includes(` ${term} `));

    if (randomized("head_accessory") && hasTerm([
        "cap", "caps", "hat", "hats", "helmet", "helmets", "hood", "hoods",
        "crown", "crowns", "tiara", "veil", "bonnet", "headpiece", "headdress",
        "halo", "horns", "cat ears", "bunny ears", "animal ears",
    ])) {
        setWidgetValue(byName.get("head_accessory"), "None");
    }

    if (randomized("cleavage_type")
        && ["halter neckline", "off-shoulder neckline"].includes(byName.get("cleavage_type")?.value)
        && hasTerm(["jacket", "jackets", "coat", "coats", "blazer", "blazers", "uniform", "uniforms", "robe", "robes", "long sleeved", "sleeves"])) {
        setWidgetValue(byName.get("cleavage_type"), "None");
    }
}

function applySoftHairCoherenceOnce(byName, randomized) {
    const styleWidget = byName.get("hair_style");
    const cutWidget = byName.get("hair_cut");
    const lengthWidget = byName.get("hair_length");
    const textureWidget = byName.get("hair_texture");
    const bangsWidget = byName.get("bangs_style");
    const shortLengths = new Set(["cropped hair", "short hair", "chin-length hair"]);
    const longLengths = new Set(["medium-long hair", "long hair", "very long hair", "waist-length hair"]);
    const lengthStyles = new Set([
        "braided hair", "dreadlocks", "twin braids", "French braid", "high ponytail",
        "low ponytail", "high bun", "low bun", "space buns",
    ]);

    if (lengthStyles.has(styleWidget?.value) && shortLengths.has(lengthWidget?.value)) {
        if (randomized("hair_length")) {
            setWidgetValue(lengthWidget, chooseFrom(["shoulder-length hair", "medium-long hair", "long hair", "very long hair"]));
        } else if (randomized("hair_style")) {
            const choices = concreteValues(styleWidget).filter((value) => !lengthStyles.has(value));
            if (choices.length) setWidgetValue(styleWidget, chooseFrom(choices));
        }
    }

    const compactCuts = new Set(["pixie cut", "fade haircut", "buzz cut", "crew cut"]);
    if (compactCuts.has(cutWidget?.value) && longLengths.has(lengthWidget?.value)) {
        if (randomized("hair_length")) {
            setWidgetValue(lengthWidget, chooseFrom(["cropped hair", "short hair", "chin-length hair"]));
        } else if (randomized("hair_cut")) {
            const choices = concreteValues(cutWidget).filter((value) => !compactCuts.has(value));
            if (choices.length) setWidgetValue(cutWidget, chooseFrom(choices));
        }
    }

    const curlyTextures = new Set(["curly", "tightly curled", "coily"]);
    if (curlyTextures.has(textureWidget?.value) && styleWidget?.value === "sleek straight styling") {
        if (randomized("hair_style")) {
            setWidgetValue(styleWidget, chooseFrom(["loose hair", "defined curls", "messy textured styling", "braided hair", "dreadlocks", "high ponytail", "low ponytail", "high bun", "low bun"]));
        } else if (randomized("hair_texture")) {
            setWidgetValue(textureWidget, chooseFrom(["straight", "silky straight", "slightly wavy"]));
        }
    }

    if (bangsWidget?.value === "long face-framing bangs" && lengthWidget?.value === "cropped hair" && randomized("bangs_style")) {
        setWidgetValue(bangsWidget, chooseFrom(["no bangs", "micro bangs", "straight bangs", "side-swept bangs", "wispy bangs", "choppy bangs"]));
    }

    if (randomized("head_accessory")
        && ["braided hair", "dreadlocks", "twin braids", "French braid"].includes(styleWidget?.value)
        && Math.random() < 0.20) {
        setWidgetValue(byName.get("head_accessory"), "decorative metal braid and loc cuffs");
    }
}

function applySoftPhotoCoherenceOnce(byName, randomized) {
    if (!randomized("lighting_style")) return;
    const effect = byName.get("optical_effect")?.value;
    const lens = byName.get("lens_style")?.value;
    const lighting = byName.get("lighting_style")?.value;
    const harshForDuotone = new Set(["hard flash", "split lighting", "neon lighting", "colored gel lighting", "dramatic chiaroscuro lighting with sculpted highlights and deep shadows"]);
    const coloredForInfrared = new Set(["neon lighting", "colored gel lighting"]);
    const sculptedForLofi = new Set(["dramatic studio lighting", "split lighting", "dramatic chiaroscuro lighting with sculpted highlights and deep shadows", "colored gel lighting"]);
    const conflict = (effect === "high-contrast duotone" && harshForDuotone.has(lighting))
        || (effect === "infrared false-color" && coloredForInfrared.has(lighting))
        || (["disposable camera look", "cheap digital camera aesthetic"].includes(lens) && sculptedForLofi.has(lighting));
    if (conflict) setWidgetValue(byName.get("lighting_style"), chooseFrom(SIMPLE_PHOTO_LIGHTING));
}

function hasBodyVisibilityPressure(node) {
    if (!node) return false;
    const byName = widgetMap(node);
    for (const key of BODY_CONTEXT_PORTRAIT_KEYS) {
        const value = byName.get(key)?.value;
        if (value !== undefined && value !== null && value !== "None") return true;
    }
    return false;
}

function hasCloseFootwearSuppressingFraming(node) {
    const byName = widgetMap(node);
    return CLOSE_FRAMING_FOOTWEAR_SUPPRESSION.has(byName.get("portrait_style")?.value)
        || byName.get("shot_composition")?.value === "tight crop";
}

function keepOrdinaryRandomFootwearForFraming(node) {
    if (hasCloseFootwearSuppressingFraming(node)) return false;
    const portrait = widgetMap(node).get("portrait_style")?.value;
    const percent = FOOTWEAR_RANDOM_PRESENCE_PERCENT.get(portrait)
        ?? DEFAULT_FOOTWEAR_RANDOM_PRESENCE_PERCENT;
    return Math.random() * 100 < percent;
}

function hasActiveEthnicityGuidance(node) {
    const byName = widgetMap(node);
    const enabled = !!byName.get("ethnicity_guidance")?.value;
    const ethnicity = byName.get("origin_ethnicity")?.value;
    return enabled && ethnicity !== undefined && ethnicity !== null && ethnicity !== "None";
}

function isPivotLocked(node, widgetName) {
    const byName = widgetMap(node);
    if (widgetName === "media_type") return !!byName.get("lock_media_type")?.value;
    if (widgetName === "gender") return !!byName.get("lock_gender")?.value;
    if (widgetName === "content_rating") return !!byName.get("lock_content_rating")?.value;
    return false;
}

function applyClothingExclusivityOnce(node, keySet) {
    const widgetsByName = new Map((node.widgets || []).filter((w) => w?.name).map((w) => [w.name, w]));
    const modes = [
        ["dress", DRESS_KEYS],
        ["separates", SEPARATES_KEYS],
        ["lingerie", LINGERIE_KEYS],
        ["sleepwear", SLEEPWEAR_KEYS],
        ["cosplay", [...COSPLAY_KEYS, ...FRANCHISE_WESTERN_KEYS, ...FRANCHISE_ASIAN_KEYS]],
    ].filter(([, keys]) => !keySet || keys.some((key) => keySet.has(key)));

    if (!modes.length) return;
    const [chosenName, chosenKeys] = modes[Math.floor(Math.random() * modes.length)];
    for (const [modeName, keys] of modes) {
        if (modeName === chosenName) {
            if (modeName === "cosplay") {
                const sources = [COSPLAY_KEYS, FRANCHISE_WESTERN_KEYS, FRANCHISE_ASIAN_KEYS];
                const chosenSource = sources[Math.floor(Math.random() * sources.length)];
                for (const sourceKeys of sources) {
                    sourceKeys.forEach((key) => {
                        if (chosenSource === sourceKeys) chooseVisibleRandomValue(widgetsByName.get(key));
                        else setWidgetValue(widgetsByName.get(key), "None");
                    });
                }
            } else {
                keys.forEach((key) => chooseVisibleRandomValue(widgetsByName.get(key)));
            }
        } else {
            keys.forEach((key) => setWidgetValue(widgetsByName.get(key), "None"));
        }
    }
}

function randomizeKeysOnce(node, keys) {
    const keySet = keys === "*" ? null : new Set(keys);
    const lockedGroupKeys = !keySet ? getLockedGroupKeySet(node) : null;

    const guidedEthnicity = hasActiveEthnicityGuidance(node);
    const portraitEligible = (!keySet || keySet.has("portrait_style"))
        && !(!keySet && lockedGroupKeys.has("portrait_style"));
    for (const widget of node.widgets || []) {
        if (!widget || widget.type === "cpf-section") continue;
        if (RANDOM_PROTECTED_KEYS.has(widget.name)) continue;
        if (guidedEthnicity && ETHNICITY_GUIDED_RANDOM_KEYS.has(widget.name)) continue;
        if (keySet && !keySet.has(widget.name)) continue;
        if (!keySet && lockedGroupKeys.has(widget.name)) continue;
        if (!keySet && (GLOBAL_PIVOT_KEYS.has(widget.name) || isPivotLocked(node, widget.name))) continue;
        if (widget.name?.startsWith("lock_")) continue;
        if (PRIMARY_CLOTHING_KEYS.includes(widget.name)) continue;
        if (["free_prompt", "seed", "control_after_generate"].includes(widget.name)) continue;
        chooseVisibleRandomValue(widget);
    }

    const clothingGroupLocked = !keySet && isGroupLocked(node, "clothes_shoes");
    if (!clothingGroupLocked) applyClothingExclusivityOnce(node, keySet);
    applySoftRandomCoherenceOnce(node, keySet, lockedGroupKeys);
    // Global one-shot randomization chooses clothing after the regular loop.
    // Re-resolve the portrait once so newly selected body-level details can
    // apply the same close-up/headshot weighting as backend Random.
    if (portraitEligible && hasBodyVisibilityPressure(node)) {
        chooseVisibleRandomValue(widgetMap(node).get("portrait_style"));
    }
    const footwearWasRandomized = !clothingGroupLocked
        && (!keySet || keySet.has("footwear") || keySet.has("footwear_color"));
    if (footwearWasRandomized && !keepOrdinaryRandomFootwearForFraming(node)) {
        const byName = widgetMap(node);
        if (!keySet || keySet.has("footwear")) setWidgetValue(byName.get("footwear"), "None");
        if (!keySet || keySet.has("footwear_color")) setWidgetValue(byName.get("footwear_color"), "None");
    }

    node.setDirtyCanvas(true, true);
    app.graph.setDirtyCanvas(true, true);
}

function setKeysToRandom(node, keys) {
    const keySet = keys === "*" ? null : new Set(keys);
    const lockedGroupKeys = !keySet ? getLockedGroupKeySet(node) : null;

    for (const widget of node.widgets || []) {
        if (!widget || widget.type === "cpf-section") continue;
        if (RANDOM_PROTECTED_KEYS.has(widget.name)) continue;
        if (keySet && !keySet.has(widget.name)) continue;
        if (!keySet && lockedGroupKeys.has(widget.name)) continue;
        if (!keySet && (GLOBAL_PIVOT_KEYS.has(widget.name) || isPivotLocked(node, widget.name))) continue;
        if (widget.name?.startsWith("lock_")) continue;
        if (["free_prompt", "seed", "control_after_generate", "override_field", "inspect_property"].includes(widget.name)) continue;
        const values = widget?.options?.values;
        if (Array.isArray(values) && values.includes("Random")) {
            setWidgetValue(widget, "Random");
        }
    }

    node.setDirtyCanvas(true, true);
    app.graph.setDirtyCanvas(true, true);
}

function resetWidgets(node, keys = null) {
    const keySet = keys ? new Set(keys) : null;
    const lockedGroupKeys = !keySet ? getLockedGroupKeySet(node) : null;

    for (const widget of node.widgets || []) {
        if (!widget || widget.type === "cpf-section") continue;
        if (widget.name?.startsWith("lock_")) continue;
        if (keySet && !keySet.has(widget.name)) continue;
        if (!keySet && lockedGroupKeys.has(widget.name)) continue;
        if (!keySet && (GLOBAL_PIVOT_KEYS.has(widget.name) || isPivotLocked(node, widget.name))) continue;

        if (widget.name === "free_prompt") {
            setWidgetValue(widget, "");
            continue;
        }
        if (widget.name === "free_prompt_position") {
            setWidgetValue(widget, "After introduction");
            continue;
        }
        if (widget.name === "species_mode") {
            setWidgetValue(widget, "Human");
            continue;
        }
        if (["seed", "control_after_generate"].includes(widget.name)) continue;

        const values = widget?.options?.values;
        if (Array.isArray(values) && values.includes("None")) {
            setWidgetValue(widget, "None");
        }
    }
    node.setDirtyCanvas(true, true);
    app.graph.setDirtyCanvas(true, true);
}

function createSectionWidget(node, group) {
    const tooltip = SECTION_TOOLTIPS[group.id] || "";
    const widget = {
        type: "cpf-section",
        name: `cpf_section_${group.id}`,
        value: group.label,
        tooltip,
        options: { serialize: false, tooltip },
        // Reserve most of the extra space above the header so each section
        // visually belongs to the widgets that follow it.
        computeSize(width) { return [width, 52]; },
        draw(ctx, targetNode, width, y, height) {
            const margin = 6;
            // Some ComfyUI frontend versions pass the default widget height
            // here instead of the height returned by computeSize(). Never use
            // that argument to size the custom header: doing so collapses the
            // panel and its buttons into a thin line.
            const boxY = y + 11;
            const boxH = 38;
            const gap = 5;
            const isAll = group.id === "all";
            const onceW = 142;
            const setW = 116;
            const resetW = 112;
            const lockW = isAll ? 0 : 70;
            const rightEdge = width - margin;
            const resetX = rightEdge - resetW;
            const setX = resetX - gap - setW;
            const onceX = setX - gap - onceW;
            const lockX = isAll ? null : onceX - gap - lockW;

            ctx.save();
            ctx.fillStyle = "rgba(28, 31, 40, 0.96)";
            ctx.strokeStyle = "rgba(137, 180, 255, 0.9)";
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.roundRect(margin, boxY, width - margin * 2, boxH, 6);
            ctx.fill();
            ctx.stroke();

            ctx.fillStyle = "#f1f5ff";
            ctx.font = "bold 13px sans-serif";
            ctx.textAlign = "left";
            ctx.textBaseline = "middle";
            ctx.fillText(group.label, margin + 10, boxY + boxH / 2);

            const drawButton = (x, w, label, fill, fontSize = 10) => {
                ctx.fillStyle = fill;
                ctx.strokeStyle = "rgba(172, 204, 255, 0.95)";
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.roundRect(x, boxY + 4, w, boxH - 8, 5);
                ctx.fill();
                ctx.stroke();
                ctx.fillStyle = "#ffffff";
                ctx.font = `bold ${fontSize}px sans-serif`;
                ctx.textAlign = "center";
                ctx.fillText(label, x + w / 2, boxY + boxH / 2);
            };

            if (!isAll) {
                const locked = isGroupLocked(node, group.id);
                drawButton(lockX, lockW, locked ? "LOCKED" : "LOCK", locked ? "rgba(181, 103, 45, 0.94)" : "rgba(201, 132, 55, 0.88)", 10);
                widget._lockButtonBounds = { x: lockX, y: boxY + 4, w: lockW, h: boxH - 8 };
            } else {
                widget._lockButtonBounds = null;
            }

            drawButton(onceX, onceW, "RANDOMIZE ALL ONCE", "rgba(75, 145, 67, 0.92)", 9);
            drawButton(setX, setW, "SET ALL RANDOM", "rgba(181, 92, 48, 0.92)", 9);
            drawButton(resetX, resetW, "RESET TO NONE", "rgba(174, 43, 61, 0.94)", 9);

            widget._onceButtonBounds = { x: onceX, y: boxY + 4, w: onceW, h: boxH - 8 };
            widget._setRandomButtonBounds = { x: setX, y: boxY + 4, w: setW, h: boxH - 8 };
            widget._resetButtonBounds = { x: resetX, y: boxY + 4, w: resetW, h: boxH - 8 };
            ctx.restore();
        },
        mouse(event, pos) {
            if (event.type !== "pointerdown" && event.type !== "mousedown") return false;
            const hit = (bounds) => {
                if (!bounds) return false;
                const localX = pos[0];
                const localY = pos[1];
                const yHit = (localY >= bounds.y && localY <= bounds.y + bounds.h) || (localY >= 4 && localY <= bounds.h + 4);
                return localX >= bounds.x && localX <= bounds.x + bounds.w && yHit;
            };
            if (hit(widget._lockButtonBounds)) {
                toggleGroupLocked(node, group.id);
                return true;
            }
            if (hit(widget._onceButtonBounds)) {
                randomizeKeysOnce(node, group.keys);
                return true;
            }
            if (hit(widget._setRandomButtonBounds)) {
                setKeysToRandom(node, group.keys);
                return true;
            }
            if (hit(widget._resetButtonBounds)) {
                resetWidgets(node, group.keys === "*" ? null : group.keys);
                return true;
            }
            return false;
        },
    };
    return widget;
}

function isSectionWidget(widget) {
    return widget?.type === "cpf-section" || String(widget?.name || "").startsWith("cpf_section_");
}

function stripSectionWidgets(node) {
    if (!Array.isArray(node.widgets)) return [];
    const sections = node.widgets.filter(isSectionWidget);
    if (sections.length) node.widgets = node.widgets.filter((widget) => !isSectionWidget(widget));
    return sections;
}

function dedupeWidgetsByName(node) {
    if (!Array.isArray(node.widgets)) return;
    const seen = new Set();
    node.widgets = node.widgets.filter((widget) => {
        if (!widget || isSectionWidget(widget)) return true;
        const name = String(widget.name || "");
        if (!name) return true;
        if (seen.has(name)) return false;
        seen.add(name);
        return true;
    });
}

function widgetMap(node) {
    return new Map((node.widgets || []).filter((widget) => widget?.name && !isSectionWidget(widget)).map((widget) => [widget.name, widget]));
}

function valuesInOrder(node, order) {
    const byName = widgetMap(node);
    return order.map((name) => byName.get(name)?.value);
}

const BOOLEAN_WIDGET_KEYS = new Set([
    "lock_media_type", "lock_gender", "lock_content_rating",
    "ethnicity_guidance", "enhance_realism",
]);

function normalizeRestoredValue(widget, value) {
    if (!widget) return undefined;
    if (widget.name === "lens_style" && value === "smartphone camera look") return "None";
    if (widget.name === "lighting_style" && value === "candlelit ambiance") return "None";
    if (widget.name === "camera_direction") {
        if (value === "high-angle view") return "pronounced high-angle view, with the camera positioned above the subject";
        if (value === "low-angle view") return "pronounced low-angle view, with the camera positioned below the subject";
    }
    if (widget.name === "origin_ethnicity") {
        if (value === "mediterranean") return "southern european";
        if (value === "latina") return "latin american";
        if (value === "mixed heritage") return "None";
        return value;
    }
    if (widget.name === "species_mode") {
        if (value === true || value === 1 || value === "1" || String(value).toLowerCase() === "true") return "Anthro Furry";
        if (value === false || value === 0 || value === "0" || String(value).toLowerCase() === "false") return "Human";
        return value;
    }
    if (BOOLEAN_WIDGET_KEYS.has(widget.name)) {
        if (typeof value === "boolean") return value;
        if (value === 1 || value === "1" || String(value).toLowerCase() === "true") return true;
        if (value === 0 || value === "0" || String(value).toLowerCase() === "false") return false;
        return undefined;
    }
    return value;
}

function looksLikeLegacyVisualValues(values) {
    return Array.isArray(values)
        && values.length >= 6
        && typeof values[1] === "boolean"
        && typeof values[3] === "boolean"
        && typeof values[5] === "boolean";
}

function looksLikeSerializedBoolean(value) {
    if (typeof value === "boolean" || value === 0 || value === 1 || value === "0" || value === "1") return true;
    const normalized = String(value).toLowerCase();
    return normalized === "true" || normalized === "false";
}

function restoreOrderForValues(values) {
    if (looksLikeLegacyVisualValues(values)) return LEGACY_VISUAL_WIDGET_ORDER;
    // v1.0 and v1.1 both contain 93 values: v1.0 has the removed boolean
    // enforce_single_subject at index 88, while v1.1 has species_mode there.
    if (values.length === V15_CANONICAL_WIDGET_ORDER.length && looksLikeSerializedBoolean(values[88])) {
        return V15_CANONICAL_WIDGET_ORDER;
    }
    if (values.length === PRE_SECONDARY_GARMENT_COLORS_CANONICAL_WIDGET_ORDER.length) {
        return PRE_SECONDARY_GARMENT_COLORS_CANONICAL_WIDGET_ORDER;
    }
    if (values.length === PRE_OPTICAL_EFFECT_CANONICAL_WIDGET_ORDER.length) {
        return PRE_OPTICAL_EFFECT_CANONICAL_WIDGET_ORDER;
    }
    if (values.length === V8_CANONICAL_WIDGET_ORDER.length) {
        return V8_CANONICAL_WIDGET_ORDER;
    }
    if (values.length === V7_CANONICAL_WIDGET_ORDER.length) {
        return V7_CANONICAL_WIDGET_ORDER;
    }
    if (values.length === PRE_SLEEPWEAR_CANONICAL_WIDGET_ORDER.length) {
        return PRE_SLEEPWEAR_CANONICAL_WIDGET_ORDER;
    }
    if (values.length === PRE_FURRY_PRE_SLEEPWEAR_CANONICAL_WIDGET_ORDER.length) {
        return PRE_FURRY_PRE_SLEEPWEAR_CANONICAL_WIDGET_ORDER;
    }
    if (values.length === PRE_SINGLE_SUBJECT_CANONICAL_WIDGET_ORDER.length) {
        return PRE_SINGLE_SUBJECT_CANONICAL_WIDGET_ORDER;
    }
    return CANONICAL_WIDGET_ORDER;
}

function isValidWidgetValue(widget, value) {
    const allowed = widget?.options?.values;
    if (!Array.isArray(allowed)) return true;
    return allowed.includes(value);
}

function restoreValuesByName(node, values) {
    if (!Array.isArray(values)) return;
    const order = restoreOrderForValues(values);
    const byName = widgetMap(node);
    const limit = Math.min(values.length, order.length);
    for (let index = 0; index < limit; index += 1) {
        const restoredName = order[index];
        const widget = byName.get(restoredName);
        const rawValue = values[index];
        if (!widget || rawValue === undefined) continue;
        if (restoredName === "hosiery" && rawValue === "black tights") {
            widget.value = "opaque tights";
            const colorWidget = byName.get("hosiery_color");
            if (colorWidget) colorWidget.value = "black";
            continue;
        }
        const value = normalizeRestoredValue(widget, rawValue);
        if (value === undefined) continue;
        if (!isValidWidgetValue(widget, value)) {
            const allowed = widget?.options?.values;
            if (Array.isArray(allowed) && allowed.includes("None")) widget.value = "None";
            continue;
        }
        widget.value = value;
    }
}

function sanitizeConfiguredWidgetValues(info) {
    if (!info || !Array.isArray(info.widgets_values)) return info;
    const sectionLabels = new Set([
        ...GROUPS.map((group) => group.label),
        "BODY SPECIFIC", "CLOTHES AND SHOES", "RANDOM ALL", "RANDOMIZE ALL ONCE", "SET ALL RANDOM",
    ]);
    if (!info.widgets_values.some((value) => sectionLabels.has(value))) return info;
    return { ...info, widgets_values: info.widgets_values.filter((value) => !sectionLabels.has(value)) };
}

function reorderWidgets(node) {
    dedupeWidgetsByName(node);
    const widgets = (node.widgets || []).filter((widget) => !isSectionWidget(widget));
    const byName = new Map(widgets.filter((w) => w?.name).map((w) => [w.name, w]));
    const sectionWidgets = new Map();
    for (const group of GROUPS) sectionWidgets.set(group.id, createSectionWidget(node, group));

    const ordered = [sectionWidgets.get("all")];
    for (const key of [
        "media_type", "lock_media_type", "gender", "lock_gender", "content_rating", "lock_content_rating",
        "ethnicity_guidance", "enhance_realism", "species_mode", "free_prompt_position", "free_prompt", "seed", "control_after_generate",
    ]) {
        const widget = byName.get(key);
        if (widget) ordered.push(widget);
    }

    for (const group of GROUPS.slice(1)) {
        ordered.push(sectionWidgets.get(group.id));
        for (const key of group.keys) {
            const widget = byName.get(key);
            if (widget) ordered.push(widget);
        }
    }


    const used = new Set(ordered);
    for (const widget of widgets) if (!used.has(widget)) ordered.push(widget);

    node.widgets = ordered;
    node.setSize([Math.max(node.size[0], 850), node.computeSize()[1]]);
    node.setDirtyCanvas(true, true);
}

function scheduleReorder(node) {
    if (node._cpfReorderTimer) clearTimeout(node._cpfReorderTimer);
    node._cpfReorderTimer = setTimeout(() => {
        node._cpfReorderTimer = null;
        try {
            reorderWidgets(node);
        } catch (error) {
            console.error("[Character Architect] Failed to rebuild custom sections", error);
        }
    }, 0);
}

app.registerExtension({
    name: "CharacterArchitect.Sections.v17",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "CharacterPromptFactory") return;

        const originalOnNodeCreated = nodeType.prototype.onNodeCreated;
        const originalConfigure = nodeType.prototype.configure;
        const originalSerialize = nodeType.prototype.serialize;

        nodeType.prototype.onNodeCreated = function () {
            const result = originalOnNodeCreated?.apply(this, arguments);
            scheduleReorder(this);
            return result;
        };

        nodeType.prototype.configure = function (info) {
            stripSectionWidgets(this);
            dedupeWidgetsByName(this);
            const sanitized = sanitizeConfiguredWidgetValues(info);
            const savedValues = Array.isArray(sanitized?.widgets_values) ? [...sanitized.widgets_values] : null;
            const cleanInfo = sanitized ? { ...sanitized } : sanitized;
            if (cleanInfo) delete cleanInfo.widgets_values;

            const result = originalConfigure?.call(this, cleanInfo);
            restoreValuesByName(this, savedValues);
            scheduleReorder(this);
            return result;
        };

        nodeType.prototype.serialize = function () {
            const originalWidgets = this.widgets;
            this.widgets = (originalWidgets || []).filter((widget) => !isSectionWidget(widget));
            try {
                const data = originalSerialize?.apply(this, arguments) || {};
                data.widgets_values = valuesInOrder(this, CANONICAL_WIDGET_ORDER);
                return data;
            } finally {
                this.widgets = originalWidgets;
            }
        };
    },
});
