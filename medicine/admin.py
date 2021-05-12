from taggit.admin import Tag

from django.contrib import admin

from django.contrib import admin
from django.template.defaultfilters import truncatewords
from django.utils.translation import gettext as _


from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category',)
    list_display_links = ('category',)
    list_filter = ('category',)


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = \
        ('id', 'name', 'category', 'tag_list', 'updated_at',)
    list_display_links = ('name',)
    list_filter = ('name', 'updated_at',)
    search_fields = ('name', 'tag_list',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tag')

    def tag_list(self, obj):
        return ', '.join(o.name for o in obj.tag.all())
    tag_list.short_description = '태그'

    # def short_prod(self, obj):
    #     return truncatewords(obj.product_info, 10)
    #     # print(obj.values)
    #     # return obj.values()[0]['product_info'] if len(obj.values()[0]['product_info']) < 10 else (obj.values()[0]['product_info'][:35] + '...')
    # short_prod.short_description = '제품정보'

    # def short_insu(self, obj):
    #     return truncatewords(obj.insurance_info, 10)
    #     # return obj.values()[0]['insurance_info'] if len(obj.values()[0]['insurance_info']) < 10 else (obj.values()[0]['insurance_info'][:35] + '...')
    # short_insu.short_description = '보험정보'
    #
    # def short_detail(self, obj):
    #     return truncatewords(obj.detail_info, 10)
    #     # return obj.values()[0]['detail_info'] if len(obj.values()[0]['detail_info']) < 10 else (obj.values()[0]['detail_info'][:35] + '...')
    # short_detail.short_description = '디테일 포인트'

    # def created(self, obj):
    #     return obj.created_at.strftime("%Y-%m-%d")
    # created.short_description = '작성일'

    def updated(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d")
    updated.short_description = '수정일'

    class Meta:
        verbose_name = _('의약품')
        verbose_name_plural = _('의약품 리스트')


@admin.register(MedicineTag)
class MedicineTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.unregister(Tag)

