from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.html import format_html
from django.urls import reverse, path
from django.utils import timezone
from django import forms
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib import messages
import secrets
import string
import logging
from .models import User, UserAccount
from .services import EmailService

# Set up logging
logger = logging.getLogger(__name__)

class CustomUserCreationForm(forms.ModelForm):
    """Custom user creation form for admin - No password fields."""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'employee_id', 
                 'job_title', 'department', 'hire_date', 'employment_status')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            # Make required fields
            self.fields['email'].required = True
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
            
            # Add help text for password
            self.fields['username'].help_text = 'Username for login. A strong password will be auto-generated.'
        except KeyError as e:
            logger.error(f"Field not found in CustomUserCreationForm: {e}")
            raise ValidationError(f"Required field missing: {e}")
    
    def clean_email(self):
        """Validate email uniqueness."""
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email is required.")
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        
        return email
    
    def clean_username(self):
        """Validate username."""
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError("Username is required.")
        
        # Check for invalid characters
        if not username.isalnum() and '_' not in username:
            raise ValidationError("Username can only contain letters, numbers, and underscores.")
        
        return username


def generate_strong_password(length=12):
    """Generate a strong password with uppercase, lowercase, digits, and special characters."""
    if length < 8:
        length = 8
    if length > 128:
        length = 128
    
    try:
        # Ensure at least one character from each category
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*"
        
        # Guarantee at least one from each category
        password = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(special)
        ]
        
        # Fill the rest randomly
        all_chars = lowercase + uppercase + digits + special
        for _ in range(length - 4):
            password.append(secrets.choice(all_chars))
        
        # Shuffle the password list
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    except Exception as e:
        logger.error(f"Error generating password: {e}")
        # Fallback to simple password generation
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(characters) for _ in range(length))


