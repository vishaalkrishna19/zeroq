from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .models import User
from .forms import ForcePasswordResetForm, UserLoginForm, PasswordResetRequestForm
from .services import EmailService


@csrf_protect
@never_cache
def user_login(request):
    """
    Custom login view that handles both username and email login.
    """
    if request.user.is_authenticated:
        # If user is already logged in but needs password reset
        if getattr(request.user, 'must_change_password', False):
            return redirect('auth:force_password_reset')
        return redirect('admin:index')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Update last login IP
            user.last_login_ip = get_client_ip(request)
            user.save(update_fields=['last_login_ip'])
            
            # Log the user in
            login(request, user)
            
            # Check if user needs to change password
            if user.must_change_password:
                messages.info(
                    request,
                    f'Welcome {user.get_full_name() or user.username}! '
                    'For security, please change your password before proceeding.'
                )
                return redirect('auth:force_password_reset')
            
            # Successful login
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            
            # Redirect to next page or admin
            next_page = request.GET.get('next', reverse('admin:index'))
            return HttpResponseRedirect(next_page)
    else:
        form = UserLoginForm()
    
    context = {
        'form': form,
        'title': 'Login to ZeroQueue',
    }
    return render(request, 'auth/login.html', context)


@login_required
def user_logout(request):
    """
    Custom logout view.
    """
    user_name = request.user.get_full_name() or request.user.username
    logout(request)
    messages.success(request, f'You have been successfully logged out. See you next time!')
    return redirect('auth:login')


@method_decorator([csrf_protect, never_cache], name='dispatch')
class ForcePasswordResetView(LoginRequiredMixin, FormView):
    """
    View for forced password reset on first login.
    """
    template_name = 'auth/force_password_reset.html'
    form_class = ForcePasswordResetForm
    
    def dispatch(self, request, *args, **kwargs):
        # If user doesn't need to change password, redirect to admin
        if not getattr(request.user, 'must_change_password', False):
            return redirect('admin:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Save the new password
        user = form.save()
        
        # Update password change timestamp
        user.password_changed_at = timezone.now()
        user.save(update_fields=['password_changed_at'])
        
        messages.success(
            self.request,
            'Your password has been successfully changed! Please log in with your new password.'
        )
        
        # Log the password change
        print(f"\n🔐 FORCED PASSWORD RESET COMPLETED")
        print(f"User: {user.username} ({user.get_full_name()})")
        print(f"Changed at: {timezone.now()}")
        print(f"IP: {get_client_ip(self.request)}\n")
        
        # Logout the user and redirect to admin login
        from django.contrib.auth import logout
        logout(self.request)
        return redirect('/admin/login/')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Change Your Password',
            'user': self.request.user,
        })
        return context


class PasswordResetRequestView(FormView):
    """
    View for requesting password reset via email.
    """
    template_name = 'auth/password_reset_request.html'
    form_class = PasswordResetRequestForm
    
    def form_valid(self, form):
        user = form.get_user()
        
        # Generate new temporary password
        import secrets
        import string
        temp_password = ''.join(secrets.choice(
            string.ascii_letters + string.digits + "!@#$%^&*"
        ) for _ in range(12))
        
        # Set temporary password and force change
        user.set_password(temp_password)
        user.must_change_password = True
        user.save()
        
        # Send email with new credentials
        email_sent = EmailService.send_user_credentials_email(
            user=user,
            password=temp_password,
            created_by=None  # Self-requested
        )
        
        if email_sent:
            messages.success(
                self.request,
                f'A new temporary password has been sent to {user.email}. '
                'Please check your email and follow the instructions to set your new password.'
            )
        else:
            messages.error(
                self.request,
                'Failed to send reset email. Please contact support for assistance.'
            )
        
        return redirect('auth:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reset Your Password'
        return context


class PasswordResetFromEmailView(FormView):
    """
    View for password reset accessed from email link with token.
    """
    template_name = 'auth/password_reset_from_email.html'
    form_class = ForcePasswordResetForm
    
    def dispatch(self, request, *args, **kwargs):
        # Get user from token (user ID in this case)
        token = request.GET.get('token')
        if not token:
            messages.error(request, 'Invalid or missing reset token.')
            return redirect('auth:login')
        
        try:
            self.user = User.objects.get(id=token, is_active=True)
        except User.DoesNotExist:
            messages.error(request, 'Invalid reset token or user not found.')
            return redirect('auth:login')
        
        # If user doesn't need password change, redirect to login
        if not self.user.must_change_password:
            messages.info(request, 'Your password has already been changed. Please log in.')
            return redirect('auth:login')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs
    
    def form_valid(self, form):
        # Save the new password
        user = form.save()
        
        # Update password change timestamp
        user.password_changed_at = timezone.now()
        user.save(update_fields=['password_changed_at'])
        
        messages.success(
            self.request,
            f'Welcome {user.get_full_name() or user.username}! '
            'Your password has been successfully changed. Please log in with your new password.'
        )
        
        # Log the password change
        print(f"\n🔐 EMAIL PASSWORD RESET COMPLETED")
        print(f"User: {user.username} ({user.get_full_name()})")
        print(f"Changed at: {timezone.now()}")
        print(f"IP: {get_client_ip(self.request)}\n")
        
        return redirect('/admin/login/')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Set Your New Password',
            'user': self.user,
            'from_email': True,
        })
        return context


def get_client_ip(request):
    """
    Get the client IP address from request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AuthHomeView(TemplateView):
    """
    Home view for authentication system.
    """
    template_name = 'auth/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ZeroQueue Authentication'
        return context 