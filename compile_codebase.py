import os
from pathlib import Path
from datetime import datetime

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, HRFlowable
)
from reportlab.pdfgen import canvas


FILES_TO_INCLUDE = [
    # Core Application
    ("Core Application", "main.py", "Streamlit Main Controller & Interactive UI Coordinator"),
    ("Core Application", "config.py", "Application Settings & Environment Loader"),
    ("Core Application", "llm_client.py", "Google Gemini API Client & JSON Completer"),
    ("Core Application", "question_generator.py", "Structured Question Generator & Normalizer"),
    ("Core Application", "evaluator.py", "Answer Evaluator & Adaptive Follow-up Generator"),
    ("Core Application", "company_presets.py", "Company-Specific Interview Profiles & Guidelines"),
    ("Core Application", "resume_parser.py", "PDF & Text Resume Context Extractor"),
    ("Core Application", "pdf_exporter.py", "Professional ReportLab PDF Performance Exporter"),
    ("Core Application", "validators.py", "Input, Question & Evaluation Schema Validators"),
    ("Core Application", "storage.py", "Local JSON Interview History Persistence"),
    ("Core Application", "utils.py", "Score Aggregation & Calculation Utilities"),
    ("Core Application", "check_models.py", "Gemini Model Discovery & Diagnostics"),
    
    # UI Components & Styling
    ("UI & Frontend", "ui/components.py", "UI Widgets, Video Room, Stepper, Timer, Audio & Header"),
    ("UI & Frontend", "ui/styles.py", "Custom CSS Styles, Theme Variables & Modern Typography"),
    ("UI & Frontend", "ui/__init__.py", "UI Package Initialization"),

    # Prompt Engineering
    ("Prompt Engineering", "prompts/base.py", "Core Prompt Generator & JSON Format Instructions"),
    ("Prompt Engineering", "prompts/technical_prompt.py", "Technical Interview Questions Prompt Builder"),
    ("Prompt Engineering", "prompts/coding_prompt.py", "Coding Problems & Architecture Prompt Builder"),
    ("Prompt Engineering", "prompts/conceptual_prompt.py", "Conceptual Understanding Prompt Builder"),
    ("Prompt Engineering", "prompts/scenario_prompt.py", "Scenario & System Design Prompt Builder"),
    ("Prompt Engineering", "prompts/behavioral_prompt.py", "Behavioral & Leadership Prompt Builder"),
    ("Prompt Engineering", "prompts/hr_prompt.py", "HR & Soft Skills Prompt Builder"),
    ("Prompt Engineering", "prompts/evaluation_prompt.py", "Rubric Evaluation Scoring Prompt Builder"),
    ("Prompt Engineering", "prompts/__init__.py", "Prompts Package Initialization"),

    # Test Suite
    ("Automated Tests", "tests/test_advanced_features.py", "Tests for Resume, Company Presets & PDF Generation"),
    ("Automated Tests", "tests/test_parser.py", "Tests for Normalization & Question Parser"),
    ("Automated Tests", "tests/test_validators.py", "Tests for Input & Evaluation Validation"),
    ("Automated Tests", "tests/test_evaluator.py", "Tests for Answer Evaluation Logic"),
    ("Automated Tests", "tests/test_prompts.py", "Tests for Prompt Generation Formatting"),
    ("Automated Tests", "tests/test_storage.py", "Tests for JSON Storage & History Loading"),

    # Configuration & Docs
    ("Configuration & Docs", "requirements.txt", "Project Dependencies & Package Specifications"),
    ("Configuration & Docs", ".streamlit/config.toml", "Streamlit Server & Theme Configuration"),
    ("Configuration & Docs", ".env.example", "Environment Variables Template"),
    ("Configuration & Docs", "architecture.md", "System Architecture & Flow Specification"),
    ("Configuration & Docs", "INTERVIEW_GUIDE.md", "Technical Interview Practice & Scoring Guide"),
    ("Configuration & Docs", "README.md", "Project Overview, Setup & Execution Instructions"),
]


def set_cell_background(cell, color_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))


