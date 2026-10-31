from typing import Any


def validate_interview_input(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "role": "Choose a job role.",
        "experience": "Choose an experience level.",
        "domain": "Choose a domain.",
        "difficulty": "Choose a difficulty.",
        "question_type": "Choose a question type.",
    }
    for field, message in required.items():
        if not str(config.get(field, "")).strip():
            errors.append(message)
    if not config.get("skills"):
        errors.append("Select or enter at least one skill.")
    count = config.get("question_count")
    if count not in {5, 10, 15, 20}:
        errors.append("Question count must be 5, 10, 15, or 20.")
    return errors


def normalize_questions_payload(payload: Any) -> dict[str, Any]:
    """Ensure payload has a 'questions' key even if Gemini returned a list or alternative key."""
    if isinstance(payload, list):
        return {"questions": payload}
    if isinstance(payload, dict):
        if "questions" in payload and isinstance(payload["questions"], list):
            return payload
        for key in ("Questions", "interview_questions", "interviewQuestions", "items", "data", "technical_questions"):
            if key in payload and isinstance(payload[key], list):
                return {"questions": payload[key]}
        for val in payload.values():
            if isinstance(val, list) and (not val or isinstance(val[0], dict)):
                return {"questions": val}
    return payload


def validate_questions(payload: Any, expected_count: int) -> list[str]:
    payload = normalize_questions_payload(payload)

    if not isinstance(payload, dict) or not isinstance(payload.get("questions"), list):
        return ["The LLM response did not contain a questions list."]
    questions = payload["questions"]
    if len(questions) != expected_count:
        return [f"The LLM returned {len(questions)} questions; expected {expected_count}."]
    errors: list[str] = []
    for index, question in enumerate(questions, start=1):
        if not isinstance(question, dict):
            errors.append(f"Question {index} is not an object.")
            continue
        for field in ("question", "type", "topic", "difficulty", "expected_answer", "evaluation_criteria", "rubric"):
            if not question.get(field):
                errors.append(f"Question {index} is missing {field}.")
        if not isinstance(question.get("evaluation_criteria"), list):
            errors.append(f"Question {index} evaluation criteria must be a list.")
        if not isinstance(question.get("rubric"), dict):
            errors.append(f"Question {index} rubric must be an object.")
    return errors


def validate_evaluation(payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return ["The LLM evaluation was not an object."]
    errors: list[str] = []
    score = payload.get("score")
    if not isinstance(score, (int, float)) or not 0 <= score <= 10:
        errors.append("Evaluation score must be between 0 and 10.")
    if payload.get("max_score") != 10:
        errors.append("Evaluation max_score must be 10.")
    for field in ("strengths", "weaknesses", "missing_concepts", "improvement_suggestions"):
        if not isinstance(payload.get(field), list):
            errors.append(f"Evaluation {field} must be a list.")
    if not isinstance(payload.get("feedback"), str) or not payload["feedback"].strip():
        errors.append("Evaluation feedback is required.")
    return errors
