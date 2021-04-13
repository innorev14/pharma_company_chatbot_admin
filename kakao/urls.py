from django.urls import path

from .views import *

urlpatterns = [
    path('keboard/', keyboard, name='keyboard'),
    path('message/', medicine, name='message')
]