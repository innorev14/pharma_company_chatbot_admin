from django.urls import path

from .views import *
from .talk_views import *


app_name = 'kakao'

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
    path('medicine_direct/', medicine_direct, name='medicine_direct'),
    path('search_category/', search_category, name='search_category'),
    path('search_tag/', search_tag, name='search_tag'),
    path('insu_info_test/', insu_info_test, name='insu_info_test'),
    path('detail_point_test/', detail_point_test, name='detail_point_test'),

    path('friends_talk/list/', FriendsTalkListView.as_view(), name='talk_list'),
    path('friends_talk/create/', FriendsTalkCreateView.as_view(), name='talk_create'),
    path('friends_talk/<int:pk>/detail/', FriendsTalkDetailView.as_view(), name='talk_detail'),
    path('friends_talk/<int:pk>/delete/', FriendsTalkDeleteView.as_view(), name='talk_delete'),

    path('friends_talk/group_send/<int:pk>/', FriendsTalkGroupSendView.as_view(), name='talk_send_group'),
    # path('friends_talk/whole_send/', FriendsTalkWholeSendView.as_view(), name='talk_send_whole'),
    # path('friends_talk/group_send/', FriendsTalkGroupSendView.as_view(), name='talk_send_group'),

]