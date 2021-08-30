import csv
from datetime import datetime, timedelta

import xlwt
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth, TruncDay
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
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
class StaffUpdateView(UpdateView):
    model = get_user_model()
    template_name = 'accounts/staff_update.html'
    success_url = reverse_lazy('accounts:staff_detail')
    fields = (
        'username',
        'email'
    )

    def get_success_url(self):
        return reverse('accounts:staff_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class StaffDetailView(DetailView):
    model = get_user_model()
    template_name = 'accounts/staff_detail.html'
    success_url = reverse_lazy('accounts:staff_detail')

    def get_success_url(self):
        return reverse('accounts:staff_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class StaffDeleteView(DeleteView):
    model = get_user_model()
    template_name = 'accounts/staff_delete.html'
    success_url = reverse_lazy('accounts:staff_list')
    success_message = '사용자가 성공적으로 삭제되었습니다.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(StaffDeleteView, self).delete(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class MemberListView(ListView):
    model = Member
    template_name = 'accounts/member_list.html'
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        qs = Member.objects.exclude(group_id=17)
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(Q(username__icontains=query) | Q(group__name__icontains=query) | Q(phone__icontains=query))
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
    success_url = reverse_lazy('accounts:member_detail')

    def get_success_url(self):
        return reverse('accounts:member_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class MemberDetailView(DetailView):
    model = Member
    template_name = 'accounts/member_detail.html'
    success_url = reverse_lazy('accounts:member_detail')

    def get_success_url(self):
        return reverse('accounts:member_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super(MemberDetailView, self).get_context_data(*args, **kwargs)
        # group_id = AccessLog.objects.get(id=self.kwargs['pk'])
        context['log'] = AccessLog.objects.filter(member=self.kwargs['pk']).order_by('-id')[:20]
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class MemberDeleteView(DeleteView):
    model = Member
    template_name = 'accounts/member_delete.html'
    success_url = reverse_lazy('accounts:member_list')
    success_message = '사용자가 성공적으로 삭제되었습니다.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(MemberDeleteView, self).delete(request, *args, **kwargs)


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
        qs = Group.objects.exclude(id=37)
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
    success_url = reverse_lazy('accounts:group_detail')

    def get_success_url(self):
        return reverse('accounts:group_detail', kwargs={'pk': self.object.pk})


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
class GroupDetailView(DetailView):
    model = Group
    queryset = Group.objects.all()
    template_name = 'accounts/group_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(GroupDetailView, self).get_context_data(*args, **kwargs)
        group_id = Group.objects.get(id=self.kwargs['pk'])
        context['member'] = Member.objects.filter(group=group_id)
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'accounts/group_delete.html'
    success_url = reverse_lazy('accounts:group_list')
    success_message = '그룹이 성공적으로 삭제되었습니다.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(GroupDeleteView, self).delete(request, *args, **kwargs)


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
        return qs \
            .exclude(group_id=37)\
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
        return qs \
            .exclude(group_id=37) \
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
        return qs \
            .exclude(group_id=37) \
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
        return qs \
            .exclude(group_id=37) \
            .filter(created_at__range=[start, today])\
            .values("group_id")\
            .annotate(group_count=Count("group_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for group in context['accesslog_list']:
            name = Group.objects.get(id=group['group_id']).name
            group['group_name'] = name
        return context


def export_users_csv(request):
    now = datetime.now()
    filename = "users_contacts_" + now.strftime('%Y%m%d')
    response = HttpResponse(content_type='text/csv', charset='euc-kr')
    response['Content-Disposition'] = "attachment; filename={}.csv".format(filename)


    writer = csv.writer(response)
    writer.writerow(['휴대폰번호', '고객명', '고객그룹'])

    users = Member.objects.filter(group__is_active=True).filter(is_active=True)\
        .values_list('phone', 'username', 'group__name')
    for user in users:
        writer.writerow(user)

    return response


def export_users_excel(request):
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment;filename*=UTF-8\'\'example.xls'
    wb = xlwt.Workbook(encoding='ansi')  # encoding은 ansi로 해준다.
    ws = wb.add_sheet('sheet1')  # 시트 추가

    row_num = 0
    col_names = ['휴대폰번호', '고객명', '고객그룹']

    for idx, col_name in enumerate(col_names):
        ws.write(row_num, idx, col_name)

    users = Member.objects.filter(group__is_active=True).filter(is_active=True)\
        .values_list('phone', 'username', 'group__name')
    for user in users:
        ws.write(user)

    wb.save(response)

    return reponse