from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, password, **extra_fields)
        return user
class User(AbstractUser,PermissionsMixin):
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('executor', 'Исполнитель'),
        ('manager', 'Менеджер'),
        ('admin', 'Администратор'),
    ]
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    login = models.CharField(max_length=150)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['login']

    def __str__(self):
        return self.email

class Equipment(models.Model):
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class RepairRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('in_progress', 'В работе'),
        ('completed', 'Выполнено'),
    ]

    number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    fault_type = models.CharField(max_length=50)
    description = models.TextField()
    client = models.ForeignKey(User, on_delete=models.CASCADE,related_name='client_request')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='executor_request')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='manager_request')
    completion_date = models.DateField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"№{self.number} - {self.client_name.name}"