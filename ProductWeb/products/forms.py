from django import forms
from .models import *

class CreateProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity', 'thumb']
