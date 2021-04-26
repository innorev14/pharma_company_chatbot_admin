from django.urls import path

from .views import *

urlpatterns = [
    path('keyboard/', keyboard, name='keyboard'),
    path('keyboard2/', keyboard2, name='keyboard2'),
    path('auth/', auth, name='auth'),
    path('valid/', validation, name='validation'),
    path('welcome/', welcome, name='welcome'),
    path('medicine/', medicine, name='medicine'),
    path('prod_info/', prod_info, name='prod_info'),
    path('insu_info/', insu_info, name='insu_info'),
    path('detail_point/', detail_point, name='detail_point'),
]