from flask import Blueprint, jsonify , request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.db import db

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

# Add auth routes here
@auth_bp.route("/signup", methods=["POST"])
def signup():
    username= request.json.get("username")
    email = request.json.get("email")
    password= request.json.get("password")

    if username is None or email is None or password is None:
        return jsonify({"msg": "All fields are required"}),400
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}),400
    
    hashed_password = generate_password_hash(password)
    new_user = User(name=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201
@auth_bp.route("/login", methods=["POST"])
def login():
    #we get the password&username from request
   
    username= request.json.get("username", None)
    password = request.json.get("password", None)

       #Get user from DB  
    if not username :
        return jsonify({"error": "Email and password is required"}), 400
    
    #Get user from DB
    user = User.query.filter_by(username=username).first()

    if user is None:
        #the user is not found
        return jsonify({"msg": "Invalid Credentials"}),401
    #check password
    if not check_password_hash(user.password_hash, password):
        return jsonify({"msg": "Invalid Credentials"}),401
    
    #create a new token with the user id inside
    access_token = create_access_token(identity = user.user_id)
    return jsonify({"token": access_token,"user_id": user.id}),200