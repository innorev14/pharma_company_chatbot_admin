from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from rest_framework.views import APIView

from accounts.forms import MemberForm, GroupForm
from accounts.models import Group, Member


class KakaoAPIView(APIView):
    def post(self, request):
        print('request : ', request)
        req_kakao = request.POST.get()
        print('req_kakao : ', req_kakao)
        kakao_id = {
            'kakao_vlink': {'user_id': req_kakao['userRequest']['user']['id']}
        }
        print('kakao_id : ', kakao_id)


class MemberListView(ListView):
    model = Member
    template_name = 'accounts/member_list.html'


class MemberCreateView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'accounts/member_create.html'
    success_url = '/accounts/member/list/'


class MemberUpdateView(UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'accounts/member_update.html'


class MemberDetailView(DetailView):
    model = Member
    template_name = 'accounts/member_detail.html'


class MemberDeleteView(DeleteView):
    model = Member
    template_name = 'accounts/member_delete.html'
    success_url = '/accounts/member/list/'


class GroupListView(ListView):
    model = Group
    template_name = 'accounts/group_list.html'


class GroupCreateView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'accounts/group_create.html'
    success_url = '/accounts/group/list/'


class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'accounts/group_update.html'


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'accounts/group_delete.html'
    success_url = '/accounts/group/list/'
