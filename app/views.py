from django.shortcuts import render, redirect
from rest_framework import generics, permissions

from app.models import User
from app.serializers import RegistrationSerializer

from django.contrib.auth import authenticate, login, logout

# Create your views here.
class RegistrationView(generics.CreateAPIView):
    serializer_class =  RegistrationSerializer
    permission_classes = (permissions.AllowAny,)

def register_page(request):
    if request.method == "POST":
        data = request.POST
        if not User.objects.filter(email=data["email"]).exists():
            user = User.objects.create_user(
                email=data["email"],
                login=data["login"],
                name=data["name"],
                phone=data.get("phone", ""),
                password=data["password"],
                role="client"
            )
            login(request, user)
            return redirect("/")
    return render(request, "registration.html")