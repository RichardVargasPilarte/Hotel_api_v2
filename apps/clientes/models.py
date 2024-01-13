from django.db import models

TIPO_IDENTIFICACION_CHOICES = (
    ("Cedula","CEDULA"),
    ("Pasaporte","PASAPORTE")
)

# Create your models here.
class Cliente(models.Model):
    objects: models.Manager()
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=250, null=True, default=None, blank=True) 
    telefono = models.CharField(max_length=8)
    email = models.CharField(max_length=50, null=True)
    tipo_identificacion = models.CharField(choices=TIPO_IDENTIFICACION_CHOICES ,max_length=9)
    num_identificacion = models.CharField(max_length=30, default='000-000000-0000A')
    eliminado = models.CharField(max_length=2, default='NO')
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'Cliente'