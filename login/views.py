from django.shortcuts import render, get_object_or_404


def login(request):
    return render(request, 'login/login.html')


def register(request):
    return render(request, 'login/register.html')
