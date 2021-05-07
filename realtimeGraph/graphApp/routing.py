from django.urls import path 
from . import views 
from .consumers import GraphConsumer

ws_urlpatterns = [
    path('ws/graph/', GraphConsumer.as_asgi() ),
]
