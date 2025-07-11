from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import transaction


class Command(BaseCommand):
    help = 'Automatically assign permissions to roles'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually doing it',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reassignment even if permissions already exist',
        )
    
    def handle(self, *args, **options):
        self.dry_run = options['dry_run']
        self.force = options['force']
        
        try:
            # Get models
            Role = apps.get_model('roles_permissions', 'Role')
            Permission = apps.get_model('roles_permissions', 'Permission')
            RolePermission = apps.get_model('roles_permissions', 'RolePermission')
            
            self.stdout.write(self.style.SUCCESS('🔐 Starting Role-Permission Assignment'))
            self.stdout.write(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
            self.stdout.write("-" * 60)
            
            # Define role-permission mappings
            role_permissions = {
                'super_admin': {
                    'display_name': 'Super Admin',
                    'permissions': 'ALL'  # Special case for all permissions
                },
                'hr_manager': {
                    'display_name': 'HR Manager',
                    'permissions': [
                        'view_users', 'create_users', 'edit_users',
                        'view_onboarding', 'create_onboarding', 'edit_onboarding', 'delete_onboarding', 'admin_onboarding',
                        'view_offboarding', 'create_offboarding', 'edit_offboarding', 'delete_offboarding', 'admin_offboarding',
                        'view_reports', 'create_reports', 'edit_reports'
                    ]
                },
                'manager': {
                    'display_name': 'Manager',
                    'permissions': [
                        'view_users', 'edit_users',
                        'view_onboarding', 'create_onboarding', 'edit_onboarding',
                        'view_offboarding', 'create_offboarding', 'edit_offboarding',
                        'view_reports', 'create_reports'
                    ]
                },
                'employee': {
                    'display_name': 'Employee',
                    'permissions': [
                        'view_onboarding',
                        'view_offboarding',
                        'view_reports'
                    ]
                },
                'read_only': {
                    'display_name': 'Read Only',
                    'permissions': [
                        'view_users', 'view_accounts', 'view_roles', 'view_system',
                        'view_reports', 'view_onboarding', 'view_offboarding'
                    ]
                }
            }
            
            # Start assignment process
            with transaction.atomic():
                for role_name, role_config in role_permissions.items():
                    self.assign_permissions_to_role(
                        Role, Permission, RolePermission,
                        role_name, role_config
                    )
            
            self.stdout.write(self.style.SUCCESS('✅ Role-Permission Assignment Complete!'))
            
            if self.dry_run:
                self.stdout.write(self.style.WARNING('📋 This was a DRY RUN - no changes made'))
                self.stdout.write(self.style.WARNING('   Run without --dry-run to apply changes'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
            raise
    
    def assign_permissions_to_role(self, Role, Permission, RolePermission, role_name, role_config):
        """Assign permissions to a specific role"""
        try:
            # Find the role
            role = Role.objects.get(name=role_name)
            display_name = role_config['display_name']
            
            self.stdout.write(f"\n🔧 Processing Role: {display_name} ({role_name})")
            
            # Get permissions to assign
            if role_config['permissions'] == 'ALL':
                permissions_to_assign = Permission.objects.filter(is_active=True)
                self.stdout.write(f"   📋 Assigning ALL permissions ({permissions_to_assign.count()} total)")
            else:
                permissions_to_assign = Permission.objects.filter(
                    codename__in=role_config['permissions'],
                    is_active=True
                )
                self.stdout.write(f"   📋 Assigning {len(role_config['permissions'])} specific permissions")
            
            # Check existing assignments
            existing_assignments = RolePermission.objects.filter(role=role).count()
            
            if existing_assignments > 0 and not self.force:
                self.stdout.write(f"   ⚠️  Role already has {existing_assignments} permissions assigned")
                self.stdout.write(f"   ⚠️  Use --force to reassign permissions")
                return
            
            # Clear existing assignments if force is enabled
            if self.force and existing_assignments > 0:
                if not self.dry_run:
                    RolePermission.objects.filter(role=role).delete()
                self.stdout.write(f"   🗑️  Cleared {existing_assignments} existing assignments")
            
            # Assign permissions
            assigned_count = 0
            for permission in permissions_to_assign:
                if not self.dry_run:
                    RolePermission.objects.get_or_create(
                        role=role,
                        permission=permission,
                        defaults={'is_granted': True}
                    )
                assigned_count += 1
                
                # Show progress for large assignments
                if assigned_count % 10 == 0:
                    self.stdout.write(f"   📄 Assigned {assigned_count}/{permissions_to_assign.count()} permissions...")
            
            self.stdout.write(f"   ✅ Successfully assigned {assigned_count} permissions to {display_name}")
            
            # Show some example permissions
            if assigned_count > 0:
                sample_permissions = list(permissions_to_assign[:3])
                sample_names = [p.name for p in sample_permissions]
                self.stdout.write(f"   📋 Examples: {', '.join(sample_names)}")
                if assigned_count > 3:
                    self.stdout.write(f"   📋 ... and {assigned_count - 3} more")
            
        except Role.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"   ❌ Role '{role_name}' not found"))
            self.stdout.write(self.style.ERROR(f"   💡 Please create the role first in Django Admin"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Error assigning permissions to {role_name}: {str(e)}")) 