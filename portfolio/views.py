from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Portfolio
from django.db.models import Max
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import os
import json
# Create your views here.
@login_required(login_url='/auth/')  # redirect when user is not logged in
def portfolio(request):
    portfolio = Portfolio.objects.all().order_by('position')

    context = {
        'portfolio': portfolio,
    }

    return render(request, 'fa/portfolio/settings.html', context)

@login_required(login_url='/auth/') #redirect when user is not logged in
def portfolio_Insert(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get('link')

        if bool(request.FILES.get('image', False)) == True:
            image = request.FILES['image']
        else:
            image = 'uploads/portfolio/nopic.jpg'

        order = Portfolio.objects.aggregate(Max('position'))['position__max']

        if order:
            order += 1
        else:
            order = 1

        obj = Portfolio.objects.create(image=image, title=title, link=link, position=order)
        obj.save()

        messages.info(request, 'اطاعات وارد شده با موفقیت ثبت شد.')
        return redirect('/portfolio')

@csrf_exempt
def change_active_portfolio(request):
    id = request.POST.get('id')
    member = Portfolio.objects.get(pk=id)
    member.active = not(member.active)
    member.save()
    if not(member.active):
        messages.info(request, 'غیر فعال شد.')
    else:
        messages.info(request, 'فعال شد.')
    return HttpResponse()

@login_required(login_url='/auth/')  # redirect when user is not logged in
def delete_portfolio(request):
    id = request.POST.get('pk_id_del')
    member = Portfolio.objects.get(id=id)
    image_path = member.image.path

    if 'nopic' not in image_path:
        os.remove(image_path)

    member.delete()

    messages.info(request, 'اطلاعات حذف شد.')
    return redirect('/portfolio')

@csrf_exempt
def portfolio_edit(request):
    objects = []
    for item in Portfolio.objects.filter(pk=request.GET.get('pk')):
        objects.append({
            "title": item.title,
            "link": item.link,
            "image": item.image.url.replace('/media/',''),
        })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def portfolio_edit_save(request):
    id = request.POST.get('pk_id_edit')
    member = Portfolio.objects.get(id=id)
    if request.method == 'POST':

        title = request.POST.get('title')
        link = request.POST.get('link')

        if bool(request.FILES.get('image', False)) == True:
            image = request.FILES['image']
        else:
            image = member.image

        member.image = image
        member.title = title
        member.link = link
        member.save()

        messages.info(request, 'اطاعات با موفقیت بروزرسانی شد.')
        return redirect('/portfolio')