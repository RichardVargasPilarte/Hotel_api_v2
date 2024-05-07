from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

# Create your models here.
class Usuario(AbstractUser):
    objects: models.Manager()
    direccion = models.CharField(max_length=250)
    telefono = models.CharField(max_length=9)
    eliminado = models.CharField(max_length=2, default='NO')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'Usuario'