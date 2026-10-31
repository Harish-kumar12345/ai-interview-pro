import json
from typing import Any
from company_presets import get_company_prompt_note


SYSTEM_PROMPT = """You are an experienced professional interviewer. Return ONLY valid JSON.
CRITICAL FORMAT RULE: Your response must be a single JSON object containing a top-level "questions" key with an array of question objects, like:
{"questions": [...]}
Do NOT return a top-level list/array. Do NOT include markdown code fences or conversational text.
Create practical, role-appropriate interview content. Do not invent requirements outside the supplied context, avoid duplicate questions, and match the requested difficulty.
"""


def build_generation_prompt(configuration: dict[str, Any], focus: str) -> tuple[str, str]:
    context = json.dumps(configuration, indent=2)
    company_note = get_company_prompt_note(configuration.get("company", ""))
    resume_note = ""
    if configuration.get("resume_text"):
        resume_snippet = str(configuration["resume_text"])[:1800]
        resume_note = f"\nCandidate Resume Context (Craft questions referencing their projects and experiences where relevant):\n{resume_snippet}\n"

    user_prompt = f"""Generate exactly {configuration['question_count']} interview questions.
Question focus: {focus}
Candidate configuration:
{context}
{company_note}
{resume_note}

Output MUST strictly follow this JSON format:
{{
  "questions": [
    {{
      "id": 1,
      "question": "What is...",
      "type": "{focus}",
      "topic": "...",
      "difficulty": "{configuration.get('difficulty', 'Medium')}",
      "expected_answer": "...",
      "evaluation_criteria": ["Conceptual understanding", "Accuracy", "Completeness"],
      "rubric": {{"concept": 3, "accuracy": 3, "example": 2, "depth": 2}}
    }}
  ]
}}
For coding questions, include the problem statement, input, output, constraints, example, and expected approach in the question or expected_answer fields.
"""
    return SYSTEM_PROMPT, user_prompt
