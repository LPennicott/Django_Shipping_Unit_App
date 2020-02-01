from django.forms import ModelForm
from .models import InboundUnits
from django.forms.widgets import CheckboxSelectMultiple

class InboundForm(ModelForm):
    class Meta:
        model = InboundUnits
        fields = ('unit_count',)