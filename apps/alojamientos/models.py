from django.db import models

# Create your models here.

class Alojamiento(models.Model):
    objects: models.Manager()
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    tiempo_estadia = models.PositiveIntegerField(default=0)
    eliminado = models.CharField(max_length=2, default='NO')

    class Meta:
        verbose_name = 'Alojamiento'
        verbose_name_plural = 'Alojamientos'
        db_table = 'Alojamiento'
