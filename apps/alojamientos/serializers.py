from rest_framework import serializers
from .models import Alojamiento

class alojamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alojamiento
        fields = ('id',
                    'nombre',
                    'descripcion',
                    'tiempo_estadia',
                    'eliminado'
                )
