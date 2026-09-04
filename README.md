# Character Architect

A ComfyUI prompt builder with high ethnicity adherence for Krea 2, deterministic conflict-aware randomization, detailed character styling, and optional Identity Forge compatibility.

## Version 4

### V4.5.0

V4.5.0 adds a missing everyday slim-curvy body recipe and repairs hosiery layering beneath covered legs:

- Adds the `Girl Next Door` Body Archetype: a predominantly slim, natural hourglass build with narrow thighs, a defined waist, slender upper arms and neck, plus specifically rounded projected bust and glutes. Its two new shape phrases and neck detail are also available manually.
- Replaces the ambiguous `underneath only on ankles` trouser wording with explicit physical layering: tights cover the legs beneath opaque trousers and remain visible only in the narrow exposed gap at the hems.
- Extends the same hosiery grammar to boiler suits, jumpsuits, denim overalls, trouser suits, and regional complete outfits built over full-length trousers.
- Removes equivalent hair wording duplicates such as `shoulder-length, shoulder-length hair` without merging genuinely distinct hairstyle, cut, texture, or length information.
- Preserves the V4.4.1 node identity, widget order, workflow serialization, hierarchy, and four outputs.

See `CHANGELOG-v4.5.0.md` for implementation and validation details.

### V4.4.1

V4.4.1 adds an optional `face_hair_text_override` input for a compact face-reference description produced upstream by ComfyUI `Generate Text`:

- Accepts semicolon-separated `key=value` pairs for face shape, jaw, chin, eyes, natural lashes, brows, nose, lips, optional facial hair, and the complete hair construction.
- Preserves the node's normal hierarchy per field: universal field override, then manual / `Forced Random`, then the reference description, then Identity Forge and ordinary `Random`.
- Suspends only the indivisible Subject wildcard and detailed Ethnicity Guidance when a valid reference is present. The simple origin category and every unrelated body, expression, makeup, clothing, pose, setting, camera, accessory, wildcard, and override control remain active.
- Reuses the existing renderers: face traits enter Full Prompt and Face Prompt, while only resolved hair enters Pre-gen Text.
- Keeps V4.4.0 workflows aligned through an appended optional widget and name-based migration. No vision dependency is added to Character Architect.

Recommended `Generate Text` instruction with `max_length` 256:

```text
Analyze the reference face image. Output only concise key=value pairs separated by semicolons, using these keys in this order when clearly visible: face_shape; jawline; chin_shape; eye_shape; eye_color; eyelashes; eyebrows; nose_shape; lip_shape; facial_hair; hair_color; hair_texture; hair_style; hair_cut; hair_length; bangs_style. Use short, literal, prompt-ready visual descriptions. For face_shape, eye_shape, eye_color, hair_color, and hair_texture, return only the descriptive value without adding the words face, eyes, or hair. Use facial_hair=none when no facial hair is visible. Do not describe expression, mouth action, gaze, makeup, complexion, skin color, age, gender, ethnicity, body, pose, clothing, accessories, background, lighting, camera, or image quality. Omit uncertain or hidden details. Output no introduction, commentary, full sentence, final period, or trailing comma.
```

See `CHANGELOG-v4.4.1.md` for the exact precedence and validation notes.

### V4.4.0

V4.4.0 adds `Composition Archetype`, a visually emphasized master row with 50 variable composition recipes:

- Coordinates framing, Pose, horizontal Camera direction, Head direction, Eye Focus, vertical Camera angle, and Shot composition without fixing Setting, Capture style, Lens, lighting, or mood.
- Uses only values available in the ordinary manual widgets. Manual and `Forced Random` fields remain authoritative; archetypes fill only `None` and ordinary `Random` fields.
- Keeps direct camera focus dominant across the catalogue while preserving action-specific focus for reading, writing, conversations, performances, and other clear visual targets.
- Preserves the rare Scene scenario branch: both rows on Random produce 90% Composition Archetype and 10% Scene scenario; a manual archetype suppresses an ordinary Random scenario, while a manual or Forced Random scenario suspends the archetype.
- Suspends Composition Archetype for free-form Pose or Photography wildcard/override input, but keeps it active with an externally supplied Setting alone.
- Keeps all V4.3 workflows unchanged through a dedicated name-based frontend migration; the new row defaults to `None`.

