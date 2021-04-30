from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .utils import generate_pin, generate_unique_username
from django.http import HttpResponse

def index(request):
    if request.user.is_authenticated :
        return redirect('inbox')
    
    if request.method == 'POST':
        name = request.POST.get('name', '')
        username = generate_unique_username()
        password = generate_pin()
        user = User.objects.create_user(
            username=username,
            password=password,
        )
        user.first_name = name
        user.last_name = password # quickfix: store raw_password in last name field
        user.save()
        auth_user = authenticate(request, username=username, password=password)
        if auth_user is not None:
            if auth_user.is_active:
                auth_login(request, auth_user)
                return redirect('inbox')
            else:
                return HttpResponse('<h1>Profile is deactivated.</h1>')
        else:
            return HttpResponse('<h1>Wrong Credentials</h1>')

    return render(request, 'website/pages/index.html')

@login_required
def inbox(request):
    return render(request, 'website/pages/inbox.html')

def login(request):
    context = {}

    if request.user.is_authenticated :
        return redirect('inbox')

    if request.method == 'POST':
        username = request.POST['userid']
        password = request.POST['pin']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('inbox')
            else:
                context['error'] = "Profile is deactivated by admin."
        else:
            context['error'] = "Wrong Userid or pin."

    return render(request, 'website/pages/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('index')

def share(request):
    # TODO: If the id is same as requsted user then redirect to inbox page
    return render(request, 'website/pages/share.html')
