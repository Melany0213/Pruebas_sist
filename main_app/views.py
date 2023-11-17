from django.shortcuts import render
from rest_framework import viewsets, filters, generics, status
import main_app.models as _models
import rest_framework.permissions as _permissions
from rest_framework.response import Response
from main_app import serializers
from django.contrib.auth.models import Group
from .serializers import UserLoginSerializer, UserModelSerializer
from certifications.models import Estudiante
from certifications.serializer import EstudianteSerializer

class UserViewSet(viewsets.ModelViewSet):
    """Genera el CRUD de los usuarios"""
    serializer_class = serializers.UserSerializer
    queryset = _models.User.objects.all()

    permission_classes = (_permissions.IsAuthenticated,
                          _permissions.DjangoModelPermissions)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email', 'apellidos')


class GroupViewSet(viewsets.ModelViewSet):
    """"Genera CRUD de los GRUPOS de permisos"""
    permission_classes = (_permissions.IsAuthenticated,
                          _permissions.DjangoModelPermissions,)
    serializer_class = serializers.GroupSerializer
    queryset = Group.objects.all()

class LoginView(generics.GenericAPIView):

    serializer_class = UserLoginSerializer
    permission_classes = []

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'access_token': token,
            'user': UserModelSerializer(instance=user).data,
        }
        estudiante = Estudiante.objects.filter(user=user)
        if(estudiante.exists()):
            return Response(data, status=status.HTTP_201_CREATED)