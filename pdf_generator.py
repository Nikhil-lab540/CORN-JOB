"""
pdf_generator.py
----------------
Generates downloadable PDF reports using ReportLab.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime


def create_pdf_report(student_reports: dict) -> BytesIO:
    """
    Generate a PDF from student reports.

    Args:
        student_reports: Dict of {username: report_text}

    Returns:
        BytesIO buffer containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=HexColor('#2E86AB'),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#666666'),
        alignment=TA_CENTER,
        spaceAfter=30
    )

    student_header_style = ParagraphStyle(
        'StudentHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#E94F37'),
        spaceBefore=20,
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        spaceAfter=12
    )

    # Build document content
    story = []

    # Title
    story.append(Paragraph("SmartLearners.ai", title_style))
    story.append(Paragraph("Weekly Performance Report", styles['Heading2']))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        subtitle_style
    ))

    # Horizontal line
    story.append(HRFlowable(
        width="100%",
        thickness=2,
        color=HexColor('#2E86AB'),
        spaceAfter=20
    ))

    # Student reports
    for username, report_text in student_reports.items():
        # Student header
        story.append(Paragraph(f"Student: {username}", student_header_style))

        # Process report text - handle line breaks and special characters
        # Replace problematic characters and format paragraphs
        cleaned_report = report_text.replace('&', '&amp;')
        cleaned_report = cleaned_report.replace('<', '&lt;').replace('>', '&gt;')

        # Split by double newlines for paragraphs
        paragraphs = cleaned_report.split('\n\n')
        for para in paragraphs:
            # Replace single newlines with <br/> for line breaks within paragraphs
            para = para.strip().replace('\n', '<br/>')
            if para:
                story.append(Paragraph(para, body_style))

        # Separator between students
        story.append(Spacer(1, 20))
        story.append(HRFlowable(
            width="80%",
            thickness=1,
            color=HexColor('#CCCCCC'),
            spaceAfter=10
        ))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def save_pdf_to_file(student_reports: dict, filename: str = None) -> str:
    """
    Save PDF report to a file.

    Args:
        student_reports: Dict of {username: report_text}
        filename: Optional filename, auto-generated if not provided

    Returns:
        Filename of saved PDF
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"weekly_reports_{timestamp}.pdf"

    buffer = create_pdf_report(student_reports)

    with open(filename, 'wb') as f:
        f.write(buffer.read())

    return filename


# Test function
if __name__ == "__main__":
    sample_reports = {
        "student123": """Weekly Performance Summary

Overall Score: 78%
Correct Answers: 12/15
Partially Correct: 2/15
Unattempted: 1/15

Strengths:
- Excellent understanding of Quadratic Equations
- Strong problem-solving in Coordinate Geometry

Areas for Improvement:
- Practice more Trigonometry problems
- Review Probability concepts

Keep up the great work! You're making steady progress.""",

        "student456": """Weekly Performance Summary

Overall Score: 85%
Correct Answers: 14/15
Partially Correct: 1/15

Outstanding performance this week!

Strengths:
- Perfect scores in Calculus
- Great improvement in Statistics

Parent Note: Your child shows excellent dedication to studies."""
    }

    filename = save_pdf_to_file(sample_reports)
    print(f"PDF saved to: {filename}")
