from flask import Blueprint , request , jsonify

orgs_bp = Blueprint('orgs', __name__)

# Add organization routes here
#get all the organizations
@orgs_bp.route('/',methods=['GET'])
def get_organizations():
    return jsonify(get_all_org()),200

#gets organization based on the id
@orgs_bp.route('/<int:id>', methods=['GET'])
def get_organization(id):
    return jsonify(get_org_by_id(id)),200

#adds a new organization
@orgs_bp.route('/',methods=['POST'])
def add_organization():
    data = request.get_json()
    return jsonify(create_org(data)),201

#updates organization info
@orgs_bp.route('/<int:id>', methods=['PUT'])
def edit_organization(id):
    data = request.get_json()
    return jsonify(update_org(data)),200

#Deletes organization
@orgs_bp.route('/<int:id>', methods=['DELETE'])
def remove_orgnization(id):
    return jsonify(delete_organization(id)),200