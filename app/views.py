from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status
from app.models import User
from app.serializers import RegistrationSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *



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

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "Пользователь успешно зарегистрирован",
            "user": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # В реальном проекте нужно добавить логику отзыва токенов
        return Response({"message": "Успешный выход"}, status=status.HTTP_200_OK)