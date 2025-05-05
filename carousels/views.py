from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import shutil
import os
from .models import Sliders
from menu.models import Main
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
# Create your views here.
@login_required(login_url='/auth/')  # redirect when user is not logged in
def carousels(request):
    pages = Main.objects.filter(active=True).order_by('position')
    sliders = Sliders.objects.order_by('position')

    context = {
        'pages': pages,
        'sliders': sliders,
    }
    return render(request, 'fa/carousels/settings.html', context)

@login_required(login_url='/auth/')  # redirect when user is not logged in
def carousels_insert(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')
        slider_type = request.POST.get('slider_type')

        slider_path = 'media/carousels/main'
        if os.path.isdir(slider_path):
            shutil.rmtree(slider_path)

        Sliders.objects.all().delete()

        i = 1
        for userfiledata in uploaded_files:
            image = userfiledata
            title = request.POST.get('title')
            desc = request.POST.get('desc')
            current_user = request.user.id
            link = request.POST.get('link')
            view_in = request.POST.get('view_in')

            obj = Sliders.objects.create(type=slider_type, image=image, title=title, link=link, description=desc,
                                          userId_id=current_user, view_in=view_in, position=i)
            obj.save()
            i += 1

    messages.info(request, 'اطاعات وارد شده با موفقیت ثبت شد.')
    return redirect('/carousels')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def delete_slider(request):
    id = request.POST.get('pk_id_del')
    member = Sliders.objects.get(id=id)
    image_path = member.image.path
    os.remove(image_path)

    member.delete()

    messages.info(request, 'اطلاعات حذف شد.')
    return redirect('/carousels')

@csrf_exempt
def change_active_slider(request):
    id = request.POST.get('id')
    member = Sliders.objects.get(pk=id)
    member.active = not(member.active)
    member.save()
    if not (member.active):
        messages.info(request, 'غیر فعال شد.')
    else:
        messages.info(request, 'فعال شد.')
    return HttpResponse()

@csrf_exempt
def carousels_edit(request):
    objects = []
    for item in Sliders.objects.filter(pk=request.GET.get('pk')):
        objects.append({
            "title": item.title,
            "short_text": item.short_text,
            "description": item.description,
            "link": item.link,
            "image": item.image.url.replace('/media/',''),
        })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def carousels_edit_save(request):
    id = request.POST.get('pk_id_edit')
    member = Sliders.objects.get(id=id)
    if request.method == 'POST':

        title = request.POST.get('title')
        short_text = request.POST.get('short_text')
        description = request.POST.get('desc')
        link = request.POST.get('link')

        if bool(request.FILES.get('image', False)) == True:
            image = request.FILES['image']
            image_path = member.image.path
            os.remove(image_path)
        else:
            image = member.image

        member.image = image
        member.title = title
        member.short_text = short_text
        member.link = link
        member.description = description
        member.save()

        messages.info(request, 'اطاعات وارد شده با موفقیت بروزرسانی شد.')
        return redirect('/carousels')
