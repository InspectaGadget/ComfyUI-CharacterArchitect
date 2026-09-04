# Character Architect V4.5.0

## Body Archetype

- Added `Girl Next Door` as the twenty-sixth Body Archetype.
- The recipe favors average height and a slim, untrained build with a soft natural hourglass rather than plump or plus-size morphology.
- It localizes fullness to a rounded naturally projected bust and prominent rounded glutes while retaining slim or narrow thighs, a very narrow defined waist, slender upper arms, and a slender neck with a delicate shoulder line.
- Added `full rounded bust with natural forward projection` to the manual Bust vocabulary.
- Added `prominent rounded glutes` to the manual Butt shape vocabulary.
- Added `slender neck and delicate shoulder line` to the shared manual Body Detail vocabulary.
- The archetype continues to fill only `None` and ordinary `Random`; manual values and `Forced Random` remain authoritative.

## Hosiery and covered legs

- Removed the ambiguous phrase `underneath only on ankles`.
- Long trousers now state that hosiery is worn fully underneath and visible only in the narrow gap between the trouser hems and footwear, or in a narrow ankle band when no footwear is present.
- Naturally long trousers receive the same protection even when their optional Length control is left on `None`; culottes and capri pants retain mid-length behavior.
- Mid-length trousers explicitly place hosiery underneath and below their hems.
- Added the same deterministic relationship for full-length jumpsuits and complete trouser-based outfits, including utility boiler suits and denim overalls.
- Hosiery and integrated footwear are emitted once, in both the Full Prompt and Pre-gen Text.

## Hair wording

- Equivalent descriptors differing only by the redundant word `hair` or punctuation are emitted once.
- Distinct texture, color, styling, cut, length, and bangs descriptors remain independent.

## Compatibility and validation

- No widget was added or removed; existing serialized workflows remain positionally compatible.
- The node keeps the `CharacterPromptFactory` backend identity and all four outputs.
- Added deterministic coverage for the new archetype, manual vocabulary reachability, trousers, boiler suits, overalls, jumpsuits, footwear integration, Pre-gen Text, and hair deduplication.
- All 63 Python tests and both frontend test suites pass.
