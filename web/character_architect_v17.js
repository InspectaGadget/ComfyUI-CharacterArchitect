// Character Architect frontend schema v28 / public v4.5.0.
import { app } from "../../scripts/app.js";

const RANDOM_PROTECTED_KEYS = new Set([
    "body_hair", "facial_hair", "skin_finish", "makeup_complexion",
    "head_accessory", "accessories_glasses", "armwear", "accessories_bag", "accessories_scarf",
    "outerwear", "outerwear_color", "outerwear_wearing_style",
    "free_prompt_position", "clothing_archetype", "scene_scenario", "optical_effect", "enforce_portrait_framing",
    "override_field", "inspect_property",
]);
const GLOBAL_PIVOT_KEYS = new Set(["ethnicity_guidance", "enhance_realism"]);
const COMPOSITION_ARCHETYPE_CONTROL_KEYS = [
    "portrait_style", "pose", "camera_direction", "head_direction",
    "eye_focus", "camera_angle", "shot_composition",
];
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
const FULL_BODY_ONE_PIECE_BOTTOM_TYPES = new Set([
    "loose flowing wide-leg halter jumpsuit",
    "sleek figure-hugging flared jumpsuit",
]);
const BODY_HEIGHT_CLASSIC_RANDOM_POOL = [
    "very short", "short", "average height", "tall", "very tall",
];
const DEFAULT_CLOTHING_MODE_WEIGHTS = new Map([
    ["separates", 4], ["dress", 4], ["lingerie", 5], ["sleepwear", 4], ["cosplay", 5],
]);
const BODY_CONTEXT_PORTRAIT_KEYS = new Set([
    "pose", "bottom_type", "dress_type", "sleepwear_type", "cosplay_type",
    "cosplay_franchise_western", "cosplay_franchise_asian", "hosiery", "footwear",
]);
const FOOTWEAR_HARD_SUPPRESSION_FRAMINGS = new Set(["close-up portrait", "headshot portrait"]);
const FOOTWEAR_FRAMING_BASE_PERCENT = new Map([
    ["portrait", 60],
    ["bust portrait", 15],
    ["half-body portrait", 50],
    ["three-quarter portrait", 75],
    ["full-body portrait", 95],
]);
const DEFAULT_FOOTWEAR_FRAMING_BASE_PERCENT = 60;
const BICYCLE_SCENARIO = "riding a full-size road bicycle along a real cycle path, seated on the saddle with both hands on the handlebars, feet placed on the pedals, and the body leaning naturally forward";
const HORSE_SCENARIO = "riding a full-size horse in an open equestrian arena, seated securely in a fitted saddle with both feet in the stirrups, both hands loosely holding the reins, and the torso following the horse's movement";
const CAR_DRIVING_SCENARIO = "seated correctly in the driver's seat inside a full-size production passenger car with a conventional enclosed cabin, visible dashboard, windshield, doors, and an empty front passenger seat, both hands naturally on the steering wheel while driving along a real road";
const CAROUSEL_SCENARIO = "riding a full-size decorative carousel horse on a working amusement-park carousel, seated astride the saddle with one hand holding the central pole as the surrounding platform turns";
const SKATEBOARD_SCENARIO = "riding a skateboard through a real urban skatepark, one foot planted on the board, the other just lifted after pushing, arms balancing naturally among ramps and painted concrete";
const VEHICLE_OR_MOUNT_SCENARIOS = new Set([
    BICYCLE_SCENARIO, HORSE_SCENARIO, CAR_DRIVING_SCENARIO, CAROUSEL_SCENARIO, SKATEBOARD_SCENARIO,
]);
const FOOTWEAR_HIGH_VISIBILITY_POSES = new Set([
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
]);
const FOOTWEAR_MEDIUM_VISIBILITY_POSES = new Set([
    "bending forward with both hands resting above the knees",
    "kneeling with hips resting on the heels, hands placed on the thighs, upright elegant posture",
    "kneeling on one knee with the other knee raised, forearm resting across the raised thigh",
    "kneeling upright with both hands behind the head, elbows open, hips shifted slightly to one side",
    "seated upright with legs crossed, one hand resting on the upper knee",
    "perched on the edge of a chair, knees together, torso leaning forward slightly, hands resting on the thighs",
    "seated with one knee raised toward the chest, arms loosely wrapped around the leg",
    "seated on the edge of a stool with one hand braced behind",
    "sitting low with knees comfortably apart, elbows resting on the thighs, shoulders slightly forward",
    "caught mid-spin while dancing, torso and arms turning dynamically",
]);
const FOOTWEAR_LOW_VISIBILITY_POSES = new Set([]);
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
    ["Japanese-inspired super-high-waisted wide-leg trousers with a broad extended waistband and deep pleats", ["mid-length", "long", "long"]],
    ["drop-crotch sarouel harem pants", ["mid-length", "long", "long"]],
    ["high-waisted performance leggings with wide sheer lace side panels", ["long"]],
    ["cutout athletic leggings with large sheer mesh panels", ["long"]],
    ["loose flowing wide-leg halter jumpsuit", ["long"]],
    ["sleek figure-hugging flared jumpsuit", ["long"]],
    ["pencil skirt", ["knee-length", "mid-length"]],
    ["A-line skirt", ["short", "knee-length", "mid-length"]],
    ["bias-cut satin midi skirt", ["mid-length"]],
    ["denim skirt", ["very short", "short", "knee-length"]],
    ["cigarette trousers", ["mid-length", "long"]],
    ["straight-leg trousers", ["mid-length", "long", "long"]],
    ["culottes", ["knee-length", "mid-length"]],
    ["tailored shorts", ["short", "knee-length"]],
    ["capri pants", ["mid-length"]],
    ["tennis skirt", ["very short", "short"]],
    ["tapered technical cargo pants", ["mid-length", "long", "long"]],
    ["asymmetrical layered skirt", ["short", "knee-length", "mid-length", "long"]],
    ["patent leather pants", ["mid-length", "long"]],
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
const LEGACY_SELFIE_CAPTURE_STYLE = "spontaneous handheld selfie";
const SELFIE_POSE = "taking a selfie with one arm extended, holding a smartphone at arm's length with its front camera aimed toward the subject, looking into the phone's camera";
const CLOSE_FRAMINGS = new Set(["close-up portrait", "headshot portrait"]);
const UPPER_BODY_POSES = new Set([
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
]);
const FULL_SCENE_POSES = new Set([
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
]);
const MID_BODY_POSES = new Set([
    ...UPPER_BODY_POSES,
    "bending forward with both hands resting above the knees",
    "seated upright with legs crossed, one hand resting on the upper knee",
    "perched on the edge of a chair, knees together, torso leaning forward slightly, hands resting on the thighs",
    "seated with one knee raised toward the chest, arms loosely wrapped around the leg",
    "seated on the edge of a stool with one hand braced behind",
    "sitting low with knees comfortably apart, elbows resting on the thighs, shoulders slightly forward",
]);
const FRONT_READABLE_POSES = new Set([
    "standing at attention with one hand raised in a formal military salute",
    "raising one hand in a friendly wave",
    "standing naturally with both arms folded across the chest",
    "giving a cheerful thumbs-up with one hand",
    "raising both shoulders in a light shrug, palms turned upward",
    "adjusting one sleeve with the opposite hand",
]);
const KINETIC_POSES = new Set([
    "caught mid-spin while dancing, torso and arms turning dynamically",
]);
const SIDE_ORIENTED_POSES = new Set([
    "low side squat, torso upright",
    "reclining on one side in a gentle S-curve, upper body supported by one forearm, upper knee drawn forward",
    "lying on the side with the head supported by one hand and the legs relaxed",
    "lying curled slightly on one side with the knees loosely drawn upward",
]);
const DEFAULT_RANDOM_CAMERA_DIRECTIONS = [
    "front-facing view", "front-facing view", "front-facing view", "front-facing view",
    "three-quarter view", "three-quarter view", "three-quarter view", "three-quarter view",
    "profile view", "profile view", "rear three-quarter view", "rear three-quarter view",
];
const FRONT_READABLE_CAMERA_DIRECTIONS = [
    "front-facing view", "front-facing view", "front-facing view", "front-facing view", "front-facing view",
    "three-quarter view", "three-quarter view", "three-quarter view", "three-quarter view", "profile view",
];
const KINETIC_CAMERA_DIRECTIONS = [
    "front-facing view", "front-facing view",
    "three-quarter view", "three-quarter view", "three-quarter view", "three-quarter view",
    "profile view", "profile view", "profile view", "rear three-quarter view",
];
const SIDE_ORIENTED_CAMERA_DIRECTIONS = [
    "profile view", "profile view", "profile view", "profile view", "profile view",
    "three-quarter view", "three-quarter view", "three-quarter view", "rear three-quarter view",
];
const CAR_SCENARIO_CAMERA_DIRECTIONS = [
    ...Array(3).fill("front-facing view"), ...Array(5).fill("three-quarter view"),
    ...Array(2).fill("profile view"),
];
const VEHICLE_MOUNT_RANDOM_FRAMINGS = [
    "three-quarter portrait", "three-quarter portrait",
    "full-body portrait", "full-body portrait", "full-body portrait",
];
const DEFAULT_RANDOM_CAMERA_ANGLES = [
    "at eye level", "at eye level", "at eye level", "at eye level", "at eye level", "at eye level",
    "from a pronounced low angle, with the camera positioned below the subject",
    "from a pronounced low angle, with the camera positioned below the subject",
    "from a pronounced high angle, with the camera positioned above the subject",
    "from a pronounced high angle, with the camera positioned above the subject",
    "from an extreme worm's-eye angle at ground level, with the camera looking sharply upward",
    "from an overhead bird's-eye angle, with the camera looking straight down",
];
const CLOSE_RANDOM_CAMERA_ANGLES = [
    "at eye level", "at eye level", "at eye level", "at eye level", "at eye level", "at eye level",
    "from a pronounced low angle, with the camera positioned below the subject",
    "from a pronounced high angle, with the camera positioned above the subject",
    "from a pronounced high angle, with the camera positioned above the subject",
];
const VEHICLE_MOUNT_RANDOM_CAMERA_ANGLES = [
    ...Array(6).fill("at eye level"),
    "from a pronounced low angle, with the camera positioned below the subject",
    "from a pronounced high angle, with the camera positioned above the subject",
];
const HIGH_CAMERA_ANGLES = new Set([
    "from a pronounced high angle, with the camera positioned above the subject",
    "from an overhead bird's-eye angle, with the camera looking straight down",
]);
const LOW_CAMERA_ANGLES = new Set([
    "from a pronounced low angle, with the camera positioned below the subject",
    "from an extreme worm's-eye angle at ground level, with the camera looking sharply upward",
]);
const HIGH_FRAME_PLACEMENT = "subject placed high in frame";
const LOW_FRAME_PLACEMENT = "subject placed low in frame";
const CAPTURE_FRAMING_POOLS = new Map([
    ["beauty", ["close-up portrait", "headshot portrait", "bust portrait", "bust portrait", "half-body portrait"]],
    ["glamour", ["bust portrait", "half-body portrait", "half-body portrait", "three-quarter portrait", "three-quarter portrait", "full-body portrait"]],
    ["editorial", ["bust portrait", "half-body portrait", "three-quarter portrait", "three-quarter portrait", "full-body portrait"]],
    ["fashion", ["bust portrait", "half-body portrait", "three-quarter portrait", "three-quarter portrait", "full-body portrait"]],
    ["cinematic", ["close-up portrait", "bust portrait", "half-body portrait", "three-quarter portrait", "full-body portrait", "full-body portrait"]],
    ["street-style", ["half-body portrait", "three-quarter portrait", "three-quarter portrait", "full-body portrait", "full-body portrait"]],
    ["environmental", ["half-body portrait", "three-quarter portrait", "full-body portrait", "full-body portrait"]],
    ["candid", ["bust portrait", "half-body portrait", "three-quarter portrait", "full-body portrait"]],
    ["dramatic", ["close-up portrait", "bust portrait", "half-body portrait", "three-quarter portrait", "full-body portrait"]],
]);
const DEFAULT_RANDOM_FRAMINGS = ["portrait", "bust portrait", "half-body portrait", "half-body portrait", "three-quarter portrait", "three-quarter portrait", "full-body portrait"];
const CAPTURE_COMPOSITION_POOLS = new Map([
    ["street-style", ["rule-of-thirds composition", "negative-space composition", "dynamic diagonal composition", "subject placed high in frame", "subject placed low in frame", "candid off-center framing"]],
    ["environmental", ["rule-of-thirds composition", "negative-space composition", "subject placed high in frame", "subject placed low in frame", "candid off-center framing", "centered composition"]],
    ["candid", ["rule-of-thirds composition", "dynamic diagonal composition", "subject placed high in frame", "subject placed low in frame", "candid off-center framing"]],
    ["cinematic", ["rule-of-thirds composition", "negative-space composition", "dynamic diagonal composition", "subject placed high in frame", "subject placed low in frame", "symmetrical composition"]],
    ["glamour", ["centered composition", "symmetrical composition", "rule-of-thirds composition", "negative-space composition", "clean precisely organized composition", "editorial magazine composition"]],
    ["editorial", ["centered composition", "symmetrical composition", "rule-of-thirds composition", "negative-space composition", "dynamic diagonal composition", "clean precisely organized composition", "editorial magazine composition"]],
    ["fashion", ["centered composition", "symmetrical composition", "rule-of-thirds composition", "dynamic diagonal composition", "clean precisely organized composition", "editorial magazine composition"]],
    ["beauty", ["centered composition", "symmetrical composition", "rule-of-thirds composition", "negative-space composition", "clean precisely organized composition", "editorial magazine composition"]],
    ["dramatic", ["centered composition", "symmetrical composition", "negative-space composition", "dynamic diagonal composition", "subject placed high in frame", "subject placed low in frame"]],
]);
const CAPTURE_LENS_POOLS = new Map([
    ["street-style", ["35mm documentary lens look", "50mm standard lens look", "wide-angle perspective", "vintage lens rendering", "disposable camera look", "cheap digital camera aesthetic"]],
    ["environmental", ["35mm documentary lens look", "50mm standard lens look", "wide-angle perspective", "vintage lens rendering", "anamorphic lens look"]],
    ["candid", ["35mm documentary lens look", "50mm standard lens look", "85mm portrait lens look", "vintage lens rendering", "disposable camera look", "cheap digital camera aesthetic"]],
    ["beauty", ["50mm standard lens look", "85mm portrait lens look", "macro-detail lens look", "soft-focus lens look"]],
]);
const NATURAL_CAPTURE_LIGHTING = ["window light", "golden-hour light", "overcast daylight", "direct flash", "hard flash", "backlit glow", "rim lighting", "neon lighting", "subdued low-key lighting with deep natural shadows"];
const DAYLIT_INTERIOR_ENVIRONMENTS = new Set([
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
    "standing at an airport baggage carousel, watching luggage pass",
    CAR_DRIVING_SCENARIO,
]);
const ENCLOSED_INTERIOR_ENVIRONMENTS = new Set([
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
]);
const EXTERIOR_NATURAL_LIGHTING = new Set(["golden-hour light", "overcast daylight"]);
const WINDOW_DEPENDENT_LIGHTING = new Set(["window light"]);
const OPTICAL_EFFECT_RANDOM_POOL = [
    ...Array(70).fill("None"), ...Array(8).fill("fisheye"),
    ...Array(8).fill("infrared false-color"), ...Array(7).fill("high-contrast duotone"),
    ...Array(7).fill("selective-color monochrome"),
];
const BODY_PHYSIQUE_RANDOM_FAMILIES = [
    ...Array(11).fill("underweight"), ...Array(14).fill("ordinary"),
    ...Array(11).fill("heavy"), ...Array(4).fill("muscular"),
];
const BODY_PHYSIQUE_RANDOM_VALUES = new Map([
    ["underweight", ["naturally extremely slender, fine-boned underweight physique", "extremely underweight physique", "very slim physique", "slim physique"]],
    ["ordinary", ["soft untrained physique", "average physique", "lightly toned physique", "toned physique"]],
    ["heavy", ["plump physique", "plus-size physique", "overweight physique", "obese physique"]],
    ["muscular", ["athletic physique", "muscular physique", "heavily muscular physique"]],
]);

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

