from flask import Blueprint, request
from app.schemas.user_schema import UserSchema
from app.services.user_service import register_user, login_user

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

user_schema = UserSchema()

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = user_schema.validate(data)
    if errors:
        return {"errors": errors}, 400
    return register_user(data)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return {"message": "Missing JSON body"}, 400
    return login_user(data)
