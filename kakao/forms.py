from django import forms
from django.contrib.auth import get_user_model

from .models import FriendsTalk
from .friendtalk import *
from accounts.models import Group


class FriendsTalkForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all().order_by('name'), required=False)
    sender = forms.CharField(initial=get_user_model().objects.get(is_superuser=True).phone)

    class Meta:
        model = FriendsTalk
        fields = '__all__'

    def get_sender(self):
        return self.cleaned_data['sender']