from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Job, UserManager
import bcrypt
from django.db.models import Count

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pw_hash)
            request.session['user_id'] = user.id
            if 'user_id' not in request.session:
                return redirect('/')
            context = {
                'current_user' : User.objects.get(id=request.session['user_id']),
                'all_jobs' : Job.objects.all(),
            }
            return render(request, 'dashboard.html', context)
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if 'user_id'in request.session:
        context = {
        'current_user' : User.objects.get(id=request.session['user_id']),
        'all_jobs' : Job.objects.all(),
        }
        return render(request, 'dashboard.html', context)
    return redirect('/')

def login(request):
    if request.method == "POST":
        registered_user = User.objects.filter(email=request.POST['email'])
        if registered_user:
            user = registered_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/dashboard')
        messages.error(request, "Incorrect email or password")
    return redirect('/')

def new(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if 'user_id'in request.session:
        context = {
        'current_user' : User.objects.get(id=request.session['user_id']),
        }
    return render(request, 'jobs/new.html', context)

def create(request):
    if request.method == "POST":
        errors = Job.objects.job_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/jobs/new')
        else:
            one_job = Job.objects.create(title = request.POST['title'], description = request.POST['description'], location = request.POST['location'], creator = User.objects.get(id=request.session['user_id']))
            User.objects.get(id=request.session['user_id']).added_jobs.add(one_job)
            return redirect('/dashboard')
    return redirect('/')

def viewjob(request, job_id):
    context = {
        'one_job' : Job.objects.get(id=job_id),
        'current_user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "jobs/jobdetails.html", context)

def edit(request, job_id):
    context = {
        'one_job' : Job.objects.get(id=job_id),
    }
    return render(request, 'jobs/edit.html', context)

def update(request, job_id):
    errors = Job.objects.job_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect((f'/jobs/{job_id}/edit'))
    to_update = Job.objects.get(id=job_id)
    to_update.title = request.POST['title']
    to_update.description = request.POST['description']
    to_update.location = request.POST['location']
    to_update.save()
    context = {
        'current_user' : User.objects.get(id=request.session['user_id']),
        'all_jobs' : Job.objects.all()
        }
    return render(request, 'dashboard.html', context)

def addjob(request, job_id):
    if 'user_id' not in request.session:
        return redirect('/')
    current_user = User.objects.get(id=request.session['user_id'])
    one_job = Job.objects.get(id=job_id)
    current_user.added_jobs.add(one_job)
    return redirect('/dashboard')

def removejob(request, job_id):
    if 'user_id' not in request.session:
        return redirect('/')
    current_user = User.objects.get(id=request.session["user_id"])
    one_job = Job.objects.get(id=job_id)
    current_user.added_jobs.remove(one_job)
    return redirect('/dashboard')

def delete(request, job_id):
        delete_job = Job.objects.get(id=job_id)
        delete_job.creator.id == request.session['user_id']
        delete_job.delete()
        return redirect('/dashboard')