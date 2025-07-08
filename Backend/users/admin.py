from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.html import format_html
from django.urls import reverse, path
from django.utils import timezone
from django import forms
import secrets
import string
from .models import User, UserAccount

from .services import EmailService

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
    # Remove the commented out admin code lines
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
        'account_count',
        'reset_password_button'
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
                'email'
            )
        }),
        ('Employment Information', {
            'fields': (
                'employee_id',
                'job_title',
                'department',
                'hire_date',
                'termination_date',
                'employment_status',
                'account',
                'role'
            )
        }),
        ('Permissions & Access', {
            'fields': (
                'is_active',
                'is_staff', 
                'is_superuser',
                'groups', 
                'user_permissions'
            )
        }),
        ('Security', {
            'fields': (
                'two_factor_enabled',
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

                'job_title',
                'department',
                'hire_date',
                'account',
                'role'
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
    
    ordering = ['last_name', 'first_name', 'username']
    
    actions = ['generate_auth_tokens', 'deactivate_users', 'activate_users', 'test_user_passwords', 'reset_passwords_admin_action']
    
    def generate_auth_tokens(self, request, queryset):
        """Admin action to generate auth tokens for selected users."""
        from rest_framework.authtoken.models import Token
        created_count = 0
        existing_count = 0
        
        for user in queryset:
            token, created = Token.objects.get_or_create(user=user)
            if created:
                created_count += 1
            else:
                existing_count += 1
        
        message = f"Generated {created_count} new tokens. {existing_count} users already had tokens."
        self.message_user(request, message)
    
    generate_auth_tokens.short_description = "Generate authentication tokens for selected users"
    
    def deactivate_users(self, request, queryset):
        """Admin action to deactivate selected users."""
        updated = queryset.update(is_active=False, employment_status='inactive')
        self.message_user(request, f"{updated} users were deactivated.")
    
    deactivate_users.short_description = "Deactivate selected users"
    
    def activate_users(self, request, queryset):
        """Admin action to activate selected users."""
        updated = queryset.update(is_active=True, employment_status='active')
        self.message_user(request, f"{updated} users were activated.")
    
    activate_users.short_description = "Activate selected users"
    
    # def test_user_passwords(self, request, queryset):
    #     """Admin action to test password verification for debugging."""
    #     from django.contrib import messages
        
    #     for user in queryset:
    #         print(f"\n🔍 PASSWORD DEBUG for {user.username}:")
    #         print(f"Database Hash: {user.password}")
    #         print(f"Must Change Password: {user.must_change_password}")
    #         print(f"Password Changed At: {user.password_changed_at}")
    #         print(f"Is Active: {user.is_active}")
            
    #         # Test with a common password to demonstrate
    #         test_password = "admin123"
    #         if user.check_password(test_password):
    #             print(f"✅ User {user.username} password is: {test_password}")
    #         else:
    #             print(f"❌ User {user.username} password is NOT: {test_password}")
    #             print("💡 Use the original generated password from terminal output")
        
    #     self.message_user(request, f"Password debug info printed to terminal for {queryset.count()} users.")
    
    # test_user_passwords.short_description = "🔍 Debug password info for selected users"
    
    def reset_passwords_admin_action(self, request, queryset):
        """Admin action to reset passwords for selected users."""
        reset_count = 0
        
        print("\n" + "="*70)
        print("🔐 BULK PASSWORD RESET INITIATED")
        print("="*70)
        
        for user in queryset:
            # Generate new password
            new_password = generate_strong_password()
            user.set_password(new_password)
            user.must_change_password = True
            user.save()
            
            # Print each password clearly
            print(f"\n👤 User: {user.username} ({user.get_full_name()})")
            print(f"📧 Email: {user.email}")
            print(f"🔑 New Password: {new_password}")
            print(f"🆔 User ID: {user.id}")
            print("-" * 50)
            
            reset_count += 1
        
        print(f"\n✅ Successfully reset {reset_count} passwords")
        print("⚠️  All users must change passwords on next login")
        print("="*70 + "\n")
        
        self.message_user(
            request, 
            f"Reset passwords for {reset_count} users. New passwords printed to terminal."
        )
    
    reset_passwords_admin_action.short_description = "🔐 Reset passwords for selected users"
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def account_count(self, obj):
        # Since user now belongs to only one account, return 1 if account exists, 0 otherwise
        count = 1 if obj.account else 0
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if count > 0 else 'orange',
            count
        )
    account_count.short_description = 'Has Account'
    
    def reset_password_button(self, obj):
        """Add reset password button for existing users."""
        if obj.pk:
            url = reverse('admin:users_user_reset_password', args=[obj.pk])
            return format_html(
                '<a class="button" href="{}">🔐 Reset Password</a>',
                url
            )
        return "Save user first"
    reset_password_button.short_description = 'Password Actions'
    
    def save_model(self, request, obj, form, change):
        """Override to generate password for new users and send email."""
        try:
            if not change:  # Creating new user
                # Generate strong password automatically
                password = generate_strong_password()
                obj.set_password(password)
                obj.created_by = request.user
                obj.must_change_password = True
                
                # Save the user first - ensure transaction is committed
                super().save_model(request, obj, form, change)
                
                # Verify the save was successful
                obj.refresh_from_db()
                
                # Print password to terminal with database verification
                # if obj.account:
                #     user_account = UserAccount.objects.create(
                #         user=obj,
                #         account=obj.account,
                #         role=obj.role,  # Use the role from User model
                #         is_primary=True,  # First account is primary
                #         is_active=True,
                #         can_access_admin=obj.is_staff,
                #         created_by=request.user
                #     )
                #     print(f"✅ UserAccount created: {user_account}")
                print("="*60)
                print(f"Username: {obj.username}")
                print(f"Email: {obj.email}")
                print(f"Full Name: {obj.get_full_name()}")
                print(f"Generated Password: {password}")
                print(f"Employee ID: {obj.employee_id or 'Not set'}")
                print(f"Job Title: {obj.job_title or 'Not set'}")
                print(f"Department: {obj.department or 'Not set'}")
                print(f"Database ID: {obj.id}")
                print(f"Password Hash (First 50 chars): {obj.password[:50]}...")
                print("⚠️  User must change password on first login")
                print("="*60)
                print("🔑 USE THIS PASSWORD FOR LOGIN:")
                print(f"    Username: {obj.username}")
                print(f"    Password: {password}")
                print("="*60)
                print("❌ DO NOT use the password hash from database!")
                print("✅ Use the Generated Password shown above!")
                print("="*60 + "\n")
                
                # Test the password immediately
                if obj.check_password(password):
                    print(f"✅ Password verification successful for {obj.username}")
                else:
                    print(f"❌ Password verification failed for {obj.username}")
                # Send email with credentials
                if obj.email:
                    email_sent = EmailService.send_user_credentials_email(
                        user=obj,
                        password=password,
                        created_by=request.user
                    )
                    if email_sent:
                        print(":white_check_mark: Email sent successfully to user's email address")
                        self.message_user(
                            request,
                            f"User '{obj.username}' created successfully and credentials sent to {obj.email}",
                            level='success'
                        )
                    else:
                        print(":x: Failed to send email - check email configuration")
                        self.message_user(
                            request,
                            f"User '{obj.username}' created but failed to send email to {obj.email}",
                            level='warning'
                        )
                else:
                    print(":warning:  No email address provided - email not sent")
                    self.message_user(
                        request,
                        f"User '{obj.username}' created but no email address provided",
                        level='warning'
                    )






   
            else:
                # Save changes to existing user
                super().save_model(request, obj, form, change)
                
                # Verify the save was successful
                obj.refresh_from_db()
                print(f"✅ User updated: {obj.username} ({obj.get_full_name()})")
                
        except Exception as e:
            print(f"❌ Error saving user: {e}")
            raise
    
    def get_urls(self):
        """Add custom admin URLs for password reset."""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/reset_password/',
                self.admin_site.admin_view(self.reset_password_view),
                name='users_user_reset_password',
            ),
        ]
        return custom_urls + urls
    
    def reset_password_view(self, request, object_id):
        """Admin view for resetting user password using Django sessions."""
        from django.shortcuts import render, redirect
        from django.contrib import messages
        from django.contrib.admin.utils import unquote
        from django.http import Http404
        
        user_id = unquote(object_id)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Http404("User not found")
        
        if request.method == 'POST':
            # Generate new password
            new_password = generate_strong_password()
            user.set_password(new_password)
            user.must_change_password = True
            user.save()
            
            # Print password to terminal
            print("\n" + "="*60)
            print("🔐 PASSWORD RESET BY ADMIN")
            print("="*60)
            print(f"Admin: {request.user.username}")
            print(f"Target User: {user.username}")
            print(f"Email: {user.email}")
            print(f"Full Name: {user.get_full_name()}")
            print(f"New Password: {new_password}")
            print("⚠️  User must change password on first login")
            print("="*60)
            print("Please securely share this password with the user.")
            print("="*60 + "\n")
            
            messages.success(
                request, 
                f'Password reset successfully for {user.get_full_name()}. '
                f'New password has been printed to the server terminal.'
            )
            return redirect('admin:users_user_change', user.pk)
        
        context = {
            'title': f'Reset Password for {user.get_full_name()}',
            'user_obj': user,
            'opts': self.model._meta,
            'original': user,
            'has_change_permission': True,
        }
        
        return render(request, 'admin/users/user/reset_password.html', context)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('account', 'role')


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
        try:
            if not change:
                obj.created_by = request.user
            
            # Save the object
            super().save_model(request, obj, form, change)
            
            # Verify the save was successful
            obj.refresh_from_db()
            
            action = "created" if not change else "updated"
            print(f"✅ UserAccount {action}: {obj.user.username} @ {obj.account.account_name}")
            
        except Exception as e:
            print(f"❌ Error saving UserAccount: {e}")
            raise
    # Simplified save_model
    # def save_model(self, request, obj, form, change):
    #     if not change:  # New user
    #         password = generate_strong_password()
    #         obj.set_password(password)
    #         obj.created_by = request.user
    #         print(f"New user: {obj.username}, Password: {password}")
    #     super().save_model(request, obj, form, change)
        
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'account', 'role'
        )