// Exact order used by v3.0.0, immediately before the obsolete Picture type
// and its lock were removed. Keep this 95-value layout intact so existing V3
// workflows restore by name instead of shifting every later widget by two.
const PRE_PICTURE_TYPE_CANONICAL_WIDGET_ORDER = V15_CANONICAL_WIDGET_ORDER.filter(
    (name) => name !== "enforce_single_subject",
);
PRE_PICTURE_TYPE_CANONICAL_WIDGET_ORDER.splice(
    PRE_PICTURE_TYPE_CANONICAL_WIDGET_ORDER.indexOf("outerwear_color") + 1,
    0,
    "outerwear_wearing_style",
);
PRE_PICTURE_TYPE_CANONICAL_WIDGET_ORDER.push("override_field", "inspect_property");

// Public v1.1 used the same layout as v3.0.0 before the final override and
// inspection widgets existed. It therefore also contains 93 values, but has
// species_mode at index 88.
const V11_CANONICAL_WIDGET_ORDER = PRE_PICTURE_TYPE_CANONICAL_WIDGET_ORDER.slice(0, -2);

// Public v3.0.1 order. The two removed names intentionally remain present in
// every historical map above and below; restoreValuesByName simply discards
// them because no matching widgets exist anymore.
const V301_CANONICAL_WIDGET_ORDER = PRE_PICTURE_TYPE_CANONICAL_WIDGET_ORDER.filter(
    (name) => name !== "content_rating" && name !== "lock_content_rating",
);

