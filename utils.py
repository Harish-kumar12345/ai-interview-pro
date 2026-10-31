from collections import defaultdict
from typing import Any


def score_percent(score: float, maximum: float = 10) -> float:
    return round((score / maximum) * 100, 1) if maximum else 0


def aggregate_scores(questions: list[dict[str, Any]], evaluations: list[dict[str, Any]]) -> dict[str, Any]:
    topic_scores: dict[str, list[float]] = defaultdict(list)
    difficulty_scores: dict[str, list[float]] = defaultdict(list)
    for question, evaluation in zip(questions, evaluations):
        score = float(evaluation.get("score", 0))
        topic_scores[question.get("topic", "General")].append(score)
        difficulty_scores[question.get("difficulty", "Mixed")].append(score)
    average = sum(float(item.get("score", 0)) for item in evaluations) / len(evaluations) if evaluations else 0
    return {
        "average": round(average, 2),
        "overall_score": round(score_percent(average), 1),
        "topic_scores": {key: round(sum(values) / len(values), 2) for key, values in topic_scores.items()},
        "difficulty_scores": {key: round(sum(values) / len(values), 2) for key, values in difficulty_scores.items()},
    }