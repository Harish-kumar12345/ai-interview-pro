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
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage, HRFlowable
)
from reportlab.pdfgen import canvas
from PIL import Image as PILImage


EXHIBITS = [
    {
        "id": "EXHIBIT-01",
        "file": "01_home_screen.png",
        "title": "Home Dashboard & Enterprise Branding",
        "summary": "Main landing interface featuring persistent AI Interview Pro branding, live system status, feature overview, and rapid navigation.",
        "features": [
            "Upper-Left Branding: Persistent 3D AI logo with 'AI Interview Pro · Enterprise Edition' title.",
            "Hero Section: Call-to-action buttons for 'Start Interview' and 'View History'.",
            "Deliberate Practice Highlights: 4 architectural pillars (Company Presets, Resume Context, Voice-to-Voice, Adaptive Review).",
            "How It Works Walkthrough: 4-step progressive preparation guide."
        ]
    },
    {
        "id": "EXHIBIT-02",
        "file": "02_create_interview.png",
        "title": "Interview Creation Workspace & Customization",
        "summary": "Session configuration studio allowing candidates to select roles, target companies, technical skills, and upload resume files.",
        "features": [
            "Company-Specific Presets: Fine-tuned configurations for Google, Amazon Leadership Principles, Microsoft, and Startups.",
            "Resume Parser: Direct upload support for PDF/TXT CVs, automatically extracting project context.",
            "Configurable Parameters: Experience level, technical domains, question types, and challenge depth.",
            "Live Interview Summary: Real-time dynamic card previewing session metadata."
        ]
    },
    {
        "id": "EXHIBIT-03",
        "file": "03_virtual_face_to_face_room.png",
        "title": "Virtual Face-to-Face Voice-to-Voice Room",
        "summary": "Live video call layout with dual tiles simulating an actual remote video interview call.",
        "features": [
            "AI Interviewer Tile: Virtual interviewer persona ('Alex · Tech Lead') with real-time soundwave audio visualizer.",
            "Candidate Webcam Tile: Live mirror video feed displaying candidate body language and facial presence.",
            "AI Speech (TTS): 'AI Ask Question' button reading technical questions aloud in conversational natural English.",
            "Speech Recognition (STT): 'Speak Your Answer' microphone button converting verbal responses into real-time text.",
            "Response Timer: Active countdown timer (03:00) with color-coded warning alerts."
        ]
    },
    {
        "id": "EXHIBIT-04",
        "file": "04_ai_evaluation_and_feedback.png",
        "title": "AI Rubric Evaluation & Adaptive Follow-up",
        "summary": "Structured evaluation engine scoring responses against rubrics and generating adaptive follow-up cross-questions.",
        "features": [
            "Multi-Dimensional Scoring: Instant evaluation score (e.g. 8.5 / 10) across concept, accuracy, example, and depth.",
            "Strengths & Missing Concepts: Actionable diagnostic feedback highlighting technical gaps.",
            "Adaptive Cross-Questioning: 'Ask Adaptive Follow-Up Question' button challenging candidate depth.",
            "Persistent Answer Storage: Candidate response and follow-up answer saved seamlessly."
        ]
    },
    {
        "id": "EXHIBIT-05",
        "file": "05_results_and_analytics.png",
        "title": "Performance Analytics Dashboard & Multi-Format Exports",
        "summary": "Comprehensive debrief screen showing competency scores, charts, question reviews, and download actions.",
        "features": [
            "Circular Score Gauge: Color-coded visual metric gauge (84% overall performance).",
            "Competency & Difficulty Charts: Granular breakdown across topics (Python, Algorithms, System Design) and difficulty.",
            "Multi-Format Export Row: 3 download buttons for PDF Report (ReportLab), Markdown, and CSV details.",
            "Question Debrief Expander: Full review of prompt, candidate response, benchmark answer, and evaluator comments."
        ]
    },
    {
        "id": "EXHIBIT-06",
        "file": "06_interview_history.png",
        "title": "Progress Archive & Session History Tracking",
        "summary": "Persistent historical session log tracking score trajectories over time.",
        "features": [
            "Local JSON Persistence: Saves all completed reports to data/interview_history.json.",
            "Session Cards: Displays date, role, company preset, question count, and performance badge (e.g. '85% · Strong').",
            "Expandable Deep Dive: Reveals topic snapshot bars and metrics for any past interview session."
        ]
    }
]


def set_cell_background(cell, color_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))


