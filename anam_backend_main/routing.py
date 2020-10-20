from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import CookieMiddleware
from NotificationApp.middlewares import TokenAuthMiddleware, TokenMiddlewareStack

from NotificationApp.consumers import NotificationConsumer

application = ProtocolTypeRouter({

    # WebSocket chat handler
    # "websocket": CookieMiddleware(TokenAuthMiddleware(
    #     URLRouter([
    #         url(r"^ws/notification/$", NotificationConsumer),
    #     ])
    # )),
    "websocket": TokenMiddlewareStack(
        URLRouter([
            url(r"^ws/notification$", NotificationConsumer),
        ])
    ),
})
