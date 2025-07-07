# Management command to create authentication tokens for testing
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class Command(BaseCommand):
    help = 'Create authentication tokens for all users'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Create token for specific username')

    def handle(self, *args, **options):
        username = options.get('username')
        
        if username:
            try:
                user = User.objects.get(username=username)
                token, created = Token.objects.get_or_create(user=user)
                if created:
                    self.stdout.write(f"✅ Created token for {user.username}: {token.key}")
                else:
                    self.stdout.write(f"ℹ️  Token already exists for {user.username}: {token.key}")
            except User.DoesNotExist:
                self.stdout.write(f"❌ User '{username}' not found")
        else:
            users = User.objects.all()
            for user in users:
                token, created = Token.objects.get_or_create(user=user)
                status = "Created" if created else "Exists"
                self.stdout.write(f"{status}: {user.username} -> {token.key}")