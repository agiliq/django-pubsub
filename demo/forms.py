from django import forms
from demo.models import Status

class StatusForm(forms.ModelForm):

    class Meta:
        model = Status
