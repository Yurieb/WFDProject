from django import forms
from .models import SupportCase
from .models import SupportCase, Response, Feedback 

class SupportCaseForm(forms.ModelForm):
    class Meta:
        model = SupportCase
        fields = ['subject', 'description']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['message']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']        
