from django.shortcuts import render
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            response_data = {'status': 'success'}
            if user.is_active:
                login(request, user)
        else:
            response_data = {'status': "Couldn't log you in, account might not exist!"}

        return JsonResponse(response_data)


def logout_user(request):
    logout(request)
    return JsonResponse({'status':'success'})


def status(request):
    if request.user.is_authenticated:
        return JsonResponse({'status': 'user'})
    else:
        return JsonResponse({'status': 'anon'})


def authenticated(request):
    if request.user.is_authenticated:
        return True
    else:
        return False



