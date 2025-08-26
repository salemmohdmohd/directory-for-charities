from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.db import db

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

# Authentication routes
@auth_bp.route("/signup", methods=["GET"])
def signup_info():
    """Get signup endpoint information"""
    return jsonify({
        "endpoint": "/auth/signup",
        "method": "POST",
        "description": "Create a new user account",
        "required_fields": ["name", "email", "password"],
        "example": {
            "name": "John Doe",
            "email": "john@example.com", 
            "password": "securepassword"
        }
    }), 200

# Test with:
# curl -X POST http://127.0.0.1:5000/auth/signup \
#   -H "Content-Type: application/json" \
#   -d '{"name": "Test User", "email": "test@example.com", "password": "password123"}'
@auth_bp.route("/signup", methods=["POST"])
def signup():
    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")

    if name is None or email is None or password is None:
        return jsonify({"msg": "All fields are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["GET"])
def login_info():
    """Get login endpoint information"""
    return jsonify({
        "endpoint": "/auth/login",
        "method": "POST",
        "description": "Authenticate user and get JWT token",
        "required_fields": ["email", "password"],
        "example": {
            "email": "john@example.com",
            "password": "securepassword"
        },
        "returns": "JWT token for authenticated requests"
    }), 200

# Test with:
# curl -X POST http://127.0.0.1:5000/auth/login \
#   -H "Content-Type: application/json" \
#   -d '{"email": "test@example.com", "password": "password123"}'
@auth_bp.route("/login", methods=["POST"])
def login():
    # Get email and password from request
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # Validate required fields
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Get user from DB by email
    user = User.query.filter_by(email=email).first()

    if user is None:
        # User not found
        return jsonify({"msg": "Invalid credentials"}), 401

    # Check password
    if not check_password_hash(user.password_hash, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    # Create access token with user ID
    access_token = create_access_token(identity=user.user_id)
    return jsonify({"token": access_token, "user_id": user.user_id}), 200
