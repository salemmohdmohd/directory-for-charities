"""
Authentication Service - Google OAuth Integration
Handles Google OAuth authentication, JWT tokens, and user management
"""

import os
import secrets
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
import requests
from ..models.user import User
from ..db import db

class GoogleOAuthService:
    """Service for handling Google OAuth 2.0 authentication"""

    # Google OAuth configuration
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid_configuration"

    @staticmethod
    def get_google_provider_cfg():
        """Get Google's OAuth 2.0 configuration"""
        try:
            response = requests.get(GoogleOAuthService.GOOGLE_DISCOVERY_URL)
            return response.json()
        except Exception as e:
            print(f"Error getting Google config: {e}")
            return None

    @staticmethod
    def get_google_auth_url(redirect_uri):
        """Generate Google OAuth authorization URL"""
        google_provider_cfg = GoogleOAuthService.get_google_provider_cfg()
        if not google_provider_cfg:
            return None

        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # OAuth 2.0 parameters
        params = {
            'client_id': GoogleOAuthService.GOOGLE_CLIENT_ID,
            'redirect_uri': redirect_uri,
            'scope': 'openid email profile',
            'response_type': 'code',
            'access_type': 'offline',
            'prompt': 'select_account'
        }

        # Build URL
        param_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        return f"{authorization_endpoint}?{param_string}"

    @staticmethod
    def exchange_code_for_token(code, redirect_uri):
        """Exchange authorization code for access token"""
        google_provider_cfg = GoogleOAuthService.get_google_provider_cfg()
        if not google_provider_cfg:
            return None

        token_endpoint = google_provider_cfg["token_endpoint"]

        token_data = {
            'client_id': GoogleOAuthService.GOOGLE_CLIENT_ID,
            'client_secret': GoogleOAuthService.GOOGLE_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
        }

        try:
            response = requests.post(token_endpoint, data=token_data)
            return response.json()
        except Exception as e:
            print(f"Error exchanging code for token: {e}")
            return None

    @staticmethod
    def get_google_user_info(access_token):
        """Get user information from Google using access token"""
        google_provider_cfg = GoogleOAuthService.get_google_provider_cfg()
        if not google_provider_cfg:
            return None

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]

        headers = {'Authorization': f'Bearer {access_token}'}

        try:
            response = requests.get(userinfo_endpoint, headers=headers)
            return response.json()
        except Exception as e:
            print(f"Error getting user info: {e}")
            return None

    @staticmethod
    def handle_google_callback(code, redirect_uri):
        """
        Handle Google OAuth callback
        Returns tuple: (user, is_new_user, tokens, error_message)
        """
        try:
            # Exchange code for token
            token_response = GoogleOAuthService.exchange_code_for_token(code, redirect_uri)
            if not token_response or 'access_token' not in token_response:
                return None, False, None, "Failed to get access token from Google"

            # Get user info from Google
            user_info = GoogleOAuthService.get_google_user_info(token_response['access_token'])
            if not user_info:
                return None, False, None, "Failed to get user information from Google"

            # Extract user data
            google_id = user_info.get('sub')
            email = user_info.get('email')
            name = user_info.get('name')
            profile_picture = user_info.get('picture')
            email_verified = user_info.get('email_verified', False)

            if not google_id or not email:
                return None, False, None, "Incomplete user information from Google"

            # Find or create user
            user, is_new_user = GoogleOAuthService.find_or_create_user(
                google_id, email, name, profile_picture, email_verified
            )

            if not user:
                return None, False, None, "Failed to create or find user"

            # Generate JWT tokens
            tokens = AuthService.create_tokens(user)

            return user, is_new_user, tokens, None

        except Exception as e:
            return None, False, None, f"Google OAuth failed: {str(e)}"

    @staticmethod
    def find_or_create_user(google_id, email, name, profile_picture, email_verified):
        """
        Find existing user or create new one from Google OAuth data
        Returns tuple: (user, is_new_user)
        """
        try:
            # Check if user exists with this Google ID
            user = User.query.filter_by(google_id=google_id).first()

            if user:
                # Update existing user info
                user.last_login = datetime.utcnow()
                if profile_picture:
                    user.profile_picture = profile_picture
                db.session.commit()
                return user, False

            # Check if user exists with this email
            user = User.query.filter_by(email=email.lower().strip()).first()

            if user:
                # Link Google account to existing user
                user.google_id = google_id
                if profile_picture:
                    user.profile_picture = profile_picture
                if email_verified:
                    user.is_verified = True
                user.last_login = datetime.utcnow()
                user.updated_at = datetime.utcnow()
                db.session.commit()
                return user, False

            # Create new user from Google account
            new_user = User(
                name=name or email.split('@')[0],
                email=email.lower().strip(),
                google_id=google_id,
                profile_picture=profile_picture,
                is_verified=email_verified,
                role='visitor',
                created_at=datetime.utcnow()
            )

            db.session.add(new_user)
            db.session.commit()

            return new_user, True

        except Exception as e:
            db.session.rollback()
            print(f"Error in find_or_create_user: {e}")
            return None, False

class AuthService:
    """Core authentication service for regular login/signup and JWT management"""

    @staticmethod
    def hash_password(password):
        """Hash a password for storing in database"""
        return generate_password_hash(password)

    @staticmethod
    def verify_password(password, password_hash):
        """Verify a password against its hash"""
        return check_password_hash(password_hash, password)

    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user with email and password"""
        user = User.query.filter_by(email=email.lower().strip()).first()

        if user and user.password_hash and AuthService.verify_password(password, user.password_hash):
            user.last_login = datetime.utcnow()
            db.session.commit()
            return user
        return None

    @staticmethod
    def create_tokens(user):
        """Create JWT access and refresh tokens for a user"""
        access_token = create_access_token(
            identity=user.user_id,
            expires_delta=timedelta(hours=24)  # 24 hour access token
        )

        return {
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': 86400,  # 24 hours in seconds
            'user_id': user.user_id,
            'user_name': user.name,
            'user_email': user.email,
            'user_role': user.role
        }

    @staticmethod
    def register_user(name, email, password, role='visitor'):
        """Register a new user"""
        try:
            # Validate input
            if not name or not email or not password:
                return None, False, "All fields are required"

            # Check if email already exists
            existing_user = User.query.filter_by(email=email.lower().strip()).first()
            if existing_user:
                return None, False, "Email already registered"

            # Create new user
            hashed_password = AuthService.hash_password(password)
            new_user = User(
                name=name.strip(),
                email=email.lower().strip(),
                password_hash=hashed_password,
                role=role,
                is_verified=False,
                created_at=datetime.utcnow()
            )

            db.session.add(new_user)
            db.session.commit()

            return new_user, True, None

        except Exception as e:
            db.session.rollback()
            return None, False, f"Registration failed: {str(e)}"

# Test with:
# 1. Set environment variables:
#    export GOOGLE_CLIENT_ID="your_google_client_id"
#    export GOOGLE_CLIENT_SECRET="your_google_client_secret"
#
# 2. Get Google OAuth URL:
#    auth_url = GoogleOAuthService.get_google_auth_url("http://localhost:5000/auth/google/callback")
#
# 3. Handle callback:
#    user, is_new, tokens, error = GoogleOAuthService.handle_google_callback(code, redirect_uri)
