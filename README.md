# Character Architect

A standalone ComfyUI prompt builder with detailed controls for character appearance, ethnicity guidance, pose, clothing, cosplay, accessories, and composition.

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

When guidance is active, random facial anatomy already covered by the anchor is omitted rather than appended as a contradictory instruction. Random eye color, hair color, hair texture, and skin finish use compatible pools. Manually selected values remain untouched, including deliberately unusual combinations.

The ethnicity anchor is emitted before `content_rating`, with its global ethnicity label at the end of the anchor. The concrete `pose` follows ethnicity and content rating, before clothing sentences.

## Pose

The `pose` dropdown contains concrete standing, seated, crouching, kneeling, all-fours, and reclining body positions. Gaze language is deliberately limited so it does not compete unnecessarily with `eye_expression`.

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

When a bottom and hosiery are both selected, the prompt uses:

```text
[bottom phrase] layered over [hosiery phrase]
```

`mid-length` bottoms describe the hosiery as partially visible, while
`long` bottoms describe it as mostly concealed. Shorter bottoms keep the
hosiery fully visible.

Manual layering remains supported. Selected lingerie can be described under a dress, separates, cosplay, or sleepwear, while outerwear is described over the main outfit.

`Forced Random` always resolves to a present feature. Explicit absence values
such as `no bag`, `no scarf`, `no glasses`, `bare feet`, and `bare legs` are
excluded from Forced Random pools, while remaining available to ordinary
`Random` and as manual choices.

Body controls deliberately separate general stature/build from physique.
This allows combinations such as `very petite` with `plump physique` or
`obese physique`, while retaining a smaller set of useful muscular options.

## Clothing archetypes

`clothing_archetype` guides clothing rows that are set to `Random` while leaving every manually selected value untouched. Choosing an archetype also injects a compatible random `outfit_style`, even when that row is left on `None`. The 11 archetypes are:

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

Random cosplay branches are suppressed while an archetype is active. Fixed manual cosplay selections remain possible. Kawaii uses mascot and cartoon-inspired everyday garments rather than randomly selecting a full franchise cosplay. Emo / Scene / Alt retains a 50% chance of a visible modern lingerie layer, including neon options; Casual Everyday has a restrained 10% chance of a subtle bra or bralette edge without turning lingerie into the main outfit.

Because cosplay entries are complete outfit descriptions whose leg coverage
cannot be inferred reliably, hosiery set to `Random` is suppressed whenever a
cosplay outfit is active. Hosiery selected explicitly by the user remains
available and is preserved.

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

`Bedroom selfie` from older workflows is migrated to `spontaneous handheld
selfie`. The portrait style now describes the framing rather than imposing a
bedroom, so the selected `Setting` remains authoritative.

## Optical effects

`Optical effect` appears at the end of the Composition section and can
apply `fisheye`, `infrared false-color`, or `high-contrast duotone` to the
selected medium. The effect is quoted and injected into the opening media
phrase, for example `A "fisheye" photograph` or `An "infrared false-color"
photograph`, rather than appended weakly at the end. Ordinary `Random`
deliberately resolves to no effect 70% of the time and to each effect 10% of the
time; `Forced Random` always chooses one of the three effects.
The previous 89-value canonical serialization order is preserved as an explicit
migration map, so existing workflows restore without positional shifts.

## Clothing-family randomization

Only garment-type widgets activate a main clothing family; fixed colors and
lengths no longer make every family concrete. Generic, Western-franchise, and
Asian-franchise cosplay now share one statistical family, followed by an
internal source draw. Without an archetype, a normal random lingerie/swimwear
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

## Installation

Extract the complete folder into:

```text
ComfyUI/custom_nodes/ComfyUI-CharacterArchitect/
```

Restart ComfyUI and force-refresh the browser with `Ctrl + F5` after updating the JavaScript frontend.

## Workflow compatibility

Character Architect visually reorganizes widgets into sections, while ComfyUI stores widget values positionally. The frontend serializes values in the backend schema's canonical order and includes migration maps for earlier canonical and visually reordered releases. Existing `mediterranean` and `latina` values migrate to `southern european` and `latin american`; the removed `mixed heritage` value returns to `None`.

## Built-in guidance

Hovering a regular widget shows its interaction rules, probabilities, silent
protections, and layering behavior. Section headers also expose a compact
summary. These tooltips are metadata only: they add no widget, do not alter the
canonical order, and therefore do not shift serialized workflow values.
