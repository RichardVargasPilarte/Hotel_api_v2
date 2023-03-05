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
                  'cliente',
                  'habitacion',
                  'pago_choices',
                  'num_tarjeta'
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
                  'cliente',
                  'habitacion',
                  'cliente_id',
                  'habitacion_id',
                  'pago_choices',
                  'num_tarjeta',
                  'descripcion'
                )
    def create(self, validated_data):
        return Reserva.objects.create(**validated_data)
