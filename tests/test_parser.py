import pytest

from question_generator import QuestionGenerationError, generate_questions


class FakeClient:
    def __init__(self, payload):
        self.payload = payload

    def complete_json(self, system_prompt, user_prompt):
        return self.payload


def test_question_generator_rejects_malformed_response():
    configuration = {"role": "Developer", "experience": "Fresher", "skills": ["Python"], "domain": "General", "difficulty": "Easy", "question_type": "Technical", "question_count": 1}
    with pytest.raises(QuestionGenerationError):
        generate_questions(configuration, FakeClient({"questions": []}))


def test_question_generator_normalizes_raw_list():
    configuration = {"role": "Developer", "experience": "Fresher", "skills": ["Python"], "domain": "General", "difficulty": "Easy", "question_type": "Technical", "question_count": 1}
    raw_list = [
        {
            "id": 1,
            "question": "What is Python?",
            "expected_answer": "A programming language",
            "type": "Technical",
            "topic": "Python",
            "difficulty": "Easy",
            "evaluation_criteria": ["Clarity"],
            "rubric": {"concept": 5}
        }
    ]
    result = generate_questions(configuration, FakeClient(raw_list))
    assert len(result) == 1
    assert result[0]["question"] == "What is Python?"


def test_question_generator_normalizes_capital_key():
    configuration = {"role": "Developer", "experience": "Fresher", "skills": ["Python"], "domain": "General", "difficulty": "Easy", "question_type": "Technical", "question_count": 1}
    capital_payload = {
        "Questions": [
            {
                "id": 1,
                "question": "Explain OOP.",
                "expected_answer": "Object oriented programming",
                "type": "Technical",
                "topic": "OOP",
                "difficulty": "Easy",
                "evaluation_criteria": ["Clarity"],
                "rubric": {"concept": 5}
            }
        ]
    }
    result = generate_questions(configuration, FakeClient(capital_payload))
    assert len(result) == 1
    assert result[0]["question"] == "Explain OOP."