def create_docx(output_path: Path, root_dir: Path):
    doc = docx.Document()
    
    # Set standard margins (0.75 in)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # Style definitions
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

    # 1. Title Page
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(80)
    title_p.paragraph_format.space_after = Pt(10)
    run_title = title_p.add_run("AI INTERVIEW PRO")
    run_title.font.name = 'Arial'
    run_title.font.size = Pt(28)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x43, 0x38, 0xca) # Indigo 700

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(20)
    run_sub = sub_p.add_run("Enterprise-Grade AI Mock Interview Platform\nComplete Source Code Compilation")
    run_sub.font.name = 'Calibri'
    run_sub.font.size = Pt(14)
    run_sub.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

    # Metadata Box Table
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Project Name:", "AI Interview Question Generator & Virtual Interview Room"),
        ("Project ID:", "P_112"),
        ("Core Stack:", "Python 3.13, Streamlit, Google Gemini AI (gemini-3.5-flash-lite)"),
        ("Features Included:", "Virtual Face-to-Face Room, Live Audio (TTS), Real-time STT, PDF Reports, Resume Parser"),
        ("Compiled File:", "Hcl_project -source _code"),
        ("Compilation Date:", datetime.now().strftime("%B %d, %Y")),
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

    # 2. Table of Contents / File Directory
    toc_heading = doc.add_paragraph()
    toc_run = toc_heading.add_run("Table of Contents / Source Code Index")
    toc_run.font.name = 'Arial'
    toc_run.font.size = Pt(18)
    toc_run.font.bold = True
    toc_run.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
    toc_heading.paragraph_format.space_after = Pt(12)

    toc_table = doc.add_table(rows=1, cols=4)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = toc_table.rows[0].cells
    hdr[0].paragraphs[0].add_run("#").bold = True
    hdr[1].paragraphs[0].add_run("Category").bold = True
    hdr[2].paragraphs[0].add_run("File Path").bold = True
    hdr[3].paragraphs[0].add_run("Description").bold = True
    for c in hdr:
        set_cell_background(c, "E2E8F0")
        c.paragraphs[0].runs[0].font.size = Pt(9)
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

    hdr[0].width = Inches(0.4)
    hdr[1].width = Inches(1.5)
    hdr[2].width = Inches(2.2)
    hdr[3].width = Inches(2.7)

    for idx, (cat, rel_path, desc) in enumerate(FILES_TO_INCLUDE, start=1):
        row = toc_table.add_row().cells
        row[0].paragraphs[0].add_run(str(idx)).font.size = Pt(8.5)
        row[1].paragraphs[0].add_run(cat).font.size = Pt(8.5)
        row[2].paragraphs[0].add_run(rel_path).font.size = Pt(8.5)
        row[2].paragraphs[0].runs[0].bold = True
        row[3].paragraphs[0].add_run(desc).font.size = Pt(8.5)
        
        bg_col = "FFFFFF" if idx % 2 == 0 else "F8FAFC"
        for c in row:
            set_cell_background(c, bg_col)
        row[0].width = Inches(0.4)
        row[1].width = Inches(1.5)
        row[2].width = Inches(2.2)
        row[3].width = Inches(2.7)

    doc.add_page_break()

    # 3. Source Code Files
    current_category = None
    for idx, (category, rel_path, desc) in enumerate(FILES_TO_INCLUDE, start=1):
        file_path = root_dir / rel_path
        if not file_path.exists():
            continue

        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            content = f"# Error reading file: {e}"

        lines = content.splitlines()
        loc = len(lines)

        # Category Header if changed
        if category != current_category:
            current_category = category
            cat_p = doc.add_paragraph()
            cat_p.paragraph_format.space_before = Pt(16)
            cat_p.paragraph_format.space_after = Pt(4)
            cat_run = cat_p.add_run(f"Section: {category.upper()}")
            cat_run.font.name = 'Arial'
            cat_run.font.size = Pt(12)
            cat_run.font.bold = True
            cat_run.font.color.rgb = RGBColor(0x63, 0x66, 0xf1)

        # File Heading
        file_p = doc.add_paragraph()
        file_p.paragraph_format.space_before = Pt(10)
        file_p.paragraph_format.space_after = Pt(2)
        f_run = file_p.add_run(f"[{idx}] {rel_path}")
        f_run.font.name = 'Consolas'
        f_run.font.size = Pt(11)
        f_run.font.bold = True
        f_run.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

        desc_p = doc.add_paragraph()
        desc_p.paragraph_format.space_after = Pt(6)
        desc_run = desc_p.add_run(f"Purpose: {desc} | Lines: {loc} lines | Path: {rel_path}")
        desc_run.font.name = 'Calibri'
        desc_run.font.size = Pt(8.5)
        desc_run.font.italic = True
        desc_run.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

        # Code Container Table (Light gray box with monospaced code)
        code_table = doc.add_table(rows=1, cols=1)
        code_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        code_cell = code_table.rows[0].cells[0]
        code_cell.width = Inches(6.8)
        set_cell_background(code_cell, "F8FAFC")

        code_p = code_cell.paragraphs[0]
        code_p.paragraph_format.space_before = Pt(4)
        code_p.paragraph_format.space_after = Pt(4)
        code_p.paragraph_format.line_spacing = Pt(11)

        # Format code without line numbers
        formatted_code = [line.replace('\t', '    ') for line in lines]
        full_code_text = "\n".join(formatted_code)
        c_run = code_p.add_run(full_code_text)
        c_run.font.name = 'Consolas'
        c_run.font.size = Pt(8)
        c_run.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

        doc.add_paragraph().paragraph_format.space_after = Pt(12)

    try:
        doc.save(str(output_path))
        print(f"DOCX created: {output_path} ({output_path.stat().st_size} bytes)")
    except PermissionError:
        alt_path = output_path.parent / "Hcl_project -source _code_clean.docx"
        doc.save(str(alt_path))
        print(f"Note: '{output_path.name}' is currently open in Word/another program.")
        print(f"Clean DOCX saved to: {alt_path} ({alt_path.stat().st_size} bytes)")


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
            return  # Skip cover page
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header
        self.drawString(36, 762, "AI Interview Pro · Complete Source Code Compilation")
        self.drawRightString(576, 762, "Project ID: P_112")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 756, 576, 756)
        
        # Footer
        self.line(36, 42, 576, 42)
        self.drawString(36, 30, "Confidential · All Rights Reserved")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 30, page_str)
        self.restoreState()


