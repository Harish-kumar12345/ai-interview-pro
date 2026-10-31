from prompt_generator import build_generation_prompt


def test_prompt_includes_configuration_and_type():
    system, user = build_generation_prompt({"role": "Python Developer", "experience": "Fresher", "skills": ["Python"], "domain": "Software Development", "difficulty": "Medium", "question_type": "Technical", "question_count": 5})
    assert "Python Developer" in user
    assert "exactly 5" in user
    assert "Technical" in user
    assert "valid JSON" in system