from django import forms 
# from .models import SeasonSelectModel

# class SeasonSelectForm(forms.ModelForm):
    
#     class Meta:
#         model = SeasonSelectModel

OPTIONS = (
    ('option1', 'Option 1'), 
    ('option2', 'Option 2'), 
    ('option3', 'Option 3'), 
)
dropdown = forms.ChoiceField(choices=OPTIONS, required=True, label='Select and Option')