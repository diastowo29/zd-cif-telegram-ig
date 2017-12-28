from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Integration Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Integration Name'}))
    api_id = forms.CharField(label='Api ID', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': '12345'}))
    api_hash = forms.CharField(label='Api Hash', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'123456abcde'}))
    phone_number = forms.CharField(label='Phone Number',  widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': '+62800000000'}))
    username = forms.CharField(label='Username',  widget=forms.TextInput(attrs={'class':'form-control'}))

class MetaContactForm(forms.Form):
    verify = forms.CharField(label = '', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'verify'}))
    metadata = forms.CharField(label = '', widget=forms.TextInput(attrs={'readonly':'readonly', 'id': 'metadata', 'hidden': 'true'}))
    return_url = forms.CharField(label = '', widget=forms.TextInput(attrs={'readonly':'readonly', 'id': 'return_url' , 'hidden': 'true'}))

class SendMetaForm(forms.Form):
    name = forms.CharField(label='Account Name',  widget=forms.TextInput(attrs={'readonly':'readonly', 'class': 'form-control'}))
    metadata = forms.CharField(label = '', widget=forms.TextInput(attrs={'readonly':'readonly', 'id': 'metadata', 'hidden': 'true'}))
    return_url = forms.CharField(label = '', widget=forms.TextInput(attrs={'readonly':'readonly', 'id': 'return_url' , 'hidden': 'true'}))