def create_docx_report(output_path: Path, screenshots_dir: Path):
    doc = docx.Document()
    
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # 1. Cover Page
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(80)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("AI INTERVIEW PRO")
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(28)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x43, 0x38, 0xca)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(24)
    r_sub = p_sub.add_run("Deployed Project Demonstration & Working Screenshots\nComprehensive Visual Evidence Document")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(14)
    r_sub.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Project Title:", "AI Interview Question Generator & Virtual Video Room"),
        ("Project ID:", "P_112"),
        ("Deployment Type:", "Full-Stack Local & Cloud-Ready Streamlit Application"),
        ("Core Capabilities:", "Voice-to-Voice Interview, Live Camera Simulation, Resume Parsing, AI Evaluation"),
        ("Document Name:", "Hcl_project -project_screenshots"),
        ("Generated Date:", datetime.now().strftime("%B %d, %Y")),
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

    doc.add_page_break()

    # 2. Exhibits Table of Contents
    p_toc = doc.add_paragraph()
    p_toc.paragraph_format.space_after = Pt(12)
    r_toc = p_toc.add_run("Index of Working System Exhibits")
    r_toc.font.name = 'Arial'
    r_toc.font.size = Pt(18)
    r_toc.font.bold = True
    r_toc.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

    toc_tbl = doc.add_table(rows=1, cols=3)
    toc_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = toc_tbl.rows[0].cells
    hdr[0].paragraphs[0].add_run("Exhibit #").bold = True
    hdr[1].paragraphs[0].add_run("System Component / Screen").bold = True
    hdr[2].paragraphs[0].add_run("Core Capabilities Demonstrated").bold = True
    for c in hdr:
        set_cell_background(c, "E2E8F0")
        c.paragraphs[0].runs[0].font.size = Pt(9)
    hdr[0].width = Inches(1.2)
    hdr[1].width = Inches(2.6)
    hdr[2].width = Inches(3.0)

    for ex in EXHIBITS:
        row = toc_tbl.add_row().cells
        row[0].paragraphs[0].add_run(ex["id"]).bold = True
        row[1].paragraphs[0].add_run(ex["title"]).bold = True
        row[2].paragraphs[0].add_run(ex["summary"])
        for c in row:
            set_cell_background(c, "F8FAFC")
            c.paragraphs[0].runs[0].font.size = Pt(8.5)
        row[0].width = Inches(1.2)
        row[1].width = Inches(2.6)
        row[2].width = Inches(3.0)

    doc.add_page_break()

    # 3. Detailed Exhibits with Screenshots
    for ex in EXHIBITS:
        img_path = screenshots_dir / ex["file"]
        
        # Header banner
        p_ex = doc.add_paragraph()
        p_ex.paragraph_format.space_before = Pt(10)
        p_ex.paragraph_format.space_after = Pt(2)
        r_ex = p_ex.add_run(f"{ex['id']}: {ex['title']}")
        r_ex.font.name = 'Arial'
        r_ex.font.size = Pt(14)
        r_ex.font.bold = True
        r_ex.font.color.rgb = RGBColor(0x43, 0x38, 0xca)

        p_desc = doc.add_paragraph()
        p_desc.paragraph_format.space_after = Pt(8)
        r_desc = p_desc.add_run(ex["summary"])
        r_desc.font.name = 'Calibri'
        r_desc.font.size = Pt(9.5)
        r_desc.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

        # Screenshot Image
        if img_path.exists():
            doc.add_picture(str(img_path), width=Inches(6.8))
        else:
            p_missing = doc.add_paragraph(f"[Screenshot {ex['file']} will be placed here]")
            p_missing.paragraph_format.space_after = Pt(10)

        # Feature bullet list
        p_feat_h = doc.add_paragraph()
        p_feat_h.paragraph_format.space_before = Pt(8)
        p_feat_h.paragraph_format.space_after = Pt(4)
        r_fh = p_feat_h.add_run("Key Features Demonstrated in this View:")
        r_fh.bold = True
        r_fh.font.size = Pt(9.5)
        r_fh.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

        for feat in ex["features"]:
            p_f = doc.add_paragraph(style='List Bullet')
            p_f.paragraph_format.space_after = Pt(2)
            r_f = p_f.add_run(feat)
            r_f.font.size = Pt(8.5)
            r_f.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

        doc.add_page_break()

    doc.save(str(output_path))
    print(f"DOCX Report created: {output_path} ({output_path.stat().st_size} bytes)")


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
        if self._pageNumber == 1:
            return  # Skip cover
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(36, 762, "AI Interview Pro · Project Screenshots & Working Evidence")
        self.drawRightString(576, 762, "Project ID: P_112")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 756, 576, 756)
        
        self.line(36, 42, 576, 42)
        self.drawString(36, 30, "Confidential · Deployed Working Evidence")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 30, page_str)
        self.restoreState()


