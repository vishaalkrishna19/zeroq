from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from django import forms
import secrets
import string
from .models import User, UserAccount


class CustomUserCreationForm(forms.ModelForm):
    """Custom user creation form for admin - No password fields."""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'employee_id', 
                 'job_title', 'department', 'hire_date', 'employment_status')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make required fields
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
        # Add help text for password
        self.fields['username'].help_text = 'Username for login. A strong password will be auto-generated.'


def generate_strong_password(length=12):
    """Generate a strong password with uppercase, lowercase, digits, and special characters."""
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


class UserAccountInline(admin.TabularInline):
    model = UserAccount
    fk_name = 'user'  # Specify which ForeignKey to use
    extra = 0
    fields = [
        'account', 
        'role', 
        'is_primary', 
        'is_active', 
        'can_access_admin',
        'onboarding_completed',
        'offboarding_started'
    ]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin with enhanced fields and password generation."""
    
    # Use custom form for adding users
    add_form = CustomUserCreationForm
    
    # Display fields
    list_display = [
        'username', 
        'email', 
        'get_full_name', 
        'employment_status',
        'is_active', 
        'is_staff',
        'account_count',
        'last_login', 
        'date_joined'
    ]
    
    list_filter = [
        'employment_status',
        'is_active', 
        'is_staff', 
        'is_superuser',
        'is_system_admin',
        'must_change_password',
        'two_factor_enabled',
        'date_joined',
        'last_login'
    ]
    
    search_fields = [
        'username', 
        'first_name', 
        'last_name', 
        'email',
        'employee_id',
        'job_title',
        'department'
    ]
    
    readonly_fields = [
        'id',
        'date_joined', 
        'last_login',
        'updated_at',
        'password_changed_at',
        'last_login_ip',
        'account_count'
    ]
    
    # Organize fields in sections
    fieldsets = (
        ('Authentication', {
            'fields': (
                'username', 
                'password',
                'must_change_password',
                'password_changed_at'
            )
        }),
        ('Personal Information', {
            'fields': (
                'first_name', 
                'last_name', 
                'email',
                'phone_number',
                'date_of_birth'
            )
        }),
        ('Employment Information', {
            'fields': (
                'employee_id',
                'job_title',
                'department',
                'manager',
                'hire_date',
                'termination_date',
                'employment_status'
            )
        }),
        ('Address', {
            'fields': (
                'address_line1',
                'address_line2', 
                'city', 
                'state', 
                'postal_code', 
                'country'
            ),
            'classes': ('collapse',)
        }),
        ('Permissions & Access', {
            'fields': (
                'is_active',
                'is_staff', 
                'is_superuser',
                'is_system_admin',
                'groups', 
                'user_permissions'
            )
        }),
        ('Security', {
            'fields': (
                'two_factor_enabled',
                'last_login_ip'
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': (
                'id',
                'account_count',
                'created_by',
                'date_joined',
                'last_login', 
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Fields for creating new user - No password fields (auto-generated)
    add_fieldsets = (
        ('Required Information', {
            'classes': ('wide',),
            'fields': (
                'username', 
                'email',
                'first_name', 
                'last_name'
            ),
            'description': 'A strong password will be automatically generated and shown in the terminal.'
        }),
        ('Employment Details', {
            'fields': (
                'employee_id',
                'job_title',
                'department',
                'hire_date'
            ),
        }),
        ('Account Settings', {
            'fields': (
                'is_active',
                'is_staff',
                'employment_status'
            ),
        }),
    )
    
    inlines = [UserAccountInline]
    ordering = ['last_name', 'first_name', 'username']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def account_count(self, obj):
        count = obj.useraccount_set.filter(is_active=True).count()
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if count > 0 else 'orange',
            count
        )
    account_count.short_description = 'Active Accounts'
    
    def save_model(self, request, obj, form, change):
        """Override to generate password for new users and print it."""
        if not change:  # Creating new user
            # Generate strong password automatically
            password = generate_strong_password()
            obj.set_password(password)
            obj.created_by = request.user
            obj.must_change_password = True
            
            # Save the user first
            super().save_model(request, obj, form, change)
            
            # Print password to terminal
            print("\n" + "="*60)
            print("🔐 NEW USER CREATED")
            print("="*60)
            print(f"Username: {obj.username}")
            print(f"Email: {obj.email}")
            print(f"Full Name: {obj.get_full_name()}")
            print(f"Generated Password: {password}")
            print(f"Employee ID: {obj.employee_id or 'Not set'}")
            print(f"Job Title: {obj.job_title or 'Not set'}")
            print(f"Department: {obj.department or 'Not set'}")
            print("⚠️  User must change password on first login")
            print("="*60)
            print("Please securely share this password with the user.")
            print("="*60 + "\n")
        else:
            super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('useraccount_set')


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    """Admin for User-Account relationships."""
    
    list_display = [
        'user_display',
        'account_display', 
        'role', 
        'is_primary',
        'is_active',
        'onboarding_status_display',
        'offboarding_status_display',
        'created_at'
    ]
    
    list_filter = [
        'is_primary',
        'is_active',
        'can_access_admin',
        'onboarding_completed',
        'offboarding_started',
        'role__name',
        'account__account_name',
        'created_at'
    ]
    
    search_fields = [
        'user__username',
        'user__first_name', 
        'user__last_name',
        'user__email',
        'account__account_name',
        'account__account_id'
    ]
    
    readonly_fields = [
        'id',
        'created_at', 
        'updated_at',
        'onboarding_completed_at',
        'offboarding_started_at',
        'offboarding_completed_at'
    ]
    
    fieldsets = (
        ('Relationship', {
            'fields': (
                'user', 
                'account', 
                'role'
            )
        }),
        ('Settings', {
            'fields': (
                'is_primary',
                'is_active', 
                'can_access_admin'
            )
        }),
        ('Onboarding', {
            'fields': (
                'onboarding_completed',
                'onboarding_completed_at'
            )
        }),
        ('Offboarding', {
            'fields': (
                'offboarding_started',
                'offboarding_started_at',
                'offboarding_completed_at'
            )
        }),
        ('Additional Information', {
            'fields': (
                'notes',
                'created_by'
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': (
                'id',
                'created_at', 
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['account__account_name', 'user__last_name', 'user__first_name']
    
    def user_display(self, obj):
        return obj.user.get_full_name()
    user_display.short_description = 'User'
    
    def account_display(self, obj):
        return f"{obj.account.account_name} ({obj.account.account_id})"
    account_display.short_description = 'Account'
    
    def onboarding_status_display(self, obj):
        status = obj.onboarding_status
        colors = {
            'completed': 'green',
            'in_progress': 'orange', 
            'not_started': 'red'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(status, 'black'),
            status.replace('_', ' ').title()
        )
    onboarding_status_display.short_description = 'Onboarding'
    
    def offboarding_status_display(self, obj):
        status = obj.offboarding_status
        colors = {
            'completed': 'red',
            'in_progress': 'orange',
            'not_started': 'green'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(status, 'black'),
            status.replace('_', ' ').title()
        )
    offboarding_status_display.short_description = 'Offboarding'
    
    def save_model(self, request, obj, form, change):
        """Override to set created_by for new objects."""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'account', 'role'
        )