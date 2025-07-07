from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'user-accounts', views.UserAccountViewSet)

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', views.login_view, name='login'),
    path('auth/first-login-password-change/', views.first_login_password_change, name='first_login_password_change'),
    path('auth/profile/', views.user_profile, name='user_profile'),
    
    # API endpoints
    path('api/', include(router.urls)),
]