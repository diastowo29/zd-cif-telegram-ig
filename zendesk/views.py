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
channelbackFlag = True
ext_resource = []


# api_id = 184365
# api_hash = '640727dc57738548a9cbc23e5d8d1bbe'
# phone = '+6281294059775'
# username = 'diastowo'

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
	state = ''
	del ext_resource[:]
	print('pull');
	metadata = '';
	newState = '';
	if request.method == 'POST':
		print('POST PULL')
		metadata = request.POST.get('metadata', '')
		newState = request.POST.get('state', '')
	else:
		print('NOT POST PULL')

	stateJson = '';
	stateLastMsg = 0;
	if newState != '':
		stateJson = json.loads(newState)
		stateLastMsg = stateJson['last_message_id']
	
	metaJson = json.loads(metadata)
	api_id = metaJson['api_id']
	api_hash = metaJson['api_hash']
	phone = metaJson['phone_number']
	username = metaJson['username']
	client = TelegramClient(username, api_id, api_hash)
	print('pull with username: ' + username)
	client.connect()
	dialogs, entities = client.get_dialogs()
	for entity in entities:
		if not entity.bot:
			if "User(" in str(entity) :
				# if entity.first_name == 'Erdit@Trees':
				result = client(GetHistoryRequest(
					entity,
					limit=20,
					offset_date=None,
					offset_id=0,
					max_id=0,
					min_id=0,
					add_offset=0
					));
				msg = len(result.messages)-1
				while msg > -1:
					lastMsg = 0
					if result.messages[msg].id > int(stateLastMsg):
						if lastMsg < result.messages[msg].id:
							lastMsg = result.messages[msg].id

						state = "{\"last_message_id\":\"" + str(lastMsg) + "\"}"
						user = client.get_entity(result.messages[msg].from_id)
						message = '';
						parent_id = 'tg-msg-' + str(entity.id)
						if msg == len(result.messages)-1:
							if len(result.messages[msg].message) != 0:
								message = {
							      'external_id': parent_id,
							      'message': result.messages[msg].message,
							      'created_at':result.messages[msg].date.isoformat("T") + "Z",
							      'author': {
							        'external_id': 'tg-acc-' + str(result.messages[msg].from_id),
							        'name': user.first_name,
							      },
							      'allow_channelback': channelbackFlag
							    }
						else:
							if len(result.messages[msg].message) != 0: 
								message = {
							      'external_id': 'tg-msg-'+ str(entity.id) + '-' + str(result.messages[msg].id),
							      'message': result.messages[msg].message,
							      'created_at':result.messages[msg].date.isoformat("T") + "Z",
							      'parent_id': parent_id,
							      'author': {
							        'external_id': 'tg-acc-' + str(result.messages[msg].from_id),
							        'name': user.first_name,
							      },
							      'allow_channelback': channelbackFlag
							    }
						ext_resource.extend([message])
					msg-=1
	client.disconnect()

	response_data = {}
	response_data['external_resources'] = ext_resource
	response_data['state'] = state
	# print(len(ext_resource))
	# return JsonResponse({'external_resources':ext_resource, 'state':state})
	return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json;charset=UTF-8")

@csrf_exempt
@xframe_options_exempt
def channelback(request):
	print('channelback');
	# return render(request, 'admin.html')
	metadata = ''
	newState = ''
	chatId = ''
	if request.method == 'POST':
		print('POST channelback')
		metadata = request.POST.get('metadata', '')
		newState = request.POST.get('state', '')
		message = request.POST.get('message', '')
		parentId = request.POST.get('parent_id', '')
		recipientId = request.POST.get('recipient_id', '')

		metaJson = json.loads(metadata)

		api_id = metaJson['api_id']
		api_hash = metaJson['api_hash']
		phone = metaJson['phone_number']
		username = metaJson['username']

		parentSplit = parentId.split('-')
		client = TelegramClient(username, api_id, api_hash)
		client.connect()
		dialogs, entities = client.get_dialogs()
		for entity in entities:
			if not entity.bot:
				if "User(" in str(entity) :
					if entity.id == int(parentSplit[2]):
						peer = utils.get_input_user(entity)
						sendMessage = client(SendMessageRequest(peer, message))
						chatId = parentSplit[0] + '-' + parentSplit[1] + '-' + parentSplit[2] + '-' + str(sendMessage.id)
		client.disconnect()
	else:
		print('NOT POST channelback')

	response_data = {}
	response_data['external_id'] = chatId
	response_data['allow_channelback'] = True
	# # print(len(ext_resource))
	# # return JsonResponse({'external_resources':ext_resource, 'state':state})
	return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json;charset=UTF-8")

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
			client.disconnect()

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
			client.disconnect()
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