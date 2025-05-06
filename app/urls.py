from django.urls import path

from app.views import RegistrationView
from .views import *

urlpatterns = [
    path("auth/register/", RegistrationView.as_view(), name="auth_register"),
    path('auth/register/', RegistrationView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

]