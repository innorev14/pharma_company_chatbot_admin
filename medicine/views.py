from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, TemplateView, UpdateView

from .models import Medicine


class MedicineListView(ListView):
    model = Medicine
    template_name = 'medicine/medicine_list.html'


class MedicineCreateView(CreateView):
    model = Medicine
    template_name = 'medicine_create.html'


class MedicineDetailView(DetailView):
    model = Medicine
    template_name = 'medicine_detail.html'

    def get_object(self, queryset=None):
        medicine = super().get_object(queryset)
        medicine.increment_view_Count()
        return medicine


class MedicineUpdateView(UpdateView):
    model = Medicine
    template_name = 'medicine_update.html'

class MedicineDeleteView(DeleteView):
    model = Medicine
    template_name = 'medicine_delete.html'


class IndexView(TemplateView):
    template_name = 'medicine/index.html'


