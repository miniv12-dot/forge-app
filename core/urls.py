from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailyLogViewSet, TopicCategoryViewSet, CommunityPostViewSet

router = DefaultRouter()
router.register(r'logs', DailyLogViewSet, basename='dailylog')

# Add the new community routes
router.register(r'categories', TopicCategoryViewSet, basename='category')
router.register(r'community', CommunityPostViewSet, basename='community')

urlpatterns = [
    path('api/', include(router.urls)),
]