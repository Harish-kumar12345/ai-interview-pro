import csv
from html import escape
from io import StringIO
from typing import Any

import streamlit as st

from company_presets import COMPANY_PROFILES
from evaluator import EvaluationError, evaluate_answer, generate_followup
from llm_client import LLMClient, LLMError
from pdf_exporter import generate_interview_pdf
from question_generator import QuestionGenerationError, generate_questions
from resume_parser import extract_resume_text
from storage import load_history, save_interview
from ui.components import (
    render_audio_speaker,
    render_badge,
    render_brand,
    render_empty_state,
    render_evaluation_lists,
    render_face_to_face_room,
    render_feature_card,
    render_followup_card,
    render_metric_card,
    render_page_intro,
    render_question_card,
    render_rubric,
    render_score_chart,
    render_score_gauge,
    render_section_header,
    render_step,
    render_stepper,
    render_timer,
    render_top_header,
    render_webcam_tile,
)
from ui.styles import APP_CSS
from utils import aggregate_scores
from validators import validate_interview_input


st.set_page_config(page_title="AI Interview Pro", page_icon="✦", layout="wide", initial_sidebar_state="expanded")
st.markdown(APP_CSS, unsafe_allow_html=True)


def initialize_state() -> None:
    defaults = {
        "page": "Home",
        "configuration": None,
        "questions": [],
        "current_index": 0,
        "answers": {},
        "evaluations": {},
        "followup_questions": {},
        "followup_answers": {},
        "report": None,
        "theme": "dark",
        "virtual_f2f_mode": True,
        "enable_webcam": False,
        "enable_timer": True,
        "timer_duration": 3,
        "resume_text": "",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)

    # Demo showcase query param support for screenshot generation
    try:
        params = st.query_params
        if params.get("demo") == "1":
            req_view = params.get("view", "Home")
            if req_view == "Home":
                st.session_state.page = "Home"
            elif req_view == "Create":
                st.session_state.page = "Create Interview"
            elif req_view in ("Interview", "Evaluated"):
                st.session_state.page = "Interview"
                if not st.session_state.questions:
                    st.session_state.configuration = {
                        "role": "Python Developer",
                        "company": "Google",
                        "experience": "1-3 Years",
                        "skills": ["Python", "FastAPI", "SQL", "System Design"],
                        "domain": "Software Development",
                        "difficulty": "Medium",
                        "question_type": "Technical",
                        "question_count": 5
                    }
                    st.session_state.questions = [
                        {
                            "id": 1,
                            "question": "Explain the Global Interpreter Lock (GIL) in Python. How does it impact multithreading, and how can high-throughput backend services bypass GIL limitations in production?",
                            "type": "Technical",
                            "topic": "Python Core & Concurrency",
                            "difficulty": "Medium",
                            "expected_answer": "The GIL is a mutex protecting access to Python objects, preventing multiple native threads from executing bytecodes concurrently. To bypass: use multiprocessing, Celery task workers, or C/Rust extensions.",
                            "evaluation_criteria": ["Thread safety", "Concurrency limitations", "Workaround strategies"],
                            "rubric": {"concept": 3, "accuracy": 3, "example": 2, "depth": 2}
                        },
                        {
                            "id": 2,
                            "question": "Write an optimal solution in Python to find the longest substring without repeating characters in O(n) time.",
                            "type": "Coding",
                            "topic": "Algorithms (Sliding Window)",
                            "difficulty": "Medium",
                            "expected_answer": "Use a sliding window with a hash map storing the last seen index of each character. Time complexity: O(n), Space complexity: O(min(n, m)).",
                            "evaluation_criteria": ["Sliding window pattern", "Time/space complexity", "Clean edge-case handling"],
                            "rubric": {"concept": 3, "accuracy": 3, "example": 2, "depth": 2}
                        }
                    ]
                    st.session_state.answers = {
                        0: "The GIL prevents multiple threads from executing Python bytecodes concurrently. For CPU-bound tasks, multithreading does not achieve true multi-core speedup because threads contest for the GIL mutex. To scale CPU-bound services, we utilize the multiprocessing module, separate worker processes via Gunicorn/Uvicorn, or offload heavy compute to C/Rust extensions."
                    }
                if req_view == "Evaluated":
                    st.session_state.evaluations = {
                        0: {
                            "score": 8.5,
                            "max_score": 10,
                            "strengths": [
                                "Clear explanation of GIL mutex mechanism",
                                "Correctly distinguished CPU-bound vs I/O-bound workloads",
                                "Practical production solutions (multiprocessing, worker processes)"
                            ],
                            "weaknesses": [
                                "Could mention Python 3.13 free-threaded / nogil build"
                            ],
                            "missing_concepts": [
                                "Free-threading in Python 3.13",
                                "I/O bound thread release behavior"
                            ],
                            "feedback": "Strong and technically accurate response demonstrating real-world backend engineering competence.",
                            "improvement_suggestions": [
                                "Mention that I/O-bound operations release the GIL during syscalls",
                                "Reference PEP 703 free-threaded Python for cutting edge context"
                            ]
                        }
                    }
                    st.session_state.followup_questions[0] = "Since you mentioned multiprocessing, how would you handle shared state and inter-process communication (IPC) across those worker processes securely without race conditions?"
            elif req_view == "Results":
                st.session_state.page = "Results"
                st.session_state.configuration = {
                    "role": "Python Developer",
                    "company": "Google",
                    "experience": "1-3 Years",
                    "skills": ["Python", "FastAPI", "SQL", "System Design"],
                    "question_count": 5
                }
                st.session_state.questions = [
                    {"id": 1, "topic": "Python Core", "difficulty": "Medium", "question": "Explain Python GIL.", "expected_answer": "..."},
                    {"id": 2, "topic": "Algorithms", "difficulty": "Medium", "question": "Sliding window substring problem.", "expected_answer": "..."},
                    {"id": 3, "topic": "System Design", "difficulty": "Hard", "question": "Design idempotent payment APIs.", "expected_answer": "..."},
                    {"id": 4, "topic": "Databases (SQL)", "difficulty": "Medium", "question": "Database indexing and B-Trees.", "expected_answer": "..."},
                    {"id": 5, "topic": "REST APIs", "difficulty": "Easy", "question": "HTTP status codes and error models.", "expected_answer": "..."}
                ]
                st.session_state.answers = {
                    0: "GIL explanation...", 1: "Sliding window solution...", 2: "Idempotency keys with Redis...", 3: "B-Tree index structure...", 4: "HTTP status conventions..."
                }
                st.session_state.report = {
                    "overall_score": 84.0,
                    "average": 8.4,
                    "questions": 5,
                    "attempted": 5,
                    "timestamp": "2026-10-31 15:30 UTC",
                    "topic_scores": {
                        "Python Core": 8.5,
                        "Algorithms": 9.0,
                        "System Design": 8.0,
                        "Databases": 8.5,
                        "REST APIs": 8.0
                    },
                    "difficulty_scores": {
                        "Easy": 8.0,
                        "Medium": 8.7,
                        "Hard": 8.0
                    },
                    "evaluations": [
                        {"score": 8.5, "feedback": "Solid understanding of Python threading and concurrency.", "strengths": ["Deep knowledge of GIL"], "weaknesses": [], "missing_concepts": []},
                        {"score": 9.0, "feedback": "Optimal O(n) solution using sliding window pattern.", "strengths": ["Optimal time complexity"], "weaknesses": [], "missing_concepts": []},
                        {"score": 8.0, "feedback": "Good architectural design with distributed locks.", "strengths": ["Idempotency keys"], "weaknesses": [], "missing_concepts": []},
                        {"score": 8.5, "feedback": "Accurate explanation of indexing trade-offs.", "strengths": ["B-tree search time"], "weaknesses": [], "missing_concepts": []},
                        {"score": 8.0, "feedback": "Clear REST API status code conventions.", "strengths": ["Idempotent verbs"], "weaknesses": [], "missing_concepts": []}
                    ]
                }
            elif req_view == "History":
                st.session_state.page = "History"
    except Exception:
        pass



