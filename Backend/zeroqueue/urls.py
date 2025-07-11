"""zeroqueue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  
from users.views import csrf, CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', CustomLoginView.as_view(), name='custom_login'),
    path('api/auth/csrf/', csrf, name='csrf'),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/users/', include('users.urls')),
    path('api/roles/', include('roles_permissions.urls')),
    path('api/boarding/', include('boarding.urls')),
    path('accounts/', include('allauth.urls')),
]