See `CHANGELOG-v4.4.0.md` for the complete catalogue, precedence rules, and validation notes.

### V4.3.0

V4.3.0 strengthens first-pass composition and expands scene variety while retaining the same node identity and four historical outputs:

- Adds `enforce_portrait_framing`, a protected switch that reduces Pre-gen Text to one minimal media/framing/age/simple-ethnicity/gender sentence. Fundamental anthropomorphic or feral subject type is retained when required.
- Adds the simple resolved `origin_ethnicity` category to normal Pre-gen Text without importing detailed Ethnicity Guidance, facial anatomy, makeup, or accessories.
- Keeps Identity Forge Archetype and Cosplayer labels as independent identity anchors, so choosing manual clothing no longer erases roles such as Lifeguard.
- Moves bicycle, horse, car-driving, carousel, and skateboard actions from Pose into five complete scenarios with explicit full-size physical context and automatic legacy migration.
- Makes ordinary Random scenarios rare at 10%, includes the branch in both global random buttons, and gives exact Pose/Setting strings and deliberate structured choices priority.
- Expands Setting from 64 to 101 environments, adds six freely combinable lying poses, adds a projected-bust Body Detail, and rewrites the tattoo session as a pre-session scene without skin contact.

See `CHANGELOG-v4.3.0.md` for the complete precedence and validation notes.

### V4.2.0

V4.2.0 consolidates the V4.1 customization build while preserving its external inputs and four historical outputs:

- Restores `content_rating` with two concrete directions: `normal` and `glamour/sexy/explicit`. The resolved treatment is included in Prompt and Pre-gen Text, protected by a default-on lock, and excluded from Face Prompt.
- Returns `media_type` to the global rows at the top of the node, outside the Media / Camera / Composition section's local random buttons.
- Restores lowercase labels for ordinary controls and reserves the stronger raised visual treatment for Body Archetype and Clothing Archetype.
- Makes the short cut of pajama short sets explicit in generated text so a downstream Prompt Refine pass cannot silently turn them into long pajama trousers.
- Migrates V4.1 workflows by name and merges historical `glamour`, `sexy`, and `explicit` ratings into the new combined value.

See `CHANGELOG-v4.2.0.md` for exact wording, migration, and validation details.

### V4.1.0

V4.1.0 keeps the same node identity and four historical output indexes while appending optional customization controls with name-based migration from V4.0.0:

- Moves Media Type beside lens, camera, lighting, and composition controls in the visual interface without changing its backend field.
- Adds independent `Eye Focus / Looking At` and `Mouth Expression` controls. Head direction now uses the universal `looking downward`; older `looking down toward camera` values migrate automatically.
- Adds dependency-free Setting and Pose text overrides. A native ComfyUI `Generate Text` node may caption a reference image upstream, but Character Architect receives only the resulting STRING and does not load Qwen, ControlNet, or a vision model.
- Adds compact arbitrary color overrides such as `top=fuchsia; hosiery=salmon pink; hair=teal`. Clothing colors modify only an active garment.
- Adds five optional expanded-wildcard inputs for Subject/Appearance, Clothing/Shoes, Pose/Action, Setting/Background, and Photography/Camera. Each replaces only its named block; Character Architect does not bundle or require a wildcard processor.
- Keeps the universal field override as the final authority. Setting/Pose reference text leads over the matching wildcard line, while all untouched categories continue to use the node normally.

See `CHANGELOG-v4.1.0.md` for validation and exact precedence details.

### V4.0.0

V4.0.0 keeps the same node identity, 86 serialized category slots, and four output indexes as the final V3.2.5 Body Archetype build. It refines generation quality without breaking existing workflows:

