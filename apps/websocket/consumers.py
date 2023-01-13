from cgi import print_form
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class Consumer(AsyncJsonWebsocketConsumer):
    user = None
    async def connect(self):
        self.user = await self.scope['user']
        if  self.user.id:
            await self.accept()
            await self.channel_layer.group_add("cambios", self.channel_name)
        print(f"Added {self.channel_name} channel to cambios")

    async def disconnect(self, close_code):
        print('close_code', close_code)
        # user = await self.scope['user'] # posible linea de error
        if self.user.id:
            print('user', self.user.id)
            # https://channels.readthedocs.io/en/latest/topics/databases.html
            await self.channel_layer.group_discard("cambios", self.channel_name)
            print(f"Removed {self.channel_name} channel to cambios")

    ## envio de los mensajes
    async def cambios(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")
