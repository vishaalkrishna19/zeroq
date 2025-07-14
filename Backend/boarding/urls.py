from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JourneyTemplateViewSet, JourneyStepViewSet, 
    JourneyInstanceViewSet, JourneyStepInstanceViewSet,analytics_dashboard
)

router = DefaultRouter()
router.register(r'templates', JourneyTemplateViewSet, basename='journeytemplate')
router.register(r'steps', JourneyStepViewSet, basename='journeystep')
router.register(r'instances', JourneyInstanceViewSet, basename='journeyinstance')
router.register(r'step-instances', JourneyStepInstanceViewSet, basename='journeystepinstance')

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', analytics_dashboard, name='boarding-analytics'),

]
