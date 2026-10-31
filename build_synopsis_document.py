import os
from pathlib import Path
from datetime import datetime

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas


SYNOPSIS_SECTIONS = [
    {
        "title": "1. Project Overview & Abstract",
        "content": [
            "AI Interview Pro (Project ID: P_112) is an enterprise-grade, intelligent mock interview and candidate assessment platform designed to bridge the gap between technical preparation and high-stakes interview performance.",
            "Traditional interview preparation relies on static, repetitive question banks that fail to simulate the dynamic unpredictability of live technical rounds. Human mock interviewers, while effective, are expensive, schedule-constrained, and prone to subjective assessment bias.",
            "AI Interview Pro introduces a dual-engine architecture: an interactive presentation and audio-visual layer coupled with an advanced Large Language Model (Google Gemini API). The system dynamically synthesizes role-specific, company-tailored questions, provides a real-time Virtual Face-to-Face Voice-to-Voice room (Webcam + Speech-To-Text + Text-To-Speech), evaluates candidate responses across 4-dimensional rubrics, conducts adaptive follow-up cross-questioning, and produces branded PDF debrief reports."
        ]
    },
    {
        "title": "2. Problem Statement",
        "content": [
            "Current computer science graduates and transitioning software professionals face distinct bottlenecks during technical hiring cycles:",
            "• Static Question Banks: LeetCode and textbook repositories present isolated coding snippets without assessing verbal technical communication, trade-off analysis, or architectural reasoning.",
            "• High Cost & Inaccessibility of Human Mentors: Expert mock interviews typically cost $100–$250 per session, making consistent deliberate practice financially prohibitive for freshers.",
            "• Lack of Objective Rubric Feedback: Standard online assessments provide binary (Pass/Fail) outcomes rather than granular diagnostic feedback detailing specific missing concepts.",
            "• Absence of Company-Specific Culture & Flavor: Candidates lack tools to practice company-calibrated standards, such as Amazon's Leadership Principles, Google's scalability demands, or TCS's foundational computer science focus.",
            "• Resume-Blind Evaluation: Generic tools cannot tailor questions to a candidate's actual projects, technologies, and past internships listed on their resume."
        ]
    },
    {
        "title": "3. Project Objectives",
        "content": [
            "The primary objective of AI Interview Pro is to deliver an accessible, hyper-realistic, objective technical interview simulation environment:",
            "• Dynamic Contextual Synthesis: Generate role-, experience-, domain-, and company-tailored technical, coding, and behavioral interview questions on demand.",
            "• Virtual Face-to-Face Voice Simulation: Provide a 2-way video room interface featuring an animated AI interviewer avatar, live webcam mirror feed, audio question synthesis (TTS), and real-time verbal speech transcription (STT).",
            "• Resume-Grounded Probing: Parse candidate PDF/TXT resumes using lightweight text extraction to formulate targeted questions probing real project implementations.",
            "• Multi-Dimensional Rubric Evaluation: Assess answers across Conceptual Clarity, Technical Accuracy, Real-World Examples, and Architectural Depth with transparent numerical scores (out of 10).",
            "• Adaptive Cross-Questioning: Detect omissions or shallow explanations and dynamically generate follow-up questions to test candidate depth.",
            "• Local Privacy & Comprehensive Reporting: Persist interview history without external database dependencies and export publication-ready performance PDF reports."
        ]
    },
    {
        "title": "4. System Architecture & Methodology",
        "content": [
            "The system employs a decoupled, modular pipeline adhering to clean architecture principles:",
            "• Presentation & Virtual Room Subsystem (Streamlit & Web APIs): Coordinates the candidate interface, custom CSS theme tokens, two-way video grid (HTML5 getUserMedia), browser SpeechSynthesis (TTS), and Web Speech API recognition (STT).",
            "• Context & Prompt Formulation Engine (prompt_generator.py, company_presets.py): Assembles candidate parameters, target company presets (Google, Amazon, Microsoft, Startups), and parsed resume text into strict JSON-enforcing system instructions.",
            "• LLM Client & Validation Gateway (llm_client.py, validators.py): Communicates with the Google Gemini API (gemini-3.5-flash-lite). All raw outputs pass through payload normalizers and defensive JSON parsers that handle markdown fences and bare arrays, eliminating runtime crashes.",
            "• Evaluation & Scoring Subsystem (evaluator.py, utils.py): Scores candidate responses against expected benchmark answers, identifies strengths and missing concepts, and synthesizes adaptive follow-ups.",
            "• Persistence & Export Engine (storage.py, pdf_exporter.py): Manages local atomic JSON storage (interview_history.json) and compiles color-coded, professional PDF performance certificates via ReportLab."
        ]
    },
    {
        "title": "5. Core Functional Modules",
        "content": [
            "The platform is organized into six cohesive technical modules:",
            "1. Studio & Profile Setup: Dropdown controls for target roles (13+ profiles), experience tiers, company presets, skills multiselect, domain settings, and question count controls.",
            "2. Resume Context Parser: PyPDF-powered document ingest engine that extracts project and skill highlights from uploaded resumes to contextualize questions.",
            "3. Virtual Face-to-Face Voice Room: Two-tile call interface with AI Interviewer avatar ('Alex'), live soundwave animation, candidate webcam stream, countdown timer, audio readout, and 1-click speech transcription.",
            "4. Interactive Solution & Code Workspace: Multi-language template selector (Python, JavaScript, Java, C++, SQL) with monospaced code editing and integrated scoring rubric previews.",
            "5. AI Rubric Evaluator & Adaptive Follow-up: Instant scoring engine providing numerical marks, positive signals, focus areas, and one-click adaptive follow-up challenges.",
            "6. Analytics & Multi-Format Reporting: Color-coded score gauge, topic competency breakdown, difficulty trend analysis, and instant downloads in PDF, Markdown, and CSV formats."
        ]
    },
    {
        "title": "6. Technology Stack & Environment",
        "content": [
            "• Programming Language: Python 3.13 (x64)",
            "• Frontend Framework: Streamlit 1.64.0 (Custom CSS, Session State Management, Component Iframes)",
            "• Artificial Intelligence / LLM: Google Gemini API (Model: gemini-3.5-flash-lite) via google-genai SDK 2.25",
            "• Client-Side Voice Processing: HTML5 Web Speech API (SpeechRecognition for STT, SpeechSynthesis for TTS)",
            "• Video Mirror: HTML5 MediaDevices API (WebRTC getUserMedia)",
            "• PDF Generation: ReportLab 5.1.0 (Platypus flowables, NumberedCanvas, table formatters)",
            "• Document Parsing: PyPDF 6.21.4 (Pure Python binary stream parser)",
            "• Testing Framework: Pytest 8.4.2 (13 Automated Unit Tests verifying normalization, validation, prompts, and exports)",
            "• Operating Environment: Localhost / Cloud Deployable (Container-Ready, Headless Mode)"
        ]
    },
    {
        "title": "7. Verification, Testing & Quality Assurance",
        "content": [
            "Quality assurance is enforced through comprehensive automated test suites and defensive schema validation:",
            "• Schema & Payload Validation: Tests verify that non-standard LLM payloads (top-level arrays, capitalized keys, markdown fences) are automatically normalized without crashing.",
            "• Unit Test Suite: 13/13 passing automated unit tests covering input sanitization, evaluation scores (0–10 boundaries), resume extraction, company preset notes, and PDF generation.",
            "• Mock Testing: Tests run with mocked clients ensuring regression tests execute in under 3 seconds without consuming live API tokens or requiring network access."
        ]
    },
    {
        "title": "8. Feasibility & Cost-Benefit Analysis",
        "content": [
            "• Economic Feasibility: Utilizing client-side browser speech APIs eliminates external cloud STT/TTS per-minute charges. The Gemini 3.5 Flash Lite model provides low-latency generation at negligible API cost ($0.0001 per interview session).",
            "• Technical Feasibility: Pure Python backend with Streamlit frontend ensures zero native C++ compiler dependencies on Windows/Linux environments.",
            "• Operational Feasibility: Self-contained local JSON persistence guarantees that users can run the app offline or on internal corporate intranets without setting up complex database servers."
        ]
    },
    {
        "title": "9. Limitations & Future Roadmap",
        "content": [
            "• Current Limitations: Single-user local session persistence; speech recognition accuracy depends on browser microphone quality and ambient noise.",
            "• Future Scope: Integration of multi-user cloud authentication (OAuth2 / Firebase), enterprise PostgreSQL persistence, full Retrieval-Augmented Generation (RAG) over company-specific technical handbooks, and computer-vision facial sentiment analysis."
        ]
    },
    {
        "title": "10. Conclusion",
        "content": [
            "AI Interview Pro represents a significant advancement in technical career enablement tools. By integrating generative AI with real-time browser audio-visual capabilities, the platform provides candidates with an authentic, pressure-tested, and diagnostic interview simulation experience.",
            "The project successfully meets all academic, technical, and industry Center of Excellence (COE) standards, demonstrating end-to-end software engineering excellence, resilient error handling, and practical AI application."
        ]
    }
]


