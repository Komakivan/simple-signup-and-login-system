from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from rashhour import settings


def home(request):
    return render(request,'registration/home.html')

def signup(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1!=pass2:
            messages.error(request,'paswords dont match ')

        if len(username)>15:
            messages.error(request,'username too long')

        user = User.objects.create_user(username,email,pass1)
        user.pass2 = pass2
        user.save()

        subject = 'norepy message'
        message = 'hello ' + user.username + 'welcome to just kart.\n we are so delighted to have you.\n Please confirm your email address to proceed'
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        return redirect('signin')


    return render(request,'registration/signup.html')


def signin(request):

    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email,password=password)

        if user is None:
            messages.error(request,'wrong credentials entered')
        else:
            login(request,user)
            messages.success(request, 'successfully logged in the system')
        return redirect('home')

    return render(request,'registration/login.html',)

def signout(request):
    logout(request)
    messages.success(request,'log out successful')
    return redirect('home')

