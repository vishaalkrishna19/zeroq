from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, JobTitle, UserAccount
import secrets
import string


def generate_strong_password(length=12):
    """Generate a strong password with mixed case, numbers, and symbols."""
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*"
    
    # Ensure at least one character from each set
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]
    
    # Fill the rest with random characters from all sets
    all_chars = lowercase + uppercase + digits + symbols
    for _ in range(length - 4):
        password.append(secrets.choice(all_chars))
    
    # Shuffle the password list
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'department',
        'user_count',
        'is_active',
        'created_at'
    ]
    
    list_filter = [
        'department',
        'is_active',
        'created_at'
    ]
    
    search_fields = [
        'title',
        'description',
        'department'
    ]
    
    readonly_fields = [
        'id',
        'user_count',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Job Title Information', {
            'fields': (
                'title',
                'description',
                'department',
                'is_active'
            )
        }),
        ('Metadata', {
            'fields': (
                'id',
                'user_count',
                'created_by',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['title']
    
    def user_count(self, obj):
        return obj.user_count
    user_count.short_description = 'Users'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'username',
        'first_name',
        'last_name',
        'email',
        'job_title',
        'department',
        'employment_status',
        'account',
        'role',
        'date_joined'
    ]
    
    list_filter = [
        'employment_status',
        'job_title',
        'department',
        'account',
        'role',
        'can_access_admin',
        'two_factor_enabled',
        'date_joined'
    ]
    
    search_fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'employee_id'
    ]
    
    readonly_fields = [
        'id',
        'date_joined',
        'last_login',
        'updated_at',
        'password_changed_at'
    ]
    
    fieldsets = (
        ('User Information', {
            'fields': (
                'username',
                'password',
                'first_name',
                'last_name',
                'email'
            )
        }),
        ('Employment', {
            'fields': (
                'employee_id',
                'hire_date',
                'job_title',
                'department',
                'employment_status',
                'termination_date'
            )
        }),
        ('Account & Role', {
            'fields': (
                'account',
                'role',
                'can_access_admin'
            )
        }),
        ('Security', {
            'fields': (
                'two_factor_enabled',
                'must_change_password',
                'password_changed_at'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'custom_permissions',
            )
        }),
        ('Metadata', {
            'fields': (
                'id',
                'date_joined',
                'last_login',
                'updated_at',
                'created_by'
            ),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('User Information', {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'email'
            )
        }),
        ('Employment', {
            'fields': (
                'employee_id',
                'hire_date',
                'job_title',
                'department',
                'employment_status'
            )
        }),
        ('Account & Role', {
            'fields': (
                'account',
                'role'
            )
        }),
    )
    
    filter_horizontal = ['custom_permissions']
    ordering = ['last_name', 'first_name', 'username']


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = [
        'user_display',
        'account',
        'role',
        'is_primary',
        'is_active',
        'onboarding_status_display',
        'created_at'
    ]
    
    list_filter = [
        'is_primary',
        'is_active',
        'onboarding_completed',
        'offboarding_started',
        'account',
        'role'
    ]
    
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'account__account_name'
    ]
    
    readonly_fields = [
        'id',
        'onboarding_status_display',
        'offboarding_status_display',
        'created_at',
        'updated_at'
    ]
    
    def user_display(self, obj):
        return obj.user.get_full_name()
    user_display.short_description = 'User'
    
    def onboarding_status_display(self, obj):
        return obj.onboarding_status
    onboarding_status_display.short_description = 'Onboarding Status'
    
    def offboarding_status_display(self, obj):
        return obj.offboarding_status
    offboarding_status_display.short_description = 'Offboarding Status'