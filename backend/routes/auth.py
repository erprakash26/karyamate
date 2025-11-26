from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from backend.extensions import db
from backend.models import User
from backend.utils import sanitize_string

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    """
    Register a new user
    ---
    tags:
      - Auth
    description: Create a new user account by providing email and password.
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: User registration details
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: user@example.com
            password:
              type: string
              example: StrongPassword123
    responses:
      201:
        description: User successfully created
        schema:
          type: object
          properties:
            id:
              type: integer
            email:
              type: string
      400:
        description: Missing email or password
      409:
        description: Email already registered
    """
    data = request.get_json(silent=True) or {}
    email = sanitize_string(data.get("email"))
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "email already registered"}), 409

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id, "email": user.email}), 201


@auth_bp.post("/login")
def login():
    """
    Login and get JWT token
    ---
    tags:
      - Auth
    description: Authenticate user and return a JWT token.
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: User login credentials
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: user@example.com
            password:
              type: string
              example: StrongPassword123
    responses:
      200:
        description: Login successful, returns JWT token
        schema:
          type: object
          properties:
            access_token:
              type: string
            token_type:
              type: string
              example: Bearer
      400:
        description: Missing email or password
      401:
        description: Invalid login credentials
    """
    data = request.get_json(silent=True) or {}
    email = sanitize_string(data.get("email"))
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "invalid credentials"}), 401

    # Fix: JWT identity must be a string
    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token, "token_type": "Bearer"}), 200
