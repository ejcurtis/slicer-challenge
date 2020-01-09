from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from . import views

# newer verions of django no longer require regular expressions for url paths

urlpatterns = [
    #url to "home" page
    path('', views.image_series_list, name='image_series_list'),
    #url to series slider page usng the series uid as the identifier
    #if I had more time I might figure out how to target a series without 
    #having to have the id in the RL for security purposes
    path('<series_uid>', views.image_slider, name='image_slider'),
]
