from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Integeration Name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    api_id = forms.CharField(label='Api ID', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    api_hash = forms.CharField(label='Api Hash', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(label='Phone Number', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))

class MetaContactForm(forms.Form):
    name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly', 'class': 'form-control'}))
    metadata = forms.CharField(label = '', max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly', 'hidden': 'true'}))
    return_url = forms.CharField(label = '', max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly', 'hidden': 'true'}))
    # api_id = forms.CharField(label='Api ID', max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # api_hash = forms.CharField(label='Api Hash', max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # phone_number = forms.CharField(label='Phone Number', max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly'}))