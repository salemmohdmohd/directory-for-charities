from flask import Blueprint, request, jsonify
from ..models.user import User
from ..db import db
from flask_jwt_extended import jwt_required, get_jwt_identity
users_bp = Blueprint('users', __name__, url_prefix="/user")

# Add user routes here
#need logged in user's profile
@users_bp.route("/profile", methods=["GET"])

@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user =User.query.get(current_user_id)
    if not user :
        return jsonify({"error":"User not found"}),404
    return jsonify(user.serialize()),200

#update profile 
@users_bp.route("/update", methods=["PUT"])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user :
        return jsonify({"error":"user not found"}), 404

    data = request.get_json()
    user.email = data.get("email", user.email)
    user.password = data.get("password", user.password)

    db.session.commit()
    return jsonify({"msg": "Profile updated successfully", "User":user.serialize()})

@users_bp.route("/all", methods=["GET"])
@jwt_required()
def get_all_users():
    users= User.query.all()
    return jsonify([user.serialize() for user in users]),200