def reset_interview() -> None:
    for key, value in {
        "configuration": None,
        "questions": [],
        "current_index": 0,
        "answers": {},
        "evaluations": {},
        "followup_questions": {},
        "followup_answers": {},
        "report": None,
    }.items():
        st.session_state[key] = value


def sidebar() -> None:
    with st.sidebar:
        render_brand()
        st.markdown('<div class="eyebrow">Workspace</div>', unsafe_allow_html=True)
        pages = ["Home", "Create Interview", "Interview", "Results", "History"]
        page = st.radio("Navigate", pages, index=pages.index(st.session_state.page), label_visibility="collapsed")
        st.session_state.page = page

        st.markdown('<div class="eyebrow">Virtual Room Settings</div>', unsafe_allow_html=True)
        st.session_state.virtual_f2f_mode = st.toggle("🎥 Face-to-Face Voice Room", value=st.session_state.virtual_f2f_mode)
        st.session_state.enable_timer = st.toggle("Countdown Timer", value=st.session_state.enable_timer)
        
        st.markdown('<div class="eyebrow">Appearance</div>', unsafe_allow_html=True)
        theme = st.toggle("Light theme", value=st.session_state.theme == "light")
        st.session_state.theme = "light" if theme else "dark"
        if theme:
            st.markdown('<style>:root { --bg:#f8fafc; --surface:#ffffff; --card:#ffffff; --line:#e2e8f0; --line-strong:#cbd5e1; --text:#172033; --muted:#475569; --subtle:#64748b; } .stApp,[data-testid="stSidebar"] { background:var(--bg); }</style>', unsafe_allow_html=True)
        
        st.divider()
        if st.session_state.configuration:
            cfg = st.session_state.configuration
            st.caption(f"Target: {cfg.get('role')} · {cfg.get('company', 'Standard')}")
        
        answered = len(st.session_state.answers)
        total = len(st.session_state.questions)
        if total:
            st.caption(f"Session progress · {answered}/{total} answered")
            st.progress(answered / total)
            
        if st.button("Reset current interview", use_container_width=True):
            reset_interview()
            st.session_state.page = "Create Interview"
            st.rerun()
            
        st.markdown('<p class="footer-note">AI Interview Pro v2.0<br>Virtual Voice-to-Voice Room</p>', unsafe_allow_html=True)