- Full Random now leaves optional outerwear, glasses, head accessories, armwear, bags, and scarves on `None`; each row can still be randomized or selected manually.
- `Free Prompt` is included in Pre-gen Text at the selected insertion position.
- Lighting is resolved against the selected setting or complete scene scenario. Manual and `Forced Random` choices keep priority; ordinary Random avoids contradictory interior/exterior combinations.
- Regional garments retain concise, concrete visual descriptions while exposing shorter, easier-to-read widget labels. Historical saved labels are migrated automatically.
- Jewelry is expressed as separate body-bound slots, preventing a choker and earrings from being fused into one pendant.
- Body Archetype and Clothing Archetype use a stronger raised, outlined treatment so the two controlling rows are immediately visible.

See `CHANGELOG-v4.0.0.md` for the complete V4 change list and validation summary.

## Version 3 history

### V3.2.4 to V3.2.5

- Added loose flowing and fitted flared jumpsuits; ordinary Random suppresses a competing top, while manual and Forced Random tops are worn over them.
- Added Japanese-inspired trousers, sarouel pants, mesh-panel athletic leggings, and an oversized fishnet sweater.
- Ordinary height Random excludes both dwarfism and giant stature; Forced Random and manual selection include them.
- Removed pure back view, strengthened the pronounced arched-back description, and refined the handshake action.
- Slightly increased lingerie and cosplay as standalone random clothing families, independently of Outfit style.
- Removed ambiguous lowered-jacket visibility wording and documented the new implicit rules in mouse-over help.

V3.2.4 makes Scene scenario a genuine alternative to Pose + Setting instead of an always-winning random layer, without changing serialization or output indexes.

### V3.2.3 to V3.2.4

- `Scene scenario = None` keeps the classic independent Pose + Setting path.
- `Scene scenario = Random` chooses evenly between one complete scenario and the classic Pose + Setting path.
- `Forced Random` guarantees a scenario, while a concrete manual scenario remains authoritative.
- The winning scenario branch clears Pose and Setting before camera coherence, so discarded pose geometry cannot influence the result.
- Keeps frontend schema v21 and every historical workflow migration unchanged.

### V3.2.2 to V3.2.3

- Simplifies the mechanically unreliable raised-heel side squat while preserving its lateral character.
- Gives intrinsically side-oriented Random poses profile and three-quarter camera directions instead of contradictory frontal views.
- Prevents ordinary Random from combining a high camera with high-in-frame placement, or a low camera with low-in-frame placement.
- Keeps every explicit and `Forced Random` combination available, including intentionally unusual geometry.
- Updates tooltips while preserving frontend schema v21 and all historical workflow migrations.

### V3.2.1 to V3.2.2

- Adds the three broad silhouette controls to `Pre-gen Text` using the same grammatical form as the main prompt.
- Continues to exclude detailed anatomy, ethnicity, face, hair, clothing, accessories, and free text.

### V3.2.0 to V3.2.1

- Adds `Pre-gen Text`, containing only the photographic introduction, subject kind, scene/action, camera and composition instructions, and the active realism epilogue.
- Excludes ethnicity detail, anatomy, body, face, hair, clothing, accessories, and free text from this companion output.
- Appends the new socket after the three existing outputs so old workflow connections remain unchanged.

### V3.1.3 to V3.2.0

- Moves the unreliable selfie capture style into a concrete phone-holding Pose and migrates old selfie workflows.
- Adds opt-in `Scene scenario` presets that replace separate Pose and Setting with one coherent action-environment clause.
- Adds social, observational, and object-based poses while retaining ordinary standalone body poses.
- Separates Body height, weighted Body physique families, and silhouette/proportions, with migration of older mixed body types.
- Treats minimalist monochrome as clothing only and adds `selective-color monochrome` as an explicit optical effect.
- Preserves garment layering, hosiery wording, footwear visibility, creature anatomy anchors, manual choices, Forced Random, and override priority.
- Uses frontend schema v21 with an explicit schema-v20 migration map.

