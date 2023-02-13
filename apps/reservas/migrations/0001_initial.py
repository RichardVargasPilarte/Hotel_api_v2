# Generated by Django 4.0 on 2023-02-13 23:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('habitaciones', '0003_habitacion_activo'),
        ('clientes', '0001_initial'),
        ('usuarios', '0002_alter_usuarios_groups_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fecha_inicio', models.DateField(auto_now=True)),
                ('fecha_fin', models.DateField()),
                ('tipo_pago', models.CharField(max_length=8)),
                ('eliminado', models.CharField(default='NO', max_length=2)),
                ('nombre_cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clientes.cliente')),
                ('nombre_habitacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='habitaciones.habitacion')),
                ('nombre_usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='usuarios.usuarios')),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
                'db_table': 'Reserva',
            },
        ),
    ]
