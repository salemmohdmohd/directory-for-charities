from flask import Blueprint, request, jsonify
from app.models.organization import Organization
from app.db import db

orgs_bp = Blueprint('orgs', __name__, url_prefix='/orgs')

# Organization routes
# Test with:
# curl -X GET http://127.0.0.1:5000/orgs/
@orgs_bp.route('/', methods=['GET'])
def get_organizations():
    """Get all organizations"""
    try:
        organizations = Organization.query.all()
        orgs_data = []
        for org in organizations:
            org_dict = {
                'org_id': org.org_id,
                'name': org.name,
                'mission': org.mission,
                'description': org.description,
                'category_id': org.category_id,
                'location_id': org.location_id,
                'address': org.address,
                'phone': org.phone,
                'email': org.email,
                'website': org.website,
                'donation_link': org.donation_link,
                'logo_url': org.logo_url,
                'operating_hours': org.operating_hours,
                'established_year': org.established_year,
                'status': org.status,
                'verification_level': org.verification_level,
                'admin_user_id': org.admin_user_id,
                'view_count': org.view_count,
                'bookmark_count': org.bookmark_count
            }
            orgs_data.append(org_dict)
        return jsonify(orgs_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Test with:
# curl -X GET http://127.0.0.1:5000/orgs/1
@orgs_bp.route('/<int:id>', methods=['GET'])
def get_organization(id):
    """Get organization by ID"""
    try:
        organization = Organization.query.get(id)
        if not organization:
            return jsonify({"error": "Organization not found"}), 404

        org_dict = {
            'org_id': organization.org_id,
            'name': organization.name,
            'mission': organization.mission,
            'description': organization.description,
            'category_id': organization.category_id,
            'location_id': organization.location_id,
            'address': organization.address,
            'phone': organization.phone,
            'email': organization.email,
            'website': organization.website,
            'donation_link': organization.donation_link,
            'logo_url': organization.logo_url,
            'operating_hours': organization.operating_hours,
            'established_year': organization.established_year,
            'status': organization.status,
            'verification_level': organization.verification_level,
            'admin_user_id': organization.admin_user_id,
            'view_count': organization.view_count,
            'bookmark_count': organization.bookmark_count
        }
        return jsonify(org_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Test with:
# curl -X POST http://127.0.0.1:5000/orgs/ \
#   -H "Content-Type: application/json" \
#   -d '{"name": "Test Charity", "mission": "Help people", "description": "A test organization", "email": "test@charity.com"}'
@orgs_bp.route('/', methods=['POST'])
def add_organization():
    """Create a new organization"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Create new organization
        new_org = Organization(
            name=data.get('name'),
            mission=data.get('mission'),
            description=data.get('description'),
            category_id=data.get('category_id'),
            location_id=data.get('location_id'),
            address=data.get('address'),
            phone=data.get('phone'),
            email=data.get('email'),
            website=data.get('website'),
            donation_link=data.get('donation_link'),
            logo_url=data.get('logo_url'),
            operating_hours=data.get('operating_hours'),
            established_year=data.get('established_year'),
            admin_user_id=data.get('admin_user_id')
        )

        db.session.add(new_org)
        db.session.commit()

        return jsonify({"msg": "Organization created successfully", "org_id": new_org.org_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Test with:
# curl -X PUT http://127.0.0.1:5000/orgs/1 \
#   -H "Content-Type: application/json" \
#   -d '{"name": "Updated Charity Name", "mission": "Updated mission"}'
@orgs_bp.route('/<int:id>', methods=['PUT'])
def edit_organization(id):
    """Update organization information"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        organization = Organization.query.get(id)
        if not organization:
            return jsonify({"error": "Organization not found"}), 404

        # Update organization fields
        if 'name' in data:
            organization.name = data['name']
        if 'mission' in data:
            organization.mission = data['mission']
        if 'description' in data:
            organization.description = data['description']
        if 'category_id' in data:
            organization.category_id = data['category_id']
        if 'location_id' in data:
            organization.location_id = data['location_id']
        if 'address' in data:
            organization.address = data['address']
        if 'phone' in data:
            organization.phone = data['phone']
        if 'email' in data:
            organization.email = data['email']
        if 'website' in data:
            organization.website = data['website']
        if 'donation_link' in data:
            organization.donation_link = data['donation_link']
        if 'logo_url' in data:
            organization.logo_url = data['logo_url']
        if 'operating_hours' in data:
            organization.operating_hours = data['operating_hours']
        if 'established_year' in data:
            organization.established_year = data['established_year']
        if 'status' in data:
            organization.status = data['status']
        if 'verification_level' in data:
            organization.verification_level = data['verification_level']

        db.session.commit()
        return jsonify({"msg": "Organization updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Test with:
# curl -X DELETE http://127.0.0.1:5000/orgs/1
@orgs_bp.route('/<int:id>', methods=['DELETE'])
def remove_organization(id):
    """Delete organization"""
    try:
        organization = Organization.query.get(id)
        if not organization:
            return jsonify({"error": "Organization not found"}), 404

        db.session.delete(organization)
        db.session.commit()
        return jsonify({"msg": "Organization deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500