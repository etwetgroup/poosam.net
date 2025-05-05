from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Main, UrlCatergory
from django.db.models import Max
from django.contrib import messages
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import os
import shutil

# Create your views here.
@login_required(login_url='/auth/')  # redirect when user is not logged in
def main_menu(request):
    mains = Main.objects.filter(sub_menu=None).order_by('position')

    context = {
        'mains': mains,
    }

    return render(request, 'fa/menu/main.html', context)

@login_required(login_url='/auth/')  # redirect when user is not logged in
def menu_add(request):
    return render(request, 'fa/menu/add.html')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def sub_menu_add(request,id):
    content = Main.objects.get(pk=id)
    # content = get_object_or_404(content, slug=slug)

    context = {
        'content': content,
    }
    return render(request, 'fa/menu/sub.html', context)

@login_required(login_url='/auth/') #redirect when user is not logged in
def main_menu_insert(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        titleseo = request.POST.get('titleseo')
        keywords = request.POST.get('keywords')
        description = request.POST.get('desc')
        current_user = request.user.id
        canonical = request.POST.get('canonical')

        if request.POST.get('noindex') == 'on':
            noindex = True
        else:
            noindex = False

        if request.POST.get('showCmnt') == 'on':
            showCmnt = True
        else:
            showCmnt = False

        text = request.POST.get('text')

        order = Main.objects.aggregate(Max('position'))['position__max']

        if order:
            order += 1
        else:
            order = 1

        obj = Main.objects.create(title=title, titleseo=titleseo, keywords=keywords, description=description, text=text, noindexnofollow=noindex, position=order, userId_id=current_user, canonical=canonical, showCmnt=showCmnt, image='uploads/pages/nopic.jpg')
        obj.save()

        messages.info(request, 'اطاعات منوی اصلی وارد شده با موفقیت ثبت شد.')
        return redirect('/mainMenu')

@login_required(login_url='/auth/') #redirect when user is not logged in
def main_submenu_insert(request):
    if request.method == 'POST':
        sub_menu_id = request.POST.get('pk_id_insert')
        title = request.POST.get('title')
        titleseo = request.POST.get('titleseo')
        keywords = request.POST.get('keywords')
        description = request.POST.get('desc')
        current_user = request.user.id
        canonical = request.POST.get('canonical')

        if request.POST.get('noindex') == 'on':
            noindex = True
        else:
            noindex = False

        if request.POST.get('showCmnt') == 'on':
            showCmnt = True
        else:
            showCmnt = False

        text = request.POST.get('text')

        order = Main.objects.aggregate(Max('position'))['position__max']

        if order:
            order += 1
        else:
            order = 1

        obj = Main.objects.create(sub_menu_id=sub_menu_id, title=title, titleseo=titleseo, keywords=keywords, description=description, text=text, noindexnofollow=noindex, position=order, userId_id=current_user, canonical=canonical, showCmnt=showCmnt, image='uploads/pages/nopic.jpg')
        obj.save()

        messages.info(request, 'اطاعات زیر منوی وارد شده با موفقیت ثبت شد.')
        return redirect('/mainMenu')


@csrf_exempt
def main_menu_parent_datasource(request):
    objects = []
    for item in Main.objects.filter(sub_menu__isnull=True).order_by('position'):
        objects.append({
            'ID': item.id,
            'title': item.title,
            'slug': item.slug,
            'sub_menu_id': item.sub_menu_id,
            'active': item.active,
        })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@csrf_exempt
def main_submenu_datasource(request):
    objects = []
    for item in Main.objects.filter(sub_menu__isnull=False).order_by('position'):
        objects.append({
            'ID': item.id,
            'title': item.title,
            'slug': item.slug,
            'sub_menu_id': item.sub_menu_id,
            'active': item.active,
        })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@csrf_exempt
def main_menu_delete(request, id):
    member = Main.objects.get(id=id)
    member.delete()
    # messages.info(request, 'اطلاعات با موفقیت حذف شد.')
    return HttpResponse('ok')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def main_menu_edit(request,id):
    # objects = []
    # for item in Main.objects.filter(pk=request.GET.get('pk')):
    #     objects.append({
    #         "title": item.title,
    #         "titleseo": item.titleseo,
    #         "keywords": item.keywords,
    #         "description": item.description,
    #         "text": item.text,
    #         "canonical": item.canonical,
    #         "noindex": item.noindexnofollow,
    #         "showCmnt": item.showCmnt,
    #     })
    # return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')
    content = Main.objects.get(pk=id)
    # content = get_object_or_404(content, slug=slug)

    context = {
        'content': content,
    }
    return render(request, 'fa/menu/edit.html', context)

@login_required(login_url='/auth/')  # redirect when user is not logged in
def sub_menu_edit(request,id):
    content = Main.objects.get(pk=id)
    img_list = []
    path = 'media/uploads/pages/{0}'.format(id)
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            img_list.append('/media/uploads/pages/{0}/{1}'.format(id, file))
    context = {
        'content': content,
        'img_list': img_list,
    }
    return render(request, 'fa/menu/sub-edit.html', context)
@login_required(login_url='/auth/')  # redirect when user is not logged in
def main_menu_edit_save(request):
    id = request.POST.get('pk_id_edit')
    member = Main.objects.get(id=id)
    if request.method == 'POST':

        title = request.POST.get('title')
        titleseo = request.POST.get('titleseo')
        keywords = request.POST.get('keywords')
        desc = request.POST.get('desc')
        text = request.POST.get('text')
        canonical = request.POST.get('canonical')
        orgimg = request.POST.get('orgimg')
        type = request.POST.get('type')
        img_delete = request.POST.get('img_delete')[1:]

        del_org_image = True
        if img_delete:
            delete_list = img_delete.split(",")
            for file in delete_list:
                path_file = 'media/uploads/pages/{0}/{1}'.format(id, file)
                if os.path.exists(path_file):
                    os.remove(path_file)
                    if file in member.image:
                        del_org_image = False
                        member.image = 'uploads/pages/nopic.jpg'
                        member.save()

            path_directory = 'media/uploads/pages/{0}'.format(id)
            files = os.listdir(path_directory)
            number_files = len(files)
            if number_files == 0:
                shutil.rmtree(path_directory)

        display = request.POST.get('display')
        if display == None:
            display = True

        if request.POST.get('noindex') == 'on':
            noindex = True
        else:
            noindex = False

        if request.POST.get('showCmnt') == 'on':
            showCmnt = True
        else:
            showCmnt = False

        if request.POST.get('showHome') == 'on':
            showHome = True
        else:
            showHome = False

        if request.POST.get('mostVisited') == 'on':
            mostVisited = True
        else:
            mostVisited = False

        if del_org_image and type == 'sub':
            member.image = 'uploads/pages/{0}/{1}'.format(id, orgimg.replace('uploads/pages/{0}/'.format(id), ''))

        member.title = title
        member.titleseo = titleseo
        member.keywords = keywords
        member.description = desc
        member.text = text
        member.canonical = canonical
        member.noindexnofollow = noindex
        member.showCmnt = showCmnt
        member.display = display
        member.showHome = showHome
        member.mostVisited = mostVisited
        member.save()

        uploaded_files = request.FILES.getlist('files')

        images_path = 'media/uploads/pages/{0}'.format(id)
        # if os.path.isdir(slider_path):
        #     shutil.rmtree(slider_path)
        fs = FileSystemStorage(location=images_path)
        for userfiledata in uploaded_files:
            fs.save(userfiledata.name, userfiledata)

        messages.info(request, 'اطاعات وارد شده با موفقیت بروزرسانی شد.')
        return redirect('/mainMenu')

@csrf_exempt
def change_main_menu_active(request,id):
    member = Main.objects.get(id=id)
    member.active = not (member.active)
    member.save()
    if not(member.active):
        messages.info(request, 'غیر فعال شد.')
    else:
        messages.info(request, 'فعال شد.')
    return HttpResponse()

@login_required(login_url='/auth/')
def url_category_main(request):
    categories = UrlCatergory.objects.all().order_by('-sh_created_at')
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'fa/link/main.html', context)

