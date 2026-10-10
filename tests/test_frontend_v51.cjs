const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const frontendPath = path.join(__dirname, "..", "web", "character_architect_v17.js");
let source = fs.readFileSync(frontendPath, "utf8");
source = source.replace(
    'import { app } from "../../scripts/app.js";',
    `let registeredExtension;
const app = {
    registerExtension(extension) { registeredExtension = extension; },
    graph: { setDirtyCanvas() {} },
};`,
);
source += `
return {
    emphasizeArchetypeWidget,
    reorderWidgets,
    registeredExtension,
    LEGACY_COMPOSITION_ARCHETYPE_LABELS,
    CANONICAL_WIDGET_ORDER,
    V500_CANONICAL_WIDGET_ORDER,
    GROUPS,
};`;

const frontend = new Function(source)();

assert.equal(frontend.CANONICAL_WIDGET_ORDER.length, frontend.V500_CANONICAL_WIDGET_ORDER.length + 1);
assert.equal(
    frontend.CANONICAL_WIDGET_ORDER[frontend.CANONICAL_WIDGET_ORDER.indexOf("top_type") + 1],
    "sleeve_length",
);
assert.equal(frontend.GROUPS.filter((group) => group.id === "body").length, 1);
assert.equal(frontend.GROUPS.some((group) => group.id === "body_specific"), false);

let registrations = 0;
const sectionNode = {
    widgets: [],
    size: [850, 200],
    addCustomWidget(section) {
        registrations += 1;
        section.widgetId = `registered-${registrations}`;
        this.widgets.push(section);
        return section;
    },
    computeSize() { return [850, 600]; },
    setSize(size) { this.size = size; },
    setDirtyCanvas() {},
};
frontend.reorderWidgets(sectionNode);
assert.equal(registrations, frontend.GROUPS.length);
assert.equal(
    sectionNode.widgets.filter((item) => item.type === "cpf-section").length,
    frontend.GROUPS.length,
);
assert.ok(
    sectionNode.widgets
        .filter((item) => item.type === "cpf-section")
        .every((item) => item.widgetId),
);
frontend.reorderWidgets(sectionNode);
assert.equal(registrations, frontend.GROUPS.length);

function MockNodeType() {}
MockNodeType.prototype.serialize = function () {
    return { widgets_values: ["legacy"] };
};
frontend.registeredExtension.beforeRegisterNodeDef(MockNodeType, { name: "CharacterPromptFactory" });
const serialNode = Object.create(MockNodeType.prototype);
serialNode.widgets = sectionNode.widgets;
const widgetsBeforeSerialize = serialNode.widgets;
serialNode.serialize();
assert.strictEqual(serialNode.widgets, widgetsBeforeSerialize);

let opened = 0;
const widget = {
    name: "body_archetype",
    value: "None",
    options: { values: ["None", "Random", "Soft Obese Male"] },
    callback() {},
    mouse() {
        opened += 1;
        return "menu";
    },
};
frontend.emphasizeArchetypeWidget(widget);
widget._cpfArchetypeWidth = 400;
const targetNode = { size: [400, 100], setDirtyCanvas() {} };

assert.equal(widget.mouse({ type: "pointerdown" }, [390, 18], targetNode), true);
assert.equal(widget.value, "Random");
assert.equal(widget.mouse({ type: "pointerdown" }, [10, 18], targetNode), true);
assert.equal(widget.value, "None");
assert.equal(widget.mouse({ type: "pointerdown" }, [10, 18], targetNode), true);
assert.equal(widget.value, "Soft Obese Male");
assert.equal(widget.mouse({ type: "pointerdown" }, [200, 18], targetNode), "menu");
assert.equal(opened, 1);

assert.equal(
    frontend.LEGACY_COMPOSITION_ARCHETYPE_LABELS.get("Direct Headshot"),
    "Headshot — centered, direct camera gaze",
);

console.log("Frontend v5.1.1 reactive sections, archetype arrows, body merge, and migration checks passed");
