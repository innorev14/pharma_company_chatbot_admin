from django import forms

from .models import Medicine


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['category', 'name', 'tag', 'product_info', 'product_url', 'insurance_info', 'detail_info']
