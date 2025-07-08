from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging
logger = logging.getLogger(__name__)
class EmailService:
    """Service class for handling email operations."""
    @staticmethod
    def send_user_credentials_email(user, password, created_by=None):
        """
        Send email with user credentials to newly created user.
        Args:
            user: User instance
            password: Plain text password
            created_by: User who created this account (optional)
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Debug: Print email configuration
            print(f"Email Config Debug:")
            print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
            print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
            print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
            # Check if email configuration is valid
            if not settings.EMAIL_HOST_USER:
                logger.error("EMAIL_HOST_USER not set in environment variables")
                print(":x: EMAIL_HOST_USER not set in environment variables")
                return False
            if not settings.EMAIL_HOST_PASSWORD:
                logger.error("EMAIL_HOST_PASSWORD not set in environment variables")
                print(":x: EMAIL_HOST_PASSWORD not set in environment variables")
                return False
            # Get email configuration - use getattr to avoid AttributeError
            email_templates = getattr(settings, 'EMAIL_TEMPLATES', {})
            email_config = email_templates.get('USER_CREATED', {})
            subject = email_config.get('subject', 'Welcome to ZeroQueue - Your Account Details')
            # Context for email templates
            context = {
                'user': user,
                'password': password,
                'created_by': created_by,
                'site_url': 'http://localhost:5173',  # Vite runs on port 5173
                'support_email': settings.ADMIN_EMAIL,
            }
            # Render HTML and text templates
            html_content = render_to_string('emails/user_created.html', context)
            text_content = render_to_string('emails/user_created.txt', context)
            
            # Create email message with HTML alternative
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            logger.info(f"User credentials email sent successfully to {user.email}")
            print(f":white_check_mark: User credentials email sent successfully to {user.email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send user credentials email to {user.email}: {str(e)}")
            print(f":x: Failed to send user credentials email to {user.email}: {str(e)}")
            return False

