import io
from typing import Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable


def generate_interview_pdf(report: dict[str, Any], configuration: dict[str, Any], questions: list[dict[str, Any]], answers: dict[int, str]) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1e293b'),
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748b'),
        fontName='Helvetica'
    )
    
    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4338ca'),
        fontName='Helvetica-Bold',
        spaceBefore=10,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1e293b'),
        fontName='Helvetica'
    )
    
    bold_label = ParagraphStyle(
        'BoldLabel',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        fontName='Helvetica-Bold'
    )
    
    quote_style = ParagraphStyle(
        'QuoteStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#0f172a'),
        fontName='Helvetica-Oblique'
    )

    story = []

    # Header
    role = configuration.get("role", "Software Professional")
    company = configuration.get("company", "Standard")
    exp = configuration.get("experience", "Not specified")
    overall_score = float(report.get("overall_score", 0))
    avg_score = float(report.get("average", 0))

    if overall_score >= 75:
        recommendation = "RECOMMENDED · STRONG CANDIDATE"
        rec_color = colors.HexColor('#15803d')
    elif overall_score >= 50:
        recommendation = "POTENTIAL CANDIDATE · DEVELOPING"
        rec_color = colors.HexColor('#b45309')
    else:
        recommendation = "NEEDS MORE PREPARATION"
        rec_color = colors.HexColor('#b91c1c')

    header_data = [
        [
            Paragraph("<b>AI Interview Performance Report</b>", title_style),
            Paragraph(f"<font color='{rec_color.hexval()}'><b>{recommendation}</b></font>", ParagraphStyle('Rec', alignment=2, fontName='Helvetica-Bold', fontSize=10, leading=14))
        ],
        [
            Paragraph(f"<b>Target Role:</b> {role} | <b>Company Prep:</b> {company} | <b>Experience:</b> {exp}", subtitle_style),
            Paragraph(f"Overall Score: <b>{overall_score:.0f}%</b> (Avg: {avg_score:.1f}/10)", ParagraphStyle('Score', alignment=2, fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#4338ca')))
        ]
    ]
    header_table = Table(header_data, colWidths=[380, 160])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=10))

    # Summary Metrics Table
    summary_data = [
        ["Total Questions", "Answered", "Average Score", "Overall Performance"],
        [
            str(report.get("questions", len(questions))),
            str(report.get("attempted", len(answers))),
            f"{avg_score:.1f} / 10",
            f"{overall_score:.0f}%"
        ]
    ]
    summary_table = Table(summary_data, colWidths=[135, 135, 135, 135])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#475569')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, 1), 12),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#1e293b')),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 12))

    # Topic Scores Table if available
    topic_scores = report.get("topic_scores", {})
    if topic_scores:
        story.append(Paragraph("Topic Breakdown", section_style))
        topic_data = [["Topic", "Score / 10", "Proficiency"]]
        for topic, tscore in topic_scores.items():
            tscore_float = float(tscore)
            status = "Strong" if tscore_float >= 7 else "Fair" if tscore_float >= 4 else "Focus Area"
            topic_data.append([topic, f"{tscore_float:.1f}", status])
        
        t_table = Table(topic_data, colWidths=[270, 135, 135])
        t_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t_table)
        story.append(Spacer(1, 12))

    # Detailed Questions & Feedback
    story.append(Paragraph("Question Analysis & Detailed Feedback", section_style))
    evaluations = report.get("evaluations", [])

    for idx, question in enumerate(questions):
        eval_data = evaluations[idx] if idx < len(evaluations) else {}
        cand_answer = answers.get(idx, "No answer submitted.")
        score = eval_data.get("score", 0)
        feedback = eval_data.get("feedback", "No feedback recorded.")
        strengths = eval_data.get("strengths", [])
        missing = eval_data.get("missing_concepts", [])

        q_topic = question.get("topic", "General")
        q_diff = question.get("difficulty", "Medium")

        q_box_data = [
            [
                Paragraph(f"<b>Q{idx + 1}: {question.get('question', '')}</b>", bold_label),
                Paragraph(f"<b>Score: {score}/10</b> ({q_topic} · {q_diff})", ParagraphStyle('ScoreR', alignment=2, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#4338ca')))
            ],
            [
                Paragraph(f"<b>Candidate Answer:</b> {cand_answer[:450]}{'...' if len(cand_answer) > 450 else ''}", quote_style),
                ""
            ],
            [
                Paragraph(f"<b>AI Evaluator Feedback:</b> {feedback}", body_style),
                ""
            ]
        ]
        if strengths or missing:
            str_text = "<b>Strengths:</b> " + (", ".join(strengths[:3]) if strengths else "None noted")
            mis_text = "<b>Missing Concepts:</b> " + (", ".join(missing[:3]) if missing else "None noted")
            q_box_data.append([Paragraph(f"{str_text} | {mis_text}", body_style), ""])

        q_table = Table(q_box_data, colWidths=[420, 120])
        q_table.setStyle(TableStyle([
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (0, 3), (1, 3)) if len(q_box_data) > 3 else ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(q_table)
        story.append(Spacer(1, 8))

    doc.build(story)
    return buffer.getvalue()

