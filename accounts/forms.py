from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Member, Group


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['group', 'username', 'phone', 'is_active']


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['affiliation', 'name', 'is_active']



class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = get_user_model()
        fields = ("username", "email")