from django import forms
from .models import SupportCase

class SupportCaseForm(forms.ModelForm):
    class Meta:
        model = SupportCase
        fields = ['subject', 'description']
