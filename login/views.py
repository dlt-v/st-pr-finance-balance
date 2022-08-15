from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as log_user, logout as logout_user
from django.contrib.auth.models import User


def login(request):
    if request.method == 'POST':
        user_mail = request.POST['email']
        user_password = request.POST['password']
        user = authenticate(request, username=user_mail, password=user_password)
        if user is not None:
            log_user(request, user)
            return redirect('savings:index')
        else:
            context = {
                "warning": "Wrong username or password."
            }
            return render(request, 'login/login.html', context)
    return render(request, 'login/login.html')


def register(request):
    if request.method == 'POST':
        user_mail = request.POST['reg_email']
        user_password = request.POST['reg_passwd']
        user_password2 = request.POST['reg_passwd2']
        if user_password == user_password2 and not User.objects.filter(email=user_mail).exists():
            new_user = User.objects.create_user(user_mail, user_mail, user_password)
            new_user.save()
            print(new_user)
            return redirect('login:login')
        else:
            context = {
                "warning": "Email already exists or the passwords don't match."
            }
            return render(request, 'login/register.html', context)
    return render(request, 'login/register.html')


def logout(request):
    logout_user(request)
    return redirect('login:login')
