from django.db import models

# Create your models here.
class Cliente(models.Model):
    objects: models.Manager()
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=250)
    telefono = models.CharField(max_length=8)
    email = models.CharField(max_length=50)
    eliminado = models.CharField(max_length=2, default='NO')
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'Cliente'