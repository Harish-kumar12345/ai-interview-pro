import json
from typing import Any


def build_prompt(question: dict[str, Any], answer: str) -> tuple[str, str]:
    system = """You are a fair, precise interview evaluator. Return only valid JSON.
Score the candidate answer against the supplied expected answer and rubric. Do not
award points merely for keyword overlap; judge correctness, reasoning, relevance,
completeness, technical accuracy, and examples."""
    user = f"""Question:
{question.get('question')}

Expected answer:
{question.get('expected_answer')}

Evaluation criteria:
{json.dumps(question.get('evaluation_criteria', []))}

Rubric:
{json.dumps(question.get('rubric', {}))}

Candidate answer:
{answer}

Return exactly:
{{"score": 0, "max_score": 10, "strengths": [], "weaknesses": [],
"missing_concepts": [], "feedback": "...", "improvement_suggestions": []}}"""
    return system, user