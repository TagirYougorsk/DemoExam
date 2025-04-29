from django.urls import path

from app.views import RegistrationView

urlpatterns = [
path("auth/register/", RegistrationView.as_view(), name="auth_register"),

]