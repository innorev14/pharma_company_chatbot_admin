from django.urls import path

from .views import *

urlpatterns = [
    path('authorize/', KakaoAPIView.as_view()),
    path('member/list/', MemberListView.as_view()),
    path('member/create/', MemberCreateView.as_view()),
    path('member/<int:pk>/detail/', MemberDetailView.as_view()),
    path('member/<int:pk>/delete/', MemberDeleteView.as_view()),
    path('member/<int:pk>/update/', MemberUpdateView.as_view()),
    path('group/list/', GroupListView.as_view()),
    path('group/create/', GroupCreateView.as_view()),
    path('group/<int:pk>/update/', GroupUpdateView.as_view()),
    path('group/<int:pk>/delete/', GroupDeleteView.as_view()),
]