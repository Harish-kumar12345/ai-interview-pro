# AI Interview Question Generator

**Project ID:** P_112  
**Domain:** AI Tooling / Education / Cross-Industry

AI Interview Question Generator is a Streamlit application for personalized interview practice. A candidate configures a target role, skills, experience, domain, difficulty, and question type. An LLM API generates structured questions and expected answers, then evaluates each candidate response against its criteria and rubric.

## Core Stack

Python + Streamlit + LLM API, with local JSON storage. The app uses an OpenAI-compatible API client and supports a custom `LLM_BASE_URL`. RAG is **not implemented** in this version.

## Features

- Dynamic technical, coding, conceptual, scenario-based, behavioral, and HR questions
- Role, skill, experience, domain, difficulty, and count controls
- Structured JSON generation and evaluation with validation
- One-question-at-a-time interview session preserved in Streamlit session state
- Score, topic, difficulty, and question-level analytics
- Local interview history without a database
- Friendly configuration, timeout, rate-limit, and malformed-response errors

## Architecture

`main.py` coordinates the UI. `prompt_generator.py` selects a focused prompt module. `llm_client.py` performs the API call. `question_generator.py` and `evaluator.py` validate structured responses. `storage.py` persists completed reports to `data/interview_history.json`.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `LLM_API_KEY` and `LLM_MODEL` in `.env`. Set `LLM_BASE_URL` only when using an OpenAI-compatible provider with a custom endpoint.

## Run

```powershell
streamlit run main.py
```

The app does not require an API key to run its shell, but generation and evaluation do require valid provider configuration.

## Test

```powershell
pytest -q
```

Tests use mocked LLM responses and never require a real API key.

## LLM and hallucination handling

An LLM is a Large Language Model. It generates context-aware interview material from the candidate configuration, while Python provides application logic and Streamlit provides the interface. Strong prompts, constrained inputs, JSON output, and validation reduce hallucination risk, but cannot eliminate incorrect or fabricated content. Human review remains appropriate.

## Example

Input: Python Developer, Fresher, Python/SQL/APIs, Software Development, Medium, Technical, 5 questions.  
Output: five structured questions with topics, expected answers, criteria, rubrics, then a score and feedback for every submitted answer.

## Limitations and future scope

The initial version is single-user and local, depends on an external LLM API, and does not provide authoritative certification of answer correctness. Future work may add RAG, resume-based questions, company-specific preparation, voice input, adaptive interviews, advanced analytics, accounts, cloud deployment, and personalized recommendations. RAG would require document chunking, embeddings, retrieval, and relevant context injection; none of that is present here.

## Screenshots

Run the app locally and capture the Home, Create Interview, Interview, and Results views for project documentation.