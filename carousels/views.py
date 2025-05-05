from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
import re
from .models import Sliders
from menu.models import Main
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from django.db import models

@login_required(login_url='/login/')  # redirect when user is not logged in
def carousels(request):
    pages = Main.objects.filter(active=True).order_by('position')
    sliders = Sliders.objects.order_by('position')
    print([x.image.url for x in sliders])
    print('----------------------------------')
    context = {
        'pages': pages,
        'sliders': sliders,
    }
    return render(request, 'fa/carousels/settings.html', context)

@login_required(login_url='/login/')  # redirect when user is not logged in
def carousels_insert(request):
    if request.method == 'POST':
        # بررسی آیا داده‌های اسلایدر در قالب JSON ارسال شده‌اند
        if 'slidersData' in request.POST:
            # دریافت داده‌های اسلایدر از JSON
            sliders_data = json.loads(request.POST.get('slidersData'))
            
            # دریافت فایل‌های آپلود شده
            uploaded_files = request.FILES.getlist('files[]')
            
            # تعیین موقعیت بعدی برای اسلایدرهای جدید
            position = Sliders.objects.aggregate(models.Max('position'))['position__max']
            if position is None:
                position = 0
            
            # ایجاد اسلایدر برای هر تصویر با داده‌های متناظر
            for slider_data in sliders_data:
                file_index = int(slider_data.get('fileIndex', 0))
                
                # اطمینان از اینکه فایل با این شاخص وجود دارد
                if file_index < len(uploaded_files):
                    # ایجاد اسلایدر جدید
                    position += 1
                    obj = Sliders.objects.create(
                        image=uploaded_files[file_index],
                        title=slider_data.get('title', ''),
                        short_text=slider_data.get('short_text', ''),
                        description=slider_data.get('description', ''),
                        link=slider_data.get('link', ''),
                        userId_id=request.user.id,
                        position=position
                    )
            
            messages.info(request, 'اسلایدرها با موفقیت اضافه شدند.')
            
            # در حالت AJAX، پاسخ JSON ارسال می‌کنیم
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'اسلایدرها با موفقیت اضافه شدند.'})
            else:
                return redirect('/carousels')
            
        # روش قدیمی برای سازگاری با نسخه‌های قبلی
        else:
            uploaded_files = request.FILES.getlist('files')
            
            # تعیین موقعیت بعدی برای اسلایدرهای جدید
            position = Sliders.objects.aggregate(models.Max('position'))['position__max']
            if position is None:
                position = 0
                
            for userfiledata in uploaded_files:
                image = userfiledata
                title = request.POST.get('title')
                short_text = request.POST.get('short_text', '')
                description = request.POST.get('desc', '')
                current_user = request.user.id
                link = request.POST.get('link', '')

                obj = Sliders.objects.create(
                    image=image, 
                    title=title, 
                    short_text=short_text,
                    description=description,
                    link=link, 
                    userId_id=current_user,
                    position=position + 1
                )
                position += 1

            messages.info(request, 'اسلایدر با موفقیت اضافه شد.')
            return redirect('/carousels')
            
    # برای درخواست‌های GET صفحه را نمایش می‌دهیم
    return redirect('/carousels')

@login_required(login_url='/login/')  # redirect when user is not logged in
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

@login_required(login_url='/login/')  # redirect when user is not logged in
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

@csrf_exempt
def save_order(request):
    if request.method == 'POST':
        order = request.POST.get('order')
        # Extract the IDs from the order string
        # Format is like "slider[]=1&slider[]=2&slider[]=3"
        ids = re.findall(r'slider\[\]=(\d+)', order)
        
        # Update position for each slider
        for i, id in enumerate(ids, 1):
            slider = Sliders.objects.get(pk=id)
            slider.position = i
            slider.save()
            
    return HttpResponse('Order saved successfully')
