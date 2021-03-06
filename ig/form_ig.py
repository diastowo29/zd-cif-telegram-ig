from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Integration Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    client_id = forms.CharField(label='Client ID', widget=forms.TextInput(attrs={'class':'form-control'}))
    client_secret = forms.CharField(label='Client Secret', widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-control'}))

class MetaContactForm(forms.Form):
    verify = forms.CharField(label = '', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'verify'}))
    metadata = forms.CharField(label = '', widget=forms.TextInput(attrs={'readonly':'readonly', 'id': 'metadata', 'hidden': 'true'}))
    return_url = forms.CharField(label = '', widget=forms.TextInput(attrs={'readonly':'readonly', 'id': 'return_url' , 'hidden': 'true'}))

class SendMetaForm(forms.Form):
    name = forms.CharField(label='Account Name', widget=forms.TextInput(attrs={'readonly':'readonly', 'class': 'form-control'}))
    metadata = forms.CharField(label = '', widget=forms.TextInput(attrs={'readonly':'readonly', 'id': 'metadata', 'hidden': 'true'}))
    return_url = forms.CharField(label = '', widget=forms.TextInput(attrs={'readonly':'readonly', 'id': 'return_url' , 'hidden': 'true'}))

class GetTokenForm(forms.Form):
    client_id = forms.CharField(label='Client ID', widget=forms.TextInput(attrs={'class':'form-control'}))
    client_secret = forms.CharField(label='Client Secret', widget=forms.TextInput(attrs={'class':'form-control'}))
    grant_type = forms.CharField(label='Grant Type', widget=forms.TextInput(attrs={'class':'form-control'}))
    redirect_uri = forms.CharField(label='Redirect Url', widget=forms.TextInput(attrs={'class':'form-control'}))
    code = forms.CharField(label='Code', widget=forms.TextInput(attrs={'class':'form-control'}))

class AccessTokenForm(forms.Form):
    token = forms.CharField(label='Token', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Access Token'}))


class GiveTokenForm(forms.Form):
    token = forms.CharField(label='Token', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Access Token'}))