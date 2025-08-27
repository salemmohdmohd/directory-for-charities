import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

    # Email Configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = int(os.getenv('SMTP_PORT')) if os.getenv('SMTP_PORT') else None
    SMTP_USERNAME = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    FROM_EMAIL = os.getenv('FROM_EMAIL')

    # Frontend URL
    FRONTEND_URL = os.getenv('FRONTEND_URL')

    # TODO: Add Redis configuration for caching
    # TODO: Add AWS S3 configuration for file uploads
    # TODO: Add social media API keys (Facebook, Twitter, Instagram)
    # TODO: Add analytics configuration (Google Analytics)
    # TODO: Add logging configuration
    # TODO: Add rate limiting configuration
    # TODO: Add CORS configuration
    # TODO: Add admin email addresses
    # TODO: Add environment-specific configurations (dev, staging, production)
