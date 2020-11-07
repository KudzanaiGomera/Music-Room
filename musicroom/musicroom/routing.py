from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
import Playlist.routing
application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter(
            Playlist.routing.websocket_urlpatterns
        )
    )
})