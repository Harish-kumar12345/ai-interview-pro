from typing import Any

from prompts.base import build_generation_prompt


def build_prompt(configuration: dict[str, Any]) -> tuple[str, str]:
    return build_generation_prompt(configuration, "Conceptual")