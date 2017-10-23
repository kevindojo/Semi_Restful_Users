from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import User
from django.contrib.messages import error

def index(request):
    context= {
        'users': User.objects.all()
    }
    return render(request, 'restful_user/index.html', context)

def new(request):
    return render(request, 'restful_user/new.html')

def create(request):
    errors= User.objects.validate(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/users/new')

    User.objects.create(
        first_name= request.POST['first_name'],
        last_name= request.POST['last_name'],
        email= request.POST['email'],
    )
    return redirect('/users')

def edit(request,user_id):
    context= {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'restful_user/edit.html', context)

def show(request,user_id):
    context= {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'restful_user/show.html', context)

def destroy(request,user_id):
    User.objects.get(id=user_id).delete()
    return HttpResponseRedirect('/users')

def update(request,user_id):
    errors= User.objects.validate(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/users/{}/edit'.format(user_id))
    user_update = User.objects.get(id=user_id)
    user_update.first_name= request.POST['first_name']
    user_update.last_name= request.POST['last_name']
    user_update.email= request.POST['email']
    user_update.save()
    return redirect('/users')