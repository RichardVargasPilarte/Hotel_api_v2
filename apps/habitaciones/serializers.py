from rest_framework import serializers
from .models import Habitacion

class habitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitacion
        fields = (  'id',
                    'nombre',
                    'descripcion',
                    'precio',
                    'numero_personas',
                    'eliminado',
                    'alojamiento_id',
                    'estado'
                )
        depth = 1

class habitacionSerializerPOST(serializers.ModelSerializer):

    class Meta:
        model = Habitacion
        fields = (  'id',
                    'nombre',
                    'descripcion',
                    'precio',
                    'numero_personas',
                    'eliminado',
                    'alojamiento_id',
                    'estado'
                )
    def create(self, validated_data):
        return Habitacion.objects.create(**validated_data)

