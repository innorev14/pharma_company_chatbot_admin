import json

from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, FormView, DetailView

from kakao.forms import FriendsTalkForm
from kakao.models import FriendsTalk


class FriendsTalkListView(ListView):
    model = FriendsTalk
    template_name = 'kakao/friendstalk_list.html'


# class FriendsTalkCreateView(CreateView):
#     model = FriendsTalk
#     form_class = FriendsTalkForm
#     template_name = 'kakao/friendstalk_create.html'
#     success_url = '/kakao/friends_talk/list/'


class FriendsTalkCreateView(FormView):
    form_class = FriendsTalkForm
    template_name = 'kakao/friendstalk_create.html'
    success_url = '/kakao/friends_talk/list/'

    def form_valid(self, form):
        print('form : ', form)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        send_talk = form.send_talk()
        talk = form.save(commit=False)
        talk.receiver = form.cleaned_data['receiver']
        talk.status = send_talk['code']
        talk.response_msg = send_talk['message']
        talk.save()
        return super().form_valid(form)



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


