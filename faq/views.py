from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Faq,Survey
from django.db.models import Max
from django.contrib import messages
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@login_required(login_url='/auth/')  # redirect when user is not logged in
def faq(request):
    faqs = Faq.objects.all().order_by('position')

    context = {
        'faqs': faqs,
    }

    return render(request, 'fa/faq/settings.html', context)

@login_required(login_url='/auth/')  # redirect when user is not logged in
def survey(request):
    surveys = Survey.objects.all().order_by('position')

    context = {
        'surveys': surveys,
    }

    return render(request, 'fa/survey/settings.html', context)

@login_required(login_url='/auth/') #redirect when user is not logged in
def faq_insert(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')

        order = Faq.objects.aggregate(Max('position'))['position__max']

        if order:
            order += 1
        else:
            order = 1

        obj = Faq.objects.create(question=question, answer=answer, position=order)
        obj.save()

        messages.info(request, 'اطاعات وارد شده با موفقیت ثبت شد.')
        return redirect('/faq')

@csrf_exempt
def faq_datasource(request):
    objects = []
    for item in Faq.objects.all().order_by('position'):
        objects.append({
            'ID': item.id,
            'question': item.question,
            'answer': item.answer,
            'active': item.active,
        })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@csrf_exempt
def survey_datasource(request):
    objects = []
    for item in Survey.objects.all().order_by('position'):
        objects.append({
            'ID': item.id,
            'description': item.description,
            'answer': item.answer,
            'active': item.active,
        })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@csrf_exempt
def faq_delete(request, id):
    member = Faq.objects.get(id=id)
    member.delete()
    return HttpResponse('ok')

@csrf_exempt
def survey_delete(request, id):
    member = Survey.objects.get(id=id)
    member.delete()
    return HttpResponse('ok')

@csrf_exempt
def change_faq_active(request,id):
    member = Faq.objects.get(id=id)
    member.active = not (member.active)
    member.save()
    if not(member.active):
        messages.info(request, 'غیر فعال شد.')
    else:
        messages.info(request, 'فعال شد.')
    return HttpResponse()

@csrf_exempt
def change_survey_active(request,id):
    member = Survey.objects.get(id=id)
    member.active = not (member.active)
    member.save()
    if not(member.active):
        messages.info(request, 'غیر فعال شد.')
    else:
        messages.info(request, 'فعال شد.')
    return HttpResponse()

@csrf_exempt
def faq_edit(request,id):
    objects = []
    member = Faq.objects.get(id=id)
    objects.append({
        'question': member.question,
        'answer': member.answer,
    })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@csrf_exempt
def survey_edit(request,id):
    objects = []
    member = Survey.objects.get(id=id)
    objects.append({
        'fullname': member.full_name,
        'mobile': member.mobile,
        'email': member.email,
        'description': member.description,
        'answer': member.answer,
    })
    return HttpResponse(json.dumps(objects), content_type='application/json; charset=utf8')

@login_required(login_url='/auth/')  # redirect when user is not logged in
def faq_edit_save(request):
    id = request.POST.get('pk_id_edit')
    member = Faq.objects.get(id=id)
    if request.method == 'POST':

        question = request.POST.get('question')
        answer = request.POST.get('answer')

        member.question = question
        member.answer = answer
        member.save()

        messages.info(request, 'اطاعات وارد شده با موفقیت بروزرسانی شد.')
        return redirect('/faq')
    
@login_required(login_url='/auth/')  # redirect when user is not logged in
def survey_edit_save(request):
    id = request.POST.get('pk_id_edit')
    member = Survey.objects.get(id=id)
    if request.method == 'POST':

        fullname = request.POST.get('fullname')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        answer = request.POST.get('answer')

        member.full_name = fullname
        member.mobile = mobile
        member.email = email
        member.description = desc
        member.answer = answer
        member.save()

        messages.info(request, 'اطاعات وارد شده با موفقیت بروزرسانی شد.')
        return redirect('/survey')
