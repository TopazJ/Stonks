from django.shortcuts import render
import json
from django.http import HttpResponse
from django.contrib.auth import authenticate

# Create your views here.


def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        # print(request.POST)
        if user is not None:
            response_data = {'yeet': 'yeet'}
            if user.is_active:
                login(request, user)
        else:
            response_data = {'bad': 'bad'}

        return HttpResponse(json.dumps(response_data), content_type="application/json")
