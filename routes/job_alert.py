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
from models.job_alert import JobAlert


job_alert_bp = Blueprint(
    "job_alert",
    __name__,
    url_prefix="/job-alerts"
)


@job_alert_bp.route("/")
@login_required
def index():

    alerts = JobAlert.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "job_alert/index.html",
        alerts=alerts
    )


@job_alert_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():

    if request.method == "POST":

        alert = JobAlert(

            user_id=current_user.id,

            keyword=request.form["keyword"],

            location=request.form["location"],

            employment_type=request.form["employment_type"],

            remote=True if request.form.get("remote") else False,

            frequency=request.form["frequency"]

        )

        db.session.add(alert)
        db.session.commit()

        flash(
            "Job Alert created successfully!",
            "success"
        )

        return redirect(
            url_for("job_alert.index")
        )

    return render_template(
        "job_alert/create.html"
    )


@job_alert_bp.route("/delete/<int:alert_id>", methods=["POST"])
@login_required
def delete(alert_id):

    alert = JobAlert.query.filter_by(
        id=alert_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(alert)
    db.session.commit()

    flash(
        "Job Alert deleted successfully!",
        "success"
    )

    return redirect(
        url_for("job_alert.index")
    )