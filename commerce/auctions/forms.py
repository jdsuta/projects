   
# import form class from django
from django import forms
 
# import GeeksModel from models.py
from .models import Auction
 
# create a ModelForm
class AuctionForm(forms.ModelForm):         
    # specify the name of model to use
    class Meta:
        # to be used in the categories https://stackoverflow.com/questions/4788388/how-do-i-use-djangos-form-framework-for-select-options
        # https://stackoverflow.com/questions/72777081/forms-selectattrs-class-form-control-edit-form-and-get-numbers-1-5-in-dro
        category_choices = (
            ('', 'Select Category'),  # Blank option
            ('miscellaneous', 'Miscellaneous'),
            ('electronics', 'Electronics'),
            ('toys', 'Toys'),
            ('fashion', 'Fashion'),
            ('home','Home')
        )    
    
    # Add form-control class to provide style to the form. 
        model = Auction
        fields = ['item', 'description', 'price', 'image_url', 'category']
        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=category_choices, attrs={'class': 'form-control'}),
        }
        