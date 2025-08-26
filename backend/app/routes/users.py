from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.db import db

users_bp = Blueprint('users', __name__, url_prefix="/users")

# User profile routes
# Test with (requires JWT token from login):
# curl -X GET http://127.0.0.1:5000/users/profile \
#   -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
@users_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """Get current user's profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        user_dict = {
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'is_verified': user.is_verified,
            'profile_picture': user.profile_picture,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None
        }
        return jsonify(user_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Test with (requires JWT token from login):
# curl -X PUT http://127.0.0.1:5000/users/profile \
#   -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
#   -H "Content-Type: application/json" \
#   -d '{"name": "Updated Name", "email": "newemail@example.com"}'
@users_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    """Update current user's profile"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Update user fields
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            # Check if email is already taken by another user
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.user_id != current_user_id:
                return jsonify({"error": "Email already exists"}), 400
            user.email = data['email']
        if 'profile_picture' in data:
            user.profile_picture = data['profile_picture']
        if 'password' in data:
            user.password_hash = generate_password_hash(data['password'])

        db.session.commit()
        return jsonify({"msg": "Profile updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Admin routes for user management
# Test with:
# curl -X GET http://127.0.0.1:5000/users/
@users_bp.route('/', methods=['GET'])
def get_users():
    """Get all users (admin only)"""
    try:
        users = User.query.all()
        users_data = []
        for user in users:
            user_dict = {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'is_verified': user.is_verified,
                'profile_picture': user.profile_picture,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'last_login': user.last_login.isoformat() if user.last_login else None
            }
            users_data.append(user_dict)
        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Test with:
# curl -X GET http://127.0.0.1:5000/users/1
@users_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    """Get specific user by ID"""
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        user_dict = {
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'is_verified': user.is_verified,
            'profile_picture': user.profile_picture,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None
        }
        return jsonify(user_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Test with:
# curl -X POST http://127.0.0.1:5000/users/ \
#   -H "Content-Type: application/json" \
#   -d '{"name": "New User", "email": "new@example.com", "password": "password123", "role": "visitor"}'
@users_bp.route('/', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Name, email, and password are required"}), 400

        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already exists"}), 400

        # Create new user
        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            name=data['name'],
            email=data['email'],
            password_hash=hashed_password,
            role=data.get('role', 'visitor'),
            is_verified=data.get('is_verified', False),
            profile_picture=data.get('profile_picture')
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User created successfully", "user_id": new_user.user_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Test with:
# curl -X DELETE http://127.0.0.1:5000/users/1
@users_bp.route('/<int:id>', methods=['DELETE'])
def remove_user(id):
    """Delete user by ID"""
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "User deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500