from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from extensions import db
from models.resume import Resume


resume_bp = Blueprint(
    "resume",
    __name__,
    url_prefix="/resume"
)


# ----------------------------
# Resume List
# ----------------------------
@resume_bp.route("/")
@login_required
def index():

    resumes = Resume.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "resume/index.html",
        resumes=resumes
    )


# ----------------------------
# Create Resume
# ----------------------------
@resume_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():

    if request.method == "POST":

        resume = Resume(

            user_id=current_user.id,

            title=request.form["title"],

            full_name=request.form["full_name"],

            email=request.form["email"],

            phone=request.form["phone"],

            summary=request.form["summary"],

            skills=request.form["skills"],

            experience=request.form["experience"],

            education=request.form["education"]

        )

        db.session.add(resume)
        db.session.commit()

        flash(
            "Resume created successfully!",
            "success"
        )

        return redirect(
            url_for("resume.index")
        )

    return render_template(
        "resume/create.html"
    )


# ----------------------------
# Resume Preview
# ----------------------------
@resume_bp.route("/<int:resume_id>")
@login_required
def preview(resume_id):

    resume = Resume.query.filter_by(
        id=resume_id,
        user_id=current_user.id
    ).first_or_404()

    return render_template(
        "resume/preview.html",
        resume=resume
    )


# ----------------------------
# Edit Resume
# ----------------------------
@resume_bp.route("/edit/<int:resume_id>", methods=["GET", "POST"])
@login_required
def edit(resume_id):

    resume = Resume.query.filter_by(
        id=resume_id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        resume.title = request.form["title"]
        resume.full_name = request.form["full_name"]
        resume.email = request.form["email"]
        resume.phone = request.form["phone"]
        resume.summary = request.form["summary"]
        resume.skills = request.form["skills"]
        resume.experience = request.form["experience"]
        resume.education = request.form["education"]

        db.session.commit()

        flash(
            "Resume updated successfully!",
            "success"
        )

        return redirect(
            url_for(
                "resume.preview",
                resume_id=resume.id
            )
        )

    return render_template(
        "resume/edit.html",
        resume=resume
    )


# ----------------------------
# Delete Resume
# ----------------------------
@resume_bp.route("/delete/<int:resume_id>", methods=["POST"])
@login_required
def delete(resume_id):

    resume = Resume.query.filter_by(
        id=resume_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(resume)
    db.session.commit()

    flash(
        "Resume deleted successfully!",
        "success"
    )

    return redirect(
        url_for("resume.index")
    )