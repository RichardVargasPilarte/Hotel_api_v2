from django.db import models
from django.db.models.deletion import PROTECT
from apps.alojamientos.models import Alojamiento

# Create your models here.
class Habitacion(models.Model):
    objects: models.Manager()
    nombre = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=150)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    numero_personas = models.PositiveIntegerField(default=0)
    activo = models.CharField(max_length=17, default='Disponible')
    eliminado = models.CharField(max_length=2, default='NO')
    nombre_alojamiento = models.ForeignKey(Alojamiento, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Habitacion'
        verbose_name_plural = 'Habitaciones'
        db_table = 'Habitacion'