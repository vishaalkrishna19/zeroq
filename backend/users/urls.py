from django.urls import path
from . import views

urlpatterns = [
    # API endpoints
    path('api/login/', views.login_api, name='login_api'),
    path('api/logout/', views.logout_api, name='logout_api'),
    path('api/change-password/', views.change_password_api, name='change_password_api'),
    path('api/profile/', views.profile_api, name='profile_api'),
    
    # Web views
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login_web'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]
