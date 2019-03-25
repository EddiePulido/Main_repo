from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    if 'id' in request.session:
        return redirect("/dashboard")
    return render(request,"belt_app/index.html")

def create(request):
    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        # redirect the user back to the form to fix the errors
        return redirect('/')

    hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=hash1)

    request.session['id'] = user.id
    request.session['first_name'] = user.first_name


    return redirect("/dashboard")

def login(request):
    errors = User.objects.login_validator(request.POST)
    print(errors)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)

        return redirect("/")

    user = User.objects.get(email=request.POST['email'])
    request.session['id'] = user.id
    request.session['first_name'] = user.first_name



    return redirect("/dashboard")



def logout(request):
    request.session.flush()

    return redirect("/")


def dashboard(request):
    if 'id' not in request.session:
        redirect("/")

    context = {
        'user': User.objects.get(id=request.session['id']),
        'jobs': Job.objects.all()
    }

    return render(request,"belt_app/dashboard.html",context)


def edit_page(request,id):
    if 'id' not in request.session:
        redirect("/")

    job = Job.objects.get(id=id)

    context = {
        'job': job
    }
    return render(request,"belt_app/edit.html",context)

def update(request):
    errors = User.objects.job_validator(request.POST)
    print(errors)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)

        return redirect("/jobs/edit/{}".format(request.POST['id']))
    job = Job.objects.get(id=request.POST['id'])
    job.title = request.POST['title']
    job.desc = request.POST['description']
    job.location = request.POST['location']
    job.save()

    return redirect('/dashboard')

def new_page(request):
    if 'id' not in request.session:
        redirect("/")
    return render(request,"belt_app/add.html")

def add_job(request):
    errors = User.objects.job_validator(request.POST)
    print(errors)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)

        return redirect("/jobs/new")

    user = User.objects.get(id=request.session['id'])
    job = Job.objects.create(title = request.POST['title'], desc=request.POST['description'],location=request.POST['location'], created_by=user)
    category_list = request.POST.getlist('category')

    for category in category_list:
        cat = Category.objects.create(category=category, job=job)

    if len(request.POST['category1']) > 1:
        cat = Category.objects.create(category=request.POST['category1'],job = job)

    return redirect("/dashboard")

def job_page(request,id):
    if 'id' not in request.session:
        redirect("/")
    pass

    job = Job.objects.get(id=id)
    context = {
        'job' : job,
        'user' : User.objects.get(id=request.session['id'])
    }

    return render(request,"belt_app/job_page.html", context)


def remove(request,id):
    job = Job.objects.get(id=id)
    job.delete()

    return redirect("/dashboard")

def work_job(request, id):
    user = User.objects.get(id=request.session['id'])
    job = Job.objects.get(id=id)

    user.current_jobs.add(job)

    return redirect("/dashboard")

def quit_job(request, id):
    job = Job.objects.get(id=id)
    user = User.objects.get(id=request.session['id'])

    user.current_jobs.remove(job)
    

    return redirect("/dashboard")








