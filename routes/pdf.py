from io import BytesIO

from flask import (
    Blueprint,
    send_file
)

from flask_login import (
    login_required,
    current_user
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

from models.resume import Resume


pdf_bp = Blueprint(
    "pdf",
    __name__,
    url_prefix="/pdf"
)


@pdf_bp.route("/resume/<int:resume_id>")
@login_required
def download_resume(resume_id):

    resume = Resume.query.filter_by(
        id=resume_id,
        user_id=current_user.id
    ).first_or_404()

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            f"<b>{resume.full_name}</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            resume.email,
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            resume.phone or "",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph("<br/><b>Professional Summary</b>",
        styles["Heading2"])
    )

    story.append(
        Paragraph(
            resume.summary or "",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph("<br/><b>Skills</b>",
        styles["Heading2"])
    )

    story.append(
        Paragraph(
            resume.skills or "",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph("<br/><b>Experience</b>",
        styles["Heading2"])
    )

    story.append(
        Paragraph(
            resume.experience or "",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph("<br/><b>Education</b>",
        styles["Heading2"])
    )

    story.append(
        Paragraph(
            resume.education or "",
            styles["BodyText"]
        )
    )

    doc.build(story)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="resume.pdf",
        mimetype="application/pdf"
    )
    