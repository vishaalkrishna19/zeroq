"""
Management command to refresh permissions in admin interface.
This command ensures the admin interface uses the latest permissions from the database.
"""

from django.core.management.base import BaseCommand
from django.contrib.admin import site
from users.admin import UserAdmin
from users.models import User
from roles_permissions.models import Permission


class Command(BaseCommand):
    help = 'Refresh permissions in admin interface to reflect database changes'
    
    def handle(self, *args, **options):
        # Count current permissions
        permission_count = Permission.objects.filter(is_active=True).count()
        
        self.stdout.write(
            self.style.SUCCESS(f'Found {permission_count} active permissions in database')
        )
        
        # The admin form will automatically pick up the new permissions
        # when the page is refreshed due to the dynamic queryset in UserAdminForm
        
        self.stdout.write(
            self.style.SUCCESS(
                'Permissions will be automatically refreshed when admin pages are loaded.\n'
                'The UserAdminForm dynamically queries the database for current permissions.'
            )
        )
        
        # List current permission categories
        categories = Permission.objects.filter(is_active=True).values_list('category', flat=True).distinct()
        
        self.stdout.write('\nCurrent permission categories:')
        for category in categories:
            count = Permission.objects.filter(category=category, is_active=True).count()
            self.stdout.write(f'  - {category.replace("_", " ").title()}: {count} permissions')
        
        self.stdout.write(
            self.style.WARNING(
                '\n⚠️  Note: If you\'re still seeing old permissions in the admin interface, '
                'try refreshing your browser or clearing browser cache.'
            )
        )