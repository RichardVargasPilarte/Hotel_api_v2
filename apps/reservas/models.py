from django.db import models

# Create your models here.
from apps.clientes.models import Cliente
from apps.habitaciones.models import Habitacion
from apps.usuarios.models import Usuarios

class Reserva(models.Model):
    objects: models.Manager()
    nombre = models.CharField(max_length=50)
    # fecha_inicio = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateField(auto_now=True)
    fecha_fin = models.DateField()
    tipo_pago = models.CharField(max_length=8)
    eliminado = models.CharField(max_length=2, default='NO')
    nombre_cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    nombre_habitacion = models.ForeignKey(Habitacion, on_delete=models.PROTECT)
    nombre_usuario = models.ForeignKey(Usuarios, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        db_table = 'Reserva'