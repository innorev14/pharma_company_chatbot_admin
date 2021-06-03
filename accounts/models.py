import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class Group(models.Model):
    name = models.CharField(max_length=20, verbose_name='지점이름')
    code = models.CharField(max_length=6, blank=True, verbose_name='그룹코드')
    is_active = models.BooleanField(default=True, verbose_name='활성상태')

    def gen_code(self):
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        new_code = ""
        for i in range(6):
            new_code += random.choice(letters)
        self.code = new_code

    def save(self, *args, **kwargs):
        if not self.code:
            self.gen_code()
        super(Group, self).save(*args, **kwargs)

    def code_update(self, commit=True):
        '코드갱신'
        if self.code:
            self.gen_code()
        if commit:
            self.save()

    def change_active(self, commit=True):
        '활성화 상태 변경'
        if self.is_active == 1:
            self.is_active = 0
        elif self.is_active == 0:
            self.is_active = 1
        if commit:
            self.save()

    class Meta:
        verbose_name = _('지점')
        verbose_name_plural = _('지점')
        ordering = ('name',)

    def __str__(self):
        return self.name


class User(AbstractUser):
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, verbose_name='지점이름')
    kakao_id = models.CharField(max_length=70, verbose_name='카카오ID', null=True, blank=True)
    phone = models.CharField(max_length=11)

    class Meta:
        verbose_name = _('사용자')
        verbose_name_plural = _("사용자")
        ordering = ['username']


class LoginHistory(models.Model):
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    group = models.ForeignKey('Group', on_delete=models.DO_NOTHING)
    login_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('LoginHistory')


class Member(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, verbose_name='지점이름')
    username = models.CharField(max_length=10, verbose_name='이름')
    kakao_id = models.CharField(max_length=70, verbose_name='카카오ID', null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True, verbose_name='전화번호')
    is_superuser = models.BooleanField(verbose_name='최고관리자여부', default=False)
    is_active = models.BooleanField(verbose_name='활성상태', default=True)
    is_staff = models.BooleanField(verbose_name='관리자여부', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('사용자')
        verbose_name_plural = _("사용자")
        ordering = ('username',)


class AccessLog(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    intent_id = models.CharField(max_length=30, verbose_name="발화ID")
    intent_name = models.CharField(max_length=30, verbose_name="발화블록명")
    utterance = models.CharField(max_length=30, verbose_name="발화내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="발화일시")

    class Meta:
        verbose_name = _('사용기록')

    def dispatch(self, *args, **kwargs):
        return super(AccessLog, self).dispatch(*args, **kwargs)
