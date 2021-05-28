from datetime import datetime, timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncDay
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
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


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class StaffListView(ListView):
    model = get_user_model()
    template_name = 'accounts/staff_list.html'
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        qs = get_user_model().objects.filter(group=None)
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(username__icontains=query)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(StaffListView, self).get_context_data(*args, **kwargs)
        qs = self.request.GET.get('q', '')
        context['q'] = qs
        return context


def staff_active(request, pk):
    status = get_user_model().objects.get(id=pk)
    if status.is_staff:
        status.is_staff = False
    else:
        status.is_staff = True
    status.save()
    return redirect('/accounts/staff/list/')


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class MemberListView(ListView):
    model = Member
    template_name = 'accounts/member_list.html'
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        qs = Member.objects.all()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(username__icontains=query)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(MemberListView, self).get_context_data(*args, **kwargs)
        qs = self.request.GET.get('q', '')
        context['q'] = qs
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class MemberCreateView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'accounts/member_create.html'
    success_url = '/accounts/member/list/'


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class MemberUpdateView(UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'accounts/member_update.html'


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class MemberDetailView(DetailView):
    model = Member
    template_name = 'accounts/member_detail.html'


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
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


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class GroupListView(ListView):
    model = Group
    template_name = 'accounts/group_list.html'
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        qs = Group.objects.all()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(name__icontains=query)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(GroupListView, self).get_context_data(*args, **kwargs)
        qs = self.request.GET.get('q', '')
        context['q'] = qs
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class GroupCreateView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'accounts/group_create.html'
    success_url = '/accounts/group/list/'


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
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


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
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


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class AccessListView(ListView):
    model = AccessLog
    template_name = 'accounts/access_log/access_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs\
            .values("group_id")\
            .annotate(group_count=Count("group_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for group in context['accesslog_list']:
            name = Group.objects.get(id=group['group_id']).name
            group['group_name'] = name
        # print(context)
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class AccessGroupDayList(ListView):
    model = AccessLog
    template_name = 'accounts/access_log/day_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        today = datetime.today()
        return qs\
            .filter(created_at__year=today.year,
                    created_at__month=today.month,
                    created_at__day=today.day)\
            .values("group_id")\
            .annotate(group_count=Count("group_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for group in context['accesslog_list']:
            name = Group.objects.get(id=group['group_id']).name
            group['group_name'] = name
        # print(context)
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class AccessGroupWeekList(ListView):
    model = AccessLog
    template_name = 'accounts/access_log/week_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        today = datetime.today()
        start = today - timedelta(days=7)
        return qs\
            .filter(created_at__range=[start, today])\
            .values("group_id")\
            .annotate(group_count=Count("group_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for group in context['accesslog_list']:
            name = Group.objects.get(id=group['group_id']).name
            group['group_name'] = name
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class AccessGroupMonthList(ListView):
    model = AccessLog
    template_name = 'accounts/access_log/month_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        today = datetime.today()
        start = today - timedelta(days=30)
        return qs\
            .filter(created_at__range=[start, today])\
            .values("group_id")\
            .annotate(group_count=Count("group_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for group in context['accesslog_list']:
            name = Group.objects.get(id=group['group_id']).name
            group['group_name'] = name
        return context