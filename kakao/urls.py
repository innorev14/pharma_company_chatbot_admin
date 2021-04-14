from django.urls import path

from .views import *

urlpatterns = [
    path('keyboard/', keyboard, name='keyboard'),
    path('keyboard2/', keyboard2, name='keyboard2'),
    path('medicine/', medicine, name='medicine')
]