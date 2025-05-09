import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from web import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tula_hack.settings")

django_application = get_asgi_application()

application = ProtocolTypeRouter(
    {"http": django_application, "websocket": AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))}
)
