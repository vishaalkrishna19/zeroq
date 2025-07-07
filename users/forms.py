from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


class ForcePasswordResetForm(forms.Form):
    """
    Form for forced password reset on first login.
    """
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your current password',
            'autocomplete': 'current-password'
        }),
        help_text="Enter the temporary password you received via email."
    )
    
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your new password',
            'autocomplete': 'new-password'
        }),
        help_text="Your password must be at least 8 characters long and contain a mix of letters, numbers, and symbols."
    )
    
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your new password',
            'autocomplete': 'new-password'
        }),
        help_text="Enter the same password as before, for verification."
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                "Your current password was entered incorrectly. Please enter it again.",
                code='password_incorrect',
            )
        return old_password
    
    def clean_new_password2(self):
        """
        Validate that the two password inputs match.
        """
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    "The two password fields didn't match.",
                    code='password_mismatch',
                )
        return password2
    
    def clean_new_password1(self):
        """
        Validate the new password using Django's password validators.
        """
        password1 = self.cleaned_data.get('new_password1')
        if password1:
            validate_password(password1, self.user)
        return password1
    
    def save(self, commit=True):
        """
        Save the new password and clear the must_change_password flag.
        """
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.must_change_password = False
        if commit:
            self.user.save()
        return self.user


class UserLoginForm(forms.Form):
    """
    Custom login form for users.
    """
    username = forms.CharField(
        label="Username or Email",
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username or email',
            'autocomplete': 'username'
        })
    )
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password'
        })
    )
    
    remember_me = forms.BooleanField(
        label="Remember me",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username is not None and password:
            # Try to find user by username or email
            try:
                if '@' in username:
                    user = User.objects.get(email=username, is_active=True)
                else:
                    user = User.objects.get(username=username, is_active=True)
            except User.DoesNotExist:
                raise ValidationError(
                    "Please enter a correct username/email and password. Note that both fields may be case-sensitive."
                )
            
            if not user.check_password(password):
                raise ValidationError(
                    "Please enter a correct username/email and password. Note that both fields may be case-sensitive."
                )
            
            self.user_cache = user
        
        return self.cleaned_data
    
    def get_user(self):
        return self.user_cache


class PasswordResetRequestForm(forms.Form):
    """
    Form for requesting password reset via email.
    """
    email = forms.EmailField(
        label="Email Address",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email'
        }),
        help_text="Enter the email address associated with your account."
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            self.user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise ValidationError("No active user found with this email address.")
        return email
    
    def get_user(self):
        return getattr(self, 'user', None) 