import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from .utils import APIException, generate_sitemap
from .admin import setup_admin
from .db import db

# Import route blueprints
from .routes.auth import auth_bp
from .routes.users import users_bp
from .routes.orgs import orgs_bp
from .routes.admin import admin_api_bp

app = Flask(__name__)
app.url_map.strict_slashes = False

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')

db_url = os.getenv("DATABASE_URL")
if db_url:
	app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
	app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../instance/example.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Initialize JWT (if available)
jwt = None
try:
	from flask_jwt_extended import JWTManager
	jwt = JWTManager(app)
except ImportError:
	print("Warning: flask-jwt-extended not installed. JWT features will not be available.")
	pass

setup_admin(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(orgs_bp)
app.register_blueprint(admin_api_bp)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
	return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
	return generate_sitemap(app)

@app.route('/health')
def health_check():
	"""Basic health check endpoint"""
	return jsonify({"status": "healthy", "message": "API is running"}), 200

if __name__ == '__main__':
	PORT = int(os.environ.get('PORT', 3000))
	app.run(host='0.0.0.0', port=PORT, debug=False)
