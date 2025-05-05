from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from notices.models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import os
import json
from django.db.models import Max
from urllib.parse import unquote
from menu.models import Main
from portfolio.models import Portfolio
from carousels.models import Sliders
from faq.models import Faq,Survey
from products.models import DetailsTitle,Products

# Create your views here.
@login_required(login_url='/auth/')  # redirect when user is not logged in
def news_category(request):
    notices = Category.objects.order_by('position')
    noticesGroup = Category.objects.order_by('position')

    context = {
        'notices': notices,
        'noticesGroup': noticesGroup,
    }
    return render(request, 'fa/notices/category.html', context)

@login_required(login_url='/auth/') #redirect when user is not logged in
def notice_category_insert(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        titleseo = request.POST.get('titleseo')
        keywords = request.POST.get('keywords')
        desc = request.POST.get('desc')
        current_user = request.user.id
        if bool(request.FILES.get('image', False)) == True:
            image = request.FILES['image']
        else:
            image = 'uploads/notices/nopic.jpg'

        order = Category.objects.aggregate(Max('position'))['position__max']

        if order:
            order += 1
        else:
            order = 1

        obj = Category.objects.create(image=image, title=title, titleseo=titleseo, keywords=keywords, description=desc, userId_id=current_user, position=order)
        obj.save()

        messages.info(request, 'اطاعات وارد شده با موفقیت ثبت شد.')
        return redirect('/newscategory')

@csrf_exempt
def notice_change_active_category(request):
    id = request.POST.get('id')
    member = Category.objects.get(pk=id)
    member.active = not(member.active)
    member.save()
    if not(member.active):
        messages.info(request, 'گروه و تمامی زیر مجموعه های آن غیر فعال شد.')
    else:
        messages.info(request, 'گروه و تمامی زیر مجموعه های آن فعال شد.')
    return HttpResponse()

@login_required(login_url='/auth/')  # redirect when user is not logged in
def notice_delete_category(request):
    id = request.POST.get('pk_id_del')
    member = Category.objects.get(id=id)
    image_path = member.image.path

    if 'nopic' not in image_path:
        os.remove(image_path)

    member.delete()

    messages.info(request, 'اطلاعات حذف شد.')
    return redirect('/newscategory')

@csrf_exempt
def notice_category_edit(request):
    objects = []
    for item in Category.objects.filter(pk=request.GET.get('pk')):
        objects.append({
            "title": item.title,
            "titleseo": item.titleseo,
            "keywords": item.keywords,
            "description": item.description,
            "image": item.image.url.replace('/media/',''),
        })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def notice_category_edit_save(request):
    id = request.POST.get('pk_id_edit')
    member = Category.objects.get(id=id)
    if request.method == 'POST':

        title = request.POST.get('title')
        titleseo = request.POST.get('titleseo')
        keywords = request.POST.get('keywords')
        description = request.POST.get('desc')

        if bool(request.FILES.get('image', False)) == True:
            image = request.FILES['image']
        else:
            image = member.image

        member.image = image
        member.title = title
        member.titleseo = titleseo
        member.keywords = keywords
        member.description = description
        member.save()

        messages.info(request, 'اطاعات وارد شده با موفقیت بروزرسانی شد.')
        return redirect('/newscategory')

@csrf_exempt
def save_order(request):
    table = request.POST.get('table')
    if table == "notices_category":
        order = request.POST.get('order')
        order = order.replace('[]=', '').replace('noticecat', '')
        order = order.split("&")

        i = 1
        for item in order:
            Category.objects.filter(id=item).update(position=i)
            i += 1

    if table == "main_slider":
        order = request.POST.get('order')
        order = order.replace('[]=', '').replace('slider', '')
        order = order.split("&")

        i = 1
        for item in order:
            Sliders.objects.filter(id=item).update(position=i)
            i += 1

    if table == "mainmenu":
        i = 1
        keys = json.loads(request.POST.get('result'))
        for course in keys:
            Main.objects.filter(pk=course['ID']).update(position=i)
            i = i + 1

    if table == "detailsTitle":
        i = 1
        keys = json.loads(request.POST.get('result'))
        for course in keys:
            DetailsTitle.objects.filter(pk=course['ID']).update(position=i)
            i = i + 1

    if table == "products":
        i = 1
        keys = json.loads(request.POST.get('result'))
        for course in keys:
            Products.objects.filter(pk=course['ID']).update(position=i)
            i = i + 1

    if table == "faq":
        i = 1
        keys = json.loads(request.POST.get('result'))
        for course in keys:
            Faq.objects.filter(pk=course['ID']).update(position=i)
            i = i + 1

    if table == "survey":
        i = 1
        keys = json.loads(request.POST.get('result'))
        for course in keys:
            Survey.objects.filter(pk=course['ID']).update(position=i)
            i = i + 1

    if table == "portfolio":
        order = request.POST.get('order')
        order = order.replace('[]=', '').replace('portfolio', '')
        order = order.split("&")

        i = 1
        for item in order:
            Portfolio.objects.filter(id=item).update(position=i)
            i += 1

    return HttpResponse()

@login_required(login_url='/auth/')  # redirect when user is not logged in
def news(request,id):
    # slug = unquote(slug)

    content = Category.objects.get(pk=id)
    # content = get_object_or_404(content, slug=slug)

    news = News.objects.filter(newscat_id=content.pk)
    paginator = Paginator(news, 5)
    num_of_pages = paginator.num_pages

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'content': content,
        'news': page_obj,
        'num_of_pages': num_of_pages,
    }

    return render(request, 'fa/notices/news.html', context)

