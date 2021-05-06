from urllib import parse

from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, TemplateView, UpdateView

from .forms import MedicineForm
from .models import Medicine


class MedicineListView(ListView):
    model = Medicine
    template_name = 'medicine/medicine_list.html'


class MedicineCreateView(CreateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'medicine/medicine_create.html'
    success_url = '/list/'


class MedicineDetailView(DetailView):
    model = Medicine
    template_name = 'medicine/medicine_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_img'] = "https://ilhwa-pharm.s3.ap-northeast-2.amazonaws.com/image/" \
                                 + parse.quote(str(context['object'].name.replace("/", ""))) + ".jpg"
        return context

        # def get_object(self, queryset=None):
    #     medicine = super().get_object(queryset)
    #     medicine.increment_view_Count()
    #     return medicine


class MedicineUpdateView(UpdateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'medicine/medicine_update.html'

class MedicineDeleteView(DeleteView):
    model = Medicine
    template_name = 'medicine/medicine_delete.html'


class IndexView(TemplateView):
    template_name = 'medicine/index.html'


