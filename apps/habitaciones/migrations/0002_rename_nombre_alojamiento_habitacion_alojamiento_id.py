# Generated by Django 4.0 on 2023-06-15 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habitaciones', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='habitacion',
            old_name='nombre_alojamiento',
            new_name='alojamiento_id',
        ),
    ]
