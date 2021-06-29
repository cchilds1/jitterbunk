from django import forms
from .models import User

class BunkForm(forms.Form):
    user_to_input = forms.ModelChoiceField(
        label="CHOOSE USER ", 
        queryset=User.objects.all().order_by('username'),
        widget=forms.Select(attrs={'class':  'bunk_form_class'}),
        initial='USER'
    )
