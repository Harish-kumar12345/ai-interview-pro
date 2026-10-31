# P_112 Architecture

## Requirement Analysis

P_112 is a lightweight AI interview preparation tool. A candidate configures an interview, receives dynamically generated questions from an LLM API, submits answers one at a time, receives rubric-based AI feedback, and gets a persisted performance report.

The core stack is Python, Streamlit, an LLM API, and local JSON storage. RAG, vector databases, user accounts, and server-side databases are intentionally out of scope for the initial version.

## Data Flow

```text
Candidate -> Streamlit form -> input validation -> prompt builder
          -> LLM client -> JSON parser/validator -> session state
          -> answer form -> evaluation prompt -> LLM client
          -> evaluation validator -> report analytics -> JSON history
```

Every LLM response crosses a validation boundary before it is used by the UI. API credentials stay in environment variables and are never placed in session state.

## UI Structure

1. Home: product overview, capability cards, and Start Interview action.
2. Create Interview: role, experience, skills, domain, difficulty, question type, and count form.
3. Interview: one question at a time, answer submission, feedback, and navigation.
4. Results: score summary, topic and difficulty breakdowns, recommendations, and question detail.
5. History: previously saved interview summaries and expandable reports.

The sidebar provides navigation and session reset controls. Session state owns the active interview so Streamlit reruns do not lose progress.

## Module Responsibilities

- `config.py`: environment-backed settings and API configuration.
- `llm_client.py`: timeout-aware, error-normalized LLM API calls.
- `prompts/`: type-specific generation templates and evaluation template.
- `prompt_generator.py`: maps interview type to the appropriate prompt.
- `question_generator.py`: requests, parses, and validates question JSON.
- `evaluator.py`: requests and validates candidate evaluation JSON.
- `validators.py`: input and structured-output validation.
- `storage.py`: atomic local JSON history persistence.
- `utils.py`: display-safe formatting and score aggregation helpers.
- `main.py`: Streamlit pages and workflow orchestration only.

## LLM Interaction

The client uses an OpenAI-compatible HTTP API configured with `LLM_API_KEY`, `LLM_MODEL`, and optionally `LLM_BASE_URL`. Generation and evaluation request JSON objects and use conservative prompts that include the candidate context, rubric, and explicit anti-duplication instructions. The parser rejects missing or malformed fields rather than silently accepting unsafe output.

## Development Roadmap

1. Establish scaffold and configuration.
2. Implement prompts, client, parsing, and validation.
3. Implement session workflow and Streamlit UI.
4. Add report analytics and local history.
5. Add mocked unit tests and documentation.
6. Run compile, tests, and smoke checks without requiring a real API key.

## Dependencies

- `streamlit`: Python presentation layer.
- `openai`: OpenAI-compatible LLM API client.
- `python-dotenv`: local `.env` loading.
- `pytest`: test runner.

No RAG or external database dependency is used.