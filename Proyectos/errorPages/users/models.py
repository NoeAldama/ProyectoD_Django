from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=255, blank=True, null=True)

    # Campos adicionales
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    control_number = models.CharField(max_length=20, unique=True)
    age = models.PositiveIntegerField()
    tel = models.CharField(max_length=15)
    join_date = models.DateTimeField(default=now)

    # Campos requeridos por Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Especificar el manager
    objects = CustomUserManager()

    # Identificador principal para el usuario
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'control_number', 'age', 'tel']

    def __str__(self):
        return self.email