// V3.1 separates framing, capture treatment, horizontal direction, head/gaze,
// and vertical angle. Preserve the exact V3.0.1 map above, then insert the new
// fields by name so older positional workflows cannot shift.
const V20_CANONICAL_WIDGET_ORDER = [...V301_CANONICAL_WIDGET_ORDER];
V20_CANONICAL_WIDGET_ORDER.splice(
    V20_CANONICAL_WIDGET_ORDER.indexOf("portrait_style") + 1,
    0,
    "capture_style",
);
V20_CANONICAL_WIDGET_ORDER.splice(
    V20_CANONICAL_WIDGET_ORDER.indexOf("camera_direction") + 1,
    0,
    "head_direction",
    "camera_angle",
);
const PRE_BODY_MORPHOLOGY_CANONICAL_WIDGET_ORDER = [...V20_CANONICAL_WIDGET_ORDER];
PRE_BODY_MORPHOLOGY_CANONICAL_WIDGET_ORDER.splice(
    PRE_BODY_MORPHOLOGY_CANONICAL_WIDGET_ORDER.indexOf("setting") + 1,
    0,
    "scene_scenario",
);
// V3.2.5 Body Archetype still serialized the now-obsolete Outfit Style widget.
// Keep that exact layout for name-based restoration, then remove only that one
// field from the active order so no later value can shift in an old workflow.
const PRE_OUTFIT_STYLE_REMOVAL_CANONICAL_WIDGET_ORDER = [...PRE_BODY_MORPHOLOGY_CANONICAL_WIDGET_ORDER];
PRE_OUTFIT_STYLE_REMOVAL_CANONICAL_WIDGET_ORDER.splice(
    PRE_OUTFIT_STYLE_REMOVAL_CANONICAL_WIDGET_ORDER.indexOf("body_type"),
    0,
    "body_archetype",
);
PRE_OUTFIT_STYLE_REMOVAL_CANONICAL_WIDGET_ORDER.splice(
    PRE_OUTFIT_STYLE_REMOVAL_CANONICAL_WIDGET_ORDER.indexOf("thigh_shape") + 1,
    0,
    "body_detail_1",
    "body_detail_2",
    "body_detail_3",
);
const V400_CANONICAL_WIDGET_ORDER = PRE_OUTFIT_STYLE_REMOVAL_CANONICAL_WIDGET_ORDER.filter(
    (name) => name !== "outfit_style",
);
const V410_CANONICAL_WIDGET_ORDER = [
    ...V400_CANONICAL_WIDGET_ORDER,
    "eye_focus", "mouth_expression", "setting_text_override", "pose_text_override",
    "custom_color_overrides", "wildcard_subject", "wildcard_clothing",
    "wildcard_pose", "wildcard_setting", "wildcard_photography",
];
const V420_CANONICAL_WIDGET_ORDER = [...V410_CANONICAL_WIDGET_ORDER];
V420_CANONICAL_WIDGET_ORDER.splice(
    V420_CANONICAL_WIDGET_ORDER.indexOf("gender") + 1,
    0,
    "content_rating",
);
V420_CANONICAL_WIDGET_ORDER.splice(
    V420_CANONICAL_WIDGET_ORDER.indexOf("lock_gender") + 1,
    0,
    "lock_content_rating",
);
const V430_CANONICAL_WIDGET_ORDER = [...V420_CANONICAL_WIDGET_ORDER];
V430_CANONICAL_WIDGET_ORDER.splice(
    V430_CANONICAL_WIDGET_ORDER.indexOf("species_mode") + 1,
    0,
    "enforce_portrait_framing",
);
const V440_CANONICAL_WIDGET_ORDER = [...V430_CANONICAL_WIDGET_ORDER];
V440_CANONICAL_WIDGET_ORDER.splice(
    V440_CANONICAL_WIDGET_ORDER.indexOf("portrait_style"),
    0,
    "composition_archetype",
);
const CANONICAL_WIDGET_ORDER = [
    ...V440_CANONICAL_WIDGET_ORDER,
    "face_hair_text_override",
];

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
        label: "MEDIA / CAMERA / COMPOSITION",
        keys: ["composition_archetype", "portrait_style", "enforce_portrait_framing", "capture_style", "pose", "pose_mood", "setting", "scene_scenario", "camera_direction", "head_direction", "eye_focus", "camera_angle", "shot_composition", "lens_style", "lighting_style", "optical_effect"],
    },
    {
        id: "body",
        label: "BODY",
        keys: ["body_archetype", "origin_age", "origin_ethnicity", "body_type", "body_physique", "body_feminine_curves"],
    },
    {
        id: "body_specific",
        label: "BODY SPECIFIC",
        keys: ["bust", "cleavage_depth", "cleavage_type", "butt_shape", "thigh_shape", "body_detail_1", "body_detail_2", "body_detail_3", "body_hair", "skin_finish"],
    },
    {
        id: "face",
        label: "FACE",
        keys: ["expression", "mouth_expression", "eye_expression", "face_shape", "jawline", "chin_shape", "eye_shape", "eye_color", "eyelashes", "eyebrows", "nose_shape", "lip_shape", "facial_hair"],
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
            "clothing_archetype", "top_type", "top_color", "bottom_type", "bottom_length", "bottom_color",
            "lingerie_type", "lingerie_color", "sleepwear_type", "sleepwear_color", "cosplay_type", "cosplay_color",
            "cosplay_franchise_western", "cosplay_franchise_asian", "hosiery", "hosiery_color",
            "dress_type", "dress_color", "outerwear", "outerwear_color", "outerwear_wearing_style", "belt", "belt_color", "footwear", "footwear_color",
        ],
    },
    {
        id: "accessories",
        label: "ACCESSORIES",
        keys: ["accessories_jewelry", "accessories_necklace", "accessories_earrings", "accessories_bracelet", "accessories_rings", "head_accessory", "accessories_glasses", "armwear", "accessories_bag", "accessories_scarf"],
    },
    {
        id: "custom_inputs",
        label: "CUSTOM INPUTS / WILDCARDS",
        keys: ["face_hair_text_override", "setting_text_override", "pose_text_override", "custom_color_overrides", "wildcard_subject", "wildcard_clothing", "wildcard_pose", "wildcard_setting", "wildcard_photography"],
    },
    {
        id: "override_inspection",
        label: "OVERRIDE AND INSPECTION",
        keys: ["override_field", "inspect_property"],
    },
];

