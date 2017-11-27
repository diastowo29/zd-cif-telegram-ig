from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.messages import SendMediaRequest
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.types import InputMediaPhotoExternal
from telethon import utils
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.views.decorators.clickjacking import xframe_options_exempt
from .form import ContactForm
from .form import MetaContactForm
from .form import SendMetaForm

import requests
import json
import datetime

return_url = ''
state = {}
states = {'state': state}
ext_resource = [
    {
      "external_id": "123456",
      "message":     "Testing Telegram dias",
      "created_at":  "2017-09-08T22:48:09Z",
      "author": {
        "external_id": "678890",
        "name":        "dias",
      },
      "allow_channelback": 'false'
    },
    {
      "external_id": "1234567",
      "message":     "cuman testing nih dias",
      "created_at":  "2017-09-08T22:48:12Z",
      "parent_id":   "123456",
      "author": {
        "external_id": "678890",
        "name":        "dias",
      },
      "allow_channelback": 'false'
    }
  ]

state = "{\"last_message_id\":\"1234567\"}"

api_id = 184365
api_hash = '640727dc57738548a9cbc23e5d8d1bbe'
phone = '+6281294059775'
username = 'diastowo'

@csrf_exempt
@xframe_options_exempt
def admin(request):
	if request.method == 'POST':
		global return_url
		return_url = request.POST.get('return_url', '')

	form = ContactForm()
	return render(request, 'admin.html', {'form': form})

@csrf_exempt
@xframe_options_exempt
def pull(request):
	print('pull');
	metadata = '';
	newState = '';
	if request.method == 'POST':
		print('POST PULL')
		metadata = request.POST.get('metadata', '')
		newState = request.POST.get('state', '')
	else:
		print('NOT POST PULL')

	# metaJson = json.loads(metadata)

	# api_id = metaJson['api_id']
	# api_hash = metaJson['api_hash']
	# phone = metaJson['phone_number']
	# username = metaJson['username']
	client = TelegramClient(username, api_id, api_hash)
	client.connect()
	dialogs, entities = client.get_dialogs()
	print(metadata)
	print(newState)
	# for entity in entities:
	# 	if not entity.bot:
	# 		if "User(" in str(entity) :
	# 			result = client(GetHistoryRequest(
	# 				entity,
	# 				limit=100,
	# 				offset_date=None,
	# 				offset_id=0,
	# 				max_id=0,
	# 				min_id=0,
	# 				add_offset=0
	# 				));
	# 			msg = len(result.messages)-1
	# 			while msg > -1:
	# 				lastMsg = 0
	# 				if (lastMsg < result.messages[msg].id):
	# 					lastMsg = result.messages[msg].id

	# 				state = {'last_message_id':lastMsg}
	# 				user = client.get_entity(result.messages[msg].from_id)
	# 				message = '';
	# 				parent_id = 'tg-msg-' + str(entity.id)
	# 				if msg == len(result.messages)-1:
	# 					message = {
	# 				      'external_id': parent_id,
	# 				      'message': result.messages[msg].message,
	# 				      'created_at':result.messages[msg].date.isoformat("T") + "Z",
	# 				      'author': {
	# 				        'external_id': 'tg-acc-' + str(result.messages[msg].from_id),
	# 				        'name': user.first_name,
	# 				      },
	# 				      'allow_channelback': 'false'
	# 				    }
	# 				else:
	# 					message = {
	# 				      'external_id': 'tg-msg-' + str(result.messages[msg].id),
	# 				      'message': result.messages[msg].message,
	# 				      'created_at':result.messages[msg].date.isoformat("T") + "Z",
	# 				      'parent_id': parent_id,
	# 				      'author': {
	# 				        'external_id': 'tg-acc-' + str(result.messages[msg].from_id),
	# 				        'name': user.first_name,
	# 				      },
	# 				      'allow_channelback': 'false'
	# 				    }
	# 				ext_resource.extend([message])
	# 				msg-=1
	# 		else:
	# 			print('not user')
	# 	else:
	# 		print('bot chat')
	# print({'external_resources':ext_resource, 'state': state})

	response_data = {}
	response_data['external_resources'] = ext_resource
	# response_data['state'] = state
	# return JsonResponse({'external_resources':ext_resource, 'state':state})
	return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json;charset=UTF-8")

