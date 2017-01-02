from django import forms

class search(forms.Form):
    querry = forms.CharField(label='search_term',widget=forms.TextInput(attrs={'placeholder': 'Enter name of the product'})	)