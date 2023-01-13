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
                  'nombre_cliente',
                  'nombre_habitacion',
                  'nombre_usuario'
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
                  'nombre_cliente',
                  'nombre_habitacion',
                  'nombre_usuario',
                  'nombre_cliente_id',
                  'nombre_habitacion_id',
                  'nombre_usuario_id',
                )
    def create(self, validated_data):
        return Reserva.objects.create(**validated_data)
