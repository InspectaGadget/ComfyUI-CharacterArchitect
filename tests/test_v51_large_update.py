import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("character_architect_v51", ROOT / "node.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CharacterArchitectV51Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.node = MODULE.CharacterArchitectNode()
        cls.by_key = {item["key"]: item for item in MODULE.SCHEMA["categories"]}
        cls.creature = json.dumps({
            "_meta": {
                "creature_of": "frog",
                "creature_class": "Animals",
                "form": "Anthropomorphic",
                "suppress_groups": ["Demographics", "Face", "Hair", "Makeup", "Body"],
            },
            "Species & Anatomy": {
                "head": "a broad frog head",
                "integument": "smooth green amphibian skin",
                "arms": "long amphibian arms",
                "hands": "webbed hands",
                "legs_feet": "powerful frog legs with webbed feet",
            },
        })

    def defaults(self):
        return {item["key"]: item.get("default", "None") for item in MODULE.SCHEMA["categories"]}

    def test_public_species_and_gender_vocabulary(self):
        self.assertEqual(
            MODULE.CharacterArchitectNode.INPUT_TYPES()["optional"]["species_mode"][0],
            ["Neutral / None", "Human", "Creature", "Anthro Furry"],
        )
        self.assertEqual(
            self.by_key["gender"]["values"][:4],
            ["woman", "female", "man", "male"],
        )

        data = self.defaults()
        data["gender"] = "male"
        prompt = self.node.build_prompt(
            identity_forge_json=self.creature,
            species_mode="Creature",
            seed=1,
            **data,
        )[0]
        self.assertIn("male anthropomorphic frog", prompt)
        self.assertNotIn("hybrid", prompt)

    def test_creature_body_random_stays_suppressed_but_directed_archetype_opts_in(self):
        random_data = self.defaults()
        random_data.update({
            "gender": "male",
            "body_archetype": "Random",
            "body_type": "Random",
            "body_physique": "Random",
            "body_feminine_curves": "Random",
            "bust": "Random",
            "butt_shape": "Random",
            "thigh_shape": "Random",
            "body_detail_1": "Random",
            "body_detail_2": "Random",
            "body_detail_3": "Random",
        })
        ordinary = self.node.build_prompt(
            identity_forge_json=self.creature,
            species_mode="Creature",
            seed=8,
            **random_data,
        )[0]
        self.assertNotIn("obese physique", ordinary)
        self.assertNotIn("masculine silhouette", ordinary)

        directed_data = dict(random_data)
        directed_data["body_archetype"] = "Soft Obese Male"
        directed = self.node.build_prompt(
            identity_forge_json=self.creature,
            species_mode="Creature",
            inspect_property="body_archetype",
            seed=8,
            **directed_data,
        )
        self.assertEqual(directed[2], "Soft Obese Male")
        self.assertIn("obese physique", directed[0])
        self.assertIn("masculine silhouette", directed[0])
        self.assertIn("masculine chest", directed[0])
        self.assertIn("prominent abdomen", directed[0])

        for selection in ("Female Random", "Male Random", "Forced Random"):
            with self.subTest(selection=selection):
                variant = dict(random_data)
                variant["body_archetype"] = selection
                resolved = self.node._resolve_values(
                    variant,
                    seed=17,
                    species_mode="Creature",
                )
                output = self.node.build_prompt(
                    identity_forge_json=self.creature,
                    species_mode="Creature",
                    inspect_property="body_archetype",
                    seed=17,
                    **variant,
                )
                self.assertEqual(output[2], resolved["body_archetype"])
                self.assertTrue(any(
                    resolved.get(field) and resolved[field] in output[0]
                    for field in MODULE.BODY_ARCHETYPE_CONTROL_FIELDS
                ))

    def test_soft_obese_male_is_non_muscular_and_manually_reachable(self):
        config = MODULE.BODY_ARCHETYPE_CONFIG["Soft Obese Male"]
        flattened = " ".join(value for values in config.values() for value in values)
        self.assertIn("obese physique", flattened)
        self.assertIn("soft masculine silhouette", flattened)
        self.assertIn("prominent abdomen", flattened)
        self.assertNotIn("muscular", flattened)

        allowed = {key: set(item["values"]) for key, item in self.by_key.items()}
        for key, values in config.items():
            manual_key = "body_detail_1" if key == "body_details" else key
            self.assertTrue(set(values).issubset(allowed[manual_key]))

    def test_cross_gender_classic_menswear_remains_menswear(self):
        expected_tops = set(MODULE.CLOTHING_ARCHETYPE_CONFIG["Classic Menswear"]["top_type"])
        expected_bottoms = set(MODULE.CLOTHING_ARCHETYPE_CONFIG["Classic Menswear"]["bottom_type"])
        for seed in range(60):
            data = self.defaults()
            data.update({
                "gender": "woman",
                "clothing_archetype": "Classic Menswear",
                "top_type": "Random",
                "sleeve_length": "Random",
                "bottom_type": "Random",
                "bottom_length": "long",
            })
            resolved = self.node._resolve_values(data, seed=seed)
            self.assertIn(resolved["top_type"], expected_tops)
            self.assertIn(resolved["bottom_type"], expected_bottoms)
            self.assertEqual(
                MODULE._gender_tag_for_value("bottom_type", resolved["bottom_type"]),
                "male",
            )

    def test_sleeve_length_is_attached_to_the_active_top(self):
        data = self.defaults()
        data.update({
            "top_type": "sweater",
            "top_color": "cream",
            "sleeve_length": "extra-long sleeves extending past the wrists and partly covering the hands",
        })
        prompt, _, inspected, pre_gen, _, _ = self.node.build_prompt(
            seed=3,
            inspect_property="sleeve_length",
            **data,
        )
        phrase = (
            "cream sweater with extra-long sleeves extending past the wrists "
            "and partly covering the hands"
        )
        self.assertIn(phrase, prompt)
        self.assertIn(phrase, pre_gen)
        self.assertEqual(
            inspected,
            "extra-long sleeves extending past the wrists and partly covering the hands",
        )

        data["top_type"] = "tank top"
        data["sleeve_length"] = "Random"
        resolved = self.node._resolve_values(data, seed=6)
        self.assertEqual(resolved["sleeve_length"], "no sleeves, leaving the arms fully uncovered")

    def test_expanded_settings_and_scenarios_are_reachable(self):
        settings = set(self.by_key["setting"]["values"])
        scenarios = set(self.by_key["scene_scenario"]["values"])
        self.assertGreaterEqual(len(settings), 145)
        self.assertGreaterEqual(len(scenarios), 40)
        self.assertIn("in Paris with the Eiffel Tower clearly visible", settings)
        self.assertIn(
            "inside the panoramic lounge of a submarine with immense windows overlooking deep-sea fish and coral",
            settings,
        )
        self.assertIn(
            "jumping over an obstacle inside a colorful platform-game world of pipes, blocks, and coins",
            scenarios,
        )

    def test_composition_labels_describe_the_recipe_but_stay_out_of_prompts(self):
        label = MODULE.LEGACY_COMPOSITION_ARCHETYPE_LABELS["Direct Headshot"]
        self.assertIn("Headshot", label)
        self.assertIn("direct camera gaze", label)
        prompt, _, inspected, pre_gen, _, _ = self.node.build_prompt(
            composition_archetype=label,
            media_type="photograph",
            gender="woman",
            inspect_property="composition_archetype",
            seed=2,
        )
        self.assertEqual(inspected, label)
        self.assertNotIn(label, prompt)
        self.assertNotIn(label, pre_gen)

    def test_frontend_merges_body_and_draws_cycling_arrows(self):
        source = (ROOT / "web" / "character_architect_v17.js").read_text(encoding="utf-8")
        self.assertNotIn('id: "body_specific"', source)
        self.assertIn("const direction = x <= 38 ? -1 : x >= width - 38 ? 1 : 0", source)
        self.assertIn("prepareBodyArchetypeOnce", source)
        self.assertIn("prepareClothingArchetypeOnce", source)
        self.assertIn('name: "CharacterArchitect.Sections.v28"', source)


if __name__ == "__main__":
    unittest.main()
