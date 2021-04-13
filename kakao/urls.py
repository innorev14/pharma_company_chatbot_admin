from django.urls import path

from .views import *

urlpatterns = [
    path('keyboard/', keyboard, name='keyboard'),
    path('message/', medicine, name='message')
]