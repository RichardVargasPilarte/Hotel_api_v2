
from unittest import result
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from apps.habitaciones.serializers import habitacionSerializerPOST, habitacionSerializer
# from django.forms.models import types_dict_convert
from apps.websocket.signals import types_dict_convert

from apps.habitaciones.models import Habitacion


@receiver(post_save, sender=Habitacion)
def announce_new_habitacion(sender, instance, created, **kwargs):
    if created:
        serializer = habitacionSerializer(instance)
        instance = dict(habitaciones=serializer.data)
        print (instance)
        instance = instance['habitaciones']
        print('se llamo al create')
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "cambios", dict(type="cambios", model="Habitacion",
                            event="c", data=instance)
        )


@receiver(post_save, sender=Habitacion)
def announce_update_habitacion(sender, instance, created, **kwargs):
    if not created:
        serializer = habitacionSerializerPOST(instance)
        instance = dict(habitaciones=serializer.data)
        instance = instance['habitaciones']
        channel_layer = get_channel_layer() # get the channel layer
        if instance['eliminado'] == 'SI':
            print('se llamo al soft-delete')
            async_to_sync(channel_layer.group_send)(
                "cambios", dict(type="cambios", model="Habitacion",
                                event="d", data=instance)
            )
        else:
            print('se llamo al update')
            async_to_sync(channel_layer.group_send)(
                "cambios", dict(type="cambios", model="Habitacion",
                                event="u", data=instance)

                # event="u", data=types_dict_convert(instance))
                # buscar como hacer que la instancia de model_to_dict convierta a decimal
            )


@receiver(post_delete, sender=Habitacion)
def announce_del_habitacion(sender, instance, **kwargs):
    print('se llamo al delete')
    dict_obj = types_dict_convert(instance)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "cambios", dict(type="cambios", model="Habitacion",
                        event="d", data=types_dict_convert(instance))
    )
