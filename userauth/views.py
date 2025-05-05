from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

# Create your views here.
def login_view(request):
    return render(request, 'fa/login.html')

def auth_view(request):
    if request.method == 'POST':
        username = request.POST['login_username']
        password = request.POST['login_password']
        user = authenticate(request, mobile=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                nxt = request.POST.get("next")
                if nxt !='':
                    return redirect(nxt)
                return redirect('/home')
            else:
                messages.info(request, 'شما مجوز دسترسی به این قسمت ندارید.')
                return render(request, 'fa/login.html')
        else:
            messages.info(request, 'نام کاربری و یا رمز عبور اشتباه است.')
            return render(request, 'fa/login.html')
    else:
        return render(request, 'fa/login.html')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def home_view(request):
    return render(request, 'fa/dashboard/home.html')

def logout_view(request):
    logout(request)
    return render(request, 'fa/login.html')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def profile_change(request):
    return render(request, 'fa/profiles/profile.html')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def profile_change_save(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        family = request.POST.get('family')

        if bool(request.FILES.get('image', False)) == True:
            image = request.FILES['image']
        else:
            image = 'profiles/nopic.png'

        user = request.user
        user.image = image
        user.first_name = name
        user.last_name = family
        user.save()
        login(request, user)

        messages.info(request, 'تغییر پروفایل با موفقیت انجام شد.')
        return render(request, 'fa/profiles/profile.html')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def password_change(request):
    return render(request, 'fa/profiles/password_change.html')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def password_change_save(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')

        user = request.user

        if password != repeat_password:
            messages.info(request, 'رمز عبور و تکرار آن همخوانی ندارد.', extra_tags='error')
            return render(request, 'fa/profiles/password_change.html')
        else:
            if len(password) < 3 or len(password) > 100:
                messages.info(request, 'تعداد کاراکترهای گذر واژه مناسب نمی باشد.', extra_tags='error')
                return render(request, 'fa/profiles/password_change.html')
            else:
                user.password = make_password(password)
                user.save()
                login(request, user)
                messages.info(request, 'تغییر گذر واژه با موفقیت انجام شد.', extra_tags='success')
                return render(request, 'fa/profiles/password_change.html')
