from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.user import User


def register_user(data):
    username = data["username"]
    email = data["email"]
    password = data["password"]

    # Kiểm tra xem email hoặc username đã tồn tại chưa
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return {"message": "Username or email already exists"}, 400

    # Tạo người dùng mới
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return {"message": "User registered successfully"}, 201


def login_user(data):
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    # Kiểm tra thông tin người dùng và mật khẩu
    if not user or not user.check_password(password):
        return {"message": "Invalid email or password"}, 401

    # Tạo JWT token
    token = create_access_token(identity=user.id)
    return {"access_token": token}, 200
