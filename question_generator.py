from typing import Any

from llm_client import LLMClient
from prompt_generator import build_generation_prompt
from validators import normalize_questions_payload, validate_questions


class QuestionGenerationError(RuntimeError):
    pass


def autofill_question_defaults(questions: list[Any], configuration: dict[str, Any]) -> list[dict[str, Any]]:
    clean_questions: list[dict[str, Any]] = []
    default_skills = configuration.get("skills", [])
    default_topic = default_skills[0] if default_skills else configuration.get("domain", "General")
    default_type = configuration.get("question_type", "Technical")
    default_diff = configuration.get("difficulty", "Medium")

    for idx, item in enumerate(questions, start=1):
        if not isinstance(item, dict):
            continue
        q = dict(item)
        if not q.get("id"):
            q["id"] = idx
        if not q.get("type"):
            q["type"] = default_type
        if not q.get("difficulty") or q.get("difficulty") == "Mixed":
            q["difficulty"] = default_diff
        if not q.get("topic"):
            q["topic"] = default_topic
        if not q.get("expected_answer") and q.get("answer"):
            q["expected_answer"] = q["answer"]
        if not q.get("evaluation_criteria"):
            q["evaluation_criteria"] = q.get("criteria", ["Accuracy", "Reasoning", "Completeness"])
        elif isinstance(q["evaluation_criteria"], str):
            q["evaluation_criteria"] = [q["evaluation_criteria"]]
        if not isinstance(q.get("rubric"), dict):
            q["rubric"] = {"concept": 3, "accuracy": 3, "example": 2, "depth": 2}
        clean_questions.append(q)

    return clean_questions


def generate_questions(configuration: dict[str, Any], client: LLMClient) -> list[dict[str, Any]]:
    system_prompt, user_prompt = build_generation_prompt(configuration)
    raw_payload = client.complete_json(system_prompt, user_prompt)
    
    # 1. Normalize top-level structure
    payload = normalize_questions_payload(raw_payload)

    # 2. Autofill fields if questions list exists
    if isinstance(payload, dict) and isinstance(payload.get("questions"), list):
        questions_list = payload["questions"]
        exp_count = configuration.get("question_count", len(questions_list))
        # If model returned more questions than requested, take the first exp_count
        if len(questions_list) > exp_count:
            questions_list = questions_list[:exp_count]
        payload["questions"] = autofill_question_defaults(questions_list, configuration)

    # 3. Validate
    errors = validate_questions(payload, configuration["question_count"])
    if errors:
        raise QuestionGenerationError("Generated interview was invalid: " + " ".join(errors))
    return payload["questions"]
