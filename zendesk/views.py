from telethon import TelegramClient
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.views.decorators.clickjacking import xframe_options_exempt
import requests

return_url = ''
@csrf_exempt
@xframe_options_exempt
def admin(request):
	# if (request.method == 'POST'):
	# 	print('POST CALL')
	# 	global return_url
	# 	return_url = request.POST.get("return_url", "")
	# 	print(return_url)
	# 	# return_url = 'return_url'
	# else:
	# 	print(request.method, ' CALL')
	print('testing post')
	print(request)
	return render(request, 'admin.html')

def pull(request):
	print('pull');
	if request.method == 'POST':
		print('POST PULL')
	else:
		print('NOT POST PULL')
	return render(request, 'admin.html')

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
	        	'pull': 'https://pure-crag-61212.herokuapp.com/zendesk/telegram/pull',
	        	'channelback': 'https://pure-crag-61212.herokuapp.com/zendesk/telegram/channelback',
	        	'clickthrough': 'https://pure-crag-61212.herokuapp.com/zendesk/telegram/clickthrough'
	        }
	    }
	return JsonResponse(tasks)

@csrf_exempt
def send_metadata(request):
	if request.method == 'POST':
		name = request.POST.get('your_name', '')
		call_api(return_url)
	else:
		print('not post')
	# return render(request, 'admin.html')

def call_api (urls):
	# url = 'https://treesdemo1.zendesk.com/zendesk/channels/integration_service_instances/editor_finalizer'
	print('make request to ', urls)
	url = urls
	data = '''{
	  "metadata": {
	    "api_id": "new_api_id",
	    "api_hash": "new_api_hash",
	    "phone_number": "new_phone_number"
	  },
	  "name": "Telegram Integeration",
	}'''
	response = requests.post(url, data=data)
	print(response.text)
	if response.status_code == 200:
		print('call success')
	else:
		print('call failed')
	# return render(request, 'admin.html')