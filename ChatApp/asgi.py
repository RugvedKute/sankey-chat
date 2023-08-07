"""
ASGI config for ChatApp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.consumers import PersonalChatConsumer, OnlineStatusConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApp.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/<int:id>/', PersonalChatConsumer.as_asgi()),
            path('ws/online/', OnlineStatusConsumer.as_asgi())

            ])
    )
})




# import os
# from django.core.asgi import get_asgi_application
 
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApp.settings')
 
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter , URLRouter
# from chat import routing
 
# application = ProtocolTypeRouter(
#     {
#         "http" : get_asgi_application() ,
#         "websocket" : AuthMiddlewareStack(
#             URLRouter(
#                 routing.websocket_urlpatterns
#             )   
#         )
#     }
# )