from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.contrib import messages
from .models import User
from .utils import generate_random_password, send_welcome_email

class UserCreationForm(forms.ModelForm):
    """Form for creating new users with generated passwords"""
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
    
    def save(self, commit=True):
        # Create user instance
        user = super().save(commit=False)
        
        # Generate random password
        password = generate_random_password()
        user.set_password(password)
        user.password_change_required = True
        user.password_changed = False
        
        if commit:
            user.save()
            
            # Print password to console (forced output)
            print("=" * 50)
            print(f"NEW USER CREATED:")
            print(f"Email: {user.email}")
            print(f"Generated Password: {password}")
            print(f"Name: {user.first_name} {user.last_name}")
            print("=" * 50)
            
            # Try to send welcome email
            try:
                send_welcome_email(user, password)
                print(f"✓ Welcome email sent to {user.email}")
            except Exception as e:
                print(f"✗ Failed to send email to {user.email}: {str(e)}")
        
        return user

class UserChangeForm(forms.ModelForm):
    """Form for updating users"""
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text="Raw passwords are not stored, so there is no way to see this "
                  "user's password, but you can change the password using "
                  "<a href=\"../password/\">this form</a>."
    )
    
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'is_active', 'is_staff')

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'password_changed', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'password_changed', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Password Management', {'fields': ('password_changed', 'password_change_required')}),
    )
    
    add_fieldsets = (
        ('User Information', {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name'),
            'description': 'A random password will be generated automatically and printed to the console.'
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')
    
    def save_model(self, request, obj, form, change):
        """Override save_model to show success message"""
        super().save_model(request, obj, form, change)
        
        if not change:  # Only for new users
            messages.success(
                request, 
                f'User {obj.email} created successfully! '
                f'Password has been generated and printed to the console. '
                f'Please check your terminal.'
            )