### V3.1.2 → V3.1.3

- Describes hosiery normally with dresses, skirts, shorts, and other short bottoms.
- With mid-length trousers, places hosiery `visible below the trouser hems`.
- With long trousers, uses the empirically validated `underneath only on ankles` wording.
- Keeps manual and `Forced Random` hosiery present, while preserving all existing cosplay and priority rules.
- Leaves frontend schema v20 and every serialization map unchanged.

### V3.1.1 → V3.1.2

- Replaces the broad `portrait` footwear rule with a combined pose, framing, and vertical-angle estimate.
- Strongly favors footwear for floor-level, crouching, all-fours, lower-body action, high-angle, and worm's-eye views.
- Strongly reduces footwear in ordinary low-angle views and keeps close-up/headshot suppression.
- Gives visible socks and hosiery a small footwear-coherence bonus.
- Leaves manual choices, `Forced Random`, complete cosplay footwear, override, and schema v20 untouched.

### V3.1.0 → V3.1.1

- Introduces worn outerwear before the underlying outfit so jackets and coats act as the dominant enclosing layer.
- Gives properly worn, shoulder-draped, and elbow-lowered outerwear distinct visibility wording for the clothes beneath.
- Keeps an item carried over one shoulder after the outfit because it is not functioning as an outer layer.
- Applies the same ordering to creature prompts without changing their JSON-derived anatomy anchors.
- Keeps frontend schema v20 and all serialization maps unchanged.

### V3.0.1 → V3.1.0

- Splits `Portrait style / framing` from the new `Capture style` control.
- Splits horizontal `Camera direction`, `Head direction`, and vertical `Camera angle`, including worm's-eye and bird's-eye views.
- Removes camera, gaze, framing, mood, and motion-blur instructions embedded inside Pose values.
- Weights ordinary Random toward readable front/three-quarter views and mostly eye-level angles; rear and extreme views remain available, while manual and `Forced Random` combinations stay free.
- Guides ordinary Random framing from pose visibility, and guides pose from an explicitly selected close framing.
- Gives handheld selfies compatible pose, direction, angle, composition, lens, and lighting pools.
- Keeps scene geometry together near the beginning of the prompt and introduces makeup/nails/tattoos as `Styling details`.
- Preserves manual choices, `Forced Random`, text override, Identity Forge compatibility, and all historical serialization maps.

### V2 → V3

- Adds direct compatibility with the JSON output of Identity Forge preset nodes.
- Keeps Archetype, Cosplayer, Modifier, and ordinary JSON documents on Character Architect's established human renderer.
- Activates the nonhuman renderer only when both `_meta.creature_of` and a non-empty `Species & Anatomy` group explicitly identify a creature.
- Uses Character Architect's Gender control for creature presentation and pronouns, avoiding inherited `woman` / `man` wording.
- Reuses the creature's own anatomy phrases as clothing anchors instead of inventing a humanoid body.
- Preserves the existing priority order: text override, manual and `Forced Random`, imported JSON, then ordinary `Random`.
- Keeps the V2 human controls and deterministic selections while deliberately replacing their old flat prompt order with V3.1's semantic scene grammar.

### Identity Forge compatibility

Connect the `character_json` output of Identity Forge Archetype, Cosplayer, Creature, Modifier, or a chained combination to Character Architect's `identity_forge_json` input. The JSON is aggregated into Character Architect's own prompt order; Identity Forge's final text-rendering node is not required.

A connected JSON document does **not** automatically mean “creature”. Archetype and Cosplayer presets remain human. The nonhuman-safe grammar is selected only when the document explicitly contains both a creature marker (`_meta.creature_of`) and actual anatomy in `Species & Anatomy`. `Anthropomorphic` and `Feral` forms use the creature renderer; `Subtle` forms keep the human renderer and add their supplied traits.

