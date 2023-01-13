"""
ASGI config for Hotel_api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hotel_api.settings')

# application = get_asgi_application()


import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from django.core.asgi import get_asgi_application
from apps.websocket.consumers import Consumer
from django.urls.conf import path
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'API.settings')
django.setup()
from .channelsmiddleware import JWTChannelMiddleware


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    "websocket": JWTChannelMiddleware(
        URLRouter([
            path("ws/", Consumer.as_asgi()),
        ])
    )
})

# application = get_asgi_application()