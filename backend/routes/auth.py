from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from backend.extensions import db
from backend.models import User
from backend.utils import sanitize_string



auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email = sanitize_string(data.get("email"))
    password = data.get("password")

    # Validation
    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    # Uniqueness
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "email already registered"}), 409

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id, "email": user.email}), 201

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = sanitize_string(data.get("email"))
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "invalid credentials"}), 401

    #token = create_access_token(identity=user.id) got error :"msg": "Subject must be a string"
    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token, "token_type": "Bearer"}), 200
