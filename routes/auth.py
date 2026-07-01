from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from services.auth_service import authenticate_user, register_user
from forms.auth_forms import RegisterForm, LoginForm

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        success, message = register_user(form)

        if success:
            flash(message, "success")
            return redirect(url_for("auth.login"))

        flash(message, "danger")

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = authenticate_user(form.email.data, form.password.data)

        if user:
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("home.home"))

        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home.home"))