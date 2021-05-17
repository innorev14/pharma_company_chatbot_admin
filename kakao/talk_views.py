import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, FormView, DetailView

from accounts.models import Group
from kakao.forms import FriendsTalkForm
from kakao.friendtalk import get_token, send_friend_msg
from kakao.models import FriendsTalk


class FriendsTalkListView(ListView):
    model = FriendsTalk
    template_name = 'kakao/friendstalk_list.html'


class FriendsTalkCreateView(CreateView):
    model = FriendsTalk
    form_class = FriendsTalkForm
    template_name = 'kakao/friendstalk_create.html'
    success_url = '/kakao/friends_talk/list/'

    def form_valid(self, form):
        msg = {}
        if self.request.POST['talk_type'] == 'img':
            msg['img'] = {}
            msg['img']['img_path'] = self.request.POST['img_path']
            msg['img']['img_link'] = self.requeest.POST['img_link']
        else:
            msg['img'] = None

        if self.request.POST['talk_button'] == 'weblink':
            msg['weblink'] = {}
            msg['weblink']['btn_name'] = self.request.POST['btn_name']
            msg['weblink']['weblink_pc'] = self.request.POST['weblink_pc']
            msg['weblink']['weblink_mobile'] = self.request.POST['weblink_pc']
        else:
            msg['weblink'] = None

        if self.request.POST['talk_receiver'] == 'whole':
            whole = Group.objects.all()
            user_list = list()
            for group in whole:
                group_id = Group.objects.get(name=group).id
                users = get_user_model().objects.filter(group_id=group_id)
                for user in users:
                    user_list.append(user.phone)
                msg['receiver'] = ','.join(user_list)
        elif self.request.POST['talk_receiver'] == 'group':
            group_id = self.request.POST['group']
            users = get_user_model().objects.filter(group_id=group_id)
            user_list = list()
            for user in users:
                user_list.append(user.phone)
            msg['receiver'] = ','.join(user_list)
        else:
            msg['receiver'] = self.request.POST['receiver']

        msg['sender'] = form.get_sender()
        msg['content'] = self.request.POST['content']
        talk_res = send_talk(msg)

        talk = form.save(commit=False)
        talk.receiver = msg['receiver']
        talk.status = talk_res['code']
        talk.response_msg = talk_res['message']
        talk.save()

        return super().form_valid(form)


class FriendsTalkGroupSendView(CreateView):
    model = FriendsTalk
    form_class = FriendsTalkForm
    template_name = 'kakao/friendstalk_group_send.html'
    success_url = '/kakao/friends_talk/list/'

    def get_context_data(self, **kwargs):
        kwargs['id'] = Group.objects.get(pk=self.kwargs['pk'])
        print(kwargs['id'])
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        msg = {}
        if self.request.POST['talk_type'] == 'img':
            msg['img'] = {}
            msg['img']['img_path'] = self.request.POST['img_path']
            msg['img']['img_link'] = self.requeest.POST['img_link']
        else:
            msg['img'] = None

        if self.request.POST['talk_button'] == 'weblink':
            msg['weblink'] = {}
            msg['weblink']['btn_name'] = self.request.POST['btn_name']
            msg['weblink']['weblink_pc'] = self.request.POST['weblink_pc']
            msg['weblink']['weblink_mobile'] = self.request.POST['weblink_pc']
        else:
            msg['weblink'] = None

        if self.request.POST['talk_receiver'] == 'whole':
            whole = Group.objects.all()
            user_list = list()
            for group in whole:
                group_id = Group.objects.get(name=group).id
                users = get_user_model().objects.filter(group_id=group_id)
                for user in users:
                    user_list.append(user.phone)
                msg['receiver'] = ','.join(user_list)
        elif self.request.POST['talk_receiver'] == 'group':
            group_id = self.request.POST['group']
            users = get_user_model().objects.filter(group_id=group_id)
            user_list = list()
            for user in users:
                user_list.append(user.phone)
            msg['receiver'] = ','.join(user_list)
        else:
            msg['receiver'] = self.request.POST['receiver']

        msg['sender'] = form.get_sender()
        msg['content'] = self.request.POST['content']
        talk_res = send_talk(msg)

        talk = form.save(commit=False)
        talk.receiver = msg['receiver']
        talk.status = talk_res['code']
        talk.response_msg = talk_res['message']
        talk.save()

        return super().form_valid(form)


def send_talk(msg):
    aligo_token = get_token()
    return send_friend_msg(aligo_token, msg)

# class FriendsTalkCreateView(FormView):
#     form_class = FriendsTalkForm
#     template_name = 'kakao/friendstalk_create.html'
#     success_url = '/kakao/friends_talk/list/'
#
#     def form_valid(self, form):
#         print('form : ', form)
#         print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
#         send_talk = form.send_talk()
#         talk = form.save(commit=False)
#         talk.receiver = form.cleaned_data['receiver']
#         talk.status = send_talk['code']
#         talk.response_msg = send_talk['message']
#         talk.save()
#         return super().form_valid(form)



class FriendsTalkDetailView(DetailView):
    model = FriendsTalk
    template_name = 'kakao/friendstalk_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['product_img'] = "https://ilhwa-pharm.s3.ap-northeast-2.amazonaws.com/image/" \
#                                  + parse.quote(str(context['object'].name.replace("/", ""))) + ".jpg"
#         return context
#
#         # def get_object(self, queryset=None):
#     #     medicine = super().get_object(queryset)
#     #     medicine.increment_view_Count()
#     #     return medicine


class FriendsTalkDeleteView(DeleteView):
    model = FriendsTalk
    template_name = 'kakao/friendstalk_delete.html'
    success_url = '/kakao/friends_talk/list/'


