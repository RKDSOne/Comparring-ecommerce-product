<<<<<<< HEAD
from django import forms

class search(forms.Form):
    querry = forms.CharField(label='querry',widget=forms.TextInput(attrs={'placeholder': 'Enter name of the product'})	)
=======
from django import forms

class search(forms.Form):
    querry = forms.CharField(label='search_term',widget=forms.TextInput(attrs={'placeholder': 'Enter name of the product'})	)
>>>>>>> 2550c8d65edfec042bdf330e7dc5db1f373473ff