def channelback(request):
	print('channelback');
	return render(request, 'admin.html')

def clickthrough(request):
	print('clickthrough');
	return render(request, 'admin.html')

def manifest(request):
	print('manifest')
	tasks = {
	        'name': 'Telegram Integeration',
	        'id': 'zendesk-internal-telegram-integration',
	        'author': 'Diastowo Faryduana', 
	        'version': 'v1.0',
	        'urls': {
	        	'admin_ui':'https://pure-crag-61212.herokuapp.com/zendesk/telegram/admin_ui',
	        	'pull_url': 'https://pure-crag-61212.herokuapp.com/zendesk/telegram/pull',
	        	'channelback_url': 'https://pure-crag-61212.herokuapp.com/zendesk/telegram/channelback',
	        	'clickthrough_url': 'https://pure-crag-61212.herokuapp.com/zendesk/telegram/clickthrough'
	        }
	    }
	return JsonResponse(tasks)

@csrf_exempt
@xframe_options_exempt
def get_verify(request):
	newForm = MetaContactForm()
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			print('valid')
			newForm.fields['metadata'].initial = '{"name":"' + form.cleaned_data['name'] + '", "api_id": "' + form.cleaned_data['api_id'] + '", "api_hash": "' + form.cleaned_data['api_hash'] + '", "phone_number": "' + form.cleaned_data['phone_number'] + '", "username": "' + form.cleaned_data['username'] + '"}'
			newForm.fields['return_url'].initial = return_url

			client = TelegramClient(form.cleaned_data['username'], form.cleaned_data['api_id'], form.cleaned_data['api_hash'])
			client.connect()
			client.send_code_request(form.cleaned_data['phone_number']);

		else :
			print('not valid')
	else:
		print('not post')
		form = ContactForm()
	return render(request, 'adminmeta.html', {'form': newForm, 'return_url': return_url})

@csrf_exempt
@xframe_options_exempt
def send_metadata(request):
	sendMetaForm = SendMetaForm()
	newReturnUrl = ''
	if request.method == 'POST':
		metaForm = MetaContactForm(request.POST)
		print('its post')
		if metaForm.is_valid():
			print('form valid')
			metadata = metaForm.cleaned_data['metadata']
			newReturnUrl = metaForm.cleaned_data['return_url']
			verify = metaForm.cleaned_data['verify']

			metadataJson = json.loads(metadata)
			name = metadataJson['name']
			api_id = metadataJson['api_id']
			api_hash = metadataJson['api_hash']
			phone_number = metadataJson['phone_number']
			username = metadataJson['username']

			client = TelegramClient(username, api_id, api_hash)
			client.connect()
			if not client.is_user_authorized():
				client.sign_in(phone=phone_number);
				client.sign_in(code=verify)
				print('attemp to logins')

			sendMetaForm.fields['name'].initial = name
			sendMetaForm.fields['metadata'].initial = metadata
			sendMetaForm.fields['return_url'].initial = newReturnUrl
		else:
			print('form not valid')
			print(metaForm.errors)

	return render(request, 'newadminmeta.html', {'form': sendMetaForm, 'return_url': newReturnUrl})



# def call_api (urls):
# 	url = 'https://treesdemo1.zendesk.com/zendesk/channels/integration_service_instances/editor_finalizer'
# 	print('make request to ', urls)
# 	url = urls
# 	data = '''{
# 	  "metadata": {
# 	    "api_id": "new_api_id",
# 	    "api_hash": "new_api_hash",
# 	    "phone_number": "new_phone_number"
# 	  },
# 	  "name": "Telegram Integeration",
# 	}'''
# 	response = requests.post(url, data=data)
# 	print(response.text)
# 	if response.status_code == 200:
# 		print('call success')
# 	else:
# 		print('call failed')
# 	return render(request, 'admin.html')