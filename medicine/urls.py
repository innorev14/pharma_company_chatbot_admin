from django.urls import path

from .views import *

app_name = 'medicine'

urlpatterns = [
    path('', IndexView.as_view()),
    path('create/', MedicineCreateView.as_view()),
    path('<int:pk>/detail/', MedicineDetailView.as_view()),
    path('<int:pk>/update/', MedicineUpdateView.as_view()),
    path('<int:pk>/delete/', MedicineDeleteView.as_view()),
    path('list/', MedicineListView.as_view()),
]