from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserAccountViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
router.register(r'accounts', UserAccountViewSet, basename='useraccount')

urlpatterns = [
    path('', include(router.urls)),
]