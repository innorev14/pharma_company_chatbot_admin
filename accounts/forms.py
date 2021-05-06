from django import forms

from .models import Member, Group


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['group', 'username', 'phone', 'is_active', 'is_staff']


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'is_active']