class UserAccountInline(admin.TabularInline):
    model = UserAccount
    fk_name = 'user'
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
                'employment_status',
                'account',
                'role'
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
        try:
            from rest_framework.authtoken.models import Token
            created_count = 0
            existing_count = 0
            errors = []
            
            for user in queryset:
                try:
                    token, created = Token.objects.get_or_create(user=user)
                    if created:
                        created_count += 1
                    else:
                        existing_count += 1
                except Exception as e:
                    errors.append(f"Error creating token for {user.username}: {str(e)}")
                    logger.error(f"Token creation error for user {user.username}: {e}")
            
            if errors:
                self.message_user(
                    request, 
                    f"Created {created_count} tokens, {existing_count} existed. Errors: {len(errors)}", 
                    level=messages.WARNING
                )
            else:
                self.message_user(
                    request, 
                    f"Generated {created_count} new tokens. {existing_count} users already had tokens."
                )
                
        except ImportError:
            self.message_user(
                request, 
                "Django REST Framework not installed. Cannot generate tokens.", 
                level=messages.ERROR
            )
        except Exception as e:
            logger.error(f"Error in generate_auth_tokens: {e}")
            self.message_user(
                request, 
                f"Error generating tokens: {str(e)}", 
                level=messages.ERROR
            )
    
    generate_auth_tokens.short_description = "Generate authentication tokens for selected users"
    
    def deactivate_users(self, request, queryset):
        """Admin action to deactivate selected users."""
        try:
            # Filter out already inactive users
            active_users = queryset.filter(is_active=True)
            if not active_users.exists():
                self.message_user(request, "No active users to deactivate.", level=messages.WARNING)
                return
            
            with transaction.atomic():
                updated = active_users.update(is_active=False, employment_status='inactive')
                # Update related UserAccount records
                UserAccount.objects.filter(user__in=active_users).update(is_active=False)
                
            self.message_user(request, f"{updated} users were deactivated.")
            logger.info(f"Admin {request.user.username} deactivated {updated} users")
            
        except Exception as e:
            logger.error(f"Error deactivating users: {e}")
            self.message_user(request, f"Error deactivating users: {str(e)}", level=messages.ERROR)
    
    deactivate_users.short_description = "Deactivate selected users"
    
    def activate_users(self, request, queryset):
        """Admin action to activate selected users."""
        try:
            # Filter out already active users
            inactive_users = queryset.filter(is_active=False)
            if not inactive_users.exists():
                self.message_user(request, "No inactive users to activate.", level=messages.WARNING)
                return
            
            with transaction.atomic():
                updated = inactive_users.update(is_active=True, employment_status='active')
                # Update related UserAccount records
                UserAccount.objects.filter(user__in=inactive_users).update(is_active=True)
                
            self.message_user(request, f"{updated} users were activated.")
            logger.info(f"Admin {request.user.username} activated {updated} users")
            
        except Exception as e:
            logger.error(f"Error activating users: {e}")
            self.message_user(request, f"Error activating users: {str(e)}", level=messages.ERROR)
    
    activate_users.short_description = "Activate selected users"
    
    def test_user_passwords(self, request, queryset):
        """Admin action to test password verification for debugging."""
        try:
            if not queryset.exists():
                self.message_user(request, "No users selected.", level=messages.WARNING)
                return
            
            debug_count = 0
            for user in queryset:
                try:
                    print(f"\n🔍 PASSWORD DEBUG for {user.username}:")
                    print(f"Database Hash: {user.password}")
                    print(f"Must Change Password: {user.must_change_password}")
                    print(f"Password Changed At: {user.password_changed_at}")
                    print(f"Is Active: {user.is_active}")
                    
                    # Test with a common password to demonstrate
                    test_password = "admin123"
                    if user.check_password(test_password):
                        print(f"✅ User {user.username} password is: {test_password}")
                    else:
                        print(f"❌ User {user.username} password is NOT: {test_password}")
                        print("💡 Use the original generated password from terminal output")
                    
                    debug_count += 1
                except Exception as e:
                    print(f"❌ Error debugging password for {user.username}: {e}")
                    logger.error(f"Password debug error for user {user.username}: {e}")
            
            self.message_user(request, f"Password debug info printed to terminal for {debug_count} users.")
            
        except Exception as e:
            logger.error(f"Error in test_user_passwords: {e}")
            self.message_user(request, f"Error testing passwords: {str(e)}", level=messages.ERROR)
    
    test_user_passwords.short_description = "🔍 Debug password info for selected users"
    
    def reset_passwords_admin_action(self, request, queryset):
        """Admin action to reset passwords for selected users."""
        try:
            if not queryset.exists():
                self.message_user(request, "No users selected.", level=messages.WARNING)
                return
            
            reset_count = 0
            errors = []
            
            print("\n" + "="*70)
            print("🔐 BULK PASSWORD RESET INITIATED")
            print("="*70)
            
            for user in queryset:
                try:
                    with transaction.atomic():
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
                        
                except Exception as e:
                    error_msg = f"Error resetting password for {user.username}: {str(e)}"
                    errors.append(error_msg)
                    logger.error(error_msg)
            
            print(f"\n✅ Successfully reset {reset_count} passwords")
            if errors:
                print(f"❌ Errors: {len(errors)}")
                for error in errors:
                    print(f"  - {error}")
            print("⚠️  All users must change passwords on next login")
            print("="*70 + "\n")
            
            if errors:
                self.message_user(
                    request, 
                    f"Reset {reset_count} passwords with {len(errors)} errors. Check terminal for details.",
                    level=messages.WARNING
                )
            else:
                self.message_user(
                    request, 
                    f"Reset passwords for {reset_count} users. New passwords printed to terminal."
                )
                
        except Exception as e:
            logger.error(f"Error in reset_passwords_admin_action: {e}")
            self.message_user(request, f"Error resetting passwords: {str(e)}", level=messages.ERROR)
    
    reset_passwords_admin_action.short_description = "🔐 Reset passwords for selected users"
    
    def get_full_name(self, obj):
        """Safely get full name."""
        try:
            return obj.get_full_name() if obj else "N/A"
        except Exception:
            return f"{obj.first_name} {obj.last_name}".strip() if obj else "N/A"
    get_full_name.short_description = 'Full Name'
    
    def account_count(self, obj):
        """Get account count with error handling."""
        try:
            count = 1 if obj and obj.account else 0
            return format_html(
                '<span style="color: {};">{}</span>',
                'green' if count > 0 else 'orange',
                count
            )
        except Exception as e:
            logger.error(f"Error getting account count for user {obj.username if obj else 'None'}: {e}")
            return format_html('<span style="color: red;">Error</span>')
    account_count.short_description = 'Has Account'
    
    def reset_password_button(self, obj):
        """Add reset password button for existing users."""
        try:
            if obj and obj.pk:
                url = reverse('admin:users_user_reset_password', args=[obj.pk])
                return format_html(
                    '<a class="button" href="{}">🔐 Reset Password</a>',
                    url
                )
            return "Save user first"
        except Exception as e:
            logger.error(f"Error creating reset password button: {e}")
            return "Error"
    reset_password_button.short_description = 'Password Actions'
    
    def save_model(self, request, obj, form, change):
        """Override to generate password for new users and send email."""
        try:
            if not change:  # Creating new user
                # Validate required fields
                if not obj.username:
                    raise ValidationError("Username is required")
                if not obj.email:
                    raise ValidationError("Email is required")
                
                with transaction.atomic():
                    # Generate strong password automatically
                    password = generate_strong_password()
                    obj.set_password(password)
                    obj.created_by = request.user
                    obj.must_change_password = True
                    
                    # Save the user first
                    super().save_model(request, obj, form, change)
                    
                    # Verify the save was successful
                    obj.refresh_from_db()
                    
                    # Print password to terminal with database verification
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
                        logger.error(f"Password verification failed for new user {obj.username}")
                    
                    # Send email with credentials
                    if obj.email:
                        try:
                            email_sent = EmailService.send_user_credentials_email(
                                user=obj,
                                password=password,
                                created_by=request.user
                            )
                            if email_sent:
                                print("✅ Email sent successfully to user's email address")
                                self.message_user(
                                    request,
                                    f"User '{obj.username}' created successfully and credentials sent to {obj.email}",
                                    level=messages.SUCCESS
                                )
                            else:
                                print("❌ Failed to send email - check email configuration")
                                self.message_user(
                                    request,
                                    f"User '{obj.username}' created but failed to send email to {obj.email}",
                                    level=messages.WARNING
                                )
                        except Exception as email_error:
                            logger.error(f"Email sending error for user {obj.username}: {email_error}")
                            print(f"❌ Email error: {email_error}")
                            self.message_user(
                                request,
                                f"User '{obj.username}' created but email failed: {str(email_error)}",
                                level=messages.WARNING
                            )
                    else:
                        print("⚠️  No email address provided - email not sent")
                        self.message_user(
                            request,
                            f"User '{obj.username}' created but no email address provided",
                            level=messages.WARNING
                        )
            else:
                # Save changes to existing user
                super().save_model(request, obj, form, change)
                
                # Verify the save was successful
                obj.refresh_from_db()
                print(f"✅ User updated: {obj.username} ({obj.get_full_name()})")
                
        except ValidationError as ve:
            logger.error(f"Validation error saving user: {ve}")
            raise
        except Exception as e:
            logger.error(f"Error saving user: {e}")
            print(f"❌ Error saving user: {e}")
            raise
    
    def get_urls(self):
        """Add custom admin URLs for password reset."""
        try:
            urls = super().get_urls()
            custom_urls = [
                path(
                    '<path:object_id>/reset_password/',
                    self.admin_site.admin_view(self.reset_password_view),
                    name='users_user_reset_password',
                ),
            ]
            return custom_urls + urls
        except Exception as e:
            logger.error(f"Error setting up custom URLs: {e}")
            return super().get_urls()
    
    def reset_password_view(self, request, object_id):
        """Admin view for resetting user password using Django sessions."""
        try:
            from django.shortcuts import render, redirect
            from django.contrib import messages
            from django.contrib.admin.utils import unquote
            from django.http import Http404
            
            user_id = unquote(object_id)
            try:
                user = User.objects.get(pk=user_id)
            except (User.DoesNotExist, ValueError):
                raise Http404("User not found")
            
            if request.method == 'POST':
                try:
                    with transaction.atomic():
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
                        
                        logger.info(f"Admin {request.user.username} reset password for user {user.username}")
                        
                        return redirect('admin:users_user_change', user.pk)
                        
                except Exception as e:
                    logger.error(f"Error resetting password for user {user.username}: {e}")
                    messages.error(request, f"Error resetting password: {str(e)}")
            
            context = {
                'title': f'Reset Password for {user.get_full_name()}',
                'user_obj': user,
                'opts': self.model._meta,
                'original': user,
                'has_change_permission': True,
            }
            
            return render(request, 'admin/users/user/reset_password.html', context)
            
        except Exception as e:
            logger.error(f"Error in reset_password_view: {e}")
            messages.error(request, f"Error accessing password reset: {str(e)}")
            return redirect('admin:users_user_changelist')
    
    def get_queryset(self, request):
        """Optimize queryset with proper error handling."""
        try:
            return super().get_queryset(request).select_related('account', 'role')
        except Exception as e:
            logger.error(f"Error in get_queryset: {e}")
            return super().get_queryset(request)


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
        """Safely display user information."""
        try:
            return obj.user.get_full_name() if obj and obj.user else "N/A"
        except Exception as e:
            logger.error(f"Error displaying user for UserAccount {obj.id if obj else 'None'}: {e}")
            return "Error"
    user_display.short_description = 'User'
    
    def account_display(self, obj):
        """Safely display account information."""
        try:
            if obj and obj.account:
                return f"{obj.account.account_name} ({obj.account.account_id})"
            return "N/A"
        except Exception as e:
            logger.error(f"Error displaying account for UserAccount {obj.id if obj else 'None'}: {e}")
            return "Error"
    account_display.short_description = 'Account'
    
    def onboarding_status_display(self, obj):
        """Safely display onboarding status."""
        try:
            if not obj:
                return "N/A"
            
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
        except Exception as e:
            logger.error(f"Error displaying onboarding status for UserAccount {obj.id if obj else 'None'}: {e}")
            return format_html('<span style="color: red;">Error</span>')
    onboarding_status_display.short_description = 'Onboarding'
    
    def offboarding_status_display(self, obj):
        """Safely display offboarding status."""
        try:
            if not obj:
                return "N/A"
            
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
        except Exception as e:
            logger.error(f"Error displaying offboarding status for UserAccount {obj.id if obj else 'None'}: {e}")
            return format_html('<span style="color: red;">Error</span>')
    offboarding_status_display.short_description = 'Offboarding'
    
    def save_model(self, request, obj, form, change):
        """Override to set created_by for new objects."""
        try:
            # Validate required relationships
            if not obj.user:
                raise ValidationError("User is required")
            if not obj.account:
                raise ValidationError("Account is required")
            
            with transaction.atomic():
                if not change:
                    obj.created_by = request.user
                
                # Save the object
                super().save_model(request, obj, form, change)
                
                # Verify the save was successful
                obj.refresh_from_db()
                
                action = "created" if not change else "updated"
                print(f"✅ UserAccount {action}: {obj.user.username} @ {obj.account.account_name}")
                logger.info(f"UserAccount {action} by {request.user.username}: {obj.user.username} @ {obj.account.account_name}")
                
        except ValidationError as ve:
            logger.error(f"Validation error saving UserAccount: {ve}")
            raise
        except Exception as e:
            logger.error(f"Error saving UserAccount: {e}")
            print(f"❌ Error saving UserAccount: {e}")
            raise
    
    def get_queryset(self, request):
        """Optimize queryset with proper error handling."""
        try:
            return super().get_queryset(request).select_related(
                'user', 'account', 'role'
            )
        except Exception as e:
            logger.error(f"Error in UserAccountAdmin get_queryset: {e}")
            return super().get_queryset(request)