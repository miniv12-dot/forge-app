from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 1. The New Public Homepage
    path('', TemplateView.as_view(template_name='landing.html'), name='home'),
    
    # 2. The Internal App Dashboard
    path('app/', TemplateView.as_view(template_name='dashboard.html'), name='app_dashboard'),
    
    path('admin/', admin.site.urls),
    path('', include('core.urls')), 
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]