from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated :
        return redirect('inbox')
    return render(request, 'website/pages/index.html')

@login_required
def inbox(request):
    return render(request, 'website/pages/inbox.html')

def login(request):
    if request.user.is_authenticated :
        return redirect('inbox')
    return render(request, 'website/pages/login.html')

def share(request):
    # TODO: If the id is same as requsted user then redirect to inbox page
    return render(request, 'website/pages/share.html')
