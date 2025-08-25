import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from .utils import APIException, generate_sitemap
from .admin import setup_admin
from .db import db
from .models import User

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url:
	app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
	app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../instance/example.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
	return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
	return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
	response_body = {
		"msg": "Hello, this is your GET /user response"
	}
	return jsonify(response_body), 200

#Elysa's code begins here: Please do not delete my comments. I need them for better understanding. Thx!
#Create - adding a new user
@app.route('/user', methods=['POST'])
def create_user():
	data = request.get_json() # gets the JSON data from the request
	new_user = User(name=data['name'], email=data['email']) # creates a new User instance or object
	db.session.add(new_user) # add the new user to the database
	db.session.commit() # makes the transaction commit
	return jsonify({"msg": "User created", "user": new_user.serialize()}), 201 #Returns a message of success

#Read - getting all users
@app.route('/user', methods=['GET'])
def get_all_users():
	users = User.query.all() #Searching the database for all users
	return jsonify([user.serialize() for user in users]), 200 #makes users into a dictionary and return them with an ok status

#also read - getting a single user with their ID
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
	user = User.query.get_or_404(user_id) # finding a usert byt their id or sending 404 error if not found
	return jsonify(user.serialize()), 200 #returning the identified used with an okay status

#Update - user modification
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
	user = User.query.get_or_404(user_id) #finding an exisitng user
	data = request.get_json() #getting updated data
	user.name = data.get('name', user.name) #updating user name
	user.email = data.get('email', user.email) #Updating user email
	db.session.commit() #saving changes
	return jsonify({"msg": "User updated", "user": user.serialize()}), 200 #if successful returning okay

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)  #finding the user to delete
    db.session.delete(user)   #marking the user for deletion             
    db.session.commit()        #removing the user from the database            
    return jsonify({"msg": "User deleted"}), 200  #deletion confirmation
#Elysa's code ends here

if __name__ == '__main__':
	PORT = int(os.environ.get('PORT', 3000))
	app.run(host='0.0.0.0', port=PORT, debug=False)
