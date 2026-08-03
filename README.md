# Character Architect

A standalone ComfyUI prompt builder with detailed controls for character appearance, ethnicity guidance, pose, clothing, cosplay, accessories, and composition.

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

The ethnicity anchor is emitted before `content_rating`, with its global ethnicity label at the end of the anchor. The concrete `pose` follows ethnicity and content rating, before clothing sentences.

## Pose

The `pose` dropdown contains concrete standing, seated, crouching, kneeling, all-fours, and reclining body positions, plus a small experimental set of action poses: cycling, horse riding, driving, carousel riding, skateboarding, and dancing mid-spin. For the first five actions, an ordinary Random setting is suppressed because the action already supplies its scene context; manual settings, `Forced Random`, and override remain free. Dancing keeps the regular setting behavior. Gaze language is limited so it does not compete unnecessarily with `eye_expression`.

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

Manual layering remains supported. Selected lingerie can be described under a dress, separates, cosplay, or sleepwear. Outerwear has its own wearing-style control: correctly worn, draped over both shoulders, slipped symmetrically to the elbows, or carried over one shoulder. Ordinary Random uses a safety-weighted 60/15/15/10 distribution while manual and Forced Random choices remain free.

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
time; `Forced Random` always chooses one of the three effects. New nodes and
resets leave this protected special-effect row on `None`, so global random
buttons do not activate it accidentally.
The previous 89-value canonical serialization order is preserved as an explicit
migration map, so existing workflows restore without positional shifts.

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

Ordinary `Random` footwear is suppressed from `close-up portrait` through
`three-quarter portrait`, and under `tight crop`. For wider or ambiguous
framing it remains deliberately probabilistic: 10% for generic `portrait`, 50%
for `full-body portrait`, 67% for `full-body glamour portrait`, and 20% for
other portrait styles. This prevents an off-frame shoe from reappearing as a
detached prop attached to a bag or floating beside the subject while still
letting genuinely wide images specify footwear. Its Random color is removed in
the same atomic decision. Hosiery remains allowed because it can appear
naturally at the edge of a crop. Manual and `Forced Random` footwear remain
authoritative, and footwear authored directly inside a complete cosplay
description is intentionally untouched.

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
