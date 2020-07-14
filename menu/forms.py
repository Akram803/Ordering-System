from django import forms
from .models import Category, Item



class CategoryCreatForm(forms.ModelForm):
    """CategoryCreatForm definition."""
    
    name = forms.CharField(label='Category Name', 
                            max_length=100, 
                            widget=forms.TextInput(attrs={'class': 'form-control'}) )

    description = forms.CharField(label='description',
                                max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control'})   )
    
    class Meta:
        model = Category
        fields =['name', 'description','image',]


class ItemCreatForm(forms.ModelForm):
    """CategoryCreatForm definition."""

    # category = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Item
        fields =['name',
                'image',
                'price',
                'availability',
                'quantity',
                'description',
                # 'category'
                ]
