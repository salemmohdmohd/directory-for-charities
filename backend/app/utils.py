from flask import jsonify

class APIException(Exception):
    """Custom API Exception for handling errors"""
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def generate_sitemap(app):
    endpoints = {
        "API Documentation": {
            "Health Check": "/health",
            "Admin Dashboard": "/admin/"
        },
        "Authentication": {
            "Login": "/auth/login",
            "Signup": "/auth/signup",
            "Google OAuth Login": "/auth/google/login",
            "Google OAuth Callback": "/auth/google/callback",
            "Link Google Account": "/auth/google/link",
            "Unlink Google Account": "/auth/google/unlink"
        },
        "Users": {
            "Profile": "/users/profile",
            "All Users": "/users/",
            "User by ID": "/users/<id>"
        },
        "Organizations": {
            "All Organizations": "/orgs/",
            "Organization by ID": "/orgs/<id>"
        },
        "Admin API": {
            "All Admin Users": "/api/admin/",
            "Admin User by ID": "/api/admin/<id>"
        }
    }

    html = """
    <div style='font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;'>
        <h1 style='text-align: center; color: #333;'>Directory for Charities API</h1>
        <p style='text-align: center; color: #666;'>Available API Endpoints</p>
    """

    for category, routes in endpoints.items():
        html += f"<h3 style='color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 5px;'>{category}</h3><ul style='list-style: none; padding: 0;'>"
        for name, url in routes.items():
            html += f"<li style='margin: 5px 0;'><a href='{url}' style='color: #3498db; text-decoration: none;'><strong>{name}</strong></a> <span style='color: #7f8c8d;'>→ {url}</span></li>"
        html += "</ul>"

    html += "</div>"
    return html
