import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .utils import APIException, generate_sitemap
from .admin import setup_admin
from .db import db
from dotenv import load_dotenv

jwt = JWTManager()
migrate = Migrate()

def create_app():
	#loads environment variables fron .env
	load_dotenv()

	app = Flask(__name__)
	app.url_map.strict_slashes = False

	#Configs Database
	db_url = os.getenv("DATABASE_URL")
	if db_url:
		app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
	else:
		app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///example.db"
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	#JWT SECRET FROM .env, should change it 
	app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")

	#initializes the extensions
	MIGRATE = Migrate(app, db)
	db.init_app(app)
	jwt.init_app(app)
	CORS(app)
	setup_admin(app) 

	#Register routes
	# from .routes import api
	# app.register_blueprint(api, url_prefix="/api")

	#error handler
	@app.errorhandler(APIException)
	def handle_invalid_usage(error):
		return jsonify(error.to_dict()), error.status_code

	return app