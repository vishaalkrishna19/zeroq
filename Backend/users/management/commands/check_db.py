from django.core.management.base import BaseCommand
from django.db import connection, transaction
from users.models import User, UserAccount
from accounts.models import Account
from roles_permissions.models import Role, Permission


class Command(BaseCommand):
    help = 'Verify database connectivity and integrity'
    
    def handle(self, *args, **options):
        self.stdout.write("🔍 Checking database connectivity...")
        
        try:
            # Test database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    self.stdout.write(self.style.SUCCESS("✅ Database connection: OK"))
                
            # Test table existence
            tables = connection.introspection.table_names()
            required_tables = ['users', 'accounts', 'user_accounts', 'roles', 'permissions']
            
            self.stdout.write("\n📋 Checking required tables:")
            for table in required_tables:
                if table in tables:
                    self.stdout.write(self.style.SUCCESS(f"✅ Table '{table}': EXISTS"))
                else:
                    self.stdout.write(self.style.ERROR(f"❌ Table '{table}': MISSING"))
            
            # Test CRUD operations
            self.stdout.write("\n🧪 Testing CRUD operations:")
            
            # Test User creation
            test_user_count = User.objects.count()
            self.stdout.write(f"📊 Current user count: {test_user_count}")
            
            # Test Account creation
            test_account_count = Account.objects.count()
            self.stdout.write(f"📊 Current account count: {test_account_count}")
            
            # Test database write capability
            with transaction.atomic():
                test_account = Account.objects.create(
                    account_id="TEST001",
                    account_name="Test Account",
                    timezone="UTC"
                )
                test_account.delete()
                self.stdout.write(self.style.SUCCESS("✅ Database write test: PASSED"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Database error: {e}"))
            
        self.stdout.write("\n" + "="*50)
        self.stdout.write("Database check completed!")
        self.stdout.write("="*50)