def set_cell_background(cell, color_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))


def create_synopsis_docx(output_path: Path):
    doc = docx.Document()
    
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # 1. Title Page / Header
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(40)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("PROJECT SYNOPSIS")
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(26)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x43, 0x38, 0xca)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(16)
    r_sub = p_sub.add_run("AI Interview Pro: Intelligent Mock Interview & Candidate Assessment Platform\nCenter of Excellence (COE) Technical Project Submission")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

    # Metadata Table
    meta_table = doc.add_table(rows=7, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Project Title:", "AI Interview Question Generator & Virtual Video Room"),
        ("Project ID:", "P_112"),
        ("Domain / Category:", "Artificial Intelligence / EdTech / Cross-Industry Hiring Tools"),
        ("Core Stack:", "Python 3.13, Streamlit, Google Gemini AI (gemini-3.5-flash-lite)"),
        ("Key Innovations:", "Voice-to-Voice AI, Webcam Mirror, Resume Parsing, Adaptive Follow-ups"),
        ("Submission Track:", "Center of Excellence (COE) Technical Project Review"),
        ("Submission Date:", datetime.now().strftime("%B %d, %Y")),
    ]
    for row_idx, (k, v) in enumerate(meta_data):
        row = meta_table.rows[row_idx]
        row.cells[0].paragraphs[0].add_run(k).bold = True
        row.cells[0].paragraphs[0].runs[0].font.size = Pt(9.5)
        row.cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        row.cells[0].width = Inches(1.8)
        set_cell_background(row.cells[0], "F1F5F9")
        
        row.cells[1].paragraphs[0].add_run(v)
        row.cells[1].paragraphs[0].runs[0].font.size = Pt(9.5)
        row.cells[1].width = Inches(5.0)
        set_cell_background(row.cells[1], "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    # 2. Sections
    for sec in SYNOPSIS_SECTIONS:
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        r_h = h.add_run(sec["title"])
        r_h.font.name = 'Arial'
        r_h.font.size = Pt(12)
        r_h.font.bold = True
        r_h.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

        for p_text in sec["content"]:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = Pt(13)
            
            if p_text.startswith("• "):
                p.style = 'List Bullet'
                r_text = p.add_run(p_text[2:])
            elif p_text.startswith("1. ") or p_text.startswith("2. ") or p_text.startswith("3. ") or p_text.startswith("4. ") or p_text.startswith("5. ") or p_text.startswith("6. "):
                p.style = 'List Number'
                r_text = p.add_run(p_text[3:])
            else:
                r_text = p.add_run(p_text)
            
            r_text.font.name = 'Calibri'
            r_text.font.size = Pt(10)
            r_text.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.save(str(output_path))
    print(f"DOCX Synopsis created: {output_path} ({output_path.stat().st_size} bytes)")


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header
        self.drawString(36, 762, "AI Interview Pro · Project Synopsis (P_112)")
        self.drawRightString(576, 762, "COE Project Submission")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 756, 576, 756)
        
        # Footer
        self.line(36, 42, 576, 42)
        self.drawString(36, 30, "Center of Excellence (COE) Technical Evaluation")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 30, page_str)
        self.restoreState()


