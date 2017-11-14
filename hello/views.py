from telethon import TelegramClient
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from .models import Greeting

tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

# Create your views here.
def index(request):

	api_id = 184365
	api_hash = '640727dc57738548a9cbc23e5d8d1bbe'
	phone = '+6281294059775'
	client = TelegramClient('diastowo', api_id, api_hash)
	client.connect()

	if not client.is_user_authorized():
		print('not logged in')
		client.send_code_request(phone);
		client.sign_in(phone, input('Enter the code: '));
	else :
		print('login success');

	# dialogs, entities = client.get_dialogs(5)
	# for entity in entities:
	# 	print('firstname: ', entity.first_name, ' username: ', entity.username, ' user id: ', entity.id);

	# result = client(GetHistoryRequest(
	# 		entities[4],
	# 		limit=20,
	# 		offset_date=None,
	# 	    offset_id=0,
	# 	    max_id=0,
	# 	    min_id=0,
	# 	    add_offset=0
	#     ));
	# print(result.messages[0].message);

    return JsonResponse({'tasks':tasks})
    # return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

