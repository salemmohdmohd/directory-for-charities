from flask import Blueprint,request, jsonify

admin_bp = Blueprint('admin', __name__,url_prefix='/admins')

# Add admin routes here
#to get all the admins 
@admin_bp.route('/',methods=['GET'])
def get_admins():
    return jsonify(get_all_admins),200

#to get one admin by the id 
@admin_bp.route('/<int:id>', methods['GET'])
def get_admin(id):
    return jsonify(get_admin_by_id),200

#to add new admin 
@admin_bp.route('/',methods['POST'])
def add_admin():
    data= request.get_json()
    return jsonify(create_admin(data)),201
#update admin info 
@admin_bp.route('/<int:id>', methods['PUT'])
def edit_admin(id):
    data = request.get_json()
    return jsonify(update_admin(id,data)),200
#to remove admin 
@admin_bp.route('/<int:id>',methods('DELETE'))
def remove_admin(id):
    return jsonify(delete_admin(id)),200