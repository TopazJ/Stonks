from django.shortcuts import render
# Create your views here.


def test(request):
    if request.user.is_authenticated:
        print("ya")
