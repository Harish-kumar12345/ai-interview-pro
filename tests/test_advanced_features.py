import io
from company_presets import COMPANY_PROFILES, get_company_prompt_note
from pdf_exporter import generate_interview_pdf
from resume_parser import extract_resume_text


def test_company_preset_note():
    note = get_company_prompt_note("Google")
    assert "Google" in note
    assert "scalability" in note.lower()

    standard_note = get_company_prompt_note("General / Standard")
    assert standard_note == ""


def test_resume_parser_handles_none():
    assert extract_resume_text(None) == ""


class DummyFile:
    def __init__(self, name: str, content: bytes):
        self.name = name
        self.content = content

    def getvalue(self) -> bytes:
        return self.content


def test_resume_parser_handles_txt():
    dummy = DummyFile("resume.txt", b"Skills: Python, FastAPI\nExperience: 2 years at TechCorp")
    extracted = extract_resume_text(dummy)
    assert "Python" in extracted
    assert "TechCorp" in extracted


def test_pdf_exporter_generates_valid_pdf():
    report = {
        "overall_score": 85,
        "average": 8.5,
        "questions": 1,
        "attempted": 1,
        "topic_scores": {"System Design": 8.5},
        "evaluations": [
            {
                "score": 8,
                "feedback": "Strong architecture with good fault tolerance.",
                "strengths": ["Clear tradeoffs"],
                "missing_concepts": []
            }
        ]
    }
    cfg = {"role": "Backend Engineer", "company": "Amazon"}
    questions = [{"question": "Design payment idempotency", "topic": "System Design", "difficulty": "Hard"}]
    answers = {0: "Use Redis distributed lock and idempotency keys with unique UUIDs."}
    
    pdf_bytes = generate_interview_pdf(report, cfg, questions, answers)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")

