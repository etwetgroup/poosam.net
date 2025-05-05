from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Config
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.
@login_required(login_url='/auth/')  # redirect when user is not logged in
def website(request):
    return render(request, 'fa/website/settings.html')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def pages(request):
    return render(request, 'fa/pages/settings.html')

@csrf_exempt
def change_website(request):
    if request.method == 'POST':
        key = request.POST['key']
        value = request.POST['value']

        Config.objects.filter(key=key).update(value=value)

    return HttpResponse()

@csrf_exempt
def uploadFile(request):
    try:
        key = request.POST.get('key')
        file = request.FILES.getlist('file')

        member = Config.objects.get(key=key)
        fs = FileSystemStorage(location='media/uploads/main')

        name = ''
        for filedata in file:
            fs.save(filedata.name, filedata)
            name = filedata.name

        os.remove('media/' + member.value)

        member.value = 'uploads/main/' + name
        member.save()

        return HttpResponse('/media/' + member.value)
    except:
        return HttpResponse('error')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def saveLink(request):
    btn = 'main_' + request.POST.get('btnlink')
    link = request.POST.get('txtLink')
    member = Config.objects.get(key=btn)
    member.link = link
    member.save()
    return redirect('/website')

