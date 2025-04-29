from rest_framework import serializers

from app.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('email', 'login', 'name','phone','password', 'role')
        extra_kwargs = {'role': {'default': 'client'}}
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password,**validated_data)
        return user