@login_required(login_url='/auth/')
def url_category_add(request):
    return render(request, 'fa/link/add.html')

@login_required(login_url='/auth/')
def url_category_insert(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        url = request.POST.get('url')
        
        if request.POST.get('is_active') == 'on':
            is_active = True
        else:
            is_active = False
            
        current_user = request.user
        
        obj = UrlCatergory.objects.create(
            title=title, 
            url=url, 
            is_active=is_active, 
            userId=current_user
        )
        obj.save()
        
        messages.info(request, 'دسته بندی لینک با موفقیت ثبت شد.')
        return redirect('/urlCategories')

@login_required(login_url='/auth/')
def url_category_edit(request, id):
    category = UrlCatergory.objects.get(pk=id)
    
    context = {
        'category': category,
    }
    return render(request, 'fa/link/edit.html', context)

@login_required(login_url='/auth/')
def url_category_edit_save(request):
    if request.method == 'POST':
        id = request.POST.get('pk_id_edit')
        category = UrlCatergory.objects.get(id=id)
        
        title = request.POST.get('title')
        url = request.POST.get('url')
        
        if request.POST.get('is_active') == 'on':
            is_active = True
        else:
            is_active = False
        
        category.title = title
        category.url = url
        category.is_active = is_active
        category.save()
        
        messages.info(request, 'دسته بندی لینک با موفقیت ویرایش شد.')
        return redirect('/urlCategories')

@csrf_exempt
def url_category_delete(request, id):
    category = UrlCatergory.objects.get(id=id)
    category.delete()
    return HttpResponse('ok')

@csrf_exempt
def url_category_datasource(request):
    objects = []
    for item in UrlCatergory.objects.all().order_by('-sh_created_at'):
        objects.append({
            'ID': item.id,
            'title': item.title,
            'url': item.url,
            'is_active': item.is_active,
            'created_date': item.sh_created_at.strftime('%Y/%m/%d')
        })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@csrf_exempt
def change_url_category_active(request, id):
    category = UrlCatergory.objects.get(id=id)
    category.is_active = not category.is_active
    category.save()
    return HttpResponse('ok')



