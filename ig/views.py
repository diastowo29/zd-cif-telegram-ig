from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.views.decorators.clickjacking import xframe_options_exempt
import requests
import json
from datetime import datetime
from .form_ig import ContactForm
from .form_ig import GetTokenForm
from .form_ig import MetaContactForm
from .form_ig import SendMetaForm
from django.shortcuts import redirect

userSelf_url = 'https://api.instagram.com/v1/users/self/?access_token='
userRecentMedia_url = 'https://api.instagram.com/v1/users/self/media/recent/?access_token='
userMediaComments_url = 'https://api.instagram.com/v1/media/'
channelbackFlag = False

name = ''
username = ''
return_url = ''

# my_redirect_url = 'http://localhost:5000/zendesk/instagram/auth'
my_redirect_url = 'https://pure-crag-61212.herokuapp.com/zendesk/instagram/auth'

# my_client_id = '1267bd385de6433ab84d06d981e4c213'
# my_client_secret = '6ac0461eccb14f99a0313ff3f846867b'
# access_token = "530621889.1267bd3.a7551d9e5f0041e19dd7e9c3cc04a0ce" #@diastowoo
# access_token = "4134206752.7d1fc69.22ff7bc7d940493facc1866741c99b4b" #@divvapes_bogor

my_client_id = 'e7571324f43d4de7a0a2ed23741c5dc9' #@trees_zd
my_client_secret = 'de94bb10002343cf81aaddba094986dd' #@trees_zd
access_token = '6681801146.935271d.0b8ba1e015024ec4b3e0759c8129abd6' #@trees_zd

@csrf_exempt
@xframe_options_exempt
def admin(request):
	if request.method == 'POST':
		global return_url
		return_url = request.POST.get('return_url', '')
	form = ContactForm()
	return render(request, 'admin_ig.html', {'form': form})

@csrf_exempt
@xframe_options_exempt
def doAuth(request):
	# testing = ''
	global username
	global name
	global my_client_id
	global my_client_secret
	if request.method == 'POST':
		print('yes it is')
		form = ContactForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			name = form.cleaned_data['name']
			my_client_id = form.cleaned_data['client_id']
			my_client_secret = form.cleaned_data['client_secret']
			# testing = {
			# 	'name': name,
			# 	'username': username,
			# 	'client_id': my_client_id,
			# 	'client_secret' : my_client_secret
			# }
	return redirect('https://api.instagram.com/oauth/authorize/?client_id=' + my_client_id + '&redirect_uri=' + my_redirect_url + '&response_type=code')
	# return JsonResponse(testing)

@csrf_exempt
@xframe_options_exempt
def adminauth(request, code):
	print('adminauth')
	parameter = {
			'client_id': my_client_id, 
			'client_secret': my_client_secret, 
			'grant_type': 'authorization_code', 
			'redirect_uri': my_redirect_url, 
			'code': request.GET.get('code')
			}
	r = requests.post("https://api.instagram.com/oauth/access_token", data=parameter)
	tokenData = json.loads(r.text)
	metaForm = SendMetaForm()
	metaForm.fields['metadata'].initial = '{"name":"' + username + '", "client_id": "' + my_client_id + '", "client_secret": "' + my_client_secret + '", "username": "' + username + '", "token": "' + tokenData['access_token'] + '"}'
	metaForm.fields['name'].initial = name
	metaForm.fields['return_url'].initial = return_url

	return render(request, 'sendmeta_ig.html', {'form': metaForm, 'return_url': return_url})

def manifest(request):
	tasks = {
	        'name': 'Instagram Integeration',
	        'id': 'zendesk-internal-instagram-integration',
	        'author': 'Diastowo Faryduana', 
	        'version': 'v1.0',
	        'urls': {
	        	'admin_ui':'https://pure-crag-61212.herokuapp.com/zendesk/instagram/admin_ui/',
	        	'pull_url': 'https://pure-crag-61212.herokuapp.com/zendesk/instagram/pull/',
	        	'channelback_url': 'https://pure-crag-61212.herokuapp.com/zendesk/instagram/channelback/',
	        	'clickthrough_url': 'https://pure-crag-61212.herokuapp.com/zendesk/instagram/clickthrough/'
	        }
	    }
	return JsonResponse(tasks)

@csrf_exempt
@xframe_options_exempt
def pull(request):
	ext_resource = []
	pull = {}

	response = call_api(userSelf_url, access_token)
	if response.status_code == 200:
		getUser = json.loads(response.text)
		user_id = getUser['data']['id']
		responseMedia = call_api(userRecentMedia_url, access_token)
		if responseMedia.status_code == 200:
			getMedia = json.loads(responseMedia.text)
			for media in getMedia['data']:
				posting_id = media['id']
				newDate = datetime.fromtimestamp(int(media['created_time'])).strftime('%Y-%m-%dT%H:%M:%SZ')
				commentUrl = userMediaComments_url + posting_id + '/comments?access_token='
				message = ''
				message = {
					"external_id": posting_id,
					"message": media['caption']['text'],
					"created_at": newDate,
					'author': {
						'external_id': 'ig-acc-' + media['user']['id'],
						'name': media['user']['full_name'],
					},
					'allow_channelback': channelbackFlag
				}
				ext_resource.extend([message])
				responseComment = call_api(commentUrl, access_token)
				if responseComment.status_code == 200 :
					getComments = json.loads(responseComment.text)
					for comment in getComments['data']:
						newCommentDate = datetime.fromtimestamp(int(comment['created_time'])).strftime('%Y-%m-%dT%H:%M:%SZ')
						message = {
						"external_id": comment['id'],
						"parent_id": posting_id,
						"message": comment['text'],
						"created_at": newCommentDate,
						'author': {
							'external_id': 'ig-acc-' + comment['from']['id'],
							'name': comment['from']['full_name'],
						},
						'allow_channelback': channelbackFlag
						}
						ext_resource.extend([message])

	return JsonResponse({'external_resources': ext_resource, 'state': "{\"last_message_id\":\"testing\"}"})


def call_api (urls, token):
	url = urls + token
	response = requests.get(url)
	return response

def handler500(request):
    return render(request, 'admin_ig.html', status=500)

@csrf_exempt
@xframe_options_exempt
def channelback(request):
	return JsonResponse({})

@csrf_exempt
@xframe_options_exempt
def clickthrough(request):
	if request.method == 'POST':
		print('POST')
	else:
		print('GET')
		print(request.GET.get('fromuid'))
	return JsonResponse({})
