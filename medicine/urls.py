from django.urls import path

from .views import *

app_name = 'medicine'

urlpatterns = [
    path('', MedicineListView.as_view(), name='home'),
    path('create/', MedicineCreateView.as_view(), name='medicine_create'),
    path('<int:pk>/detail/', MedicineDetailView.as_view(), name='medicine_detail'),
    path('<int:pk>/update/', MedicineUpdateView.as_view(), name='medicine_update'),
    path('<int:pk>/delete/', MedicineDeleteView.as_view(), name='medicine_delete'),
    path('list/', MedicineListView.as_view(), name='medicine_list'),
]