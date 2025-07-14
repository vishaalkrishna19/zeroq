import secrets
import string

def generate_strong_password(length=12):
    """Generate a strong password with uppercase, lowercase, digits, and special characters."""
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password