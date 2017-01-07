from django import forms

class search(forms.Form):
    querry = forms.CharField(label='querry',widget=forms.TextInput(attrs={'placeholder': 'Enter name of the product'})	)
