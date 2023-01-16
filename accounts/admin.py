from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html

from kakao.forms import FriendsTalkForm
from .models import *



class UserInline(admin.TabularInline):
    model = User


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    # inlines = [
    #     UserInline,
    # ]
    list_display = ('affiliation', 'name', 'code', 'is_active', 'group_actions')
    readonly_fields = ('code', 'is_active')
    list_filter = ('name',)
    search_fields = ('name',)
    actions = ['code_update', 'change_active']
    change_active_template = 'admin/change_group_activie.html'

    def code_update(self, request, queryset):
        '코드를 갱신합니다.'
        total = queryset.count()
        if total > 0:
            for group in queryset:
                group.code_update()
            self.message_user(request, f'{total}건의 그룹코드를 갱신했습니다.')
        else:
            self.message_user(request, '갱신할 그룹이 없습니다.')
    code_update.short_description = '선택된 그룹들의 코드를 갱신합니다.'

    def change_active(self, request, queryset):
        '비활성화합니다.'
        total = queryset.count()
        if total > 0:
            for group in queryset:
                group.change_active()
            self.message_user(request, f'{total}건의 그룹를 활성화 상태를 변경했습니다.')
        else:
            self.message_user(request, '변경할 그룹이 없습니다.')
    change_active.short_description = '선택된 그룹들의 활성화 상태를 변경합니다.'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<group_id>/send_group/', self.admin_site.admin_view(self.process_send_group), name='send_group',),
        ]
        return custom_urls + urls

    def group_actions(self, obj):
        return format_html('<a class="button" href="{}">보내기</a>&nbsp;',
                           reverse('admin:send_group', args=[obj.pk]),
                           )

    group_actions.short_description = '친구톡'
    group_actions.allow_tags = True

    def process_send_group(self, request, group_id, *args, **kwargs):
        return self.process_action(request=request, group_id=group_id, action_form=FriendsTalkForm,)

    def process_action(self, request, group_id, action_form):
        group = self.get_object(request, group_id)

        if request.method != 'POST':
            form = action_form()
        else:
            form = action_form(request.POST)
            if form.is_valid():
                try:
                    form.save(group, request.user)
                except:
                    pass
                else:
                    self.message_user(request, 'Success')
                    url = reverse(
                        'admin:account_account_change',
                        args=[group.pk],
                        current_app=self.admin_site.name,
                    )
                    return HttpResponseRedirect(url)
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['account'] = accounts
        context['title'] = action_title
        return TemplateResponse(
            request,
            'admin/account/account_action.html',
            context,
        )

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ('id', 'username', 'email', 'group', 'is_active', 'last_login')
    list_display_links = ('username',)
    list_filter = ('username', )
    search_fields = ('username', )
    #
    # list_display = ('username', 'group_name', 'is_active')
    # list_filter = ('username', 'group_name')
    # search_fields = ('username', 'group_name')

    # def group_name(self, obj):
    #     return obj.group.name


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    list_display = ('id', 'username', 'group', 'representative', 'is_superuser', 'is_active', 'is_staff', 'created_at')
    list_display_links = ('username',)
