from urllib import parse

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, DeleteView, TemplateView, UpdateView

from .forms import MedicineForm
from .models import Medicine


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required(login_url='accounts:login'), name='dispatch')
class MedicineListView(ListView):
    model = Medicine
    template_name = 'medicine/medicine_list.html'
    paginate_by = 15

    def get_queryset(self, *args, **kwargs):
        qs = Medicine.objects.order_by('-view_count')
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(name__icontains=query)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(MedicineListView, self).get_context_data(*args, **kwargs)
        qs = self.request.GET.get('q', '')
        context['q'] = qs
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class MedicineCreateView(CreateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'medicine/medicine_create.html'
    success_url = '/list/'


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class MedicineDetailView(DetailView):
    model = Medicine
    template_name = 'medicine/medicine_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_img'] = "https://ilhwa-pharm.s3.ap-northeast-2.amazonaws.com/media/product_img/" \
                                 + parse.quote(str(context['object'].name.replace("/", ""))) + ".jpg"
        return context

    # def get_object(self, queryset=None):
    #     medicine = super().get_object(queryset)
    #     medicine.increment_view_Count()
    #     return medicine


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class MedicineUpdateView(UpdateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'medicine/medicine_update.html'
    success_url = reverse_lazy('medicine:medicine_detail')

    def get_success_url(self):
        return reverse('medicine:medicine_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name='dispatch')
class MedicineDeleteView(DeleteView):
    model = Medicine
    template_name = 'medicine/medicine_delete.html'
    success_url = reverse_lazy('medicine:medicine_list')
    success_message = '제품이 성공적으로 삭제되었습니다.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(MedicineDeleteView, self).delete(request, *args, **kwargs)


class IndexView(TemplateView):
    template_name = 'medicine/index.html'