Character Architect remains the authority for gender. Its Gender value becomes `feminine`, `masculine`, or `androgynous` in the creature subject and controls subsequent pronouns. JSON gender metadata is deliberately not allowed to reintroduce `of a woman` or `of a man`.

For leading creatures, ordinary Random human anatomy and organ-dependent accessories are suppressed. Manually selected values, `Forced Random`, the universal text override, and explicit JSON values remain deliberate escape hatches. Garments are adapted with a small deterministic grammar that quotes the JSON's own `integument`, `arms`, and `legs_feet` descriptions; Character Architect does not classify or reinterpret the creature itself.

## Version 2

### V1 → V2 in seven lines

- Independent per-property Random, preserved migrations, and universal override/inspection.
- Stronger Ethnicity Guidance with profile-compatible anatomy and eye-color pools.
- Exclusive garment families, fairer complete-cosplay draws, and safer layering.
- Close framing, action poses, gloves, nails, footwear, and settings resolve hidden conflicts.
- Glasses appear at 33%, bags at 40%, and deliberately randomized scarves at 30%.
- Hair, neckline, and bottom-length combinations are softly guided, never rigidly banned.
- Harsh photo-treatment collisions are softened while preserving a 20% wild-card share.

V2.1.1 keeps V1 workflows compatible while adding a final soft-coherence pass to both Random systems. Complete cosplays now protect authored headwear from an ordinary Random head accessory. When a structured cosplay already contains a jacket, coat, blazer, uniform, robe, or sleeves, ordinary Random `halter neckline` and `off-shoulder neckline` are suppressed; neckline depth remains independent. Manual choices, `Forced Random`, and text override always remain authoritative.

## Outputs

- **Prompt**: complete character and scene prompt.
- **Face Prompt**: reduced face-detail prompt retaining the selected medium, ethnicity anchor, facial traits, hair, makeup, facial hair, head accessories, earrings, and lighting.

## Main controls

Each visual category header includes:

- **LOCK / LOCKED**: preserves the category during global operations.
- **RANDOMIZE ALL ONCE**: immediately replaces eligible rows with concrete visible choices.
- **SET ALL RANDOM**: places eligible dropdowns on `Random`, so they resolve again when the seed changes.
- **RESET TO NONE**: restores eligible rows to `None`.

The top global controls respect pivot locks, locked categories, and protected rows such as `body_hair`, `facial_hair`, `skin_finish`, and `free_prompt_position`.

## Ethnicity guidance

`ethnicity_guidance` can be activated to replace the broad `origin_ethnicity` label with a stronger, concrete phenotype anchor. The official classification contains 13 profiles:

- northern european
- western european
- eastern european
- southern european
- middle eastern
- north african
- sub-saharan african
- east asian
- southeast asian
- south asian
- central asian
- latin american
- afro-caribbean

When guidance is active, random facial anatomy already covered by the anchor is omitted rather than appended as a contradictory instruction. Eye color set to either `None` or `Random` uses a weighted ethnicity-specific pool and is injected directly into the anchor, preventing duplicate color instructions. `Forced Random` and manual eye colors deliberately override that pool. Random hair color, hair texture, and skin finish retain their compatible pools.

The ethnicity anchor stays in the opening identity sentence, with its global ethnicity label at the end of the anchor. Scene geometry follows immediately, before body detail and clothing inventories can bury it.

## Scene geometry

`Portrait style / framing` controls only how much of the subject is visible. `Capture style` controls photographic intent such as glamour, editorial, candid, and documentary treatments. `Camera direction` is horizontal, `Head direction` is independent, and `Camera angle` is vertical. This allows useful combinations such as rear three-quarter + looking back + worm's-eye without hiding those directions inside a pose.

`Composition Archetype` sits above these controls and provides 50 variable, setting-independent recipes. Each recipe coordinates Portrait style, Pose, Camera direction, Head direction, Eye Focus, Camera angle, and Shot composition. It does not control Media type, Capture style, Pose mood, Setting, Scene scenario, Lens style, Lighting style, or Optical effect. The recipe name is never written into the prompt; only its resolved manual vocabulary is rendered.

