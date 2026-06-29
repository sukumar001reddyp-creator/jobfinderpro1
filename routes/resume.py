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