def create_synopsis_pdf(output_path: Path):
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'SynTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#3730a3"),
        spaceAfter=4
    )
    
    sub_style = ParagraphStyle(
        'SynSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=12
    )

    sec_title_style = ParagraphStyle(
        'SecTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4
    )

    story = []

    # Title Banner
    story.append(Paragraph("<b>PROJECT SYNOPSIS</b>", title_style))
    story.append(Paragraph("<b>AI Interview Pro: Intelligent Mock Interview & Candidate Assessment Platform</b><br/>Center of Excellence (COE) Project Submission · Track: AI & Machine Learning Tooling", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#6366f1"), spaceAfter=10))

    # Metadata Table
    meta_rows = [
        [Paragraph("<b>Project Title:</b>", body_style), Paragraph("AI Interview Question Generator & Virtual Video Room", body_style)],
        [Paragraph("<b>Project ID:</b>", body_style), Paragraph("P_112", body_style)],
        [Paragraph("<b>Core Stack:</b>", body_style), Paragraph("Python 3.13, Streamlit, Google Gemini AI (gemini-3.5-flash-lite)", body_style)],
        [Paragraph("<b>Key Features:</b>", body_style), Paragraph("Voice-to-Voice AI, Webcam Mirror, Resume Context, Adaptive Follow-ups, PDF Export", body_style)],
        [Paragraph("<b>Submission Date:</b>", body_style), Paragraph(datetime.now().strftime("%B %d, %Y"), body_style)],
    ]
    meta_table = Table(meta_rows, colWidths=[120, 420])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#f1f5f9")),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor("#f8fafc")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Sections
    for sec in SYNOPSIS_SECTIONS:
        story.append(Paragraph(f"<b>{sec['title']}</b>", sec_title_style))
        for line in sec["content"]:
            # Format bullet points cleanly
            if line.startswith("• "):
                story.append(Paragraph(f"&bull; {line[2:]}", ParagraphStyle('Bullet', parent=body_style, leftIndent=12, spaceAfter=2)))
            elif line.startswith("1. ") or line.startswith("2. ") or line.startswith("3. ") or line.startswith("4. ") or line.startswith("5. ") or line.startswith("6. "):
                story.append(Paragraph(f"<b>{line[:3]}</b> {line[3:]}", ParagraphStyle('Numbered', parent=body_style, leftIndent=12, spaceAfter=2)))
            else:
                story.append(Paragraph(line, body_style))
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Synopsis created: {output_path} ({output_path.stat().st_size} bytes)")


if __name__ == "__main__":
    root = Path(__file__).parent
    docx_out = root / "Hcl_project -synopsis.docx"
    pdf_out = root / "Hcl_project -synopsis.pdf"
    
    print("Generating DOCX Project Synopsis...")
    create_synopsis_docx(docx_out)
    
    print("Generating PDF Project Synopsis...")
    create_synopsis_pdf(pdf_out)
    print("Done!")

