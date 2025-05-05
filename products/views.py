from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from menu.models import Main
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
import os

# Create your views here.
@login_required(login_url='/auth/')  # redirect when user is not logged in
def detailsTitle(request):
    pages = Main.objects.filter(sub_menu_id=6).order_by('position')

    context = {
        'pages': pages,
    }

    return render(request, 'fa/products/settings.html', context)

@login_required(login_url='/auth/')  # redirect when user is not logged in
def detailsAdd(request):
    product = Main.objects.filter(title='محصولات', sub_menu__isnull=True).order_by('position')
    pages = Main.objects.filter(sub_menu_id__in =[x.pk for x in product]).order_by('position')
    context = {
        'pages': pages,
    }
    return render(request, 'fa/products/details_add.html', context)

@login_required(login_url='/auth/') #redirect when user is not logged in
def details_title_insert(request):
    if request.method == 'POST':
        pages = request.POST.getlist('pages')
        title = request.POST.get('title')
        for page in pages:
            obj = DetailsTitle.objects.create(title=title, pages_id=page)
            obj.save()

        messages.info(request, 'اطاعات وارد شده با موفقیت ثبت شد.')
        return redirect('/detailsTitle')

@csrf_exempt
def details_title_datasource(request):
    objects = []
    for item in DetailsTitle.objects.all().order_by('position'):
        objects.append({
            'ID': item.id,
            'title': item.title,
            'pages': item.pages.title,
            'active': item.active,
        })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@csrf_exempt
def details_title_delete(request, id):
    member = DetailsTitle.objects.get(id=id)
    member.delete()
    # messages.info(request, 'اطلاعات با موفقیت حذف شد.')
    return HttpResponse('ok')

@csrf_exempt
def change_details_title_active(request,id):
    member = DetailsTitle.objects.get(id=id)
    member.active = not (member.active)
    member.save()
    if not(member.active):
        messages.info(request, 'غیر فعال شد.')
    else:
        messages.info(request, 'فعال شد.')
    return HttpResponse()

@csrf_exempt
def details_title_edit(request):
    id = request.GET.get('pk')
    objects = []
    for item in DetailsTitle.objects.filter(id=id):
        objects.append({
            'title': item.title,
            'pages_id': item.pages_id,
        })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def details_title_edit_save(request):
    id = request.POST.get('pk_id_edit')
    member = DetailsTitle.objects.get(id=id)

    if request.method == 'POST':

        page = request.POST.get('page')
        title = request.POST.get('title')

        member.title = title
        member.pages_id = page
        member.save()


        messages.info(request, 'اطاعات وارد شده با موفقیت بروزرسانی شد.')
        return redirect('/detailsTitle')


@login_required(login_url='/auth/')  # redirect when user is not logged in
def products_list(request):
    # pages = Main.objects.filter(sub_menu_id=6).order_by('position')
    #
    # context = {
    #     'pages': pages,
    # }
    #
    # return render(request, 'fa/products/settings.html', context)
    return render(request, 'fa/products/list.html')


@login_required(login_url='/auth/')  # redirect when user is not logged in
def products_add(request):
    product = Main.objects.filter(title='محصولات', sub_menu__isnull=True).order_by('position')
    pages = Main.objects.filter(sub_menu_id__in =[x.pk for x in product]).order_by('position')
    context = {
        'pages': pages,
    }

    return render(request, 'fa/products/add.html', context)


@csrf_exempt
def details_title_list(request):
    id = request.GET.get('pk')
    objects = []
    for item in DetailsTitle.objects.filter(pages_id=id).order_by('position'):
        objects.append({
            'id': item.id,
            'title': item.title,
            'pages_id': item.pages_id,
        })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@csrf_exempt
def get_products(request):
    value = request.GET.get('value')
    details = Main.objects.filter(sub_menu_id=value).order_by('position')
    objects = []
    for item in details:
        objects.append({
            "value": item.pk,
            "text": item.title,
        })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@login_required(login_url='/auth/') #redirect when user is not logged in
