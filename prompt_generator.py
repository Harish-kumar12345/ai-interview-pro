from typing import Any

from prompts.behavioral_prompt import build_prompt as behavioral_prompt
from prompts.coding_prompt import build_prompt as coding_prompt
from prompts.conceptual_prompt import build_prompt as conceptual_prompt
from prompts.hr_prompt import build_prompt as hr_prompt
from prompts.scenario_prompt import build_prompt as scenario_prompt
from prompts.technical_prompt import build_prompt as technical_prompt
from prompts.base import build_generation_prompt as build_base_prompt


PROMPT_BUILDERS = {
    "Technical": technical_prompt,
    "Coding": coding_prompt,
    "Conceptual": conceptual_prompt,
    "Scenario-Based": scenario_prompt,
    "Behavioral": behavioral_prompt,
    "HR": hr_prompt,
}


def build_generation_prompt(configuration: dict[str, Any]) -> tuple[str, str]:
    question_type = configuration["question_type"]
    if question_type == "Mixed":
        return build_base_prompt(configuration, "Mixed: balance technical, coding, conceptual, scenario-based, behavioral, and HR questions")
    builder = PROMPT_BUILDERS[question_type]
    return builder(configuration)