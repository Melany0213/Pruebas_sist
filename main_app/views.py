from django.shortcuts import render
from rest_framework import viewsets, filters
import main_app.models as _models
import rest_framework.permissions as _permissions
from main_app import serializers
from django.contrib.auth.models import Group


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
