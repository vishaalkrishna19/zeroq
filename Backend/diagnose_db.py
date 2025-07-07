#!/usr/bin/env python
"""
Database diagnostic script for Zeroqueue
Run this to check if database operations are working correctly
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append('/Users/happyfox/Documents/HappyFox/Zeroqueue')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zeroqueue.settings')
django.setup()

from django.db import connection, transaction
from users.models import User, UserAccount
from accounts.models import Account
from roles_permissions.models import Role, Permission

def main():
    print("🔍 Zeroqueue Database Diagnostic Tool")
    print("="*50)
    
    try:
        # Test 1: Database connection
        print("\n1️⃣ Testing database connection...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("✅ Database connection: WORKING")
            
        # Test 2: Check tables
        print("\n2️⃣ Checking database tables...")
        tables = connection.introspection.table_names()
        required_tables = ['users', 'accounts', 'user_accounts', 'roles', 'permissions']
        
        for table in required_tables:
            if table in tables:
                print(f"✅ Table '{table}': EXISTS")
            else:
                print(f"❌ Table '{table}': MISSING")
        
        # Test 3: Count existing data
        print("\n3️⃣ Checking existing data...")
        print(f"👥 Users: {User.objects.count()}")
        print(f"🏢 Accounts: {Account.objects.count()}")
        print(f"🔗 UserAccounts: {UserAccount.objects.count()}")
        print(f"👔 Roles: {Role.objects.count()}")
        print(f"🔐 Permissions: {Permission.objects.count()}")
        
        # Test 4: Create/Update/Delete test
        print("\n4️⃣ Testing CRUD operations...")
        
        with transaction.atomic():
            # Create test account
            test_account = Account.objects.create(
                account_id="TEST123",
                account_name="Test Company",
                timezone="UTC",
                contact_email="test@test.com"
            )
            print(f"✅ Created test account: {test_account.account_id}")
            
            # Update test account
            test_account.account_name = "Updated Test Company"
            test_account.save()
            test_account.refresh_from_db()
            print(f"✅ Updated test account: {test_account.account_name}")
            
            # Delete test account
            test_account.delete()
            print("✅ Deleted test account")
            
            print("✅ All CRUD operations: WORKING")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*50)
    print("Diagnostic completed!")

if __name__ == "__main__":
    main()