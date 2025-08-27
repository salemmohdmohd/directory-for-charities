"""
OAuth authentication routes - Google OAuth integration
"""

from flask import Blueprint, request, jsonify, redirect, url_for, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.auth_service import GoogleOAuthService, AuthService
from ..models.user import User
from ..db import db

oauth_bp = Blueprint('oauth', __name__, url_prefix='/auth')

@oauth_bp.route('/google/login', methods=['GET'])
def google_login():
    """
    Initiate Google OAuth login
    Returns the Google OAuth authorization URL
    """
    try:
        # Generate OAuth URL
        redirect_uri = request.url_root.rstrip('/') + '/auth/google/callback'
        auth_url = GoogleOAuthService.get_google_auth_url(redirect_uri)

        if not auth_url:
            return jsonify({
                'success': False,
                'message': 'Failed to generate Google OAuth URL'
            }), 500

        return jsonify({
            'success': True,
            'auth_url': auth_url,
            'message': 'Redirect to this URL for Google OAuth'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'OAuth initialization failed: {str(e)}'
        }), 500

@oauth_bp.route('/google/callback', methods=['GET'])
def google_callback():
    """
    Handle Google OAuth callback
    Processes the authorization code and creates/logs in user
    """
    try:
        # Get authorization code from callback
        code = request.args.get('code')
        error = request.args.get('error')

        if error:
            return jsonify({
                'success': False,
                'message': f'Google OAuth error: {error}'
            }), 400

        if not code:
            return jsonify({
                'success': False,
                'message': 'Authorization code not received'
            }), 400

        # Handle the OAuth callback
        redirect_uri = request.url_root.rstrip('/') + '/auth/google/callback'
        user, is_new_user, tokens, error_message = GoogleOAuthService.handle_google_callback(
            code, redirect_uri
        )

        if error_message:
            return jsonify({
                'success': False,
                'message': error_message
            }), 400

        if not user:
            return jsonify({
                'success': False,
                'message': 'Failed to authenticate with Google'
            }), 401

        # Return success response with tokens
        response_data = {
            'success': True,
            'message': 'Successfully authenticated with Google',
            'is_new_user': is_new_user,
            'user': {
                'id': user.user_id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'profile_picture': user.profile_picture,
                'is_verified': user.is_verified
            },
            'tokens': tokens
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'OAuth callback failed: {str(e)}'
        }), 500

@oauth_bp.route('/google/link', methods=['POST'])
@jwt_required()
def link_google_account():
    """
    Link Google account to existing logged-in user
    Requires existing JWT authentication
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404

        # Get authorization code from request
        data = request.get_json()
        code = data.get('code')

        if not code:
            return jsonify({
                'success': False,
                'message': 'Authorization code required'
            }), 400

        # Exchange code for token and get user info
        redirect_uri = request.url_root.rstrip('/') + '/auth/google/callback'
        token_response = GoogleOAuthService.exchange_code_for_token(code, redirect_uri)

        if not token_response or 'access_token' not in token_response:
            return jsonify({
                'success': False,
                'message': 'Failed to get Google access token'
            }), 400

        user_info = GoogleOAuthService.get_google_user_info(token_response['access_token'])
        if not user_info:
            return jsonify({
                'success': False,
                'message': 'Failed to get Google user info'
            }), 400

        google_id = user_info.get('sub')
        google_email = user_info.get('email')

        # Check if Google account is already linked to another user
        existing_google_user = User.query.filter_by(google_id=google_id).first()
        if existing_google_user and existing_google_user.user_id != user.user_id:
            return jsonify({
                'success': False,
                'message': 'This Google account is already linked to another user'
            }), 400

        # Link Google account
        user.google_id = google_id
        user.profile_picture = user_info.get('picture', user.profile_picture)

        # If emails match and Google email is verified, verify the user
        if google_email == user.email and user_info.get('email_verified'):
            user.is_verified = True

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Google account linked successfully',
            'user': {
                'id': user.user_id,
                'name': user.name,
                'email': user.email,
                'profile_picture': user.profile_picture,
                'is_verified': user.is_verified
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to link Google account: {str(e)}'
        }), 500

@oauth_bp.route('/google/unlink', methods=['POST'])
@jwt_required()
def unlink_google_account():
    """
    Unlink Google account from current user
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404

        if not user.google_id:
            return jsonify({
                'success': False,
                'message': 'No Google account linked'
            }), 400

        # Make sure user has a password before unlinking Google
        if not user.password_hash:
            return jsonify({
                'success': False,
                'message': 'Cannot unlink Google account. Please set a password first.'
            }), 400

        # Unlink Google account
        user.google_id = None
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Google account unlinked successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to unlink Google account: {str(e)}'
        }), 500

# Testing commands:
"""
# 1. Get Google OAuth URL:
curl -X GET http://localhost:5000/auth/google/login

# 2. Test linking Google account (requires JWT token):
curl -X POST http://localhost:5000/auth/google/link \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"code": "google_auth_code_from_callback"}'

# 3. Test unlinking Google account:
curl -X POST http://localhost:5000/auth/google/unlink \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
"""
