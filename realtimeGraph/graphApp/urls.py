from django.urls import path 
from . import views 

from django.views.generic import TemplateView
urlpatterns = [
    #path('', TemplateView.as_view(template_name='index.html')),
    path('', views.index , name = 'home'),
    path('main/', views.stream, name='index'),
    path('video_feed', views.video_feed, name='video_feed'),
]
