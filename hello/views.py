from telethon import TelegramClient
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext

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
	print('testing')
	return JsonResponse({'tasks':tasks})
    # return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def pull(request, user_id):
	# print(request)
	print(user_id)
	return JsonResponse({'tasks':tasks})

def get(request):
	userId = request.GET['userId']
	print(userId)
	return JsonResponse({'tasks':tasks})

@csrf_exempt
def post(request):
	if (request.method == 'POST') :
		title = request.POST.get("title", "")
		print(title)
	else:
		print('ITS NOT POST, ITS', request.method)
	# return JsonResponse({'tasks':tasks})
	return render(request, 'index.html')