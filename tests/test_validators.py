from validators import validate_evaluation, validate_interview_input, validate_questions


def test_input_validation_rejects_missing_fields():
    errors = validate_interview_input({"question_count": 3})
    assert len(errors) == 7


def test_question_validation_accepts_structured_questions():
    question = {"question": "Explain X", "type": "Technical", "topic": "X", "difficulty": "Easy", "expected_answer": "...", "evaluation_criteria": ["accuracy"], "rubric": {"concept": 10}}
    assert validate_questions({"questions": [question]}, 1) == []


def test_evaluation_validation_rejects_bad_score():
    payload = {"score": 11, "max_score": 10, "strengths": [], "weaknesses": [], "missing_concepts": [], "feedback": "ok", "improvement_suggestions": []}
    assert "Evaluation score must be between 0 and 10." in validate_evaluation(payload)