An archetype fills only fields left on `None` or ordinary `Random`. Manual and `Forced Random` choices become fixed anchors, and the remaining recipe fields adapt around them when possible. If two explicit fields contradict each other, both remain untouched. `SET ALL RANDOM` places Composition Archetype on Random; `RANDOMIZE ALL ONCE` selects a concrete recipe and leaves its seven controlled rows on Random so the backend can resolve their conditional relationships from the visible seed.

The `Pose` dropdown contains body mechanics plus a restrained set of social and object-based actions. `Taking a selfie` now means extending an arm and holding a smartphone toward the subject; it is an action seen by the camera rather than a framing style. Its old capture-style form migrates to `candid` plus this pose. Ordinary Random jointly guides pose visibility and framing; manual choices, `Forced Random`, and override stay authoritative.

`Scene scenario` is a rare complete action-and-environment phrase which replaces separate Pose and Setting. When Scene scenario and Composition Archetype are both on Random, the existing ten-percent scenario branch is preserved and the remaining ninety percent uses a composition recipe. A manual Composition Archetype suppresses only an ordinary Random scenario; a manual or Forced Random scenario wins and suspends the archetype.

For cycling, riding, driving, carousel riding, and skateboarding, an ordinary Random setting is suppressed because the action already supplies its physical context. Manual settings, `Forced Random`, and override remain free. Dancing keeps the regular setting behavior.

The generated prompt groups the scene directly after the identity introduction. Body and facial traits, hair, clothing, accessories, and a final `Styling details include ...` sentence follow as separate semantic clauses instead of loose comma fragments.

## Clothing

Automated randomization chooses only one primary clothing branch at a time:

- top + bottom
- dress
- lingerie / swimwear
- sleepwear / loungewear
- generic cosplay
- Western franchise cosplay
- Asian franchise cosplay

`bottom_length` adds an explicit lower-body length choice: `very short`, `short`, `knee-length`, `mid-length`, or `long`.

When hosiery and a lower garment are both selected, the wording follows the garment family:

```text
short bottom, skirt, or dress: [garment phrase], [hosiery phrase]
mid-length trousers: [trousers], with [hosiery] visible below the trouser hems
long trousers: [trousers], with [hosiery] underneath only on ankles
```

The unusual long-trouser wording is intentional: it was more reliable in image tests than a grammatically richer description. Manual and `Forced Random` hosiery remain injected because the user has explicitly accepted the combination; the rule only changes how that combination is expressed.

Manual layering remains supported. Selected lingerie can be described under a dress, separates, cosplay, or sleepwear. Outerwear has its own wearing-style control: correctly worn, draped over both shoulders, slipped symmetrically to the elbows, or carried over one shoulder. Ordinary Random uses a safety-weighted 60/15/15/10 distribution while manual and Forced Random choices remain free.

`Forced Random` always resolves to a present feature. Explicit absence values
such as `no bag`, `no scarf`, `no glasses`, `bare feet`, and `bare legs` are
excluded from Forced Random pools, while remaining available to ordinary
`Random` and as manual choices.

Body controls deliberately separate `Body height`, `Body physique`, and
silhouette/proportions. Ordinary physique Random draws from balanced
underweight, ordinary, heavier, and muscular families instead of overweighting
near-synonymous average builds. This allows combinations such as `short` with
`obese physique`, while manual and `Forced Random` remain unrestricted.

## Clothing archetypes

`clothing_archetype` guides clothing rows that are set to `Random` or `None` while leaving every manually selected or `Forced Random` value untouched. Concrete garments now carry the visual direction formerly represented by the removed `outfit_style` row. The 12 archetypes are:

