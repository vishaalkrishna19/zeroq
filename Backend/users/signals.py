from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.apps import apps
from .services import EmailService
User = get_user_model()


@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs):
    """Handle actions when a user is created."""
    if created:
        # Log user creation
        print(f"\n👤 User created: {instance.username} ({instance.get_full_name()})")
        
        # Auto-assign default role if user has accounts
        from roles_permissions.models import Role
        try:
            default_role = Role.objects.get(is_default=True, is_active=True)
            # Note: UserAccount creation with default role should be handled 
            # at the application level, not automatically here
        except Role.DoesNotExist:
            pass


@receiver(post_migrate)
def create_default_admin_user(sender, **kwargs):
    """Create default admin user after migration."""
    if sender.name != 'users':
        return
    
    User = apps.get_model('users', 'User')
    
    # Create superuser if none exists
    if not User.objects.filter(is_superuser=True).exists():
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@zeroqueue.com',
            first_name='System',
            last_name='Administrator',
            is_staff=True,
            is_superuser=True,
            employee_id='ADMIN001',
            job_title='System Administrator',
            department='IT',
            employment_status='active'
        )
        admin_user.set_password('admin123')  # Change this in production!
        admin_user.must_change_password = True
        admin_user.save()
        
        print("\n" + "="*60)
        print("🔐 DEFAULT ADMIN USER CREATED")
        print("="*60)
        print(f"Username: admin")
        print(f"Password: admin123")
        print(f"Email: admin@zeroqueue.com")
        print("⚠️  CHANGE PASSWORD IMMEDIATELY IN PRODUCTION!")
        print("="*60 + "\n")