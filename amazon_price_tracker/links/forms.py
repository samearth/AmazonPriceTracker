from django import forms
from .models import *

class AddLinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('url' , )
        widgets = {
            'url':forms.TextInput(attrs={'class':'form-control'})
        }