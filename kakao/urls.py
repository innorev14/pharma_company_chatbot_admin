from django.urls import path

from .views import *

urlpatterns = [
    path('keyboard/', keyboard, name='keyboard'),
    path('keyboard2/', keyboard, name='keyboard2'),
    path('message/', medicine, name='message')
]