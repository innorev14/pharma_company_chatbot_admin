from django import forms
from django.contrib.auth import get_user_model

from .models import FriendsTalk
from .friendtalk import *
from accounts.models import Group


class FriendsTalkForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all().order_by('name'), required=False)
    sender = forms.CharField(initial=get_user_model().objects.get(id=13).phone, disabled=True)

    class Meta:
        model = FriendsTalk
        fields = '__all__'

        widgets = {
            'sender': forms.Textarea(
                attrs={'placeholder': '내용을 입력해주세요'}
            )
        }

    def get_sender(self):
        return self.cleaned_data['sender']