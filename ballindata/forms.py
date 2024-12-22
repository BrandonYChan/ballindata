from django import forms 
from .models import DropdownModel 

class DropDownModelForm(forms.Form):
    options = forms.ModelChoiceField(
        queryset=DropdownModel.objects.all(),
        empty_label="Sample Player",
        to_field_name="name",
        label="Dropdown Options",
    )
    
    
    
    