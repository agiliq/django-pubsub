from django import forms
from demo.models import Status

class StatusForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea, label='Message')

    class Meta:
        model = Status
