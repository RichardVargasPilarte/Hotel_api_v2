# Generated by Django 4.0 on 2023-03-06 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0001_initial'),
        ('habitaciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(auto_now=True)),
                ('fecha_fin', models.DateField()),
                ('tipo_pago', models.CharField(max_length=8)),
                ('eliminado', models.CharField(default='NO', max_length=2)),
                ('pago_choices', models.CharField(choices=[('Tarjeta Debito', 'TARJETA DEBITO'), ('Tarjeta Credito', 'TARJETA CREDITO'), ('Efectivo', 'EFECTIVO')], default='Efectivo', max_length=30)),
                ('num_tarjeta', models.CharField(max_length=25, null=True)),
                ('descripcion', models.CharField(max_length=150)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clientes.cliente')),
                ('habitacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='habitaciones.habitacion')),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
                'db_table': 'Reserva',
            },
        ),
    ]
