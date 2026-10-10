# Character Architect v5.1.1

## ComfyUI frontend compatibility

- Registers custom section widgets with `node.addCustomWidget()` so each section receives the identity required by ComfyUI frontend 1.55's reactive widget store.
- Reuses registered section widgets on every layout pass, preventing duplicate headers while retaining colors, locks, and randomization controls.
- No longer removes and restores custom section widgets inside `serialize()`. Autosave can therefore serialize the canonical prompt values without exposing a temporary degraded layout to the reactive store.
- Rebuilds the layout from both the node-definition hooks and the current `nodeCreated` / `loadedGraphNode` extension hooks.

## Compatibility

- No Python prompt-generation behavior changed.
- No widget names, canonical value order, output positions, archetype rules, randomization behavior, or legacy migrations changed from v5.1.0.
- Existing v5.1.0 workflows remain compatible.

## Validation

- JavaScript syntax check.
- Frontend migration, grouping, archetype-arrow, registered-section reuse, and non-mutating serialization tests.
- Complete Python unit-test suite plus import validation.
