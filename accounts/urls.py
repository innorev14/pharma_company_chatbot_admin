from django.urls import path

from .views import KakaoAPIView

urlpatterns = [
    path('authorize/', KakaoAPIView.as_view),
]