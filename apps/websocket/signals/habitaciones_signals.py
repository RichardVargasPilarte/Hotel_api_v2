from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from apps.websocket.signals import types_dict_convert

from apps.habitaciones.models import Habitacion


@receiver(post_save, sender=Habitacion)
def announce_new_habitacion(sender, instance, created, **kwargs):
    print(model_to_dict(instance))
    entity = model_to_dict(instance)
    entity = json.dumps(entity, default=types_dict_convert)
    if created:
        print('se llamo al create')
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "cambios", {"type": "chat_message", "message": {
                'model': 'Habitacion',
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
            async_to_sync(channel_layer.group_send)(
                "cambios", {"type": "chat_message", "message": {
                    'model': 'Habitacion',
                    'event': 'd',
                    'data': entity
                }}
            )
            print('enviado delete a cambios channel', channel_layer)
        else:
            async_to_sync(channel_layer.group_send)(
                "cambios", {"type": "chat_message", "message": {
                    'model': 'Habitacion',
                    'event': 'u',
                    'data': entity
                }}
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
