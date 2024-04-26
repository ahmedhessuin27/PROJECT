from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from notification import consumers
from servfix import notification

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/chat/", consumers.ChatConsumer.as_asgi()),
        ])
    ),
})