from .node import CharacterArchitectNode

NODE_CLASS_MAPPINGS = {
    "CharacterPromptFactory": CharacterArchitectNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CharacterPromptFactory": "Character Architect",
}

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
