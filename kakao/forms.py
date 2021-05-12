from django import forms
from django.contrib.auth import get_user_model

from .models import FriendsTalk
from .friendtalk import *
from accounts.models import Group


class FriendsTalkForm(forms.ModelForm):
    image = forms.ImageField()
    # whole = forms.CharField(initial=1)
    group = forms.ModelChoiceField(queryset=Group.objects.all().order_by('name'), required=False)
    sender = forms.CharField(initial=get_user_model().objects.get(is_superuser=True).phone)
    class Meta:
        model = FriendsTalk
        fields = '__all__'

    def send_talk(self):
        print(self.cleaned_data)
        # try:
        group = self.cleaned_data['group']
        group_id = Group.objects.get(name=group).id
        users = get_user_model().objects.filter(group_id=group_id)
        user_list = list()
        for user in users:
            user_list.append(user.phone)
        receiver = ','.join(user_list)
        # except:
        #     whole = Group.obejcts.all()
        #     for group in whole:
        #         group_id = Group.objects.get(name=group).id
        #         users = get_user_model().objects.filter(group_id=group_id)
        #         user_list = list()
        #         for user in users:
        #             user_list.append(user.phone)
        #         receiver = ','.join(user_list)

        print('receiver : ', receiver)

        aligo_token = get_token()
        self.cleaned_data['receiver'] = receiver
        sender = self.cleaned_data['sender']
        msg_contents = self.cleaned_data['content']
        msg_title = self.cleaned_data['content'][:30]
        return send_friend_msg(aligo_token, sender, receiver, msg_title, msg_contents, image=None)