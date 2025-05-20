from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from app.models import User
from .models import RepairRequest, Equipment

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'login', 'name', 'phone', 'password', 'password2', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'default': 'client'}
        }

    def validate(self, data):
        if data[ 'password' ] != data[ 'password2' ]:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password2')
        user = User.objects.create_user(password=password,**validated_data)
        return user

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Пароль должен содержать минимум 8 символов")
        return value

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Добавляем кастомные поля в токен
        token['role'] = user.role
        token['email'] = user.email
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'role']


class EquipmentShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = [ 'id', 'name', 'serial_number' ]


class RepairRequestSerializer(serializers.ModelSerializer):
    equipment = EquipmentShortSerializer(read_only=True)
    equipment_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipment.objects.all(),
        source='equipment',
        write_only=True
    )

    class Meta:
        model = RepairRequest
        fields = '__all__'
        read_only_fields = ('number', 'created_at', 'client', 'status')

    def create(self, validated_data):
        # Автоматически назначаем текущего пользователя как клиента
        validated_data[ 'client' ] = self.context[ 'request' ].user
        return super().create(validated_data)