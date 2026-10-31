from textwrap import dedent


APP_CSS = dedent(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    :root {
        --bg: #0b0f14;
        --surface: #11161d;
        --card: #151b23;
        --card-hover: #1a2330;
        --line: #252d38;
        --line-strong: #344152;
        --text: #f8fafc;
        --muted: #94a3b8;
        --subtle: #64748b;
        --accent: #818cf8;
        --accent-strong: #6366f1;
        --accent-soft: rgba(99,102,241,.14);
        --accent-glow: rgba(99,102,241,.25);
        --success: #22c55e;
        --warning: #f59e0b;
        --danger: #ef4444;
    }
    
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    
    code, pre, .code-editor, textarea.stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .stApp {
        background: var(--bg);
        color: var(--text);
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
        color: var(--text) !important;
    }
    
    [data-testid="collapsedControl"] {
        color: var(--text) !important;
        background: #151b23 !important;
        border: 1px solid var(--line-strong) !important;
        border-radius: 8px !important;
        margin: 10px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        border-color: var(--accent) !important;
    }
    
    [data-testid="stSidebar"] {
        background: #0d1218;
        border-right: 1px solid var(--line);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 2rem 1.2rem 1.2rem;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: var(--muted);
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        gap: .35rem;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        padding: .7rem .85rem;
        border-radius: 10px;
        color: var(--muted);
        transition: all .2s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid transparent;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255, 255, 255, 0.04);
        color: var(--text);
        border-color: rgba(255, 255, 255, 0.08);
    }
    
    [data-testid="stSidebar"] .stRadio label:has(input:checked) {
        background: var(--accent-soft);
        color: var(--text);
        border-color: rgba(99, 102, 241, 0.35);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
    }
    
    [data-testid="stSidebar"] .stRadio label p {
        color: inherit;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: -0.01em;
        color: var(--text);
    }
    
    h1 {
        font-size: 2.35rem;
        line-height: 1.15;
        margin-bottom: .4rem;
    }
    
    h2 { font-size: 1.5rem; }
    h3 { font-size: 1.08rem; }
    p, label, .stCaption { color: var(--muted); }
    
    .block-container {
        max-width: 1240px;
        padding: 2.5rem 3rem 4rem;
    }
    
    .stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
        border-radius: 10px;
        border: 1px solid var(--line-strong);
        min-height: 2.85rem;
        font-weight: 700;
        font-size: 0.92rem;
        letter-spacing: 0.01em;
        transition: all .2s cubic-bezier(0.4, 0, 0.2, 1);
        background: var(--card);
        color: var(--text);
    }
    
    .stButton > button:hover, .stDownloadButton > button:hover {
        border-color: var(--accent);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        border: 1px solid #818cf8;
        color: white;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35);
    }
    
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 24px rgba(99, 102, 241, 0.55);
        transform: translateY(-2px);
    }
    
    input, textarea, [data-baseweb="select"] > div, [data-baseweb="input"] > div {
        background: var(--card) !important;
        border-color: var(--line) !important;
        color: var(--text) !important;
        border-radius: 10px !important;
        transition: border-color 0.2s ease !important;
    }
    
    input:focus, textarea:focus, [data-baseweb="select"]:focus-within > div {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-soft) !important;
    }
    
    [data-testid="stMetric"] {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 1.15rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.2);
    }
    
    .brand-mark {
        display: flex;
        align-items: center;
        gap: .75rem;
        margin-bottom: .35rem;
    }
    
    .brand-icon {
        display: grid;
        place-items: center;
        width: 2.4rem;
        height: 2.4rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #818cf8 0%, #6366f1 100%);
        color: white;
        font-weight: 700;
        box-shadow: 0 8px 24px rgba(99,102,241,.35);
    }
    
    .brand-name {
        color: var(--text);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .brand-subtitle {
        color: var(--muted);
        font-size: .8rem;
        line-height: 1.45;
        margin: 0 0 1.5rem;
    }
    
    .eyebrow {
        color: var(--accent);
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .12em;
        text-transform: uppercase;
    }
    
    .hero {
        position: relative;
        overflow: hidden;
        background: radial-gradient(circle at 80% 20%, rgba(99,102,241,.24), transparent 40%), linear-gradient(135deg, #13182b 0%, #151b23 60%, #0d1218 100%);
        border: 1px solid rgba(129,140,248,.25);
        border-radius: 16px;
        padding: 3rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .hero h1 {
        font-size: clamp(2.3rem, 4.5vw, 3.8rem);
        max-width: 720px;
        margin: .55rem 0 1rem;
        position: relative;
        z-index: 1;
    }
    
    .preview-card, .surface, .feature-card, .metric-card, .history-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 12px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .feature-card:hover, .history-card:hover {
        border-color: var(--line-strong);
        transform: translateY(-2px);
    }
    
    .question-box {
        background: linear-gradient(135deg, rgba(99,102,241,.12), var(--card));
        border: 1px solid rgba(129,140,248,.32);
        border-left: 5px solid var(--accent-strong);
        border-radius: 12px;
        padding: 1.6rem;
        margin: 1.1rem 0;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }
    
    .question-box h3 {
        color: var(--text);
        font-size: clamp(1.15rem, 2vw, 1.5rem);
        line-height: 1.45;
        margin: 0;
    }
    
    .badge {
        display: inline-block;
        padding: .32rem .65rem;
        border: 1px solid var(--line-strong);
        border-radius: 999px;
        color: var(--muted);
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .05em;
        text-transform: uppercase;
    }
    
    .badge-accent {
        background: var(--accent-soft);
        border-color: rgba(129,140,248,.35);
        color: var(--accent);
    }
    
    .badge-company {
        background: rgba(245, 158, 11, 0.12);
        border-color: rgba(245, 158, 11, 0.4);
        color: #f59e0b;
    }
    
    .stepper {
        display: flex;
        align-items: center;
        gap: .35rem;
        margin: .8rem 0 1.4rem;
    }
    
    .step-dot {
        display: grid;
        place-items: center;
        width: 2.1rem;
        height: 2.1rem;
        border-radius: 50%;
        border: 1px solid var(--line-strong);
        color: var(--muted);
        font-size: .76rem;
        font-weight: 700;
        transition: all 0.2s ease;
    }
    
    .step-dot.answered {
        background: rgba(34,197,94,.15);
        border-color: rgba(34,197,94,.6);
        color: var(--success);
    }
    
    .step-dot.current {
        background: var(--accent-strong);
        border-color: var(--accent);
        color: white;
        box-shadow: 0 0 0 4px var(--accent-soft);
    }
    
    .step-line {
        height: 2px;
        flex: 1;
        background: var(--line);
    }
    
    .interactive-card {
        background: rgba(21, 27, 35, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .followup-box {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.08), var(--card));
        border: 1px solid rgba(245, 158, 11, 0.35);
        border-left: 4px solid #f59e0b;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
    }
    </style>
    """
)
