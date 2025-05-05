from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Users
import json
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# Create your views here.
@login_required(login_url='/auth/')  # redirect when user is not logged in
def userMgmt(request):
    return render(request, 'fa/membership/list.html')

@csrf_exempt
def user_datasource(request):
    objects = []
    for item in Users.objects.filter(is_superuser=False).order_by('-id'):
        objects.append({
            'ID': item.id,
            'first_name': item.first_name,
            'last_name': item.last_name,
            'mobile': item.mobile,
            'active': item.is_active,
        })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@csrf_exempt
def change_user_active(request,id):
    member = Users.objects.get(id=id)
    member.is_active = not (member.is_active)
    member.save()
    if not(member.is_active):
        messages.info(request, 'غیر فعال شد.')
    else:
        messages.info(request, 'فعال شد.')
    return HttpResponse()

@csrf_exempt
def user_delete(request, id):
    member = Users.objects.get(id=id)
    member.delete()
    return HttpResponse('ok')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def user_add(request):
    return render(request, 'fa/membership/add.html')

@login_required(login_url='/auth/') #redirect when user is not logged in
def user_insert(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')

        if password != repeat_password:
            messages.info(request, 'رمز عبور و تکرار آن همخوانی ندارد.', extra_tags='error')
            return render(request, 'fa/membership/add.html')

        password = make_password(password)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        tel = request.POST.get('tel')
        mob = request.POST.get('mob')

        if bool(request.FILES.get('image', False)) == True:
            image = request.FILES['image']
        else:
            image = 'profiles/nopic.png'

        if request.POST.get('staff') == 'on':
            staff = True
        else:
            staff = False

        if request.POST.get('active') == 'on':
            active = True
        else:
            active = False

        if request.POST.get('gender') == 'on':
            gender = True
        else:
            gender = False

        obj = Users.objects.create(image=image, first_name=first_name, last_name=last_name, tel=tel, email=email, mobile=mob, is_active=active, is_staff=staff, password=password, address=address, gender=gender)
        obj.save()

        messages.info(request, 'اطاعات کاربر با موفقیت ثبت شد.')
        return redirect('/userMgmt')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def user_edit(request,id):
    content = Users.objects.get(pk=id)

    context = {
        'content': content,
    }
    return render(request, 'fa/membership/edit.html', context)

@login_required(login_url='/auth/')  # redirect when user is not logged in
def user_edit_save(request):
    id = request.POST.get('pk_id_edit')
    member = Users.objects.get(id=id)
    if request.method == 'POST':
        # password = request.POST.get('password')
        # repeat_password = request.POST.get('repeat_password')
        #
        # if password != repeat_password:
        #     messages.info(request, 'رمز عبور و تکرار آن همخوانی ندارد.', extra_tags='error')
        #     return redirect('/userEdit/{0}'.format(id))
        #
        # password = make_password(password)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        tel = request.POST.get('tel')
        mob = request.POST.get('mob')

        if bool(request.FILES.get('image', False)) == True:
            image = request.FILES['image']
        else:
            image = member.image

        if request.POST.get('staff') == 'on':
            staff = True
        else:
            staff = False

        if request.POST.get('active') == 'on':
            active = True
        else:
            active = False

        if request.POST.get('gender') == 'on':
            gender = True
        else:
            gender = False


        member.image = image
        # member.password = password
        member.first_name = first_name
        member.last_name = last_name
        member.email = email
        member.address = address
        member.tel = tel
        member.mob = mob
        member.is_staff = staff
        member.is_active = active
        member.gender = gender
        member.save()

        messages.info(request, 'اطاعات وارد شده با موفقیت بروزرسانی شد.')
        return redirect('/userMgmt')