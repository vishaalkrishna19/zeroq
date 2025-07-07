from django.db import models
from django.core.exceptions import ValidationError
import uuid


class Permission(models.Model):
    """
    Represents a specific permission that can be granted to roles.
    Permissions are granular and can be combined to create flexible access control.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Permission identification
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Unique permission name (e.g., can_view_users, can_edit_accounts)'
    )
    
    codename = models.CharField(
        max_length=100,
        unique=True,
        help_text='Machine-readable permission code (e.g., view_users, edit_accounts)'
    )
    
    # Permission details
    description = models.TextField(
        blank=True,
        help_text='Detailed description of what this permission allows'
    )
    
    # Permission categorization
    CATEGORY_CHOICES = [
        ('user_management', 'User Management'),
        ('account_management', 'Account Management'),
        ('role_management', 'Role Management'),
        ('system_admin', 'System Administration'),
        ('reporting', 'Reporting'),
        ('onboarding', 'Employee Onboarding'),
        ('offboarding', 'Employee Offboarding'),
    ]
    
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        help_text='Permission category for grouping'
    )
    
    # Permission level
    LEVEL_CHOICES = [
        ('view', 'View Only'),
        ('create', 'Create'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
        ('admin', 'Full Admin'),
    ]
    
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='view',
        help_text='Permission level/type'
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this permission is currently active'
    )
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'permissions'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
        ordering = ['category', 'level', 'name']
        
    def __str__(self):
        return f"{self.name} ({self.level})"
    
    def save(self, *args, **kwargs):
        # Auto-generate codename if not provided
        if not self.codename:
            self.codename = self.name.lower().replace(' ', '_')
        super().save(*args, **kwargs)


class Role(models.Model):
    """
    Represents a role that can be assigned to users.
    Roles contain a collection of permissions and define user access levels.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Role identification
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Unique role name (e.g., admin, staff, manager)'
    )
    
    display_name = models.CharField(
        max_length=100,
        help_text='Human-readable role name for display'
    )
    
    # Role details
    description = models.TextField(
        blank=True,
        help_text='Detailed description of this role'
    )
    
    # Role level hierarchy
    ROLE_LEVEL_CHOICES = [
        (1, 'Super Admin'),
        (2, 'Account Admin'),
        (3, 'Manager'),
        (4, 'Staff'),
        (5, 'Read Only'),
    ]
    
    level = models.IntegerField(
        choices=ROLE_LEVEL_CHOICES,
        default=4,
        help_text='Role hierarchy level (lower numbers = higher authority)'
    )
    
    # Permissions
    permissions = models.ManyToManyField(
        Permission,
        through='RolePermission',
        blank=True,
        help_text='Permissions granted to this role'
    )
    
    # Role settings
    is_system_role = models.BooleanField(
        default=False,
        help_text='Whether this is a system-defined role (cannot be deleted)'
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this role is currently active'
    )
    
    # Default role settings
    is_default = models.BooleanField(
        default=False,
        help_text='Whether this role should be assigned to new users by default'
    )
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['level', 'name']
        
    def __str__(self):
        return self.display_name or self.name
    
    def clean(self):
        # Ensure only one default role exists
        if self.is_default:
            existing_default = Role.objects.filter(is_default=True).exclude(pk=self.pk)
            if existing_default.exists():
                raise ValidationError('Only one role can be set as default.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def has_permission(self, permission_codename):
        """Check if this role has a specific permission."""
        return self.rolepermission_set.filter(
            permission__codename=permission_codename,
            is_granted=True
        ).exists()
    
    def get_permissions_by_category(self):
        """Get permissions grouped by category."""
        permissions = {}
        role_permissions = self.rolepermission_set.select_related('permission').filter(is_granted=True)
        
        for rp in role_permissions:
            category = rp.permission.category
            if category not in permissions:
                permissions[category] = []
            permissions[category].append(rp.permission)
        
        return permissions


class RolePermission(models.Model):
    """
    Through model for Role-Permission relationship with granular control.
    Allows for granted/denied permissions and additional constraints.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
    # Permission state
    is_granted = models.BooleanField(
        default=True,
        help_text='Whether this permission is granted or denied'
    )
    
    # Additional constraints
    constraints = models.JSONField(
        default=dict,
        blank=True,
        help_text='Additional constraints for this permission (JSON format)'
    )
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'role_permissions'
        verbose_name = 'Role Permission'
        verbose_name_plural = 'Role Permissions'
        unique_together = ['role', 'permission']
        ordering = ['role__name', 'permission__category', 'permission__name']
        
    def __str__(self):
        status = "✓" if self.is_granted else "✗"
        return f"{self.role.name} - {self.permission.name} {status}"