from django.urls import path 
from . import views 


urlpatterns = [
    path('', views.index , name = 'home'),
    path('main/', views.stream, name='index'),
    path('video_feed', views.video_feed, name='video_feed'),
]
