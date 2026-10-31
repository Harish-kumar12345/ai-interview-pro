from typing import Any

from llm_client import LLMClient
from prompts.evaluation_prompt import build_prompt
from validators import validate_evaluation


class EvaluationError(RuntimeError):
    pass


def evaluate_answer(question: dict[str, Any], answer: str, client: LLMClient) -> dict[str, Any]:
    system_prompt, user_prompt = build_prompt(question, answer)
    payload = client.complete_json(system_prompt, user_prompt)
    errors = validate_evaluation(payload)
    if errors:
        raise EvaluationError("Evaluation was invalid: " + " ".join(errors))
    return payload


def generate_followup(question: dict[str, Any], answer: str, evaluation: dict[str, Any], client: LLMClient) -> str:
    system_prompt = (
        "You are an expert interviewer conducting an adaptive technical interview. "
        "Return only valid JSON with the shape: {\"followup_question\": \"...\", \"focus_concept\": \"...\"}"
    )
    missing = ", ".join(evaluation.get("missing_concepts", [])) or "depth and trade-offs"
    user_prompt = f"""Original Question: {question.get('question')}
Candidate Answer: {answer}
Identified Missing Concepts: {missing}
Candidate Score: {evaluation.get('score')}/10

Based on the candidate's answer and what they missed or glossed over, ask ONE sharp, concise, realistic follow-up question to probe their depth or understanding of edge cases.
"""
    try:
        payload = client.complete_json(system_prompt, user_prompt)
        return payload.get("followup_question", "Could you elaborate on the trade-offs of your proposed approach?")
    except Exception:
        return "Can you explain how this solution handles scale, concurrency, or failure edge cases?"
