from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from taggit.models import TagBase, TaggedItemBase


class MedicineTag(TagBase):
    # NOTE: django-taggit does not allow unicode by default.
    slug = models.SlugField(verbose_name=_('slug'), unique=True, max_length=100, allow_unicode=True,)

    class Meta:
        verbose_name = _("태그")
        verbose_name_plural = _("태그")

    # def slugify(self, tag, i=None):
    #     return default_slugify(tag, allow_unicode=True)


class TaggedMedicine(TaggedItemBase):
    content_object = models.ForeignKey('Medicine', on_delete=models.CASCADE,)
    tag = models.ForeignKey('MedicineTag', related_name="%(app_label)s_%(class)s_items", on_delete=models.CASCADE,)

    class Meta:
        verbose_name = _("태그된 게시물")
        verbose_name_plural = _("태그된 게시물")


class Category(models.Model):
    category = models.CharField(max_length=45, verbose_name='제품분류')

    class Meta:
        verbose_name = _('제품분류')
        verbose_name_plural = _('제품분류')
        unique_together = ["category"]

    def __str__(self):
        return self.category


class Medicine(models.Model):
    name = models.CharField(max_length=45, verbose_name='제품명')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='제품분류')
    product_info = RichTextField(verbose_name='제품정보')
    product_url = models.URLField(max_length=200, verbose_name='제품상세URL', null=True, blank=True)
    insurance_info = RichTextField(verbose_name='보험정보')
    detail_info = RichTextField(verbose_name='디테일 포인트', null=True, blank=True)
    detail_url = models.URLField(max_length=200, verbose_name='디테일 정보', null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0, verbose_name='조회수')
    tag = TaggableManager(
        verbose_name=_('tag'),
        help_text=_('태그는 콤마(,) 혹은 띄워쓰기로 구분해주세요'),
        blank=True,
        through='TaggedMedicine',
    )
    created_at = models.DateTimeField(auto_now=True, verbose_name='등록일')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='수정일')

    class Meta:
        verbose_name = _('의약품')
        verbose_name_plural = _('의약품 리스트')
        ordering = ('-view_count',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('medicine:medicine_detail', args=(self.slug, ))

    def get_previous(self):
        return self.get_previous_by_modify_dt()

    def get_next(self):
        return self.get_next_by_modify_dt()

    def increment_view_count(self):
        self.view_count += 1
        self.save()
