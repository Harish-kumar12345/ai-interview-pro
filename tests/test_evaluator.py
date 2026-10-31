from evaluator import evaluate_answer


class FakeClient:
    def complete_json(self, system_prompt, user_prompt):
        return {"score": 8, "max_score": 10, "strengths": ["Correct"], "weaknesses": ["Depth"], "missing_concepts": [], "feedback": "Good answer.", "improvement_suggestions": ["Add an example."]}


def test_evaluator_returns_validated_payload():
    question = {"question": "What is Python?", "expected_answer": "A language", "evaluation_criteria": ["accuracy"], "rubric": {"concept": 10}}
    result = evaluate_answer(question, "A programming language", FakeClient())
    assert result["score"] == 8