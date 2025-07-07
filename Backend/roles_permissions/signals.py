from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


@receiver(post_migrate)
def create_default_permissions_and_roles(sender, **kwargs):
    """Create default permissions and roles after migration."""
    if sender.name != 'roles_permissions':
        return
    
    Permission = apps.get_model('roles_permissions', 'Permission')
    Role = apps.get_model('roles_permissions', 'Role')
    RolePermission = apps.get_model('roles_permissions', 'RolePermission')
    
    # Default permissions
    default_permissions = [
        # User Management
        ('Can View Users', 'view_users', 'user_management', 'view'),
        ('Can Create Users', 'create_users', 'user_management', 'create'),
        ('Can Edit Users', 'edit_users', 'user_management', 'edit'),
        ('Can Delete Users', 'delete_users', 'user_management', 'delete'),
        ('Can Manage User Roles', 'manage_user_roles', 'user_management', 'admin'),
        
        # Account Management
        ('Can View Accounts', 'view_accounts', 'account_management', 'view'),
        ('Can Create Accounts', 'create_accounts', 'account_management', 'create'),
        ('Can Edit Accounts', 'edit_accounts', 'account_management', 'edit'),
        ('Can Delete Accounts', 'delete_accounts', 'account_management', 'delete'),
        
        # Role Management
        ('Can View Roles', 'view_roles', 'role_management', 'view'),
        ('Can Create Roles', 'create_roles', 'role_management', 'create'),
        ('Can Edit Roles', 'edit_roles', 'role_management', 'edit'),
        ('Can Delete Roles', 'delete_roles', 'role_management', 'delete'),
        ('Can Manage Permissions', 'manage_permissions', 'role_management', 'admin'),
        
        # Employee Onboarding
        ('Can View Onboarding', 'view_onboarding', 'onboarding', 'view'),
        ('Can Create Onboarding', 'create_onboarding', 'onboarding', 'create'),
        ('Can Edit Onboarding', 'edit_onboarding', 'onboarding', 'edit'),
        ('Can Complete Onboarding', 'complete_onboarding', 'onboarding', 'admin'),
        
        # Employee Offboarding
        ('Can View Offboarding', 'view_offboarding', 'offboarding', 'view'),
        ('Can Create Offboarding', 'create_offboarding', 'offboarding', 'create'),
        ('Can Edit Offboarding', 'edit_offboarding', 'offboarding', 'edit'),
        ('Can Complete Offboarding', 'complete_offboarding', 'offboarding', 'admin'),
        
        # System Administration
        ('Can View System Settings', 'view_system_settings', 'system_admin', 'view'),
        ('Can Edit System Settings', 'edit_system_settings', 'system_admin', 'edit'),
        ('Can Access Admin Panel', 'access_admin_panel', 'system_admin', 'admin'),
        
        # Reporting
        ('Can View Reports', 'view_reports', 'reporting', 'view'),
        ('Can Create Reports', 'create_reports', 'reporting', 'create'),
        ('Can Export Reports', 'export_reports', 'reporting', 'admin'),
    ]
    
    created_permissions = {}
    for name, codename, category, level in default_permissions:
        permission, created = Permission.objects.get_or_create(
            codename=codename,
            defaults={
                'name': name,
                'category': category,
                'level': level,
                'description': f'Permission to {name.lower()}'
            }
        )
        created_permissions[codename] = permission
        if created:
            print(f"Created permission: {name}")
    
    # Default roles
    default_roles = [
        ('admin', 'Administrator', 'Full system administrator with all permissions', 2, True),
        ('staff', 'Staff Member', 'Regular staff member with limited permissions', 4, False),
    ]
    
    for name, display_name, description, level, is_default in default_roles:
        role, created = Role.objects.get_or_create(
            name=name,
            defaults={
                'display_name': display_name,
                'description': description,
                'level': level,
                'is_system_role': True,
                'is_default': is_default,
                'is_active': True
            }
        )
        
        if created:
            print(f"Created role: {display_name}")
            
            # Assign permissions to roles
            if name == 'admin':
                # Admin gets all permissions
                for permission in created_permissions.values():
                    RolePermission.objects.get_or_create(
                        role=role,
                        permission=permission,
                        defaults={'is_granted': True}
                    )
            
            elif name == 'staff':
                # Staff gets basic view permissions
                staff_permissions = [
                    'view_users', 'view_accounts', 'view_roles',
                    'view_onboarding', 'view_offboarding', 'view_reports'
                ]
                for codename in staff_permissions:
                    if codename in created_permissions:
                        RolePermission.objects.get_or_create(
                            role=role,
                            permission=created_permissions[codename],
                            defaults={'is_granted': True}
                        )
    
    print("Default permissions and roles setup completed.")