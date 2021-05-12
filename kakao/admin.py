from django.contrib import admin

from django.contrib.admin.utils import flatten_fieldsets
from django.template.response import TemplateResponse
from django.urls import path

from kakao.models import FriendsTalk


@admin.register(FriendsTalk)
class FriendsTalkAdmin(admin.ModelAdmin):
    list_display = ('content', 'sender', 'receiver', 'status', 'response_msg', 'sended_at')
    list_filter = ('sended_at',)
    search_fields = ('content',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields

        if self.declared_fieldsets:
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))


# class CustomFriendsTalkAdmin(admin.AdminSite):
#
#     def get_urls(self):
#         urls = super(CustomFriendsTalkAdmin, self).get_urls()
#         custom_urls = [
#             path('admin/', self.admin_view(self.send_talk_view), name="preview"),
#         ]
#         return urls + custom_urls
#
#     def send_talk_view(self, request):
#         context = dict(
#             self.admin_site.each_contet(request),
#
#         )
#         return TemplateResponse(request, "kakao/friendstalk_create.html", context)


# class TemplateAdmin(admin.ModelAdmin):
#     change_form_template = 'admin/preview_template.html'
#
#
# CustomFriendsTalkAdmin.register(FriendsTalk, TemplateAdmin)