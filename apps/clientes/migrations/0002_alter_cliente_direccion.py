# Generated by Django 4.0 on 2024-01-13 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='direccion',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
    ]