const SECTION_TOOLTIPS = {
    all: "Global controls affect every unlocked category. Pivot locks protect Media type, Gender, and Content rating; optional protected fields and the seed are not overwritten. Scene scenario is the deliberate exception: SET ALL RANDOM arms its ten-percent branch, while RANDOMIZE ALL ONCE resolves that same rare chance immediately.",
    composition: "Composition Archetype coordinates framing, pose, horizontal camera direction, head direction, Eye Focus, vertical camera angle, and frame placement while preserving manual and Forced Random choices. Scene scenario remains a rare mutually exclusive branch.",
    body: "Height, weight/fitness, and silhouette are independent. Ordinary Random balances underweight, ordinary, heavier, and muscular physique families instead of overproducing average synonyms; manual and Forced Random choices remain free.",
    body_specific: "Detailed morphology, body hair, and skin. Ordinary Random favors compatible neckline depth/type pairs 90% of the time. Body hair and skin finish stay protected from one-click randomization.",
    face: "Facial structure and expression. Ethnicity Guidance can constrain compatible Random traits; explicit manual values always win.",
    hair: "Hair color, texture, style, cut, length, and bangs remain combinable. Ordinary Random softens only the clearest structural clashes 75% of the time, preserving experimental undercuts and mixed constructions.",
    tattoos_makeup: "Independent tattoo, makeup, and nail controls. Random nails are silently removed when full hand-covering gloves are detected.",
    clothes_shoes: "Main garment families are mutually exclusive for ordinary Random. Outerwear, its color, and its wearing style stay protected on global random buttons; manual and field-level Random remain available. Cosplay protection, manual choices, Forced Random, and override retain their established priority.",
    accessories: "Optional additions guided by clothing archetypes. Head accessories, glasses, armwear, bags, and scarves stay protected on global random buttons and remain available manually or through their own Random setting.",
    custom_inputs: "Reference-image captions and expanded wildcard text enter as dependency-free STRING overrides. A structured Face/Hair description fills only fields left on None or Random, above Identity Forge and Subject wildcard but below manual, Forced Random, and the universal field override. Setting/Pose text overrides lead over their matching wildcard line. Custom colors use target=value pairs.",
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
    if (widget.name === "optical_effect") {
        setWidgetValue(widget, chooseFrom(OPTICAL_EFFECT_RANDOM_POOL));
        return true;
    }
    if (widget.name === "body_type") {
        setWidgetValue(widget, chooseFrom(BODY_HEIGHT_CLASSIC_RANDOM_POOL));
        return true;
    }
    if (widget.name === "body_physique") {
        const family = chooseFrom(BODY_PHYSIQUE_RANDOM_FAMILIES);
        setWidgetValue(widget, chooseFrom(BODY_PHYSIQUE_RANDOM_VALUES.get(family)));
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

function setFromPool(byName, key, pool) {
    if (!pool?.length) return;
    setWidgetValue(byName.get(key), chooseFrom(pool));
}

function environmentFamilyOnce(byName) {
    const scenario = byName.get("scene_scenario")?.value;
    const setting = byName.get("setting")?.value;
    const environment = scenario && !["None", "Random", "Forced Random"].includes(scenario)
        ? scenario
        : setting;
    if (!environment || ["None", "Random", "Forced Random"].includes(environment)) return "unknown";
    if (DAYLIT_INTERIOR_ENVIRONMENTS.has(environment)) return "daylit_interior";
    if (ENCLOSED_INTERIOR_ENVIRONMENTS.has(environment)) return "enclosed_interior";
    return "outdoor";
}

function lightingCompatibleOnce(family, lighting) {
    if (family === "enclosed_interior") {
        return !EXTERIOR_NATURAL_LIGHTING.has(lighting) && !WINDOW_DEPENDENT_LIGHTING.has(lighting);
    }
    if (family === "outdoor") return !WINDOW_DEPENDENT_LIGHTING.has(lighting);
    return true;
}

function applyEnvironmentLightingCoherenceOnce(byName, randomized, scenarioWasRandomized = false) {
    const lightingWidget = byName.get("lighting_style");
    const lighting = lightingWidget?.value;
    if (!lighting || ["None", "Random", "Forced Random"].includes(lighting)) return;

    if (randomized("lighting_style")) {
        const family = environmentFamilyOnce(byName);
        if (lightingCompatibleOnce(family, lighting)) return;
        const compatible = concreteValues(lightingWidget).filter((value) => lightingCompatibleOnce(family, value));
        if (compatible.length) setWidgetValue(lightingWidget, chooseFrom(compatible));
        return;
    }

    const scenarioWidget = byName.get("scene_scenario");
    const scenario = scenarioWidget?.value;
    if (scenarioWasRandomized && scenario && scenario !== "None") {
        const compatible = concreteValues(scenarioWidget).filter((value) => {
            const family = DAYLIT_INTERIOR_ENVIRONMENTS.has(value)
                ? "daylit_interior"
                : ENCLOSED_INTERIOR_ENVIRONMENTS.has(value) ? "enclosed_interior" : "outdoor";
            return lightingCompatibleOnce(family, lighting);
        });
        if (compatible.length) setWidgetValue(scenarioWidget, chooseFrom(compatible));
        return;
    }

    if ((!scenario || scenario === "None") && randomized("setting")) {
        const settingWidget = byName.get("setting");
        const compatible = concreteValues(settingWidget).filter((value) => {
            const family = DAYLIT_INTERIOR_ENVIRONMENTS.has(value)
                ? "daylit_interior"
                : ENCLOSED_INTERIOR_ENVIRONMENTS.has(value) ? "enclosed_interior" : "outdoor";
            return lightingCompatibleOnce(family, lighting);
        });
        if (compatible.length) setWidgetValue(settingWidget, chooseFrom(compatible));
    }
}

function applySceneGeometryCoherenceOnce(byName, randomized) {
    let framing = byName.get("portrait_style")?.value;
    const capture = byName.get("capture_style")?.value;
    let pose = byName.get("pose")?.value;
    const scenario = byName.get("scene_scenario")?.value;

    if (randomized("portrait_style")) {
        const capturePool = CAPTURE_FRAMING_POOLS.get(capture) || DEFAULT_RANDOM_FRAMINGS;
        let allowed = new Set(capturePool);
        let fallback = capturePool;
        if (VEHICLE_OR_MOUNT_SCENARIOS.has(scenario)) {
            allowed = new Set(["three-quarter portrait", "full-body portrait"]);
            fallback = VEHICLE_MOUNT_RANDOM_FRAMINGS;
        } else if (FULL_SCENE_POSES.has(pose)) {
            allowed = new Set(["three-quarter portrait", "full-body portrait"]);
            fallback = ["three-quarter portrait", "full-body portrait", "full-body portrait"];
        } else if (UPPER_BODY_POSES.has(pose)) {
            allowed = new Set(["bust portrait", "half-body portrait", "three-quarter portrait"]);
            fallback = ["bust portrait", "half-body portrait", "three-quarter portrait"];
        } else if (MID_BODY_POSES.has(pose)) {
            allowed = new Set(["half-body portrait", "three-quarter portrait", "full-body portrait"]);
            fallback = ["half-body portrait", "three-quarter portrait", "full-body portrait"];
        }
        const compatible = capturePool.filter((value) => allowed.has(value));
        setFromPool(byName, "portrait_style", compatible.length ? compatible : fallback);
        framing = byName.get("portrait_style")?.value;
        if (randomized("pose") && CLOSE_FRAMINGS.has(framing)) setWidgetValue(byName.get("pose"), "None");
        else if (randomized("pose") && framing === "bust portrait" && !UPPER_BODY_POSES.has(byName.get("pose")?.value)) {
            setFromPool(byName, "pose", [...UPPER_BODY_POSES]);
        }
    }

    if (randomized("pose") && !randomized("portrait_style") && CLOSE_FRAMINGS.has(framing)) {
        setWidgetValue(byName.get("pose"), "None");
    } else if (randomized("pose") && !randomized("portrait_style") && framing === "bust portrait") {
        setFromPool(byName, "pose", [...UPPER_BODY_POSES]);
    }

    const explicitHorizontal = byName.get("camera_direction")?.value;
    if (randomized("pose") && !randomized("camera_direction")
        && SIDE_ORIENTED_POSES.has(byName.get("pose")?.value)
        && ["front-facing view", "back view"].includes(explicitHorizontal)) {
        const compatible = [...new Set([...UPPER_BODY_POSES, ...MID_BODY_POSES, ...FULL_SCENE_POSES])]
            .filter((value) => !SIDE_ORIENTED_POSES.has(value));
        setFromPool(byName, "pose", compatible);
    }

    const compositionPool = CAPTURE_COMPOSITION_POOLS.get(capture);
    if (randomized("shot_composition") && compositionPool) setFromPool(byName, "shot_composition", compositionPool);
    const lensPool = CAPTURE_LENS_POOLS.get(capture);
    if (randomized("lens_style") && lensPool) setFromPool(byName, "lens_style", lensPool);
    if (randomized("lighting_style") && ["street-style", "environmental", "candid"].includes(capture)) {
        setFromPool(byName, "lighting_style", NATURAL_CAPTURE_LIGHTING);
    }

    if (randomized("camera_direction")) {
        const finalPose = byName.get("pose")?.value;
        let directionPool = DEFAULT_RANDOM_CAMERA_DIRECTIONS;
        if (scenario === CAR_DRIVING_SCENARIO) {
            directionPool = CAR_SCENARIO_CAMERA_DIRECTIONS;
        } else if (VEHICLE_OR_MOUNT_SCENARIOS.has(scenario)) {
            directionPool = KINETIC_CAMERA_DIRECTIONS;
        } else if (SIDE_ORIENTED_POSES.has(finalPose)) {
            directionPool = SIDE_ORIENTED_CAMERA_DIRECTIONS;
        } else if (FRONT_READABLE_POSES.has(finalPose)) {
            directionPool = FRONT_READABLE_CAMERA_DIRECTIONS;
        } else if (KINETIC_POSES.has(finalPose)) {
            directionPool = KINETIC_CAMERA_DIRECTIONS;
        }
        setFromPool(byName, "camera_direction", directionPool);
    }

    if (randomized("camera_angle")) {
        let anglePool = VEHICLE_OR_MOUNT_SCENARIOS.has(scenario)
            ? VEHICLE_MOUNT_RANDOM_CAMERA_ANGLES
            : (["close-up portrait", "headshot portrait", "bust portrait"].includes(framing))
                ? CLOSE_RANDOM_CAMERA_ANGLES
                : DEFAULT_RANDOM_CAMERA_ANGLES;
        const placement = byName.get("shot_composition")?.value;
        if (placement === HIGH_FRAME_PLACEMENT) anglePool = anglePool.filter((value) => !HIGH_CAMERA_ANGLES.has(value));
        else if (placement === LOW_FRAME_PLACEMENT) anglePool = anglePool.filter((value) => !LOW_CAMERA_ANGLES.has(value));
        setFromPool(byName, "camera_angle", anglePool);
    }


    const angle = byName.get("camera_angle")?.value;
    const placement = byName.get("shot_composition")?.value;
    const verticalConflict = (HIGH_CAMERA_ANGLES.has(angle) && placement === HIGH_FRAME_PLACEMENT)
        || (LOW_CAMERA_ANGLES.has(angle) && placement === LOW_FRAME_PLACEMENT);
    if (randomized("shot_composition") && verticalConflict) {
        const source = CAPTURE_COMPOSITION_POOLS.get(capture) || [];
        const incompatible = HIGH_CAMERA_ANGLES.has(angle) ? HIGH_FRAME_PLACEMENT : LOW_FRAME_PLACEMENT;
        setFromPool(byName, "shot_composition", source.filter((value) => value !== incompatible));
    }

    const horizontal = byName.get("camera_direction")?.value;
    if (randomized("head_direction")) {
        if (horizontal === "back view") setWidgetValue(byName.get("head_direction"), "None");
        else if (horizontal === "rear three-quarter view") setFromPool(byName, "head_direction", ["looking back over one shoulder", "looking back over one shoulder", "looking back over one shoulder", "head held level", "glancing slightly to one side"]);
        else if (byName.get("head_direction")?.value === "looking back over one shoulder") setFromPool(byName, "head_direction", ["head held level", "head tilted slightly", "looking upward", "looking downward", "glancing slightly to one side"]);
    }

}

function applySceneScenarioExclusivityOnce(byName, resolveRandomBranch = false, forceOrdinaryBranch = false) {
    const widget = byName.get("scene_scenario");
    let scenario = widget?.value;
    if (!scenario || (scenario === "None" && !forceOrdinaryBranch)) return false;
    let wasRandomized = false;

    // RANDOMIZE ALL ONCE gives this marked alternative only a ten-percent
    // chance. An explicitly armed Forced Random remains guaranteed.
    if (forceOrdinaryBranch && scenario !== "Forced Random") {
        wasRandomized = true;
        if (Math.random() >= 0.10) {
            setWidgetValue(widget, "None");
            return true;
        }
        const choices = concreteValues(widget);
        if (!choices.length) return wasRandomized;
        scenario = chooseFrom(choices);
        setWidgetValue(widget, scenario);
    } else if (resolveRandomBranch && scenario === "Random") {
        wasRandomized = true;
        if (Math.random() >= 0.10) {
            setWidgetValue(widget, "None");
            return true;
        }
        const choices = concreteValues(widget);
        if (!choices.length) return wasRandomized;
        scenario = chooseFrom(choices);
        setWidgetValue(widget, scenario);
    } else if (resolveRandomBranch && scenario === "Forced Random") {
        wasRandomized = true;
        const choices = concreteValues(widget);
        if (!choices.length) return wasRandomized;
        scenario = chooseFrom(choices);
        setWidgetValue(widget, scenario);
    } else if (["Random", "Forced Random"].includes(scenario)) {
        return false;
    }

    setWidgetValue(byName.get("composition_archetype"), "None");
    setWidgetValue(byName.get("pose"), "None");
    setWidgetValue(byName.get("setting"), "None");
    return wasRandomized;
}

function prepareCompositionArchetypeOnce(byName, randomized) {
    const archetype = byName.get("composition_archetype")?.value;
    const scenario = byName.get("scene_scenario")?.value;
    if (!archetype || ["None", "Random", "Forced Random"].includes(archetype)) return;
    if (scenario && !["None", "Random", "Forced Random"].includes(scenario)) return;
    if (!randomized("composition_archetype")) return;

    // RANDOMIZE ALL ONCE selects a concrete recipe, then leaves the seven
    // recipe-owned fields on ordinary Random so the deterministic backend can
    // resolve their conditional relationships from the visible seed.
    for (const key of COMPOSITION_ARCHETYPE_CONTROL_KEYS) {
        if (!randomized(key)) continue;
        const widget = byName.get(key);
        if (widget?.options?.values?.includes("Random")) setWidgetValue(widget, "Random");
    }
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

function ordinaryRandomFootwearPresencePercent(node) {
    const byName = widgetMap(node);
    const portrait = byName.get("portrait_style")?.value;
    if (FOOTWEAR_HARD_SUPPRESSION_FRAMINGS.has(portrait)) return 0;

    let percent = FOOTWEAR_FRAMING_BASE_PERCENT.get(portrait)
        ?? DEFAULT_FOOTWEAR_FRAMING_BASE_PERCENT;
    const pose = byName.get("pose")?.value;
    if (FOOTWEAR_HIGH_VISIBILITY_POSES.has(pose)) percent = Math.max(percent, 90);
    else if (FOOTWEAR_MEDIUM_VISIBILITY_POSES.has(pose)) percent = Math.max(percent, 70);
    else if (FOOTWEAR_LOW_VISIBILITY_POSES.has(pose)) percent = Math.min(percent, 10);

    const hosiery = byName.get("hosiery")?.value;
    if (hosiery && !["None", "Random", "Forced Random", "bare legs"].includes(hosiery)) {
        percent = Math.min(98, percent + 5);
    }

    const angle = byName.get("camera_angle")?.value;
    if (angle === "low-angle view, with the camera positioned below the subject") percent = Math.min(percent, 8);
    else if (angle === "worm's-eye view from ground level") percent = Math.max(percent, 90);
    else if (angle === "pronounced high-angle view, with the camera positioned above the subject") percent = Math.min(98, percent + 20);
    else if (angle === "bird's-eye view from directly overhead") percent = Math.max(percent, 90);

    return Math.max(0, Math.min(100, Math.round(percent)));
}

function keepOrdinaryRandomFootwearForVisibility(node) {
    const percent = ordinaryRandomFootwearPresencePercent(node);
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
    const weightedModes = modes.flatMap(([name, keys]) =>
        Array(DEFAULT_CLOTHING_MODE_WEIGHTS.get(name) || 1).fill([name, keys])
    );
    const [chosenName, chosenKeys] = weightedModes[Math.floor(Math.random() * weightedModes.length)];
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

    if (chosenName === "separates") {
        const bottom = widgetsByName.get("bottom_type")?.value;
        if (FULL_BODY_ONE_PIECE_BOTTOM_TYPES.has(bottom)) {
            setWidgetValue(widgetsByName.get("top_type"), "None");
            setWidgetValue(widgetsByName.get("top_color"), "None");
        }
    }
}

function randomizeKeysOnce(node, keys) {
    const keySet = keys === "*" ? null : new Set(keys);
    const lockedGroupKeys = !keySet ? getLockedGroupKeySet(node) : null;

    const guidedEthnicity = hasActiveEthnicityGuidance(node);
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
    const randomized = (key) => keySet ? keySet.has(key) : !lockedGroupKeys.has(key);
    const scenarioBranchInScope = (!keySet || keySet.has("scene_scenario"))
        && (keySet || !lockedGroupKeys.has("scene_scenario"));
    const scenarioWasRandomized = applySceneScenarioExclusivityOnce(
        widgetMap(node), scenarioBranchInScope, scenarioBranchInScope,
    );
    applySceneGeometryCoherenceOnce(widgetMap(node), randomized);
    applyEnvironmentLightingCoherenceOnce(widgetMap(node), randomized, scenarioWasRandomized);
    const footwearWasRandomized = !clothingGroupLocked
        && (!keySet || keySet.has("footwear") || keySet.has("footwear_color"));
    if (footwearWasRandomized && !keepOrdinaryRandomFootwearForVisibility(node)) {
        const byName = widgetMap(node);
        if (!keySet || keySet.has("footwear")) setWidgetValue(byName.get("footwear"), "None");
        if (!keySet || keySet.has("footwear_color")) setWidgetValue(byName.get("footwear_color"), "None");
    }

    prepareCompositionArchetypeOnce(widgetMap(node), randomized);

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

    // The generic loop protects Scene scenario because it is a rare branch,
    // not an ordinary always-on field. Global or Media-section SET ALL RANDOM
    // explicitly arms that ten-percent backend branch.
    const scenarioInScope = (!keySet || keySet.has("scene_scenario"))
        && (keySet || !lockedGroupKeys.has("scene_scenario"));
    if (scenarioInScope) setWidgetValue(widgetMap(node).get("scene_scenario"), "Random");

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
    "ethnicity_guidance", "enhance_realism", "enforce_portrait_framing",
]);

const CONTROL_AFTER_GENERATE_VALUES = new Set(["fixed", "increment", "decrement", "randomize"]);

const LEGACY_PORTRAIT_FRAMING = new Map([
    ["bedroom selfie", "portrait"],
    ["spontaneous handheld selfie", "portrait"],
    ["full-body glamour portrait", "full-body portrait"],
    ["editorial portrait", "portrait"], ["cinematic portrait", "portrait"],
    ["fashion portrait", "portrait"], ["beauty portrait", "portrait"],
    ["street-style portrait", "portrait"], ["environmental portrait", "portrait"],
    ["candid portrait", "portrait"], ["dramatic portrait", "portrait"],
]);
const LEGACY_PORTRAIT_CAPTURE = new Map([
    ["bedroom selfie", "candid"],
    ["spontaneous handheld selfie", "candid"],
    ["full-body glamour portrait", "glamour"],
    ["editorial portrait", "editorial"], ["cinematic portrait", "cinematic"],
    ["fashion portrait", "fashion"], ["beauty portrait", "beauty"],
    ["street-style portrait", "street-style"], ["environmental portrait", "environmental"],
    ["candid portrait", "candid"], ["dramatic portrait", "dramatic"],
]);
const LEGACY_CATEGORY_VALUES = new Map([
    ["outfit_style", new Map([["minimalist monochrome style", "minimalist monochrome clothing"]])],
    ["dress_type", new Map([
        ["contemporary djellaba, a full-length loose hooded robe", "contemporary djellaba"],
        ["contemporary kaftan dress with long flowing sleeves", "contemporary kaftan"],
        ["salwar kameez ensemble with a long tunic and straight trousers", "salwar kameez ensemble"],
        ["kurta and flowing trouser ensemble", "kurta and trouser ensemble"],
        ["contemporary sari draped over a fitted blouse", "contemporary sari"],
        ["embroidered anarkali dress with a long flared silhouette", "Anarkali suit"],
        ["kebaya blouse with a coordinated batik sarong", "kebaya and batik sarong ensemble"],
        ["baju kurung ensemble with a long tunic and ankle-length skirt", "baju kurung ensemble"],
        ["ao dai tunic over flowing trousers", "ao dai ensemble"],
        ["West African boubou robe over a matching underdress", "West African boubou ensemble"],
        ["modern qipao dress with a mandarin collar and side slits", "modern qipao"],
    ])],
    ["body_type", new Map([
        ["very petite", "very short"], ["petite", "short"], ["short compact", "short"], ["compact", "short"],
        ["lanky", "tall"], ["tall slender", "tall"], ["tall curvy", "tall"], ["statuesque", "tall"],
        ["slim", "average height"], ["slender", "average height"], ["average", "average height"],
        ["voluptuous", "average height"], ["plus-size", "average height"], ["stocky", "average height"],
        ["broad-built", "average height"], ["androgynous", "average height"],
    ])],
    ["body_physique", new Map([
        ["soft physique", "soft untrained physique"], ["wiry physique", "toned physique"],
        ["lean masculine physique", "athletic physique"], ["broad-shouldered physique", "muscular physique"],
        ["very muscular physique", "heavily muscular physique"], ["powerfully muscular physique", "heavily muscular physique"],
        ["heavy muscular physique", "heavily muscular physique"], ["dance-athletic physique", "athletic physique"],
        ["plush physique", "plump physique"],
    ])],
    ["body_feminine_curves", new Map([
        ["flat silhouette", "almost no curves"], ["boyish silhouette", "straight silhouette"],
        ["androgynous build", "androgynous silhouette"], ["gentle curves", "subtle curves"],
        ["moderate curves", "balanced curves"],
        ["pronounced curves", "pronounced hourglass silhouette"], ["gentle hourglass silhouette", "soft hourglass silhouette"],
        ["curvy silhouette", "pronounced hourglass silhouette"], ["pear silhouette", "pear-shaped silhouette"],
        ["top heavy silhouette", "top-heavy silhouette"], ["narrow hips", "narrow-hip silhouette"],
        ["wide hips", "wide-hip silhouette"],
        ["pronounced inward lumbar curve with a deeply arched lower-back silhouette", "pronounced lumbar lordosis, with a deeply concave lower back, the abdomen projecting forward, and the pelvis tilted so the buttocks project prominently backward"],
    ])],
    ["camera_direction", new Map([["back view", "rear three-quarter view"]])],
]);
const LEGACY_CURVE_DETAIL_VALUES = new Map([
    ["short-legged proportions", "short-legged proportions"],
    ["long-legged proportions", "long-legged proportions"],
    ["pronounced inward lumbar curve with a deeply arched lower-back silhouette", "pronounced inward lumbar curve"],
    ["pronounced lumbar lordosis, with a deeply concave lower back, the abdomen projecting forward, and the pelvis tilted so the buttocks project prominently backward", "pronounced inward lumbar curve"],
]);
const LEGACY_POSE_VALUES = new Map([
    ["low side squat, one heel raised, torso upright", "low side squat, torso upright"],
    ["standing with the back partly turned, looking over one shoulder, hips shifted softly to one side", "standing with the weight shifted softly onto one hip"],
    ["standing in a three-quarter pose, one hand in the hair, hips turned away", "standing with one hand in the hair and the weight shifted onto one hip"],
    ["leaning back against a wall, one knee bent, hips angled slightly, relaxed sensual posture", "leaning back against a wall with one knee bent and the hips angled slightly"],
    ["sitting sideways on a stool, upper body twisting toward the camera, one hand braced behind", "seated on the edge of a stool with one hand braced behind"],
    ["on hands and knees, back mostly straight, head turned toward the camera, natural elegant body line", "on hands and knees with the back mostly straight"],
    ["on hands and knees viewed from a rear three-quarter angle, hips angled toward the camera, looking back over one shoulder", "on hands and knees with the weight shifted onto one arm"],
    ["on hands and knees, back softly arched, shoulders lowered, chin slightly raised toward the camera", "on hands and knees with a gentle arch through the lower back and the shoulders lowered"],
    ["on hands and knees with one knee drawn forward between the hands, torso twisted slightly toward the camera", "on hands and knees with one knee drawn forward between the hands and the torso gently twisted"],
    ["kneeling with forearms resting on the floor, hips raised, back curved, head turned toward the camera", "kneeling with forearms resting on the floor, hips raised, and the back gently curved"],
    ["riding a bicycle through the scene, both hands holding the handlebars, body leaning naturally forward, captured in gentle motion", "riding a bicycle with both hands holding the handlebars and the body leaning naturally forward"],
    ["seated behind the wheel of a car, both hands placed naturally on the steering wheel, glancing toward the camera while driving", "seated behind the wheel of a car with both hands placed naturally on the steering wheel while actively driving"],
    ["riding a carousel horse in motion, seated astride the saddle, one hand holding the central pole, background lights streaking with motion blur", "riding a moving carousel horse, seated astride the saddle with one hand holding the central pole"],
    ["raising one hand in a friendly wave toward someone off-frame", "raising one hand in a friendly wave"],
    ["on hands and knees with the back mostly straight and the head raised naturally", "on hands and knees with the back mostly straight"],
    ["on hands and knees with a gentle arch through the lower back, shoulders lowered, chin slightly raised", "on hands and knees with a gentle arch through the lower back and the shoulders lowered"],
    ["kneeling with forearms resting on the floor, hips raised, back gently curved, and head raised naturally", "kneeling with forearms resting on the floor, hips raised, and the back gently curved"],
]);
const LEGACY_ACTION_POSE_TO_SCENARIO = new Map([
    ["riding a bicycle with both hands holding the handlebars and the body leaning naturally forward", BICYCLE_SCENARIO],
    ["riding a horse, seated securely in the saddle, both hands loosely holding the reins, torso following the horse's movement", HORSE_SCENARIO],
    ["seated behind the wheel of a car with both hands placed naturally on the steering wheel while actively driving", CAR_DRIVING_SCENARIO],
    ["riding a moving carousel horse, seated astride the saddle with one hand holding the central pole", CAROUSEL_SCENARIO],
    ["riding a skateboard through the scene, one foot planted on the board, the other just lifted after pushing, arms balancing naturally", SKATEBOARD_SCENARIO],
]);
const LEGACY_POSE_MOOD_VALUES = new Map([
    ["relaxed pose", "relaxed attitude"], ["confident pose", "confident attitude"],
    ["playful pose", "playful attitude"], ["seductive pose", "seductive attitude"],
    ["elegant pose", "elegant bearing"], ["guarded pose", "guarded attitude"],
]);

function normalizeRestoredValue(widget, value) {
    if (!widget) return undefined;
    const mappedValues = LEGACY_CATEGORY_VALUES.get(widget.name);
    if (mappedValues?.has(value)) return mappedValues.get(value);
    if (widget.name === "capture_style" && value === LEGACY_SELFIE_CAPTURE_STYLE) return "candid";
    if (widget.name === "lens_style" && value === "smartphone camera look") return "None";
    if (widget.name === "lighting_style" && value === "candlelit ambiance") return "None";
    if (widget.name === "portrait_style" && LEGACY_PORTRAIT_FRAMING.has(value)) return LEGACY_PORTRAIT_FRAMING.get(value);
    if (widget.name === "pose" && LEGACY_POSE_VALUES.has(value)) return LEGACY_POSE_VALUES.get(value);
    if (widget.name === "pose_mood" && LEGACY_POSE_MOOD_VALUES.has(value)) return LEGACY_POSE_MOOD_VALUES.get(value);
    if (widget.name === "shot_composition" && value === "clean studio composition") return "clean precisely organized composition";
    if (widget.name === "shot_composition" && ["tight crop", "wide framing"].includes(value)) return "None";
    if (widget.name === "head_direction" && ["looking down toward camera", "looking downward toward the camera"].includes(value)) return "looking downward";
    if (widget.name === "content_rating" && ["glamour", "sexy", "explicit", "glamour / sexy / explicit"].includes(value)) {
        return "glamour/sexy/explicit";
    }
    if (widget.name === "camera_direction") {
        const frontValues = new Set([
            "facing camera", "looking down toward camera", "looking upward", "front-facing symmetrical view",
            "head tilted toward camera", "high-angle view", "low-angle view",
            "pronounced high-angle view, with the camera positioned above the subject",
            "pronounced low-angle view, with the camera positioned below the subject",
        ]);
        if (frontValues.has(value)) return "front-facing view";
        if (value === "three-quarter angle" || value === "slight sideways glance") return "three-quarter view";
        if (value === "rear three-quarter view with the subject looking back over one shoulder") return "rear three-quarter view";
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
    if (values.length === V301_CANONICAL_WIDGET_ORDER.length) {
        if (CONTROL_AFTER_GENERATE_VALUES.has(String(values[88]).toLowerCase())) {
            return V301_CANONICAL_WIDGET_ORDER;
        }
        if (looksLikeSerializedBoolean(values[88])) return V15_CANONICAL_WIDGET_ORDER;
        return V11_CANONICAL_WIDGET_ORDER;
    }
    if (values.length === PRE_PICTURE_TYPE_CANONICAL_WIDGET_ORDER.length) {
        return PRE_PICTURE_TYPE_CANONICAL_WIDGET_ORDER;
    }
    // Public v1.0 and v1.1 share a length with older canonical layouts. At
    // index 88, their boolean/species signatures disambiguate them.
    // v3.0.1 has control_after_generate, v1.0 has the former boolean
    // enforce_single_subject, and v1.1 has species_mode. These signatures keep
    // the three identical lengths from being mistaken for each other.
    if (values.length === CANONICAL_WIDGET_ORDER.length) {
        return CANONICAL_WIDGET_ORDER;
    }
    if (values.length === V440_CANONICAL_WIDGET_ORDER.length) {
        return V440_CANONICAL_WIDGET_ORDER;
    }
    if (values.length === V430_CANONICAL_WIDGET_ORDER.length) {
        return V430_CANONICAL_WIDGET_ORDER;
    }
    if (values.length === V420_CANONICAL_WIDGET_ORDER.length) {
        return V420_CANONICAL_WIDGET_ORDER;
    }
    if (values.length === V410_CANONICAL_WIDGET_ORDER.length) {
        return V410_CANONICAL_WIDGET_ORDER;
    }
    if (values.length === V400_CANONICAL_WIDGET_ORDER.length) {
        return V400_CANONICAL_WIDGET_ORDER;
    }
    if (values.length === PRE_OUTFIT_STYLE_REMOVAL_CANONICAL_WIDGET_ORDER.length) {
        return PRE_OUTFIT_STYLE_REMOVAL_CANONICAL_WIDGET_ORDER;
    }
    if (values.length === PRE_BODY_MORPHOLOGY_CANONICAL_WIDGET_ORDER.length) {
        return PRE_BODY_MORPHOLOGY_CANONICAL_WIDGET_ORDER;
    }
    if (values.length === V20_CANONICAL_WIDGET_ORDER.length) {
        return V20_CANONICAL_WIDGET_ORDER;
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
    const legacySelfie = order.some((name, index) =>
        ["portrait_style", "capture_style"].includes(name)
        && ["bedroom selfie", LEGACY_SELFIE_CAPTURE_STYLE].includes(values[index]));
    const limit = Math.min(values.length, order.length);
    for (let index = 0; index < limit; index += 1) {
        const restoredName = order[index];
        const widget = byName.get(restoredName);
        const rawValue = values[index];
        if (!widget || rawValue === undefined) continue;
        if (restoredName === "body_feminine_curves" && LEGACY_CURVE_DETAIL_VALUES.has(rawValue)) {
            const detailWidget = byName.get("body_detail_1");
            if (detailWidget && [undefined, null, "None"].includes(detailWidget.value)) {
                detailWidget.value = LEGACY_CURVE_DETAIL_VALUES.get(rawValue);
            }
            widget.value = "None";
            continue;
        }
        if (restoredName === "portrait_style") {
            const capture = LEGACY_PORTRAIT_CAPTURE.get(rawValue);
            if (capture) {
                const captureWidget = byName.get("capture_style");
                if (captureWidget) captureWidget.value = capture;
            }
        }
        if (restoredName === "camera_direction") {
            const headWidget = byName.get("head_direction");
            const angleWidget = byName.get("camera_angle");
            if (headWidget) {
                if (rawValue === "looking upward") headWidget.value = "looking upward";
                if (["looking down toward camera", "looking downward toward the camera"].includes(rawValue)) headWidget.value = "looking downward";
                if (rawValue === "head tilted toward camera") headWidget.value = "head tilted slightly";
                if (rawValue === "slight sideways glance") headWidget.value = "glancing slightly to one side";
                if (rawValue === "rear three-quarter view with the subject looking back over one shoulder") headWidget.value = "looking back over one shoulder";
            }
            if (angleWidget) {
                if (["high-angle view", "pronounced high-angle view, with the camera positioned above the subject"].includes(rawValue)) {
                    angleWidget.value = "from a pronounced high angle, with the camera positioned above the subject";
                }
                if (["low-angle view", "pronounced low-angle view, with the camera positioned below the subject"].includes(rawValue)) {
                    angleWidget.value = "from a pronounced low angle, with the camera positioned below the subject";
                }
            }
            if (rawValue === "front-facing symmetrical view") {
                const compositionWidget = byName.get("shot_composition");
                if (compositionWidget) compositionWidget.value = "symmetrical composition";
            }
        }
        if (restoredName === "shot_composition" && rawValue === "tight crop") {
            const portraitWidget = byName.get("portrait_style");
            if (portraitWidget && ["None", "Random", "portrait"].includes(portraitWidget.value)) portraitWidget.value = "close-up portrait";
        }
        if (restoredName === "shot_composition" && rawValue === "wide framing") {
            const portraitWidget = byName.get("portrait_style");
            if (portraitWidget && ["None", "Random", "portrait"].includes(portraitWidget.value)) portraitWidget.value = "full-body portrait";
        }
        if (restoredName === "hosiery" && rawValue === "black tights") {
            widget.value = "opaque tights";
            const colorWidget = byName.get("hosiery_color");
            if (colorWidget) colorWidget.value = "black";
            continue;
        }
        if (restoredName === "pose") {
            const normalizedLegacyPose = LEGACY_POSE_VALUES.get(rawValue) || rawValue;
            const migratedScenario = LEGACY_ACTION_POSE_TO_SCENARIO.get(normalizedLegacyPose);
            if (migratedScenario) {
                const scenarioWidget = byName.get("scene_scenario");
                if (scenarioWidget) scenarioWidget.value = migratedScenario;
                widget.value = "None";
                continue;
            }
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

    if (legacySelfie) {
        const captureWidget = byName.get("capture_style");
        const poseWidget = byName.get("pose");
        if (captureWidget) captureWidget.value = "candid";
        if (poseWidget && ["None", "Random"].includes(poseWidget.value)) poseWidget.value = SELFIE_POSE;
    }

    if (![CANONICAL_WIDGET_ORDER, V440_CANONICAL_WIDGET_ORDER, V430_CANONICAL_WIDGET_ORDER, V420_CANONICAL_WIDGET_ORDER, V410_CANONICAL_WIDGET_ORDER, V400_CANONICAL_WIDGET_ORDER].includes(order)) {
        const legacyBodyTypeIndex = order.indexOf("body_type");
        const legacyBodyType = legacyBodyTypeIndex >= 0 ? values[legacyBodyTypeIndex] : undefined;
        const physiqueWidget = byName.get("body_physique");
        const curvesWidget = byName.get("body_feminine_curves");
        const detailWidget = byName.get("body_detail_1");
        const physiqueFromType = new Map([
            ["slim", "slim physique"], ["slender", "slim physique"], ["lanky", "very slim physique"],
            ["voluptuous", "plump physique"], ["plus-size", "plus-size physique"],
            ["stocky", "soft untrained physique"], ["broad-built", "muscular physique"],
        ]);
        const curvesFromType = new Map([
            ["voluptuous", "pronounced hourglass silhouette"], ["tall curvy", "pronounced hourglass silhouette"],
            ["androgynous", "androgynous silhouette"],
        ]);
        const detailFromType = new Map([
            ["short-legged", "short-legged proportions"], ["short-legged proportions", "short-legged proportions"],
            ["long-legged", "long-legged proportions"], ["long-legged proportions", "long-legged proportions"],
        ]);
        if (physiqueWidget && ["None", undefined].includes(physiqueWidget.value) && physiqueFromType.has(legacyBodyType)) {
            physiqueWidget.value = physiqueFromType.get(legacyBodyType);
        }
        if (curvesWidget && ["None", undefined].includes(curvesWidget.value) && curvesFromType.has(legacyBodyType)) {
            curvesWidget.value = curvesFromType.get(legacyBodyType);
        }
        if (detailWidget && ["None", undefined].includes(detailWidget.value) && detailFromType.has(legacyBodyType)) {
            detailWidget.value = detailFromType.get(legacyBodyType);
        }
    }

    // V3.0 and older compressed several independent V3.1 axes into one
    // positional widget. Re-expand those intentions only while restoring a
    // historical layout; a native V3.1 workflow already stores every axis.
    if (![CANONICAL_WIDGET_ORDER, V440_CANONICAL_WIDGET_ORDER, V430_CANONICAL_WIDGET_ORDER, V420_CANONICAL_WIDGET_ORDER, V410_CANONICAL_WIDGET_ORDER, V400_CANONICAL_WIDGET_ORDER].includes(order)) {
        const oldValue = (name) => {
            const index = order.indexOf(name);
            return index >= 0 && index < values.length ? values[index] : undefined;
        };
        const legacyPortrait = oldValue("portrait_style");
        const legacyPose = oldValue("pose");
        const legacyCamera = oldValue("camera_direction");
        const captureWidget = byName.get("capture_style");
        const cameraWidget = byName.get("camera_direction");
        const headWidget = byName.get("head_direction");
        const angleWidget = byName.get("camera_angle");

        if (captureWidget && legacyPortrait === "Random") captureWidget.value = "Random";

        const poseHorizontal = new Map([
            ["standing with the back partly turned, looking over one shoulder, hips shifted softly to one side", "three-quarter view"],
            ["standing in a three-quarter pose, one hand in the hair, hips turned away", "three-quarter view"],
            ["sitting sideways on a stool, upper body twisting toward the camera, one hand braced behind", "three-quarter view"],
            ["on hands and knees viewed from a rear three-quarter angle, hips angled toward the camera, looking back over one shoulder", "rear three-quarter view"],
        ]);
        const poseHead = new Map([
            ["standing with the back partly turned, looking over one shoulder, hips shifted softly to one side", "looking back over one shoulder"],
            ["on hands and knees viewed from a rear three-quarter angle, hips angled toward the camera, looking back over one shoulder", "looking back over one shoulder"],
            ["on hands and knees, back mostly straight, head turned toward the camera, natural elegant body line", "head held level"],
            ["on hands and knees, back softly arched, shoulders lowered, chin slightly raised toward the camera", "head held level"],
            ["on hands and knees with one knee drawn forward between the hands, torso twisted slightly toward the camera", "head held level"],
            ["kneeling with forearms resting on the floor, hips raised, back curved, head turned toward the camera", "head held level"],
        ]);

        if (legacyPose && legacyPose !== "Random" && [undefined, null, "None", "Random"].includes(legacyCamera)) {
            if (cameraWidget && poseHorizontal.has(legacyPose)) cameraWidget.value = poseHorizontal.get(legacyPose);
            if (headWidget && poseHead.has(legacyPose)) headWidget.value = poseHead.get(legacyPose);
        } else if (legacyCamera === "Random") {
            if (headWidget) headWidget.value = "Random";
        }
        if (legacyCamera === "Random" && angleWidget) angleWidget.value = "Random";
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

function emphasizeArchetypeWidget(widget) {
    if (!widget || widget._cpfArchetypeEmphasis) return;
    widget._cpfArchetypeEmphasis = true;
    if (!widget.options) widget.options = {};
    widget.options.color = "rgba(137, 180, 255, 0.98)";
    widget.options.bgcolor = "rgba(54, 63, 82, 0.98)";
    widget.options.text_color = "#f4f7ff";
    const label = widget.name === "body_archetype"
        ? "BODY ARCHETYPE"
        : widget.name === "composition_archetype"
            ? "COMPOSITION ARCHETYPE"
            : "CLOTHING ARCHETYPE";
    widget.label = label;
    widget.options.label = label;
    widget.computeSize = (width) => [width, 38];
    widget.draw = (ctx, targetNode, width, y) => {
        const margin = 6;
        const boxY = y + 3;
        const boxH = 30;
        const radius = 7;
        const value = String(widget.value ?? "None");

        const fittedText = (textValue, maxWidth) => {
            if (ctx.measureText(textValue).width <= maxWidth) return textValue;
            let shortened = textValue;
            while (shortened.length > 1 && ctx.measureText(`${shortened}…`).width > maxWidth) {
                shortened = shortened.slice(0, -1);
            }
            return `${shortened}…`;
        };

        ctx.save();
        ctx.shadowColor = "rgba(0, 0, 0, 0.58)";
        ctx.shadowBlur = 7;
        ctx.shadowOffsetY = 3;
        ctx.fillStyle = "rgba(57, 66, 86, 0.98)";
        ctx.beginPath();
        ctx.roundRect(margin, boxY, width - margin * 2, boxH, radius);
        ctx.fill();

        ctx.shadowColor = "transparent";
        ctx.strokeStyle = "rgba(151, 190, 255, 1)";
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.fillStyle = "rgba(151, 190, 255, 1)";
        ctx.beginPath();
        ctx.roundRect(margin + 5, boxY + 6, 4, boxH - 12, 2);
        ctx.fill();

        ctx.textBaseline = "middle";
        ctx.textAlign = "left";
        ctx.fillStyle = "#ffffff";
        ctx.font = "800 14px Inter, Arial, sans-serif";
        ctx.fillText(label, margin + 17, boxY + boxH / 2);

        const valueX = Math.max(275, width * 0.40);
        const valueWidth = Math.max(60, width - valueX - 34);
        ctx.font = "600 13px Inter, Arial, sans-serif";
        ctx.fillStyle = value === "None" ? "rgba(210, 218, 232, 0.78)" : "#f7f9ff";
        ctx.fillText(fittedText(value, valueWidth), valueX, boxY + boxH / 2);

        const arrowX = width - margin - 16;
        const arrowY = boxY + boxH / 2;
        ctx.fillStyle = "#dce8ff";
        ctx.beginPath();
        ctx.moveTo(arrowX - 5, arrowY - 3);
        ctx.lineTo(arrowX + 5, arrowY - 3);
        ctx.lineTo(arrowX, arrowY + 4);
        ctx.closePath();
        ctx.fill();
        ctx.restore();
    };
}

const CUSTOM_WIDGET_LABELS = new Map([
    ["media_type", "media_type"],
    ["eye_focus", "eye_focus"],
    ["mouth_expression", "mouth_expression"],
    ["enforce_portrait_framing", "enforce_portrait_framing"],
    ["setting_text_override", "setting_text_override"],
    ["pose_text_override", "pose_text_override"],
    ["face_hair_text_override", "face_hair_text_override"],
    ["custom_color_overrides", "custom_color_overrides"],
    ["wildcard_subject", "wildcard_subject"],
    ["wildcard_clothing", "wildcard_clothing"],
    ["wildcard_pose", "wildcard_pose"],
    ["wildcard_setting", "wildcard_setting"],
    ["wildcard_photography", "wildcard_photography"],
]);

function applyCustomWidgetLabel(widget) {
    const label = CUSTOM_WIDGET_LABELS.get(widget?.name);
    if (!label) return;
    if (!widget.options) widget.options = {};
    widget.label = label;
    widget.options.label = label;
}

function reorderWidgets(node) {
    dedupeWidgetsByName(node);
    const widgets = (node.widgets || []).filter((widget) => !isSectionWidget(widget));
    const byName = new Map(widgets.filter((w) => w?.name).map((w) => [w.name, w]));
    for (const widget of widgets) applyCustomWidgetLabel(widget);
    emphasizeArchetypeWidget(byName.get("composition_archetype"));
    emphasizeArchetypeWidget(byName.get("body_archetype"));
    emphasizeArchetypeWidget(byName.get("clothing_archetype"));
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
    name: "CharacterArchitect.Sections.v26",
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
