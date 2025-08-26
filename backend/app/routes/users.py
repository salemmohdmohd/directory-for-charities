from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..__init__ import get_all_users, create_user, get_user, update_user, delete_user


users_bp = Blueprint('users', __name__, url_prefix="/user")

# GET  user's profile
@users_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    return jsonify(get_user(current_user_id)),200

# UPDATE logged-in user's profile
@users_bp.route("/update", methods=["PUT"])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    return jsonify(update_user(current_user_id, data)),200

# GET all users
@users_bp.route('/', methods=['GET'])
def get_users():
    return jsonify(get_all_users()),200

#delete user
@users_bp.route('/<int:id>', methods=['DELETE'])
def remove_user(id):
    return jsonify(delete_user(id)),200