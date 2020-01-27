from django import forms

class ReleaseForm(forms.Form):
    shipments = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
    )