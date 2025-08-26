from flask import Blueprint, request, jsonify
from ..models import User
from ..db import db

admin_api_bp = Blueprint('admin_api', __name__, url_prefix='/api/admin')

# Add admin routes here
# Test with:
# curl -X GET http://127.0.0.1:5000/api/admin/
@admin_api_bp.route('/', methods=['GET'])
def get_admins():
    users = User.query.filter_by(role='admin').all()
    return jsonify([{'id': u.user_id, 'name': u.name, 'email': u.email} for u in users]), 200

# Test with:
# curl -X GET http://127.0.0.1:5000/api/admin/1
@admin_api_bp.route('/<int:id>', methods=['GET'])
def get_admin(id):
    user = User.query.get(id)
    if user and user.role == 'admin':
        return jsonify({'id': user.user_id, 'name': user.name, 'email': user.email}), 200
    return jsonify({'error': 'Admin not found'}), 404

# Test with:
# curl -X POST http://127.0.0.1:5000/api/admin/ \
#   -H "Content-Type: application/json" \
#   -d '{"name": "Admin User", "email": "admin@example.com"}'
@admin_api_bp.route('/', methods=['POST'])
def create_admin():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], role='admin')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'Admin created', 'id': new_user.user_id}), 201

# Test with:
# curl -X PUT http://127.0.0.1:5000/api/admin/1 \
#   -H "Content-Type: application/json" \
#   -d '{"name": "Updated Admin", "email": "updated@example.com"}'
@admin_api_bp.route('/<int:id>', methods=['PUT'])
def update_admin(id):
    user = User.query.get(id)
    if user and user.role == 'admin':
        data = request.get_json()
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        db.session.commit()
        return jsonify({'msg': 'Admin updated'}), 200
    return jsonify({'error': 'Admin not found'}), 404

# Test with:
# curl -X DELETE http://127.0.0.1:5000/api/admin/1
@admin_api_bp.route('/<int:id>', methods=['DELETE'])
def delete_admin(id):
    user = User.query.get(id)
    if user and user.role == 'admin':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'msg': 'Admin deleted'}), 200
    return jsonify({'error': 'Admin not found'}), 404