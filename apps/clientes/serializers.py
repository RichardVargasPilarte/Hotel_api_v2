from rest_framework import serializers
from .models import Cliente

class clienteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cliente
        fields = ('id',
                    'nombre',
                    'apellido',
                    'direccion',
                    'telefono',
                    'email',
                    'tipo_identificacion',
                    'num_identificacion',
                    'eliminado'
                )