from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

no_inv_regex = RegexValidator(
    '^(MB-|MB)\d{6,}$', 'Número de inventario no valido')
name_regex = RegexValidator('^[A-Za-záéíóúñ\s]*$',
                            "El/Los nombre(s) no puede poseer caracteres extraños")
apellidos_regex = RegexValidator('^[A-Za-záéíóúñ\s]*$',
                                 "El/Los apellido(s) no puede poseer caracteres extraños")
local_regex = RegexValidator(
    '^[A-Za-záéíóúñ\d\s]*$', "El nombre no puede poseer caracteres extraños")

no_serie_regex = RegexValidator('^[A-Za-z0-9_-]{5,}$',
                                "El número de serie es invalido, debe contener al menos 5 caracteres y no contener espacios")


class UserManager(BaseUserManager):
    """Manager para usuarios"""

    def create_user(self, email, name, apellidos, password=None, **extra_fields):
        """Crea un nuevo Usuario"""
        if not email:
            raise ValueError("El usuario debe tener un email")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,
                          apellidos=apellidos, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, apellidos, password, role=None,**extra_fields):
        user = self.create_user(email, name, apellidos,
                                password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True

        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Modelo BD para Users"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, validators=[name_regex])
    apellidos = models.CharField(max_length=255, validators=[apellidos_regex])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'apellidos']

    def get_full_name(self):
        return "%s %s" % (self.name, self.apellidos)

    def get_short_name(self):
        return self.name

    def __str__(self):
        """Return String"""
        return self.email
