from django.db import models

# Create your models here.
from apps.clientes.models import Cliente
from apps.habitaciones.models import Habitacion
from apps.usuarios.models import Usuario

PAGO_CHOICES = (
    ("Tarjeta Debito","TARJETA DEBITO"),
    ("Tarjeta Credito","TARJETA CREDITO"),
    ("Efectivo","EFECTIVO")
)

class Reserva(models.Model):
    objects: models.Manager()
    fecha_inicio = models.DateField(auto_now=True)
    fecha_fin = models.DateField()
    tipo_pago = models.CharField(max_length=8)
    eliminado = models.CharField(max_length=2, default='NO')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.PROTECT)
    pago_choices = models.CharField(choices=PAGO_CHOICES, max_length=30,default='Efectivo')
    num_tarjeta = models.CharField(max_length=25, null=True)
    descripcion = models.CharField(max_length=150)
    # created_by = models.ForeignKey(Usuario, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        db_table = 'Reserva'