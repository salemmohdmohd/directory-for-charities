"""
Email Service - User Registration and Organization Approval Notifications
Handles email sending for various platform notifications
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from flask import current_app

class EmailService:
    """Service for sending various types of emails"""

    # Email configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    FROM_EMAIL = os.getenv('FROM_EMAIL', SMTP_USERNAME)

    @staticmethod
    def _send_email(to_email, subject, html_content, text_content=None):
        """
        Send an email using SMTP
        Returns: (success: bool, error_message: str)
        """
        try:
            if not EmailService.SMTP_USERNAME or not EmailService.SMTP_PASSWORD:
                return False, "Email credentials not configured"

            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = EmailService.FROM_EMAIL
            msg['To'] = to_email
            msg['Subject'] = subject

            # Add text and HTML parts
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)

            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Send email
            with smtplib.SMTP(EmailService.SMTP_SERVER, EmailService.SMTP_PORT) as server:
                server.starttls()
                server.login(EmailService.SMTP_USERNAME, EmailService.SMTP_PASSWORD)
                server.send_message(msg)

            return True, None

        except Exception as e:
            return False, str(e)

    @staticmethod
    def send_welcome_email(user_name, user_email):
        """
        Send welcome email to new user registrations
        """
        subject = "Welcome to Charity Directory!"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .button {{ background-color: #3498db; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to Charity Directory</h1>
                </div>
                <div class="content">
                    <h2>Hello {user_name}!</h2>
                    <p>Thank you for joining our CEO-friendly platform designed for small and mid-size charity organizations.</p>
                    <p>You can now:</p>
                    <ul>
                        <li>Explore charity organizations</li>
                        <li>Connect with other users</li>
                        <li>Access social media advertising and marketing tactics</li>
                        <li>Manage your profile and preferences</li>
                    </ul>
                    <p>Get started by visiting your dashboard:</p>
                    <a href="{os.getenv('FRONTEND_URL', 'http://localhost:5173')}/dashboard" class="button">Go to Dashboard</a>
                    <p>If you have any questions, feel free to contact our support team.</p>
                    <p>Best regards,<br>The Charity Directory Team</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Welcome to Charity Directory!

        Hello {user_name}!

        Thank you for joining our CEO-friendly platform designed for small and mid-size charity organizations.

        You can now:
        - Explore charity organizations
        - Connect with other users
        - Access social media advertising and marketing tactics
        - Manage your profile and preferences

        Visit your dashboard at: {os.getenv('FRONTEND_URL', 'http://localhost:5173')}/dashboard

        If you have any questions, feel free to contact our support team.

        Best regards,
        The Charity Directory Team
        """

        return EmailService._send_email(user_email, subject, html_content, text_content)

    @staticmethod
    def send_organization_approval_email(org_name, contact_email, admin_name, status):
        """
        Send organization approval/rejection notification
        status: 'approved' or 'rejected'
        """
        if status == 'approved':
            subject = f"Congratulations! {org_name} has been approved"
            status_message = "approved"
            status_color = "#27ae60"
            next_steps = """
                <p>Next steps:</p>
                <ul>
                    <li>Complete your organization profile</li>
                    <li>Add your team members</li>
                    <li>Start exploring marketing tools</li>
                    <li>Connect with other charity organizations</li>
                </ul>
            """
        else:
            subject = f"Update on {org_name} application"
            status_message = "under review"
            status_color = "#e74c3c"
            next_steps = """
                <p>You can:</p>
                <ul>
                    <li>Update your application with additional information</li>
                    <li>Contact our support team for guidance</li>
                    <li>Resubmit your application when ready</li>
                </ul>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .status {{ background-color: {status_color}; color: white; padding: 10px; text-align: center; font-weight: bold; margin: 20px 0; }}
                .button {{ background-color: #3498db; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Charity Directory</h1>
                </div>
                <div class="content">
                    <h2>Organization Application Update</h2>
                    <p>Dear {org_name} team,</p>
                    <div class="status">Your organization has been {status_message}</div>
                    <p>We have reviewed your application and your organization status has been updated by {admin_name}.</p>
                    {next_steps}
                    <a href="{os.getenv('FRONTEND_URL', 'http://localhost:5173')}/org-profile" class="button">Manage Organization</a>
                    <p>Thank you for your interest in joining our platform dedicated to helping small and mid-size charities succeed.</p>
                    <p>Best regards,<br>The Charity Directory Team</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Charity Directory - Organization Application Update

        Dear {org_name} team,

        Your organization has been {status_message}.

        We have reviewed your application and your organization status has been updated by {admin_name}.

        Visit your organization profile at: {os.getenv('FRONTEND_URL', 'http://localhost:5173')}/org-profile

        Thank you for your interest in joining our platform dedicated to helping small and mid-size charities succeed.

        Best regards,
        The Charity Directory Team
        """

        return EmailService._send_email(contact_email, subject, html_content, text_content)

# TODO: Implement additional email services
# TODO: Password reset emails with secure tokens
# TODO: Admin notification emails for new organization applications
# TODO: Marketing email campaigns for charity advertising tactics
# TODO: Newsletter service for platform updates and tips
# TODO: Event notification emails
# TODO: Email templates for different user roles (CEO, admin, volunteer)
# TODO: Email analytics and tracking
# TODO: Bulk email service for announcements
# TODO: Email verification for new registrations

# Environment variables needed:
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USERNAME=your_email@gmail.com
# SMTP_PASSWORD=your_app_password
# FROM_EMAIL=noreply@charitydirectory.com
# FRONTEND_URL=http://localhost:5173

# Usage examples:
# success, error = EmailService.send_welcome_email("John Doe", "john@example.com")
# success, error = EmailService.send_organization_approval_email("My Charity", "contact@mycharity.org", "Admin Name", "approved")
