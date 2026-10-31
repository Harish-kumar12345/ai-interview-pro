from html import escape
import base64
import json
from pathlib import Path
from typing import Any

import streamlit as st
import streamlit.components.v1 as components


def get_logo_data_uri() -> str:
    """Read local logo and return embedded base64 data URI for zero-lag rendering."""
    logo_file = Path(__file__).parent.parent / "assets" / "logo.png"
    if logo_file.exists():
        try:
            raw = logo_file.read_bytes()
            b64 = base64.b64encode(raw).decode()
            return f"data:image/png;base64,{b64}"
        except Exception:
            return ""
    return ""


def render_top_header() -> None:
    """Render a persistent branded header with logo at the top-left of the main view."""
    logo_uri = get_logo_data_uri()
    if logo_uri:
        logo_html = f'<img src="{logo_uri}" width="40" height="40" style="border-radius:10px;box-shadow:0 4px 16px rgba(99,102,241,0.45);object-fit:cover;display:block;">'
    else:
        logo_html = '<div class="brand-icon" style="width:40px;height:40px;font-size:1.25rem;">✦</div>'

    st.markdown(
        f'''
        <div style="display:flex;align-items:center;justify-content:space-between;padding-bottom:1rem;margin-bottom:1.5rem;border-bottom:1px solid #1f2733;">
          <div style="display:flex;align-items:center;gap:14px;">
            {logo_html}
            <div>
              <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:1.22rem;color:var(--text);line-height:1.2;letter-spacing:-0.01em;">
                AI Interview Pro
              </div>
              <span style="font-size:0.68rem;color:#818cf8;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;">
                Enterprise Mock Room
              </span>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:8px;">
            <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#22c55e;box-shadow:0 0 8px #22c55e;"></span>
            <span style="font-size:0.75rem;color:#94a3b8;font-weight:600;">System Online</span>
          </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )


def render_brand() -> None:
    logo_uri = get_logo_data_uri()
    if logo_uri:
        logo_html = f'<img src="{logo_uri}" width="42" height="42" style="border-radius:10px;box-shadow:0 4px 16px rgba(99,102,241,0.45);object-fit:cover;display:block;">'
    else:
        logo_html = '<div class="brand-icon">✦</div>'

    st.markdown(
        f'''
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:0.4rem;">
          {logo_html}
          <div>
            <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:1.15rem;color:var(--text);line-height:1.2;">
              AI Interview Pro
            </div>
            <span style="font-size:0.68rem;color:#818cf8;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;">
              Enterprise Edition
            </span>
          </div>
        </div>
        <p class="brand-subtitle" style="margin-top:0.4rem;font-size:0.78rem;color:var(--muted);">
          Enterprise-grade AI mock interview practice.
        </p>
        ''',
        unsafe_allow_html=True,
    )



def render_page_intro(eyebrow: str, title: str, description: str) -> None:
    st.markdown(
        f'<div class="page-intro"><div class="eyebrow">{escape(eyebrow)}</div>'
        f'<h1>{escape(title)}</h1><p>{escape(description)}</p></div>',
        unsafe_allow_html=True,
    )


def render_section_header(title: str, description: str = "") -> None:
    text = f'<h2>{escape(title)}</h2>'
    if description:
        text += f'<p>{escape(description)}</p>'
    st.markdown(text, unsafe_allow_html=True)


def render_feature_card(number: str, title: str, description: str) -> None:
    st.markdown(
        f'<div class="feature-card" style="padding:1.25rem;"><div class="feature-icon" style="color:var(--accent);font-weight:700;">{escape(number)}</div>'
        f'<h3 style="margin:0.5rem 0 0.3rem;">{escape(title)}</h3><p style="font-size:0.9rem;margin:0;">{escape(description)}</p></div>',
        unsafe_allow_html=True,
    )


def render_step(number: str, title: str, description: str) -> None:
    st.markdown(
        f'<div class="step-card"><div class="step-number">{escape(number)}</div>'
        f'<h3>{escape(title)}</h3><p>{escape(description)}</p></div>',
        unsafe_allow_html=True,
    )


def render_badge(text: str, accent: bool = False, company: bool = False) -> str:
    if company:
        class_name = "badge badge-company"
    elif accent:
        class_name = "badge badge-accent"
    else:
        class_name = "badge"
    return f'<span class="{class_name}">{escape(text)}</span>'


def render_metric_card(label: str, value: str, detail: str = "") -> None:
    detail_markup = f'<div class="metric-detail">{escape(detail)}</div>' if detail else ""
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{escape(label)}</div>'
        f'<div class="metric-value">{escape(value)}</div>{detail_markup}</div>',
        unsafe_allow_html=True,
    )


def render_empty_state(icon: str, title: str, description: str) -> None:
    st.markdown(
        f'<div class="empty-state"><div class="empty-icon">{escape(icon)}</div>'
        f'<h3>{escape(title)}</h3><p>{escape(description)}</p></div>',
        unsafe_allow_html=True,
    )


def render_question_card(question: dict[str, Any]) -> None:
    st.markdown(
        f'<div class="question-box"><div class="eyebrow">Question Prompt</div>'
        f'<h3>{escape(str(question.get("question", "")))}</h3></div>',
        unsafe_allow_html=True,
    )


def render_stepper(total: int, current: int, answered: set[int]) -> None:
    parts = ['<div class="stepper" aria-label="Interview progress">']
    for index in range(total):
        state = "current" if index == current else "answered" if index in answered else ""
        marker = "✓" if index in answered else str(index + 1)
        parts.append(f'<div class="step-dot {state}">{marker}</div>')
        if index < total - 1:
            parts.append('<div class="step-line"></div>')
    parts.append('</div>')
    st.markdown("".join(parts), unsafe_allow_html=True)


def render_rubric(question: dict[str, Any]) -> None:
    rubric = question.get("rubric", {})
    if not isinstance(rubric, dict):
        rubric = {}
    criteria = [
        ("Concept", rubric.get("concept", rubric.get("conceptual", 7))),
        ("Accuracy", rubric.get("accuracy", 7)),
        ("Example", rubric.get("example", rubric.get("examples", 7))),
        ("Depth", rubric.get("depth", rubric.get("detail", 7))),
    ]
    with st.expander("Scoring Rubric Dimensions", expanded=False):
        st.caption("Your answer is assessed against these target dimensions.")
        for label, value in criteria:
            try:
                score = max(0, min(10, float(value)))
            except (TypeError, ValueError):
                score = 7
            st.markdown(
                f'<div class="rubric-row"><div class="rubric-label" style="display:flex;justify-content:space-between;color:var(--muted);font-size:0.8rem;margin-bottom:0.25rem;">'
                f'<span>{escape(label)}</span><span>{score:g} / 10</span></div>'
                f'<div class="rubric-track" style="height:6px;background:var(--line);border-radius:99px;overflow:hidden;">'
                f'<div class="rubric-fill" style="height:100%;width:{score * 10:.0f}%;background:linear-gradient(90deg,var(--accent-strong),var(--accent));border-radius:inherit;"></div></div></div>',
                unsafe_allow_html=True,
            )


def render_score_gauge(score: float, label: str = "Overall score") -> None:
    score = max(0, min(100, float(score)))
    color = "var(--success)" if score >= 70 else "var(--warning)" if score >= 40 else "var(--danger)"
    st.markdown(
        f'<div class="score-gauge" style="--score:{score};--gauge-color:{color};width:154px;height:154px;border-radius:50%;display:grid;place-items:center;background:conic-gradient({color} calc({score} * 1%),var(--line) 0);position:relative;margin:0 auto;">'
        f'<div style="position:absolute;inset:12px;border-radius:50%;background:var(--card);"></div>'
        f'<div class="score-gauge-content" style="position:relative;z-index:1;text-align:center;"><span class="score-gauge-value" style="font-size:2rem;font-weight:700;">{score:.0f}%</span>'
        f'<span class="score-gauge-label" style="display:block;font-size:0.75rem;color:var(--muted);">{escape(label)}</span></div></div>',
        unsafe_allow_html=True,
    )


def render_score_chart(values: dict[str, Any], title: str) -> None:
    st.markdown(f'<h3>{escape(title)}</h3>', unsafe_allow_html=True)
    if not values:
        st.caption("No scored data yet.")
        return
    for label, value in values.items():
        try:
            score = max(0, min(10, float(value)))
        except (TypeError, ValueError):
            score = 0
        color = "var(--success)" if score >= 7 else "var(--warning)" if score >= 4 else "var(--danger)"
        st.markdown(
            f'<div class="chart-row" style="display:grid;grid-template-columns:minmax(110px,.7fr) 1.3fr 45px;gap:.8rem;align-items:center;margin:.65rem 0;">'
            f'<div class="chart-label" style="font-size:0.84rem;color:var(--muted);">{escape(str(label))}</div>'
            f'<div class="chart-track" style="height:7px;background:var(--line);border-radius:99px;overflow:hidden;"><div class="chart-fill" style="height:100%;width:{score * 10:.0f}%;background:{color};border-radius:inherit;"></div></div>'
            f'<div class="chart-value" style="font-size:0.84rem;font-weight:700;text-align:right;">{score:.1f}</div></div>',
            unsafe_allow_html=True,
        )


def render_evaluation_lists(evaluation: dict[str, Any]) -> None:
    columns = st.columns(3)
    for column, label, key in zip(
        columns,
        ["Strengths", "Weaknesses", "Missing concepts"],
        ["strengths", "weaknesses", "missing_concepts"],
    ):
        with column:
            st.markdown(f"**{label}**")
            items = evaluation.get(key, [])
            if items:
                for item in items:
                    st.write(f"- {item}")
            else:
                st.caption("None identified")


def render_audio_speaker(question_text: str) -> None:
    safe_text = json.dumps(question_text)
    html_code = f"""
    <div style="display:flex; align-items:center; gap:8px; margin: 0.6rem 0 1rem;">
      <button id="ttsBtn" onclick="speakText()" style="
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(129, 140, 248, 0.4);
        color: #818cf8;
        padding: 6px 14px;
        border-radius: 8px;
        font-family: sans-serif;
        font-size: 0.82rem;
        font-weight: 600;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        transition: all 0.2s;
      ">
        <span>🔊</span> AI Interviewer Voice
      </button>
      <button onclick="stopVoice()" style="
        background: transparent;
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #94a3b8;
        padding: 6px 10px;
        border-radius: 8px;
        font-family: sans-serif;
        font-size: 0.82rem;
        cursor: pointer;
      ">⏹ Stop</button>
      <span id="ttsStatus" style="font-family:sans-serif;font-size:0.75rem;color:#64748b;"></span>
    </div>
    <script>
      const speechText = {safe_text};
      function speakText() {{
        if ('speechSynthesis' in window) {{
          window.speechSynthesis.cancel();
          const utterance = new SpeechSynthesisUtterance(speechText);
          utterance.rate = 1.0;
          utterance.pitch = 1.0;
          utterance.onstart = () => {{ document.getElementById('ttsStatus').innerText = 'Reading aloud...'; }};
          utterance.onend = () => {{ document.getElementById('ttsStatus').innerText = ''; }};
          window.speechSynthesis.speak(utterance);
        }} else {{
          alert('Speech synthesis not supported in this browser.');
        }}
      }}
      function stopVoice() {{
        if ('speechSynthesis' in window) {{
          window.speechSynthesis.cancel();
          document.getElementById('ttsStatus').innerText = '';
        }}
      }}
    </script>
    """
    components.html(html_code, height=52)


def render_timer(duration_minutes: int = 3) -> None:
    html_code = f"""
    <div style="background: rgba(21, 27, 35, 0.8); border: 1px solid #252d38; border-radius: 10px; padding: 10px 14px; display: inline-flex; align-items: center; gap: 14px; font-family: sans-serif; margin-bottom: 0.8rem;">
      <span style="color: #94a3b8; font-size: 0.82rem; font-weight: 600;">⏱️ Response Timer:</span>
      <span id="timerDisplay" style="font-family: monospace; font-size: 1.15rem; font-weight: 700; color: #22c55e;">03:00</span>
      <button onclick="resetTimer()" style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15); color: #cbd5e1; border-radius: 6px; padding: 3px 8px; font-size: 0.72rem; cursor: pointer;">Reset</button>
    </div>
    <script>
      let totalSeconds = {duration_minutes} * 60;
      let interval = null;
      function start() {{
        clearInterval(interval);
        interval = setInterval(() => {{
          if (totalSeconds <= 0) {{
            clearInterval(interval);
            const el = document.getElementById('timerDisplay');
            if (el) {{
              el.innerText = '00:00 (Time Up)';
              el.style.color = '#ef4444';
            }}
            return;
          }}
          totalSeconds--;
          const mins = Math.floor(totalSeconds / 60);
          const secs = totalSeconds % 60;
          const el = document.getElementById('timerDisplay');
          if (el) {{
            el.innerText = (mins < 10 ? '0' : '') + mins + ':' + (secs < 10 ? '0' : '') + secs;
            if (totalSeconds < 45) {{
              el.style.color = '#ef4444';
            }} else if (totalSeconds < 90) {{
              el.style.color = '#f59e0b';
            }} else {{
              el.style.color = '#22c55e';
            }}
          }}
        }}, 1000);
      }}
      function resetTimer() {{
        totalSeconds = {duration_minutes} * 60;
        start();
      }}
      start();
    </script>
    """
    components.html(html_code, height=60)


def render_webcam_tile() -> None:
    html_code = """
    <div style="border: 1px solid #252d38; border-radius: 12px; overflow: hidden; background: #000; position: relative; margin-bottom: 1rem;">
      <video id="liveVideo" autoplay playsinline muted style="width: 100%; height: 180px; object-fit: cover; transform: scaleX(-1); display: block;"></video>
      <div id="camStatus" style="position: absolute; bottom: 8px; left: 10px; font-family: sans-serif; font-size: 0.72rem; color: #cbd5e1; background: rgba(0,0,0,0.6); padding: 2px 8px; border-radius: 4px;">
        🔴 Live Interview Camera Feed
      </div>
    </div>
    <script>
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
          .then(stream => {
            const video = document.getElementById('liveVideo');
            if (video) video.srcObject = stream;
          })
          .catch(err => {
            const status = document.getElementById('camStatus');
            if (status) status.innerText = '📷 Camera Preview Off / Not Permitted';
          });
      }
    </script>
    """
    components.html(html_code, height=200)


def render_followup_card(question_text: str) -> None:
    st.markdown(
        f'<div class="followup-box"><div class="eyebrow" style="color:#f59e0b;">Adaptive Follow-Up Question</div>'
        f'<h4 style="margin:0.4rem 0 0;color:var(--text);font-size:1.05rem;">{escape(question_text)}</h4></div>',
        unsafe_allow_html=True,
    )


def render_face_to_face_room(question_text: str, interviewer_name: str = "Elena (Lead AI Interviewer)") -> None:
    safe_q = json.dumps(question_text)
    html_code = f"""
    <div style="background: #0d1218; border: 1px solid #252d38; border-radius: 14px; padding: 16px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #f8fafc; margin-bottom: 1.2rem;">
      <!-- Call Header -->
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e2633; padding-bottom: 10px; margin-bottom: 12px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #22c55e; box-shadow: 0 0 10px #22c55e;"></span>
          <span style="font-weight: 700; font-size: 0.92rem; letter-spacing: -0.01em;">Live Virtual Face-to-Face Room</span>
        </div>
        <span style="font-size: 0.74rem; color: #a5b4fc; background: rgba(99,102,241,0.15); padding: 3px 10px; border-radius: 99px; border: 1px solid rgba(129,140,248,0.3);">Voice-to-Voice Active</span>
      </div>

      <!-- Split Video Grid -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 12px;">
        <!-- Left: AI Interviewer Tile -->
        <div style="background: radial-gradient(circle at 50% 30%, rgba(99,102,241,0.2), #0b0f14); border: 1px solid #2d3748; border-radius: 12px; height: 215px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; overflow: hidden;">
          <div id="aiAvatarRing" style="width: 78px; height: 78px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #818cf8); display: grid; place-items: center; font-size: 2rem; color: white; box-shadow: 0 4px 20px rgba(99,102,241,0.35); transition: all 0.3s;">
            ✦
          </div>
          <!-- Voice Sound Wave -->
          <div id="voiceWave" style="display: flex; gap: 4px; align-items: center; height: 16px; margin-top: 10px;">
            <div style="width: 3px; height: 6px; background: #818cf8; border-radius: 2px;"></div>
            <div style="width: 3px; height: 12px; background: #818cf8; border-radius: 2px;"></div>
            <div style="width: 3px; height: 18px; background: #818cf8; border-radius: 2px;"></div>
            <div style="width: 3px; height: 10px; background: #818cf8; border-radius: 2px;"></div>
            <div style="width: 3px; height: 5px; background: #818cf8; border-radius: 2px;"></div>
          </div>
          <div style="margin-top: 6px; font-weight: 600; font-size: 0.88rem;">{escape(interviewer_name)}</div>
          <span id="aiStatus" style="font-size: 0.72rem; color: #94a3b8;">Ready to interview</span>
          <div style="position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.65); font-size: 0.68rem; padding: 2px 8px; border-radius: 4px; color: #a5b4fc;">AI Interviewer</div>
        </div>

        <!-- Right: Candidate Webcam Tile -->
        <div style="background: #000; border: 1px solid #2d3748; border-radius: 12px; height: 215px; position: relative; overflow: hidden;">
          <video id="f2fCam" autoplay playsinline muted style="width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1);"></video>
          <div style="position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.65); font-size: 0.68rem; padding: 2px 8px; border-radius: 4px; color: #f8fafc;">You (Candidate)</div>
          <div style="position: absolute; bottom: 10px; right: 10px; background: rgba(0,0,0,0.65); font-size: 0.72rem; padding: 2px 8px; border-radius: 4px; color: #94a3b8; display: flex; align-items: center; gap: 4px;">
            <span>🎙️</span> <span id="micLabel">Mic Ready</span>
          </div>
        </div>
      </div>

      <!-- Action Bar & Real-time Voice to Text Subtitles -->
      <div style="background: #141b24; border: 1px solid #232c3a; border-radius: 10px; padding: 12px; display: flex; flex-direction: column; gap: 10px;">
        <div style="display: flex; gap: 10px; flex-wrap: wrap; align-items: center;">
          <button id="aiAskBtn" onclick="speakQuestion()" style="background: linear-gradient(135deg, #6366f1, #4f46e5); color: white; border: none; padding: 8px 18px; border-radius: 8px; font-size: 0.84rem; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 4px 12px rgba(99,102,241,0.3);">
            <span>🔊</span> AI Ask Question
          </button>
          <button onclick="stopVoice()" style="background: rgba(255,255,255,0.06); color: #cbd5e1; border: 1px solid rgba(255,255,255,0.15); padding: 8px 12px; border-radius: 8px; font-size: 0.82rem; cursor: pointer;">
            ⏹ Stop Voice
          </button>
          <button id="micBtn" onclick="toggleRecognition()" style="background: #22c55e; color: white; border: none; padding: 8px 20px; border-radius: 8px; font-size: 0.84rem; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 4px 12px rgba(34,197,94,0.3);">
            <span>🎙️</span> <span id="micBtnText">Speak Your Answer</span>
          </button>
          <button id="copyTranscriptBtn" onclick="copyAnswerText()" style="background: rgba(255,255,255,0.08); color: #cbd5e1; border: 1px solid rgba(255,255,255,0.2); padding: 8px 14px; border-radius: 8px; font-size: 0.82rem; cursor: pointer; display: none;">
            📋 Copy to Answer Box
          </button>
        </div>

        <!-- Subtitles / Live Speech Transcription -->
        <div style="border-top: 1px solid #232c3a; padding-top: 8px;">
          <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #94a3b8; margin-bottom: 4px;">
            <span>Real-time Voice Transcription:</span>
            <span id="sttStatus" style="color: #64748b;">Click 'Speak Your Answer' and answer verbally</span>
          </div>
          <div id="spokenTranscript" style="min-height: 48px; max-height: 90px; overflow-y: auto; background: #0b0f14; border: 1px solid #1e2633; border-radius: 6px; padding: 8px 10px; font-size: 0.84rem; color: #e2e8f0; line-height: 1.45;">
            (Your spoken words will appear here in real-time as you speak...)
          </div>
        </div>
      </div>
    </div>

    <script>
      const questionText = {safe_q};

      // 1. Initialize Webcam
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {{
        navigator.mediaDevices.getUserMedia({{ video: true, audio: false }})
          .then(stream => {{
            const vid = document.getElementById('f2fCam');
            if (vid) vid.srcObject = stream;
          }})
          .catch(err => {{
            console.log('Camera off or denied', err);
          }});
      }}

      // 2. AI Voice (Text-To-Speech)
      let waveInterval = null;
      function speakQuestion() {{
        if ('speechSynthesis' in window) {{
          window.speechSynthesis.cancel();
          const utt = new SpeechSynthesisUtterance(questionText);
          utt.rate = 0.95;
          utt.pitch = 1.0;
          
          utt.onstart = () => {{
            document.getElementById('aiStatus').innerText = 'Speaking question...';
            document.getElementById('aiAvatarRing').style.boxShadow = '0 0 28px rgba(99,102,241,0.9)';
            startWaveAnimation();
          }};
          utt.onend = () => {{
            document.getElementById('aiStatus').innerText = 'Listening to candidate...';
            document.getElementById('aiAvatarRing').style.boxShadow = '0 4px 20px rgba(99,102,241,0.35)';
            stopWaveAnimation();
          }};
          window.speechSynthesis.speak(utt);
        }} else {{
          alert('Speech synthesis is not supported on this browser.');
        }}
      }}

      function stopVoice() {{
        if ('speechSynthesis' in window) {{
          window.speechSynthesis.cancel();
          document.getElementById('aiStatus').innerText = 'Ready to interview';
          stopWaveAnimation();
        }}
      }}

      function startWaveAnimation() {{
        clearInterval(waveInterval);
        const bars = document.querySelectorAll('#voiceWave div');
        waveInterval = setInterval(() => {{
          bars.forEach(b => {{
            const h = Math.floor(Math.random() * 16) + 4;
            b.style.height = h + 'px';
          }});
        }}, 120);
      }}

      function stopWaveAnimation() {{
        clearInterval(waveInterval);
        const bars = document.querySelectorAll('#voiceWave div');
        bars.forEach((b, idx) => {{
          b.style.height = (idx % 2 === 0 ? '6px' : '12px');
        }});
      }}

      // 3. Candidate Voice (Speech-To-Text)
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      let recognition = null;
      let isListening = false;
      let recordedWords = '';

      if (SpeechRecognition) {{
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onstart = () => {{
          isListening = true;
          document.getElementById('micBtnText').innerText = 'Listening... (Click to Stop)';
          document.getElementById('micBtn').style.background = '#ef4444';
          document.getElementById('micLabel').innerText = 'Listening...';
          document.getElementById('micLabel').style.color = '#ef4444';
          document.getElementById('sttStatus').innerText = '🔴 Listening to your voice... Speak your response clearly.';
          document.getElementById('sttStatus').style.color = '#ef4444';
        }};

        recognition.onresult = (e) => {{
          let interim = '';
          let final = '';
          for (let i = 0; i < e.results.length; ++i) {{
            if (e.results[i].isFinal) {{
              final += e.results[i][0].transcript + ' ';
            }} else {{
              interim += e.results[i][0].transcript;
            }}
          }}
          recordedWords = (final + interim).trim();
          document.getElementById('spokenTranscript').innerText = recordedWords;
          document.getElementById('copyTranscriptBtn').style.display = 'inline-block';
        }};

        recognition.onerror = (e) => {{
          console.log('STT Error', e);
          document.getElementById('sttStatus').innerText = 'Mic message: ' + (e.error || 'Check mic permission');
          stopListening();
        }};

        recognition.onend = () => {{
          stopListening();
        }};
      }}

      function toggleRecognition() {{
        if (!SpeechRecognition) {{
          alert('Speech recognition is supported in Google Chrome and Microsoft Edge. Please open this page in Chrome or Edge to speak your answer.');
          return;
        }}
        if (isListening) {{
          recognition.stop();
          stopListening();
        }} else {{
          if ('speechSynthesis' in window) window.speechSynthesis.cancel();
          recognition.start();
        }}
      }}

      function stopListening() {{
        isListening = false;
        document.getElementById('micBtnText').innerText = 'Speak Your Answer';
        document.getElementById('micBtn').style.background = '#22c55e';
        document.getElementById('micLabel').innerText = 'Mic Ready';
        document.getElementById('micLabel').style.color = '#94a3b8';
        document.getElementById('sttStatus').innerText = 'Transcription complete! Click Copy to Answer Box below.';
        document.getElementById('sttStatus').style.color = '#22c55e';
      }}

      function copyAnswerText() {{
        if (recordedWords) {{
          navigator.clipboard.writeText(recordedWords).then(() => {{
            document.getElementById('copyTranscriptBtn').innerText = '✓ Copied to Clipboard!';
            setTimeout(() => {{
              document.getElementById('copyTranscriptBtn').innerText = '📋 Copy to Answer Box';
            }}, 2000);
          }});
        }}
      }}
    </script>
    """
    components.html(html_code, height=395)
