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
from .form_ig import AccessTokenForm
from django.shortcuts import redirect

userSelf_url = 'https://api.instagram.com/v1/users/self/?access_token='
userRecentMedia_url = 'https://api.instagram.com/v1/users/self/media/recent/?access_token='
userMediaComments_url = 'https://api.instagram.com/v1/media/'

herokuDomain = 'https://radiant-plains-54875.herokuapp.com/'

name = ''
username = ''
return_url = ''

# my_redirect_url = 'http://localhost:5000/zendesk/instagram/auth'
# my_redirect_url = 'https://pure-crag-61212.herokuapp.com/zendesk/instagram/auth'
my_redirect_url = herokuDomain + 'zendesk/instagram/givetoken'

my_client_id = 'efb368fd043148c0a0ca192aafbeb5d9' #@trees_zd
my_client_secret = '1a6cd86f5ff34efcac208292116039bc' #@trees_zd
my_access_token = '6681801146.935271d.0b8ba1e015024ec4b3e0759c8129abd6' #@trees_zd

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
		form = ContactForm(request.POST)
		if form.is_valid():
			print('form valid')
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
		else:
			print(form.errors)
	iframe_url = 'https://api.instagram.com/oauth/authorize/?client_id=' + my_client_id + '&redirect_uri=' + my_redirect_url + '&response_type=code&scope=comments+public_content'
	tokenForm = AccessTokenForm()
	# return redirect(iframe_url)
	return render(request, 'auth_ig.html', {'iframe_url': iframe_url, 'form': tokenForm})
	# return JsonResponse(testing)

@csrf_exempt
@xframe_options_exempt
def adminauth(request):
	print('adminauth')
	global my_access_token
	code = ''
	tokenForm = AccessTokenForm(request.POST)
	if tokenForm.is_valid():
		code = tokenForm.cleaned_data['token']

	parameter = {
			'client_id': my_client_id, 
			'client_secret': my_client_secret, 
			'grant_type': 'authorization_code', 
			'redirect_uri': my_redirect_url, 
			'code': code
			}
	r = requests.post("https://api.instagram.com/oauth/access_token", data=parameter)
	tokenData = json.loads(r.text)
	print(tokenData)
	my_access_token = tokenData['access_token']
	metaForm = SendMetaForm()
	metaForm.fields['metadata'].initial = '{"name":"' + username + '", "client_id": "' + my_client_id + '", "client_secret": "' + my_client_secret + '", "username": "' + username + '", "token": "' + my_access_token + '"}'
	metaForm.fields['name'].initial = name
	metaForm.fields['return_url'].initial = return_url

	return render(request, 'sendmeta_ig.html', {'form': metaForm, 'return_url': return_url})

@csrf_exempt
@xframe_options_exempt
def givetoken(request, code):
	code = request.GET.get('code')
	return render(request, 'givetoken.html', {'givemetoken': code})


def manifest(request):
	tasks = {
	        'name': 'Instagram Integeration',
	        'id': 'zendesk-internal-instagram-integration',
	        'author': 'Diastowo Faryduana', 
	        'version': 'v1.0',
	        'urls': {
	        	'admin_ui': herokuDomain + 'zendesk/instagram/admin_ui/',
	        	'pull_url': herokuDomain + 'zendesk/instagram/pull/',
	        	'channelback_url': herokuDomain + 'zendesk/instagram/channelback/',
	        	'clickthrough_url': herokuDomain + 'zendesk/instagram/clickthrough/'
	        }
	    }
	return JsonResponse(tasks)

@csrf_exempt
@xframe_options_exempt
def pull(request):
	channelbackFlag = True
	ext_resource = []
	pull = {}

	metadata = ''
	newState = ''
	if request.method == 'POST':
		print('POST PULL')
		metadata = request.POST.get('metadata', '')
		newState = request.POST.get('state', '')
	else:
		print('NOT POST PULL')
	
	metaJson = json.loads(metadata)
	client_id = metaJson['client_id']
	client_secret = metaJson['client_secret']
	access_token = metaJson['token']
	name = metaJson['name']

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
					"external_id": "post-" + posting_id,
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
						"external_id": "cmnt-" + comment['id'] + '-' + posting_id,
						"parent_id": "post-" + posting_id,
						"message": comment['text'],
						"created_at": newCommentDate,
						'author': {
							'external_id': 'ig-acc-' + comment['from']['id'],
							'name': comment['from']['username'],
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
	if request.method == 'POST':
		metadata = request.POST.get('metadata', '')
		newState = request.POST.get('state', '')
		message = request.POST.get('message', '')
		parentId = request.POST.get('parent_id', '')
		recipientId = request.POST.get('recipient_id', '')
		metaJson = json.loads(metadata)
		client_id = metaJson['client_id']
		client_secret = metaJson['client_secret']
		access_token = metaJson['token']
		name = metaJson['name']

		mediaId = parentId.split('-')
		print(mediaId)

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