def create_pdf_report(output_path: Path, screenshots_dir: Path):
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
        'CoverTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#3730a3"),
        alignment=1,
        spaceAfter=10
    )
    
    sub_style = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#64748b"),
        alignment=1,
        spaceAfter=30
    )

    ex_title_style = ParagraphStyle(
        'ExTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4338ca"),
        spaceBefore=8,
        spaceAfter=4
    )
    
    desc_style = ParagraphStyle(
        'ExDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#475569"),
        spaceAfter=6
    )

    feat_style = ParagraphStyle(
        'ExFeat',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=2
    )

    story = []

    # 1. Cover
    story.append(Spacer(1, 100))
    story.append(Paragraph("<b>AI INTERVIEW PRO</b>", title_style))
    story.append(Paragraph("Enterprise-Grade AI Mock Interview Platform<br/><b>Deployed Project Demonstration & Working Screenshots</b>", sub_style))
    story.append(HRFlowable(width="60%", thickness=1.5, color=colors.HexColor("#6366f1"), spaceAfter=30))

    meta_rows = [
        [Paragraph("<b>Project Title:</b>", styles['Normal']), Paragraph("AI Interview Question Generator & Virtual Video Room", styles['Normal'])],
        [Paragraph("<b>Project ID:</b>", styles['Normal']), Paragraph("P_112", styles['Normal'])],
        [Paragraph("<b>Technology Stack:</b>", styles['Normal']), Paragraph("Python 3.13, Streamlit, Google Gemini AI, Web Speech API, ReportLab", styles['Normal'])],
        [Paragraph("<b>Key Features:</b>", styles['Normal']), Paragraph("Face-to-Face Video Room, Real-time STT Voice, AI Speech (TTS), Resume Parser, Rubric Evaluation", styles['Normal'])],
        [Paragraph("<b>Document:</b>", styles['Normal']), Paragraph("Hcl_project -project_screenshots.pdf", styles['Normal'])],
        [Paragraph("<b>Compilation Date:</b>", styles['Normal']), Paragraph(datetime.now().strftime("%B %d, %Y"), styles['Normal'])],
    ]
    meta_table = Table(meta_rows, colWidths=[130, 370])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#f1f5f9")),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor("#f8fafc")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    story.append(meta_table)
    story.append(PageBreak())

    # 2. Exhibits Table of Contents
    story.append(Paragraph("<b>Index of Working System Exhibits</b>", ex_title_style))
    story.append(Spacer(1, 6))

    toc_data = [["Exhibit #", "Component / View", "Description"]]
    for ex in EXHIBITS:
        toc_data.append([ex["id"], ex["title"], ex["summary"]])

    toc_table = Table(toc_data, colWidths=[70, 180, 290])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # 3. Exhibits Pages
    for ex in EXHIBITS:
        img_path = screenshots_dir / ex["file"]
        
        story.append(Paragraph(f"<b>{ex['id']}: {ex['title']}</b>", ex_title_style))
        story.append(Paragraph(ex["summary"], desc_style))

        if img_path.exists():
            # Calculate height maintaining aspect ratio for width = 520
            with PILImage.open(img_path) as im:
                w, h = im.size
                ratio = h / w
                target_w = 520
                target_h = target_w * ratio
                # Cap height if too large
                if target_h > 420:
                    target_h = 420
                    target_w = target_h / ratio
            
            story.append(RLImage(str(img_path), width=target_w, height=target_h))
            story.append(Spacer(1, 6))

        story.append(Paragraph("<b>Demonstrated Capabilities:</b>", feat_style))
        for feat in ex["features"]:
            story.append(Paragraph(f"• {feat}", feat_style))

        story.append(PageBreak())

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Report created: {output_path} ({output_path.stat().st_size} bytes)")


if __name__ == "__main__":
    root = Path(__file__).parent
    sc_dir = root / "assets" / "screenshots"
    docx_out = root / "Hcl_project -project_screenshots.docx"
    pdf_out = root / "Hcl_project -project_screenshots.pdf"
    
    print("Generating DOCX Screenshots Report...")
    create_docx_report(docx_out, sc_dir)
    
    print("Generating PDF Screenshots Report...")
    create_pdf_report(pdf_out, sc_dir)
    print("Done!")

