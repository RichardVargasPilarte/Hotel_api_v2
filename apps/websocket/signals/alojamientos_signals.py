from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from apps.websocket.signals import types_dict_convert

from apps.alojamientos.models import Alojamiento


@receiver(post_save, sender=Alojamiento)
def announce_new_alojamiento(sender, instance, created, **kwargs):
    print(model_to_dict(instance))
    entity = model_to_dict(instance)
    if created:
        print('se llamo al create')
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "cambios", {"type": "chat_message", "message": {
                'model': 'Alojamiento',
                'event': 'c',
                'data': entity
            }}
        )
    else:
        print('se llamo al update')
        dict_obj = types_dict_convert(instance)
        channel_layer = get_channel_layer()
        print(get_channel_layer())
        if instance.eliminado == 'SI':
            print('se llamo al soft-delete')
            # async_to_sync(channel_layer.group_send)(
            #     "cambios", dict(type="chat_message", model="Alojamiento",
            #                     event="d", data=dict_obj)
            # )
            async_to_sync(channel_layer.group_send)(
                "cambios", {"type": "chat_message", "message": {
                    'model': 'Alojamiento',
                    'event': 'd',
                    'data': entity
                }}
            )
            print('enviado delete a cambios channel', channel_layer)
        else:
            async_to_sync(channel_layer.group_send)(
                "cambios", {"type": "chat_message", "message": {
                    'model': 'Alojamiento',
                    'event': 'u',
                    'data': entity
                }}
            )


@receiver(post_delete, sender=Alojamiento)
def announce_del_alojamiento(sender, instance, **kwargs):
    print('se llamo al delete')
    entity = model_to_dict(instance)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "cambios", {"type": "chat_message", "message": {
                    'model': 'Alojamiento',
                    'event': 'd',
                    'data': entity
                    }}
    )
