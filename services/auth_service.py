from models.user import User
from extensions import db


def register_user(form):

    # Check email already exists
    existing_user = User.query.filter_by(
        email=form.email.data
    ).first()

    if existing_user:
        return False, "Email already exists."

    user = User(
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        email=form.email.data,
        phone=form.phone.data
    )

    user.set_password(form.password.data)

    db.session.add(user)
    db.session.commit()

    return True, "Account created successfully."
    from models.user import User


def authenticate_user(email, password):

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        return user

    return None