def render_home() -> None:
    st.markdown(
        '<div class="hero"><div class="hero-grid"><div><div class="eyebrow">Virtual Face-to-Face AI Practice</div>'
        '<h1>Practice Real Voice-to-Voice Interviews.</h1>'
        '<p>Simulate authentic face-to-face video interviews: the AI interviewer asks questions by voice, and you speak your answers directly into your microphone while viewing your live webcam preview.</p></div>'
        '<div class="preview-card"><div class="eyebrow">Sample Live Prompt</div>'
        '<blockquote>How would you design a distributed idempotency layer for payment transaction APIs?</blockquote>'
        '<p><strong>Evaluation Criteria</strong><br>Scalability · Data consistency · Trade-offs · Edge cases</p></div></div></div>',
        unsafe_allow_html=True,
    )
    actions = st.columns([1, 1, 3])
    with actions[0]:
        if st.button("Start Interview", type="primary", use_container_width=True):
            st.session_state.page = "Create Interview"
            st.rerun()
    with actions[1]:
        if st.button("View History", use_container_width=True):
            st.session_state.page = "History"
            st.rerun()
    st.caption("Personalized questions · Voice audio · Resume parsing · PDF Performance Reports")
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_header("Engineered for High-Stakes Interview Prep", "Everything you need to turn preparation into confidence.")
    features = [
        ("01", "Voice-to-Voice Call", "AI speaks questions aloud and you speak your answers via microphone in real-time."),
        ("02", "Virtual Face-to-Face", "Two-way video call layout with AI Interviewer avatar and your live webcam mirror."),
        ("03", "Company Presets", "Practice questions tuned for Google, Amazon Leadership Principles, Microsoft, and Startups."),
        ("04", "Resume-Grounded Questions", "Upload your PDF CV so the AI asks targeted questions based on your actual projects."),
    ]
    columns = st.columns(4)
    for column, feature in zip(columns, features):
        with column:
            render_feature_card(*feature)
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_header("How it works", "A systematic loop to refine your technical responses.")
    steps = [
        ("01", "Configure", "Select role, company focus, skills, or upload your resume."),
        ("02", "Voice-to-Voice Call", "Listen to the AI question, then speak your answer aloud via microphone."),
        ("03", "Adaptive Review", "Get rubric feedback and answer adaptive follow-ups."),
        ("04", "Report & Export", "Review deep analytics and download professional PDF reports."),
    ]
    columns = st.columns(4)
    for column, step in zip(columns, steps):
        with column:
            render_step(*step)


