from telethon import TelegramClient
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import requests

return_url = ''
@csrf_exempt
def admin(request):
	if (request.method == 'POST'):
		print('POST CALL')
		# return_url = request.POST.get("return_url", "")
		global return_url
		return_url = 'return_url'
	else:
		print(request.method, ' CALL')

	return render(request, 'admin.html')

def pull(request):
	print('pull');
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
	        	'admin_ui':'admin_ui',
	        	'pull': 'pull',
	        	'channelback': 'channelback',
	        	'clickthrough': 'clickthrough'
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

def call_api (url):
	url = url
	data = '''{
	  "metadata": {
	    "api_id": "new_api_id",
	    "api_hash": "new_api_hash",
	    "phone_number": "new_phone_number"
	  },
	  "name": "Telegram Integeration",
	}'''
	response = requests.post(url, data=data)
	if response.status_code == 200:
		print('call success')
	else:
		print('call failed')

	return render(request, 'admin.html')