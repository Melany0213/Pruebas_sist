from rest_framework import serializers
import main_app.models as _models
from django.contrib.auth.models import Group


class UserSerializer(serializers.ModelSerializer):
    """SERIALIZA EL OBJETO DE PERFIL DE USUARIO"""

    class Meta:
        model = _models.User
        fields = ['id', 'name', 'email', 'apellidos',
                  'password', "groups"]
        extra_kwargs = {
            'password': {
                "write_only": True,
                "style": {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Crear y retorna un nuevo usuario"""
        user = _models.User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            apellidos=validated_data["apellidos"],
            password=validated_data["password"],
            groups=validated_data['groups'],
        )

        return user

    def update(self, instance, validated_data):
        """Actualiza un usuario"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ["id", "name"]
        extra_kwargs = {
            'name': {
                "read_only": True,
            }
        }
