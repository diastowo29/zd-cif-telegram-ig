from telethon import TelegramClient
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.views.decorators.clickjacking import xframe_options_exempt
from .form import ContactForm
from .form import MetaContactForm

import requests

@csrf_exempt
@xframe_options_exempt
def send_metadata(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			print('valid')
			newForm = MetaContactForm()
			newForm.fields['name'].initial = form.cleaned_data['name']
			newForm.fields['metadata'].initial = '{\"api_id\":\"', form.cleaned_data['api_id'], '\", \"api_has\": \"', form.cleaned_data['api_hash'], '\", \"phone_number\": \"', form.cleaned_data['api_hash'], '\"}'
		else:
			print('not valid')
	else:
		print('not post')
	return render(request, 'adminmeta.html', {'form': newForm, 'return_url': return_url})