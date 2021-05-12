from django.urls import path

from .views import *


app_name = 'accounts'

urlpatterns = [
    path('authorize/', KakaoAPIView.as_view()),
    path('member/list/', MemberListView.as_view(), name='member_list'),
    path('member/create/', MemberCreateView.as_view(), name='member_create'),
    path('member/<int:pk>/detail/', MemberDetailView.as_view(), name='member_detail'),
    path('member/<int:pk>/delete/', MemberDeleteView.as_view(), name='member_delete'),
    path('member/<int:pk>/update/', MemberUpdateView.as_view(), name='member_update'),
    path('group/list/', GroupListView.as_view(), name='group_list'),
    path('group/create/', GroupCreateView.as_view(), name='group_create'),
    path('group/<int:pk>/update/', GroupUpdateView.as_view(), name='group_update'),
    path('group/<int:pk>/delete/', GroupDeleteView.as_view(), name='group_delete'),
]