def products_insert(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        pages = request.POST.get('pages')
        product = request.POST.get('product')
        # input_details = request.POST.getlist('input_details')

        if bool(request.FILES.get('image', False)) == True:
            image = request.FILES['image']
        else:
            image = 'uploads/products/nopic.jpg'

        obj = Products.objects.create(image=image, title=title, price=price, pages_id=pages, product=product)
        obj.save()

        details_pk = obj.pk

        for item in DetailsTitle.objects.filter(pages_id=pages):
            val = request.POST.get('input_values_%s'%item.id)
            obj = Details.objects.create(product_id=details_pk, detail_id=item.id, value=val)
            obj.save()

        messages.info(request, 'اطاعات وارد شده با موفقیت ثبت شد.')
        return redirect('/productsList')

@csrf_exempt
def products_datasource(request):
    objects = []
    for item in Products.objects.all().order_by('pages').order_by('position'):
        objects.append({
            'ID': item.id,
            'title': item.title,
            'pages': item.pages.title,
            'active': item.active,
        })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@csrf_exempt
def products_delete(request, id):
    member = Products.objects.get(id=id)
    image_path = member.image.path

    if 'nopic' not in image_path:
        os.remove(image_path)

    member.delete()
    # messages.info(request, 'اطلاعات با موفقیت حذف شد.')
    return HttpResponse('ok')

@csrf_exempt
def change_products_active(request,id):
    member = Products.objects.get(id=id)
    member.active = not (member.active)
    member.save()
    if not(member.active):
        messages.info(request, 'غیر فعال شد.')
    else:
        messages.info(request, 'فعال شد.')
    return HttpResponse()

@login_required(login_url='/auth/')  # redirect when user is not logged in
def products_edit(request,id):
    product = Products.objects.get(id=id)
    pages = Main.objects.filter(sub_menu_id=6).order_by('position')
    products = Main.objects.filter(sub_menu_id=product.pages_id).order_by('position')

    context = {
        'product': product,
        'pages': pages,
        'products': products,
    }

    return render(request, 'fa/products/edit.html', context)

@csrf_exempt
def products_edit_list(request):
    id = request.GET.get('pk')
    objects = []
    for item in Details.objects.filter(product_id=id):
        objects.append({
            'id': item.detail.id,
            'title': item.detail.title,
            'value': item.value,
        })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')


@login_required(login_url='/auth/') #redirect when user is not logged in
def products_edit_save(request):
    id = request.POST.get('pk_id_edit')
    member = Products.objects.get(id=id)

    if request.method == 'POST':
        price = request.POST.get('price')
        title = request.POST.get('title')
        product = request.POST.get('product')

        if bool(request.FILES.get('image', False)) == True:
            image = request.FILES['image']
            image_path = member.image.path

            if 'nopic' not in image_path:
                os.remove(image_path)
        else:
            image = 'uploads/products/nopic.jpg'

        for item in Details.objects.filter(product_id=id):
            val = request.POST.get('input_values_%s'%item.detail_id)
            obj = Details.objects.get(product_id=id, detail_id=item.detail_id)
            obj.value = val
            obj.save()

        member.title = title
        member.product = product
        member.price = price
        member.image = image
        member.save()

        messages.info(request, 'اطاعات وارد شده با موفقیت بروزرسانی شد.')
        return redirect('/productsList')

    # if request.method == 'POST':
    #     title = request.POST.get('title')
    #     price = request.POST.get('price')
    #     pages = request.POST.get('pages')
    #     # input_details = request.POST.getlist('input_details')
    #
    #     if bool(request.FILES.get('image', False)) == True:
    #         image = request.FILES['image']
    #     else:
    #         image = 'uploads/products/nopic.jpg'
    #
    #     obj = Products.objects.create(image=image, title=title, price=price, pages_id=pages)
    #     obj.save()
    #
    #     details_pk = obj.pk
    #
    #     for item in DetailsTitle.objects.filter(pages_id=pages):
    #         val = request.POST.get('input_values_%s'%item.id)
    #         obj = Details.objects.create(product_id=details_pk, detail_id=item.id, value=val)
    #         obj.save()
    #
    #     messages.info(request, 'اطاعات وارد شده با موفقیت ثبت شد.')
    #     return redirect('/productsList')
