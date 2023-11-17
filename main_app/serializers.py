from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, password_validation
from rest_framework.authtoken.models import Token
from rest_framework import serializers
import main_app.models as _models



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


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        # authenticate recibe las credenciales, si son válidas devuelve el objeto del usuario
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError(
                'Las credenciales no son válidas')

        if not user.is_active:
            raise serializers.ValidationError('user deactivated')

        # Guardar el usuario en el contexto para posteriormente en create recuperar el token
        self.context['user'] = user
        return super().validate(data)

    def create(self, data):
        """Generar o recuperar token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key

class UserModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = _models.User
        exclude = (
            'password',
            'last_login',
            'user_permissions',
        )