def create_pdf(output_path: Path, root_dir: Path):
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
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=14,
        spaceAfter=6
    )

    file_title_style = ParagraphStyle(
        'FileHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#4338ca")
    )
    
    file_sub_style = ParagraphStyle(
        'FileSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#64748b")
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8.2,
        textColor=colors.HexColor("#0f172a"),
    )

    story = []

    # 1. Cover Page
    story.append(Spacer(1, 100))
    story.append(Paragraph("<b>AI INTERVIEW PRO</b>", title_style))
    story.append(Paragraph("Enterprise-Grade AI Mock Interview Platform<br/><b>Complete Source Code Compilation</b>", sub_style))
    story.append(HRFlowable(width="60%", thickness=1.5, color=colors.HexColor("#6366f1"), spaceAfter=30))

    meta_rows = [
        [Paragraph("<b>Project Title:</b>", styles['Normal']), Paragraph("AI Interview Question Generator & Virtual Video Room", styles['Normal'])],
        [Paragraph("<b>Project ID:</b>", styles['Normal']), Paragraph("P_112", styles['Normal'])],
        [Paragraph("<b>Technology Stack:</b>", styles['Normal']), Paragraph("Python 3.13, Streamlit, Google Gemini AI, ReportLab, Web Speech API", styles['Normal'])],
        [Paragraph("<b>Key Features:</b>", styles['Normal']), Paragraph("Virtual Face-to-Face Room, Live Audio (TTS), Real-time STT, PDF Reports, Resume Parser", styles['Normal'])],
        [Paragraph("<b>Document:</b>", styles['Normal']), Paragraph("Hcl_project -source _code.pdf", styles['Normal'])],
        [Paragraph("<b>Compiled Date:</b>", styles['Normal']), Paragraph(datetime.now().strftime("%B %d, %Y"), styles['Normal'])],
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

    # 2. Table of Contents
    story.append(Paragraph("<b>Table of Contents / Source Code Index</b>", h1_style))
    story.append(Spacer(1, 6))

    toc_data = [["#", "Category", "File Path", "Description"]]
    for idx, (cat, rel_path, desc) in enumerate(FILES_TO_INCLUDE, start=1):
        toc_data.append([str(idx), cat, rel_path, desc])

    toc_table = Table(toc_data, colWidths=[24, 110, 160, 246])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # 3. Source Code Files
    current_cat = None
    for idx, (cat, rel_path, desc) in enumerate(FILES_TO_INCLUDE, start=1):
        file_path = root_dir / rel_path
        if not file_path.exists():
            continue

        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            content = f"# Error reading file: {e}"

        lines = content.splitlines()
        loc = len(lines)

        if cat != current_cat:
            current_cat = cat
            story.append(Paragraph(f"<b>SECTION: {cat.upper()}</b>", h1_style))
            story.append(Spacer(1, 4))

        # File Banner
        file_card = [
            [
                Paragraph(f"<b>[{idx}] {rel_path}</b>", file_title_style),
                Paragraph(f"<b>{loc} lines</b>", ParagraphStyle('R', alignment=2, fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#6366f1')))
            ],
            [
                Paragraph(f"Purpose: {desc}", file_sub_style),
                ""
            ]
        ]
        banner_table = Table(file_card, colWidths=[440, 100])
        banner_table.setStyle(TableStyle([
            ('SPAN', (0, 1), (1, 1)),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(banner_table)
        story.append(Spacer(1, 4))

        # Format code text without line numbers in splittable Preformatted chunks
        chunk_size = 40
        code_lines = [line.replace('\t', '    ') for line in lines]

        if not code_lines:
            code_lines = ["(Empty file)"]

        for c_idx in range(0, len(code_lines), chunk_size):
            chunk = code_lines[c_idx:c_idx + chunk_size]
            chunk_text = "\n".join(chunk)
            story.append(Preformatted(chunk_text, code_style))

        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceBefore=6, spaceAfter=14))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF created: {output_path} ({output_path.stat().st_size} bytes)")


if __name__ == "__main__":
    root = Path(__file__).parent
    docx_file = root / "Hcl_project -source _code.docx"
    pdf_file = root / "Hcl_project -source _code.pdf"
    
    print("Generating DOCX compilation...")
    create_docx(docx_file, root)
    
    print("Generating PDF compilation...")
    create_pdf(pdf_file, root)
    print("Done!")
