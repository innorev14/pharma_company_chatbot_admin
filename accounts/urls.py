from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *


app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),

    path('authorize/', KakaoAPIView.as_view()),
    path('member/list/', MemberListView.as_view(), name='member_list'),
    path('member/create/', MemberCreateView.as_view(), name='member_create'),
    path('member/<int:pk>/detail/', MemberDetailView.as_view(), name='member_detail'),
    path('member/<int:pk>/delete/', MemberDeleteView.as_view(), name='member_delete'),
    path('member/<int:pk>/update/', MemberUpdateView.as_view(), name='member_update'),
    path('group/list/', GroupListView.as_view(), name='group_list'),
    path('group/create/', GroupCreateView.as_view(), name='group_create'),
    path('group/<int:pk>/update/', GroupUpdateView.as_view(), name='group_update'),
    path('group/<int:pk>/detail/', GroupDetailView.as_view(), name='group_detail'),
    path('group/<int:pk>/delete/', GroupDeleteView.as_view(), name='group_delete'),

    path('group/change_active/<int:pk>/', group_change_active, name='group_change_active'),
    path('member/change_active/<int:pk>/', member_change_active, name='member_change_active'),

    path('access_log/', AccessListView.as_view(), name='access_log'),
    path('access_log/day/', AccessGroupDayList.as_view(), name='access_day_log'),
    path('access_log/week/', AccessGroupWeekList.as_view(), name='access_week_log'),
    path('access_log/month/', AccessGroupMonthList.as_view(), name='access_month_log'),

    path('staff/list/', StaffListView.as_view(), name='staff_list'),
    path('staff/<int:pk>/update/', StaffUpdateView.as_view(), name='staff_update'),
    path('staff/<int:pk>/detail/', StaffDetailView.as_view(), name='staff_detail'),
    path('staff/<int:pk>/delete/', StaffDeleteView.as_view(), name='staff_delete'),
    path('staff/active/<int:pk>/', staff_active, name='staff_active'),

    path('export/csv/', export_users_csv, name='export_users_csv'),
    path('export/excel/', export_users_excel, name='export_users_excel'),
]