- Classy Chic
- Casual Everyday
- Streetwear
- Romantic / Feminine Soft
- Glam / Night Out
- Gothic / Dark Romantic
- Emo / Scene / Alt
- Sporty / Athleisure
- Boho / Festival
- Loungewear / Sleepwear / Boudoir
- Kawaii
- Regional Everyday / Formalwear

Random cosplay branches are suppressed while an archetype is active. Fixed manual cosplay selections remain possible. Kawaii uses mascot and cartoon-inspired everyday garments rather than randomly selecting a full franchise cosplay. Emo / Scene / Alt retains a 50% chance of a visible modern lingerie layer, including neon options; Casual Everyday has a restrained 10% chance of a subtle bra or bralette edge without turning lingerie into the main outfit.

Because cosplay entries are complete outfit descriptions whose leg coverage
cannot be inferred reliably, hosiery set to `Random` is suppressed whenever a
cosplay outfit is active. Hosiery selected explicitly by the user remains
available and is preserved.

Generic cosplay also suppresses ordinary Random outfit styling, outerwear,
belts, footwear, and their dependent colors. Light accessories remain
available. Manual values, `Forced Random`, and text override deliberately
bypass these protections.

Franchise cosplay entries also suppress random outfit styling, outerwear,
belts, footwear and accessory additions. Their signature colors and equipment
are described directly in the franchise prompt. Explicit manual additions are
still preserved for users who intentionally want to customize the costume.

## Seed behavior

The node includes:

- `seed`
- `control_after_generate`

Dropdowns set to `Random` resolve deterministically from the current seed. Each category uses an independent seed stream, so changing one fixed property does not reshuffle unrelated random values such as clothing. With `control_after_generate` set to `randomize`, all random categories still receive new choices at each queued generation because the global seed changes.

Every category dropdown also provides `Forced Random`. Unlike ordinary
`Random`, it deliberately bypasses archetype, ethnicity, cosplay, and other
protective random filters for that specific field. Global and section buttons
continue to set ordinary `Random`; forced randomization must be selected
manually. Mutually exclusive main clothing branches still resolve to one
randomly selected branch, while a forced-random lingerie layer can accompany a
manually selected main outfit.

The `Setting` category contains an expanded pool of contextual environments.
Entries describe atmosphere, architectural depth, materials, and diffuse
background activity without locking each generation to one overly specific
event or prop.

## Gloves and nail compatibility

When a resolved cosplay or armwear choice fully covers the hands, an ordinary
`Random` nail style is suppressed to avoid contradictory glove-and-nail prompts.
Fingerless pieces do not trigger the rule. Manual nail choices and
`Forced Random` remain untouched.

`Bedroom selfie` and `spontaneous handheld selfie` from older workflows migrate
to the `candid` capture style plus the explicit phone-holding selfie pose. The
selected `Setting` remains authoritative.

## Optical effects

`Optical effect` appears at the end of the Composition section and can
apply `fisheye`, `infrared false-color`, `high-contrast duotone`, or
`selective-color monochrome` to the
selected medium. The effect is quoted and injected into the opening media
phrase, for example `A "fisheye" photograph` or `An "infrared false-color"
photograph`, rather than appended weakly at the end. Ordinary `Random`
deliberately resolves to no effect 70% of the time and distributes the remaining
30% across the four effects; `Forced Random` always chooses an effect. New nodes and
resets leave this protected special-effect row on `None`, so global random
buttons do not activate it accidentally.
The previous schema-v20 canonical serialization order is preserved as an
explicit migration map, so existing workflows restore without positional shifts.

## Clothing-family randomization

Only garment-type widgets activate a main clothing family; fixed colors and
lengths no longer make every family concrete. Generic, Western-franchise, and
Asian-franchise cosplay share one statistical family. The internal source draw
is weighted by each source's number of entries, so every individual costume has
approximately the same chance of appearing. Without an archetype, a normal random lingerie/swimwear
layer is retained beneath separates or a dress 10% of the time. When their main
outfit is separates or a dress, other clothing archetypes use the same restrained
10% chance, while Emo / Scene / Alt uses 50%.
Swimwear remains eligible because the constrained-visibility sentence
keeps it subordinate. Manual and `Forced Random` layers remain valid.