def render_create() -> None:
    top_col1, _ = st.columns([1, 4])
    with top_col1:
        if st.button("⬅ Back to Home", key="create_back_home"):
            st.session_state.page = "Home"
            st.rerun()

    render_page_intro("Interview workspace", "Create your interview", "Customize a focused practice session around your target company and role.")
    controls, preview = st.columns([1.45, .75], gap="large")
    with controls:
        st.markdown('<div class="surface">', unsafe_allow_html=True)
        render_section_header("Role & Target Company", "Set the organizational context for your interviewer.")
        role_options = [
            "Software Developer", "Python Developer", "Java Developer", "C++ Developer",
            "Frontend Developer", "Backend Developer", "Full Stack Developer", "Data Scientist",
            "Data Analyst", "Machine Learning Engineer", "AI Engineer", "DevOps Engineer", "Custom"
        ]
        role_choice = st.selectbox("Target role", role_options)
        custom_role = st.text_input("Custom role", disabled=role_choice != "Custom", placeholder="e.g. Platform Engineer")
        experience = st.selectbox("Experience level", ["Fresher", "0-1 Years", "1-3 Years", "3-5 Years", "5+ Years"])
        
        company_options = list(COMPANY_PROFILES.keys())
        company_choice = st.selectbox("Company Focus Preset", company_options)
        st.caption(f"💡 {COMPANY_PROFILES[company_choice]['description']}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="surface">', unsafe_allow_html=True)
        render_section_header("Resume Context (Optional)", "Upload your CV to ask questions about your actual projects.")
        uploaded_resume = st.file_uploader("Upload Resume (.pdf or .txt)", type=["pdf", "txt"], help="AI extracts projects and skills from your resume.")
        resume_text = ""
        if uploaded_resume:
            resume_text = extract_resume_text(uploaded_resume)
            if resume_text and not resume_text.startswith("[Error"):
                st.success(f"✓ Resume parsed successfully ({len(resume_text)} characters analyzed)")
                st.session_state.resume_text = resume_text
            elif resume_text.startswith("[Error"):
                st.error(resume_text)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="surface">', unsafe_allow_html=True)
        render_section_header("Technical Skills & Focus", "Choose the core technologies to evaluate.")
        skills = st.multiselect("Skills", [
            "Python", "C++", "Java", "JavaScript", "React", "Node.js", "SQL", "MongoDB",
            "DSA", "OOP", "DBMS", "Operating Systems", "Computer Networks", "Machine Learning", "System Design"
        ])
        custom_skills = st.text_input("Additional skills", placeholder="e.g. REST APIs, Docker, Redis, Kubernetes")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="surface">', unsafe_allow_html=True)
        render_section_header("Interview Format & Challenge", "Tune the length and challenge depth.")
        setting_columns = st.columns(2)
        with setting_columns[0]:
            domain_value = st.selectbox("Domain", [
                "Software Development", "Data Science", "Artificial Intelligence",
                "Machine Learning", "Web Development", "Cloud Computing", "Cybersecurity", "General"
            ])
            difficulty_value = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Mixed"])
        with setting_columns[1]:
            question_type = st.selectbox("Question type", ["Technical", "Coding", "Conceptual", "Scenario-Based", "Behavioral", "HR", "Mixed"])
            count = st.select_slider("Questions", options=[5, 10, 15, 20], value=5, format_func=lambda value: f"{value} Questions")
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.button("Generate personalized interview", type="primary", use_container_width=True)
    with preview:
        final_role_preview = custom_role if role_choice == "Custom" and custom_role else role_choice
        selected_skills = skills + [item.strip() for item in custom_skills.split(",") if item.strip()]
        skill_label = ", ".join(selected_skills[:4]) if selected_skills else "Choose skills"
        if len(selected_skills) > 4:
            skill_label += f" + {len(selected_skills) - 4} more"
        has_resume = "Yes (Attached)" if resume_text else "None"
        st.markdown(
            f'<div class="surface"><div class="eyebrow">Live Interview Summary</div><h3>{escape(final_role_preview)}</h3>'
            f'<p>{escape(experience)} · {escape(domain_value)}</p><hr>'
            f'<p><strong>Company Preset</strong><br>{escape(company_choice)}</p>'
            f'<p><strong>Resume Context</strong><br>{has_resume}</p>'
            f'<p><strong>Focus Skills</strong><br>{escape(skill_label)}</p>'
            f'<p><strong>Format</strong><br>{escape(question_type)} · {escape(difficulty_value)}</p>'
            f'<p><strong>Length</strong><br>{count} questions</p></div>',
            unsafe_allow_html=True,
        )
        st.info("Virtual Face-to-Face Room, Live Audio, timer, and adaptive follow-up questions are enabled automatically.")
    if submitted:
        final_role = custom_role if role_choice == "Custom" else role_choice
        final_skills = skills + [item.strip() for item in custom_skills.split(",") if item.strip()]
        configuration = {
            "role": final_role,
            "experience": experience,
            "skills": final_skills,
            "domain": domain_value,
            "difficulty": difficulty_value,
            "question_type": question_type,
            "question_count": count,
            "company": company_choice,
            "resume_text": resume_text,
        }
        errors = validate_interview_input(configuration)
        if errors:
            for error in errors:
                st.error(error)
            return
        with st.spinner("Building your personalized interview questions with Gemini AI..."):
            try:
                questions = generate_questions(configuration, LLMClient())
            except (LLMError, QuestionGenerationError) as exc:
                st.error(str(exc))
                return
        st.session_state.configuration = configuration
        st.session_state.questions = questions
        st.session_state.current_index = 0
        st.session_state.answers = {}
        st.session_state.evaluations = {}
        st.session_state.followup_questions = {}
        st.session_state.followup_answers = {}
        st.session_state.report = None
        st.session_state.page = "Interview"
        st.rerun()


def render_evaluation(evaluation: dict[str, Any]) -> None:
    render_section_header("AI Rubric Evaluation", "A structured assessment of your response against technical criteria.")
    metric_columns = st.columns(3)
    with metric_columns[0]:
        render_metric_card("Score", f"{evaluation['score']} / 10", "Current answer")
    with metric_columns[1]:
        render_metric_card("Strengths", str(len(evaluation.get("strengths", []))), "Identified positive signals")
    with metric_columns[2]:
        render_metric_card("Focus areas", str(len(evaluation.get("missing_concepts", []))), "Concepts to sharpen")
    st.markdown("<br>", unsafe_allow_html=True)
    render_evaluation_lists(evaluation)
    st.info(f"**Evaluator Feedback:** {evaluation['feedback']}")
    with st.expander("Improvement suggestions"):
        for item in evaluation["improvement_suggestions"]:
            st.write(f"- {item}")


def render_interview() -> None:
    if not st.session_state.questions:
        render_page_intro("Interview workspace", "No interview in progress", "Create an interview first, then return here to practice one question at a time.")
        render_empty_state("01", "No questions generated", "Your active interview will appear here after you configure a session.")
        if st.button("Create Interview", type="primary"):
            st.session_state.page = "Create Interview"
            st.rerun()
        return

    index = st.session_state.current_index
    question = st.session_state.questions[index]
    total_q = len(st.session_state.questions)
    
    # Top navigation / Back to setup bar
    col_nav1, col_nav2 = st.columns([1, 4])
    with col_nav1:
        if st.button("⬅ Back to Setup", key="interview_back_setup"):
            st.session_state.page = "Create Interview"
            st.rerun()

    render_page_intro("Live Interview Session", f"Question {index + 1} of {total_q}", "Explain your reasoning clearly. Answers are evaluated against a structured rubric.")
    render_stepper(total_q, index, set(st.session_state.evaluations))
    st.progress((index + 1) / total_q, text=f"Interview Progress · {round(((index + 1) / total_q) * 100)}%")

    # Quick Jump Buttons: Click any question to navigate back or forth anytime
    st.caption("Quick Navigation (Click to jump to any question):")
    nav_cols = st.columns(min(total_q, 10))
    for i in range(total_q):
        col_slot = nav_cols[i % 10]
        label = f"Q{i+1}"
        if i in st.session_state.evaluations:
            label = f"✓ Q{i+1}"
        with col_slot:
            btn_type = "primary" if i == index else "secondary"
            if st.button(label, key=f"jump_btn_{i}", type=btn_type, use_container_width=True):
                # Save draft text before jumping
                current_text = st.session_state.get(f"answer_{index}", "")
                if current_text:
                    st.session_state.answers[index] = current_text
                st.session_state.current_index = i
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Question metadata & timer
    top_cols = st.columns([2, 1])
    with top_cols[0]:
        company_name = st.session_state.configuration.get("company", "General") if st.session_state.configuration else "General"
        st.markdown(
            f'<div class="question-meta">{render_badge(str(question["difficulty"]), True)}'
            f'{render_badge(str(question["type"]))}'
            f'{render_badge(str(question["topic"]))}'
            f'{render_badge(company_name, company=True)}</div>',
            unsafe_allow_html=True,
        )
    with top_cols[1]:
        if st.session_state.enable_timer:
            render_timer(st.session_state.timer_duration)

    render_question_card(question)

    # 🎥 VIRTUAL FACE-TO-FACE VOICE-TO-VOICE ROOM
    if st.session_state.virtual_f2f_mode:
        interviewer = f"Alex · {company_name} Tech Lead"
        render_face_to_face_room(question.get("question", ""), interviewer)
    else:
        render_audio_speaker(question.get("question", ""))

    render_rubric(question)

    is_coding = question.get("type", "").lower() == "coding"
    code_mode = False
    if is_coding:
        col_type, _ = st.columns([1, 2])
        with col_type:
            code_lang = st.selectbox("Language template", ["Python", "JavaScript", "Java", "C++", "SQL"], key=f"lang_{index}")
            code_mode = True

    default_answer = st.session_state.answers.get(index, "")
    if is_coding and not default_answer:
        if code_lang == "Python":
            default_answer = "# Write your solution here:\ndef solution(*args):\n    pass\n"
        elif code_lang == "JavaScript":
            default_answer = "// Write your solution here:\nfunction solution() {\n}\n"

    answer = st.text_area(
        "Code / Solution Area" if code_mode else "Candidate Answer (Type or speak above & paste)",
        value=default_answer,
        height=240 if is_coding else 180,
        key=f"answer_{index}",
        placeholder="Type your explanation or paste your spoken voice answer here..."
    )
    st.markdown('<p class="answer-helper">💡 Tip: You can speak your answer using the microphone above, click Copy, and paste it here.</p>', unsafe_allow_html=True)

    if index not in st.session_state.evaluations:
        col_back_q, col_submit_q, col_fwd_q = st.columns([1, 1.6, 1])
        with col_back_q:
            if index > 0:
                if st.button("⬅ Previous Question", key=f"prev_q_{index}", use_container_width=True):
                    if answer:
                        st.session_state.answers[index] = answer
                    st.session_state.current_index -= 1
                    st.rerun()
            else:
                st.caption("First Question")
        with col_submit_q:
            if st.button("Submit Answer", type="primary", use_container_width=True, key=f"sub_btn_{index}"):
                if not answer.strip():
                    st.warning("Please enter your answer before submitting.")
                else:
                    with st.spinner("AI Evaluator is assessing your answer against the rubric..."):
                        try:
                            evaluation = evaluate_answer(question, answer, LLMClient())
                        except (LLMError, EvaluationError) as exc:
                            st.error(str(exc))
                            return
                    st.session_state.answers[index] = answer
                    st.session_state.evaluations[index] = evaluation
                    st.rerun()
        with col_fwd_q:
            if index + 1 < total_q:
                if st.button("Skip / Next ➔", key=f"skip_q_{index}", use_container_width=True):
                    if answer:
                        st.session_state.answers[index] = answer
                    st.session_state.current_index += 1
                    st.rerun()
    else:
        render_evaluation(st.session_state.evaluations[index])
        
        # Adaptive Follow-Up Question Feature
        current_followup = st.session_state.followup_questions.get(index)
        if not current_followup:
            if st.button("🎯 Ask Adaptive Follow-Up Question", use_container_width=True):
                with st.spinner("Interviewer is crafting a targeted follow-up question..."):
                    followup_text = generate_followup(question, answer, st.session_state.evaluations[index], LLMClient())
                    st.session_state.followup_questions[index] = followup_text
                    st.rerun()
        else:
            render_followup_card(current_followup)
            followup_ans = st.text_area("Your response to follow-up", value=st.session_state.followup_answers.get(index, ""), key=f"followup_ans_{index}")
            if st.button("Save Follow-up Response"):
                st.session_state.followup_answers[index] = followup_ans
                st.success("Follow-up response recorded!")

        st.markdown("<br>", unsafe_allow_html=True)
        col_prev_ev, col_next_ev = st.columns([1, 1.4])
        with col_prev_ev:
            if index > 0:
                if st.button("⬅ Previous Question", key=f"prev_ev_btn_{index}", use_container_width=True):
                    st.session_state.current_index -= 1
                    st.rerun()
        with col_next_ev:
            next_label = "Proceed to Next Question ➔" if index + 1 < total_q else "Finalize & View Results ➔"
            if st.button(next_label, type="primary", use_container_width=True, key=f"next_ev_btn_{index}"):
                if index + 1 < total_q:
                    st.session_state.current_index += 1
                    st.rerun()
                else:
                    finalize_interview()


def finalize_interview() -> None:
    questions = st.session_state.questions
    evaluations = [st.session_state.evaluations.get(i, {"score": 0, "feedback": "Unanswered", "strengths": [], "weaknesses": [], "missing_concepts": []}) for i in range(len(questions))]
    report = aggregate_scores(questions, evaluations)
    report["questions"] = len(questions)
    report["attempted"] = len(st.session_state.answers)
    report["evaluations"] = evaluations
    st.session_state.report = report
    configuration = st.session_state.configuration
    save_interview({
        **configuration,
        "overall_score": report["overall_score"],
        "average": report["average"],
        "topic_scores": report["topic_scores"],
        "strengths": [],
        "weaknesses": [],
        "question_count": len(questions)
    })
    st.session_state.page = "Results"
    st.rerun()


def report_exports(report: dict[str, Any]) -> tuple[str, str]:
    configuration = st.session_state.configuration or {}
    lines = [
        "# AI Interview Report",
        "",
        f"- Role: {configuration.get('role', 'Interview')}",
        f"- Target Company: {configuration.get('company', 'Standard')}",
        f"- Date: {report.get('timestamp', 'Current session')}",
        f"- Overall score: {report.get('overall_score', 0)}%",
        f"- Average answer score: {report.get('average', 0)} / 10",
        "",
        "## Question feedback",
    ]
    rows = []
    for index, (question, evaluation) in enumerate(zip(st.session_state.questions, report.get("evaluations", [])), start=1):
        lines.extend([
            f"### {index}. {question.get('question', '')}",
            f"Score: {evaluation.get('score', 0)} / 10",
            f"Answer: {st.session_state.answers.get(index - 1, 'Not answered')}",
            f"Feedback: {evaluation.get('feedback', '')}",
            "",
        ])
        rows.append([index, question.get("topic", ""), question.get("difficulty", ""), evaluation.get("score", 0), st.session_state.answers.get(index - 1, "Not answered")])
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["Question", "Topic", "Difficulty", "Score", "Answer"])
    writer.writerows(rows)
    return "\n".join(lines), csv_buffer.getvalue()


