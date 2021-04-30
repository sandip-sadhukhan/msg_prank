from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .utils import generate_pin, generate_unique_username
from django.http import HttpResponse, JsonResponse
from .models import Message

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
    messages = Message.objects.filter(user=request.user)
    context = {'messages': messages}
    return render(request, 'website/pages/inbox.html', context)

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
    id = request.GET.get('id')
    try:
        user = User.objects.get(username=id)
        if request.user.is_authenticated:
            if user.username == request.user.username:
                return redirect('inbox')
    except User.DoesNotExist:
        return HttpResponse('<h1>Link doesn\'t exists</h1>')

    if request.method == 'POST':
        message = request.POST.get('message', '')
        if message.strip() == '':
            return redirect('index')
        else:
            # create msg
            Message.objects.create(user=user, message=message)
            context = {'msg': '👍 Message Sent Successfully'}
            return render(request, 'website/pages/index.html', context)

    context = {'curr_user': user}
    return render(request, 'website/pages/share.html', context)

@login_required
def deleteMessage(request):
    id = request.GET.get('id')
    try:
        message = Message.objects.get(id=id)
        if message.user == request.user:
            message.delete()
        return JsonResponse({"success":True, "msg": "Message Successfully deleted"})
    except:
        return JsonResponse({"success":False, "msg": "Message Not Found!"})

@login_required
def deleteAccount(request):
    request.user.delete()
    return redirect('index')