Ordinary underlayers use the standalone sentence `Through the small parts that
protrude from the clothing, one can guess a [lingerie] beneath the clothes.`
Casual and Emo archetypes retain their established subtle-peeking and visibly
layered wording.

Concrete garment types now suppress ordinary `Random` competing families even
without an archetype; `Forced Random` remains exempt. Casual and Emo may still
layer lingerie beneath a manually selected cosplay according to their 10% and
50% rules, while an unstyled cosplay - or a cosplay under another archetype -
suppresses ordinary random lingerie.

Hosiery, outerwear, and belts have independent color widgets. Legacy `black
tights` restores as `black opaque tights`. Ordinary random glasses now resolve
to `no glasses` 67% of the time and to a concrete pair 33% of the time; manual
and `Forced Random` selections retain their normal behavior.

Ordinary `Random` footwear estimates probable foot visibility from the resolved
pose, framing, and vertical camera angle instead of treating every `portrait` as
a close crop. Floor-level, crouching, all-fours, and lower-body action poses are
strong signals; high-angle and worm's-eye views favor footwear, while an ordinary
low-angle view strongly reduces it. Visible socks or hosiery add a small
coherence bonus. Only close-up and headshot framing impose automatic suppression.
When Random footwear is omitted, its Random color is removed in the same atomic
decision. Manual and `Forced Random` footwear remain authoritative, and footwear
authored directly inside a complete cosplay description is intentionally untouched.

## Universal override and inspection

`Override field` selects one structured property and the connectable
`Override text` socket supplies its replacement. A non-empty connected string
is applied after randomization, ethnicity guidance, clothing archetypes,
compatibility checks, framing suppression, and every other hidden rule. It is
therefore the final authority for that one property.

When the overridden property is a main garment type (`top_type`,
`bottom_type`, `dress_type`, `sleepwear_type`, or a cosplay source), competing
main garment families are cleared after resolution. This guarantees that a
custom connected garment appears in the prompt instead of remaining hidden
behind a previously resolved dress or franchise cosplay. Compatible secondary
layers such as lingerie, outerwear, belts, hosiery, footwear, and accessories
remain independent; a sleepwear override clears a competing lingerie main
outfit because those two families cannot both occupy the primary slot.

`Inspect property` selects one resolved property. The `Inspected Value` output
returns only its final text, after all rules and any override, making it easy to
label comparison grids, add image overlays, or collect statistics without
parsing the complete prompt. The two selectors were appended to the canonical
widget order; older workflows restore by their historical order and receive
`None` for both new controls.

## Installation

Extract the complete folder into:

```text
ComfyUI/custom_nodes/ComfyUI-CharacterArchitect/
```

Restart ComfyUI and force-refresh the browser with `Ctrl + F5` after updating the JavaScript frontend.

## Workflow compatibility

Character Architect visually reorganizes widgets into sections, while ComfyUI stores widget values positionally. The frontend serializes values in the backend schema's canonical order and includes migration maps for earlier canonical and visually reordered releases. Existing `mediterranean` and `latina` values migrate to `southern european` and `latin american`; the removed `mixed heritage` value returns to `None`.

Public v1.1 replaces the ineffective `Force Single Subject` control with
`Outerwear wearing style`. Although both releases contain the same total number
of positional values, the migration layer distinguishes the former boolean
layout explicitly before restoring by widget name. Legacy smartphone-lens and
candlelit-ambiance choices return to `None`; legacy high- and low-angle values
migrate to their stronger camera-position formulations.

## Built-in guidance

Hovering a regular widget shows its interaction rules, probabilities, silent
protections, and layering behavior. Section headers also expose a compact
summary. These tooltips are metadata only: they add no widget, do not alter the
canonical order, and therefore do not shift serialized workflow values.
