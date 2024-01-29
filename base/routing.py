# your_app/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from . import consumers

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/balance_updates/", consumers.BalanceUpdateConsumer.as_asgi()),
            ]
        )
    ),
})
