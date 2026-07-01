from models.user import User
from extensions import db


def register_user(form):
    try:
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            return False, "Email already registered!"

        existing_phone = User.query.filter_by(phone=form.phone.data).first()
        if existing_phone:
            return False, "Phone number already registered!"

        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data
        )

        # Hash password
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        return True, "Registration successful! Please login."

    except Exception as e:
        db.session.rollback()
        return False, f"Registration failed: {e}"


def authenticate_user(email, password):
    try:
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            return user

        return None

    except Exception:
        return None