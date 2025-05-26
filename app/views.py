from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status
from rest_framework.decorators import action

from app.models import User
from app.serializers import RegistrationSerializer
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from rest_framework import viewsets
from .models import RepairRequest
from .serializers import RepairRequestSerializer
from .filters import RepairRequestFilter



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

class RepairRequestViewSet(viewsets.ModelViewSet):
    queryset = RepairRequest.objects.all()
    serializer_class = RepairRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = RepairRequestFilter

    def get_queryset(self):
        # Фильтрация по ролям:
        user = self.request.user
        if user.is_executor:
            return self.queryset.filter(assigned_to=user)
        elif user.is_client:
            return self.queryset.filter(client=user)
        return self.queryset

    @action(detail=True, methods=[ 'post' ])
    def change_status(self, request, pk=None):
        request_obj = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(RepairRequest.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=400)

        request_obj.status = new_status
        request_obj.save()
        return Response({"status": "updated"})