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
                print("❌ EMAIL_HOST_USER not set in environment variables")
                return False
                
            if not settings.EMAIL_HOST_PASSWORD:
                logger.error("EMAIL_HOST_PASSWORD not set in environment variables")
                print("❌ EMAIL_HOST_PASSWORD not set in environment variables")
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
                'site_url': 'http://127.0.0.1:8000',  # Update for production
                'support_email': settings.ADMIN_EMAIL,
            }
            
            # Render HTML and text content from templates
            try:
                html_content = render_to_string('emails/user_created.html', context)
                text_content = render_to_string('emails/user_created.txt', context)
                
                # Create email message with HTML and text alternatives
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email],
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
                
            except Exception as template_error:
                logger.warning(f"Failed to render email templates, falling back to simple text: {str(template_error)}")
                # Fallback to simple text email
                text_content = f"""Dear {user.get_full_name() or user.username},

Welcome to ZeroQueue! Your account has been successfully created.

LOGIN CREDENTIALS:
Username: {user.username}
Email: {user.email}
Temporary Password: {password}

🔑 Set your new password: {context['site_url']}/auth/reset-password/?token={user.id}

After setting your password, log in at: {context['site_url']}/admin/

Best regards,
ZeroQueue Team

Support: {settings.ADMIN_EMAIL}"""
                
                # Send simple text email
                send_mail(
                    subject=subject,
                    message=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            
            logger.info(f"User credentials email sent successfully to {user.email}")
            print(f"✅ User credentials email sent successfully to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send user credentials email to {user.email}: {str(e)}")
            print(f"❌ Failed to send user credentials email to {user.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_password_reset_notification(user, new_password, reset_by=None):
        """
        Send email notification when admin resets user password.
        
        Args:
            user: User instance
            new_password: New plain text password
            reset_by: User who reset the password (optional)
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            subject = "ZeroQueue - Password Reset Notification"
            
            context = {
                'user': user,
                'password': new_password,
                'reset_by': reset_by,
                'site_url': 'http://127.0.0.1:8000',
                'support_email': settings.ADMIN_EMAIL,
            }
            
            # For now, use the same template as user creation
            # You can create a separate template for password reset
            html_content = render_to_string('emails/user_created.html', context)
            text_content = render_to_string('emails/user_created.txt', context)
            
            # Create email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            logger.info(f"Password reset notification sent successfully to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password reset notification to {user.email}: {str(e)}")
            return False
                
        except Exception as e:
            logger.error(f"Failed to send password reset notification to {user.email}: {str(e)}")
            return False
