from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.user import User
from app.utils.validators import validate_email


class UserService:
    @staticmethod
    def register(data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return {"message": "Missing fields", "status": 400}

        if not validate_email(email):
            return {"message": "Invalid email", "status": 400}

        if User.query.filter((User.username == username) | (User.email == email)).first():
            return {"message": "User already exists", "status": 400}

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully", "status": 201}

    @staticmethod
    def login(data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"message": "Missing fields", "status": 400}

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            token = create_access_token(identity=user.username)
            return {"message": "Login successful", "token": token, "status": 200}

        return {"message": "Invalid credentials", "status": 401}

    @staticmethod
    def change_password(current_user, data):
        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if not old_password or not new_password:
            return {"message": "Missing fields", "status": 400}

        user = User.query.filter_by(username=current_user).first()

        if not user or not user.check_password(old_password):
            return {"message": "Old password is incorrect", "status": 401}

        user.set_password(new_password)
        db.session.commit()

        return {"message": "Password updated successfully", "status": 200}
