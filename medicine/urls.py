from django.urls import path

from .views import *


urlpatterns = [
    path('create/', MedicineCreateView.as_view()),
    path('<int:pk>/detail/', MedicineDetailView.as_view()),
    path('<int:pk>/delete/', MedicineDeleteView.as_view()),
    path('list/', MedicineListView.as_view()),
]