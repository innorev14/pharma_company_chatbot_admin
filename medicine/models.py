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


class Medicine(models.Model):
    name = models.CharField(max_length=45, verbose_name='제품명')
    product_info = RichTextField(verbose_name='제품정보')
    insurance_info = RichTextField(verbose_name='보험정보')
    detail_info = RichTextField(verbose_name='디테일 포인트')
    view_count = models.PositiveIntegerField(default=0, verbose_name='조회수')
    tag = TaggableManager(
        verbose_name=_('tag'),
        help_text=_('태그는 콤마(,) 혹은 띄워쓰기로 구분해주세요'),
        blank=True,
        through='TaggedMedicine',
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('의약품')
        verbose_name_plural = _('의약품 리스트')
        ordering = ('-updated_at',)

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
