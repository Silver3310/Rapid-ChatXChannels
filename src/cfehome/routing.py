from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter

from chat.consumer import ChatConsumer

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    # make sure whatever the host is doing the request is matching
    # the ALLOWED_HOSTS
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(
                        r"^messages/(?P<username>[\w.@+-]+)/$",
                        ChatConsumer
                    )
                ]
            )
        )
    )
})
