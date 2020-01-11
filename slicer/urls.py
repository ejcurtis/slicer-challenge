from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from . import views

# newer verions of django no longer require regular expressions for url paths

urlpatterns = [
    #url to "home" page
    path('', views.image_series_list, name='image_series_list'),
    #url to series slider page usng the PK as the identifier
    path('<id>', views.image_slider, name='image_slider'),
]
