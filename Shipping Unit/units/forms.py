from django import forms
from .models import Shipping_Units
from django.forms.widgets import CheckboxSelectMultiple

# class ConsolForm(forms.ModelForm):
#     class Meta:
#         model = Shipping_Units
#         fields = ['hawb', 'mawb',]

#     def __init__(self, *args, **kwargs):

#     	super(ConsolForm, self).__init__(*args, **kwargs)

#     	self.fields['on_hands'].widget = CheckboxSelectMultiple()
#     	self.fields['on_hands'].queryset = Shipping_Units.objects.filter(
#     		mawb = None)