import secrets
import string
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def generate_random_password(length=12):
    """Generate a secure random password"""
    # Use a mix of uppercase, lowercase, digits, and special characters
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def send_welcome_email(user, password):
    """Send welcome email with login credentials"""
    subject = f'Welcome to Workforce Platform - Login Credentials for {user.first_name}'
    
    context = {
        'user': user,
        'password': password,
        'login_url': getattr(settings, 'FRONTEND_URL', 'http://localhost:8000'),
    }
    
    # Create plain text message
    plain_message = f"""
Welcome to Workforce Platform!

Dear {user.first_name},

Your account has been created successfully. Here are your login details:

Email: {user.email}
Temporary Password: {password}
Login URL: {context['login_url']}

IMPORTANT: You will be required to change your password upon first login for security reasons.

If you have any questions, please contact your administrator.

Best regards,
Workforce Platform Team
"""
    
    try:
        # Try to render HTML template if it exists
        html_message = render_to_string('emails/welcome_email.html', context)
    except:
        html_message = None
    
    # Send email
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )
