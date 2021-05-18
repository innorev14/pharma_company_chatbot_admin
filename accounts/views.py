from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from rest_framework.views import APIView

from accounts.forms import MemberForm, GroupForm, UserForm
from accounts.models import Group, Member, AccessLog


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
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        qs = Member.objects.all()
        query = self.request.GET.get("qs", None)
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(MemberListView, self).get_context_data(*args, **kwargs)
        return context


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


def member_change_active(request, pk):
    status = Member.objects.get(id=pk)
    if status.is_active:
        status.is_active = False
    else:
        status.is_active = True
    status.save()
    return redirect('/accounts/member/list/')


class GroupListView(ListView):
    model = Group
    template_name = 'accounts/group_list.html'
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        qs = Group.objects.all()
        query = self.request.GET.get("qs", None)
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(GroupListView, self).get_context_data(*args, **kwargs)
        return context


class GroupCreateView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'accounts/group_create.html'
    success_url = '/accounts/group/list/'


class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'accounts/group_update.html'


def group_change_active(request, pk):
    status = Group.objects.get(id=pk)
    if status.is_active:
        status.is_active = False
    else:
        status.is_active = True
    status.save()
    return redirect('/accounts/group/list/')


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'accounts/group_delete.html'
    success_url = '/accounts/group/list/'


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/list/')
    else:
        form = UserForm()
    return render(request, 'accounts/signup.html', {'form': form})


class AccessListView(ListView):
    model = AccessLog
    template_name = 'accounts/access_list.html'
