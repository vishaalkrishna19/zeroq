from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponseRedirect


class ForcePasswordResetMiddleware:
    """
    Middleware to force users to reset their password if must_change_password is True.
    Redirects users to password reset page after login if they haven't changed their password.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs that don't require password reset check
        self.exempt_paths = [
            '/admin/login/',              # Allow Django admin login
            '/admin/logout/',
            '/admin/password_change/',
            '/admin/jsi18n/',
            '/auth/reset-password/',
            '/auth/login/',
            '/auth/logout/',
            '/api/auth/logout/',
            '/api/auth/password/reset/',
            '/static/',
            '/media/',
        ]
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip if user is not authenticated
        if not request.user.is_authenticated:
            return None
        
        # Skip if user doesn't need to change password
        if not getattr(request.user, 'must_change_password', False):
            return None
        
        # Skip for superusers (they can access admin normally)
        if getattr(request.user, 'is_superuser', False):
            return None
        
        # Skip if this is an exempt path
        path = request.path
        for exempt_path in self.exempt_paths:
            if path.startswith(exempt_path):
                return None
        
        # Skip for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return None
        
        # Skip for API requests
        if path.startswith('/api/'):
            return None
        
        # If user must change password, redirect to password reset
        messages.warning(
            request,
            'You must change your password before continuing. Please set a new password below.'
        )
        return HttpResponseRedirect(reverse('auth:force_password_reset'))


class LoginRedirectMiddleware:
    """
    Middleware to handle first login and redirect to appropriate page.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Check if user just logged in and needs password reset
        # Only redirect after successful login to /admin/, not during login process
        if (request.user.is_authenticated and 
            getattr(request.user, 'must_change_password', False) and 
            request.path == '/admin/' and 
            request.method == 'GET' and
            not request.user.is_superuser):  # Don't redirect superusers
            
            messages.info(
                request,
                f'Welcome {request.user.get_full_name() or request.user.username}! '
                'For security, please change your password before proceeding.'
            )
            return HttpResponseRedirect(reverse('auth:force_password_reset'))
        
        return None 