def render_results() -> None:
    report = st.session_state.report
    if not report:
        render_page_intro("Results", "No results available", "Complete an interview to see your score and detailed feedback.")
        render_empty_state("02", "Your results are waiting", "Submit your answers to unlock performance insights for this session.")
        if st.button("Create Interview", type="primary"):
            st.session_state.page = "Create Interview"
            st.rerun()
        return

    # Back buttons on results page
    col_nav_r1, col_nav_r2, _ = st.columns([1.2, 1.2, 2.5])
    with col_nav_r1:
        if st.button("⬅ Back to Questions Review", use_container_width=True, key="res_back_review"):
            st.session_state.page = "Interview"
            st.session_state.current_index = 0
            st.rerun()
    with col_nav_r2:
        if st.button("🏠 Back to Home", use_container_width=True, key="res_back_home"):
            st.session_state.page = "Home"
            st.rerun()

    render_page_intro("Interview Results & Evaluation", "Performance Debrief", "Review your score, competencies, and question-by-question breakdown.")
    metrics = st.columns(4)
    metric_data = [
        ("Overall Score", f"{report['overall_score']}%", "Across evaluated answers"),
        ("Average Score", f"{report['average']} / 10", "Mean answer score"),
        ("Questions", str(report["questions"]), "In this interview"),
        ("Answered", str(report["attempted"]), "Submitted answers")
    ]
    for column, data in zip(metrics, metric_data):
        with column:
            render_metric_card(*data)

    markdown_report, csv_report = report_exports(report)
    
    # Generate PDF report
    pdf_bytes = generate_interview_pdf(
        report,
        st.session_state.configuration or {},
        st.session_state.questions,
        st.session_state.answers
    )

    st.markdown('<div class="export-row" style="display:flex;gap:12px;margin:1.2rem 0;">', unsafe_allow_html=True)
    export_columns = st.columns(3)
    with export_columns[0]:
        st.download_button(
            "📄 Download PDF Report",
            pdf_bytes,
            file_name="ai-interview-report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    with export_columns[1]:
        st.download_button(
            "📝 Download Markdown",
            markdown_report,
            file_name="ai-interview-report.md",
            mime="text/markdown",
            use_container_width=True
        )
    with export_columns[2]:
        st.download_button(
            "📊 Download CSV Data",
            csv_report,
            file_name="ai-interview-report.csv",
            mime="text/csv",
            use_container_width=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    score_column, insight_column = st.columns([.35, .65], gap="large")
    with score_column:
        render_score_gauge(float(report.get("overall_score", 0)))
    with insight_column:
        render_section_header("Performance Snapshot", "Scores are color-coded to highlight your strongest competencies and focus areas.")
        st.caption("🟢 Green: 7-10 (Strong) · 🟡 Amber: 4-6 (Fair) · 🔴 Red: below 4 (Needs Work)")
        
    tab_topics, tab_difficulty, tab_questions = st.tabs(["Topic Competencies", "Difficulty Breakdown", "Detailed Question Review"])
    with tab_topics:
        render_section_header("Topic Performance", "Average score across technical domains.")
        render_score_chart(report["topic_scores"], "Topic Scores")
    with tab_difficulty:
        render_section_header("Difficulty Performance", "Score consistency across challenge levels.")
        render_score_chart(report["difficulty_scores"], "Difficulty Scores")
    with tab_questions:
        for index, (question, evaluation) in enumerate(zip(st.session_state.questions, report["evaluations"]), start=1):
            with st.expander(f"Question {index} · {question['topic']} · {evaluation['score']} / 10"):
                st.markdown(f"**Question Prompt**  \n{question['question']}")
                st.markdown(f"**Your Answer**  \n{st.session_state.answers.get(index - 1, 'Not answered')}")
                if index - 1 in st.session_state.followup_questions:
                    st.markdown(f"**Follow-Up Question**  \n{st.session_state.followup_questions[index - 1]}")
                    st.markdown(f"**Follow-Up Answer**  \n{st.session_state.followup_answers.get(index - 1, 'No answer provided')}")
                st.markdown(f"**Expected Benchmark Answer**  \n{question['expected_answer']}")
                render_evaluation_lists(evaluation)
                st.info(f"**Evaluator Feedback:** {evaluation['feedback']}")
                
    st.markdown(
        f'<div class="surface" style="margin-top:1.5rem;"><div class="eyebrow">Session Summary</div><h3>Ready for the next round?</h3>'
        f'<p>You completed {report["attempted"]} of {report["questions"]} questions with an average score of {report["average"]} out of 10.</p></div>',
        unsafe_allow_html=True,
    )


def render_history() -> None:
    top_col, _ = st.columns([1, 4])
    with top_col:
        if st.button("⬅ Back to Home", key="history_back_home"):
            st.session_state.page = "Home"
            st.rerun()

    render_page_intro("Progress Archive", "Interview History", "Review past practice sessions, score trajectories, and track technical growth.")
    try:
        history = load_history()
    except RuntimeError as exc:
        st.error(str(exc))
        return
    if not history:
        render_empty_state("03", "No interviews yet", "Create your first AI-powered interview to start tracking your performance over time.")
        if st.button("Create Interview", type="primary"):
            st.session_state.page = "Create Interview"
            st.rerun()
        return

    for index, item in enumerate(history):
        timestamp = str(item.get("timestamp", ""))
        date_label = timestamp[:10] if timestamp else "Unknown date"
        skills = " · ".join(str(skill) for skill in item.get("skills", [])) or "Skills not recorded"
        role = str(item.get("role", "Interview"))
        company = str(item.get("company", "Standard Prep"))
        score = float(item.get("overall_score", 0) or 0)
        score_label = "Strong" if score >= 70 else "Developing" if score >= 40 else "Keep practicing"
        st.markdown(
            f'<div class="history-card" style="padding:1.25rem;margin-bottom:0.8rem;"><div class="history-top">'
            f'<div><div class="eyebrow">{escape(date_label)} · {escape(company)}</div>'
            f'<h3 style="margin:0.25rem 0 0.35rem;">{escape(role)}</h3>'
            f'<p>{escape(str(item.get("question_type", "Interview")))} · {escape(str(item.get("difficulty", "Mixed")))} · {int(item.get("question_count", 0) or 0)} questions</p>'
            f'<p style="color:var(--subtle);font-size:0.82rem;">{escape(skills)}</p></div>'
            f'<div>{render_badge(f"{score:.0f}% · {score_label}", score >= 70)}</div></div></div>',
            unsafe_allow_html=True,
        )
        with st.expander(f"View session details · {index + 1}"):
            detail_columns = st.columns(3)
            with detail_columns[0]:
                render_metric_card("Overall score", f"{score:.0f}%")
            with detail_columns[1]:
                render_metric_card("Average", f"{float(item.get('average', 0) or 0):.1f} / 10")
            with detail_columns[2]:
                render_metric_card("Questions", str(item.get("question_count", 0)))
            topic_scores = item.get("topic_scores", {})
            if isinstance(topic_scores, dict):
                render_score_chart(topic_scores, "Topic snapshot")


initialize_state()
sidebar()
render_top_header()
{"Home": render_home, "Create Interview": render_create, "Interview": render_interview, "Results": render_results, "History": render_history}[st.session_state.page]()
