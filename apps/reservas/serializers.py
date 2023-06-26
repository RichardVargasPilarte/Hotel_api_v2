from rest_framework import serializers
from .models import Reserva


class reservaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserva
        fields = ('id',
                  'fecha_inicio',
                  'fecha_fin',
                  'tipo_pago',
                  'eliminado',
                  'cliente_id',
                  'habitacion_id',
                  )
        depth = 1


class reservaSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ('id',
                  'fecha_inicio',
                  'fecha_fin',
                  'tipo_pago',
                  'eliminado',
                  'cliente_id',
                  'habitacion_id',
                  'descripcion'
                )
    def create(self, validated_data):
        return Reserva.objects.create(**validated_data)
