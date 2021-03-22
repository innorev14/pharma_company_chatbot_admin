from django.contrib import admin

from .models import *



class UserInline(admin.TabularInline):
    model = User


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    # inlines = [
    #     UserInline,
    # ]
    list_display = ('name', 'code', 'is_active')
    readonly_fields = ('code', 'is_active')
    list_filter = ('name',)
    search_fields = ('name',)
    actions = ['code_update', 'change_active']

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

