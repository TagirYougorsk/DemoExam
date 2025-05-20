from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RepairRequestViewSet

from app.views import RegistrationView
from .views import *

urlpatterns = [
    path("auth/register/", RegistrationView.as_view(), name="auth_register"),
    path('auth/register/', RegistrationView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),


]
router = DefaultRouter()
router.register(r'repair-requests', RepairRequestViewSet, basename='repair-request')

urlpatterns = [
    path('api/', include(router.urls)),
]
