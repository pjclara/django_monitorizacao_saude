from typing import Any
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        if not extra_fields:
            raise ValueError('The Extra Fields must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
    def update(self, **kwargs: Any) -> int:
        return super().update(**kwargs) 
    
TYPE_USERS = [
        ('profissional', 'Profissional'),
        ('paciente', 'Paciente'),
        ('admin', 'Admin')
    ]
    
class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    mobile_phone = models.CharField(max_length=9, blank=True, null=True)
    health_number = models.CharField(max_length=9, blank=True, null=True)
    taxpayer_number = models.CharField(max_length=9, blank=True, null=True)
    type_user = models.CharField(max_length=255, choices=TYPE_USERS, default='profissional')
    groups = models.ManyToManyField('auth.Group', related_name='users', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