@login_required(login_url='/auth/')  # redirect when user is not logged in
def notice_news_add(request,id):
    content = Category.objects.get(pk=id)
    # content = get_object_or_404(content, slug=slug)

    context = {
        'content': content,
    }

    return render(request, 'fa/notices/add-news.html', context)

@login_required(login_url='/auth/') #redirect when user is not logged in
def notice_news_insert(request):
    if request.method == 'POST':
        slug = request.POST.get('slug')
        slug_pk = request.POST.get('slug_pk')
        title = request.POST.get('title')
        titleseo = request.POST.get('titleseo')
        short_text = request.POST.get('short_text')

        if request.POST.get('hot') == 'on':
            hot = True
        else:
            hot = False

        text = request.POST.get('text')

        if bool(request.FILES.get('image', False)) == True:
            image = request.FILES['image']
        else:
            image = 'uploads/notices/nopic.jpg'

        obj = News.objects.create(image=image, title=title, titleseo=titleseo, short_text=short_text, text=text, newscat_id=slug_pk, hot=hot)
        obj.save()

        messages.info(request, 'اطاعات وارد شده با موفقیت ثبت شد.')
        return redirect('/news/{0}/'.format(slug_pk))

@login_required(login_url='/auth/')  # redirect when user is not logged in
def notice_delete_news(request):
    id = request.POST.get('pk_id_del')
    member = News.objects.get(id=id)
    content = Category.objects.get(id=member.newscat_id)
    slug = content.id
    image_path = member.image.path

    if 'nopic' not in image_path:
        os.remove(image_path)

    member.delete()

    messages.info(request, 'اطلاعات حذف شد.')
    return redirect('/news/{0}/'.format(slug))

@csrf_exempt
def notice_change_active_news(request):
    id = request.POST.get('id')
    member = News.objects.get(pk=id)
    content = Category.objects.get(id=member.newscat_id)
    slug = content.slug
    member.active = not(member.active)
    member.save()
    if not(member.active):
        messages.info(request, 'غیر فعال شد.')
    else:
        messages.info(request, 'فعال شد.')
    return HttpResponse('/news/{0}/'.format(slug))

@login_required(login_url='/auth/')  # redirect when user is not logged in
def notice_news_edit(request,id,idd):
    content = Category.objects.get(pk=id)
    # content = get_object_or_404(content, slug=slug)

    edit_news = News.objects.get(pk=idd)
    # edit_news = get_object_or_404(edit_news, slug=news)

    context = {
        'content': content,
        'edit_news': edit_news,
    }

    return render(request, 'fa/notices/edit-news.html', context)
    # objects = []
    # for item in News.objects.filter(pk=request.GET.get('pk')):
    #     objects.append({
    #         "title": item.title,
    #         "titleseo": item.titleseo,
    #         "short_text": item.short_text,
    #         "text": item.text,
    #         "hot": item.hot,
    #         "image": item.image.url.replace('/media/',''),
    #     })
    # return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')


@login_required(login_url='/auth/')  # redirect when user is not logged in
def notice_news_edit_save(request):
    id = request.POST.get('pk_id_edit')
    member = News.objects.get(id=id)
    content = Category.objects.get(id=member.newscat_id)
    slug = content.id
    if request.method == 'POST':

        title = request.POST.get('title')
        titleseo = request.POST.get('titleseo')
        short_text = request.POST.get('short_text')
        text = request.POST.get('text')
        if request.POST.get('hot') == 'on':
            hot = True
        else:
            hot = False

        if bool(request.FILES.get('image', False)) == True:
            image = request.FILES['image']
        else:
            image = member.image

        member.image = image
        member.title = title
        member.titleseo = titleseo
        member.short_text = short_text
        member.text = text
        member.hot = hot
        member.save()

        messages.info(request, 'اطاعات وارد شده با موفقیت بروزرسانی شد.')
        return redirect('/news/{0}/'.format(slug))




