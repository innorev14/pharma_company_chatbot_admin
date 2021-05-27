from django.utils.translation import gettext as _

from ckeditor.fields import RichTextField
from django.db import models


class FriendsTalk(models.Model):
    content = models.TextField(max_length=1000, verbose_name='내용')
    img_url = models.ImageField(upload_to='friendstalk', verbose_name='이미지URL',null=True, blank=True)
    img_link = models.URLField(null=True, blank=True, verbose_name='이미지 링크')
    btn_name = models.CharField(max_length=14, null=True, blank=True, verbose_name='버튼이름')
    weblink_pc = models.URLField(null=True, blank=True, verbose_name='웹링크PC')
    weblink_mobile = models.URLField(null=True, blank=-True, verbose_name='웹링크Mobile')
    sender = models.CharField(max_length=15, verbose_name='발신자')
    receiver = models.TextField(null=True, blank=True, verbose_name='수신자')
    status = models.CharField(max_length=5, null=True, blank=True, verbose_name='발송상태')
    response_msg = models.CharField(max_length=50, null=True, blank=True, verbose_name='상태메세지')
    sended_at = models.DateTimeField(auto_now_add=True, verbose_name='발송일시')

    class Meta:
        verbose_name = _("친구톡")
        verbose_name_plural = _("친구톡")
        ordering = ['-sended_at']
