from django.urls import path
from . import auth_views

app_name = 'auth'

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.user_login, name='login'),
    path('logout/', auth_views.user_logout, name='logout'),
    
    # Password reset URLs
    path('reset-password/', auth_views.PasswordResetFromEmailView.as_view(), name='reset_password'),
    path('force-password-reset/', auth_views.ForcePasswordResetView.as_view(), name='force_password_reset'),
    path('request-password-reset/', auth_views.PasswordResetRequestView.as_view(), name='request_password_reset'),
    
    # Home
    path('', auth_views.AuthHomeView.as_view(), name='home'),
] 