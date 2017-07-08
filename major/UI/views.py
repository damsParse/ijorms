from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Permission, User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CvForm, UserForm
from .models import Cv,Job


# Create your views here.


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        jobs = Job.objects.all()
        query = request.GET.get("q")
        if query:
            jobs = Job.objects.filter(
                Q(company__icontains=query) |
                Q(category__icontains=query) |
                Q(post__icontains=query) |
                Q(skills__icontains=query) |
                Q(work_exp__icontains=query) |
                Q(title__icontains=query)
            ).distinct()
        context = {
            'user':request.user,
            'jobs':jobs,
        }
        return render(request, 'home.html', context)


def logout_user(request):
    logout(request)
    # form = UserForm(request.POST or None)
    # context = {
    #     'form':form
    # }
    return redirect('index')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('index')
            else:
                return render(request, 'login.html', {'error_message':'Account Deactivated'})
        else:
            return render(request, 'login.html', {'error_message':'Login Invalid'})
    return render(request, 'login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('index')
    context = {'form':form}
    return render(request, 'register.html', context)


def vitae(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        form = CvForm(request.POST or None, request.FILES or None)
        print("test ho a")
        if form.is_valid():
            cv = form.save(commit=False)
            cv.applicant = request.user
            print("test ho b")
            cv.resume = request.FILES['resume']
            file_type = cv.resume.url.split('.')[-1]
            file_type = file_type.lower()
            print(file_type)
            if file_type not in ['pdf','doc','docx']:
                context = {
                    'form': form,
                    'error_message': 'File must in PDF',
                }
                return render(request, 'submit_cv.html', context)
            cv.save()
            return redirect('index')
        context = {
            'form': form,
        }
        return render(request, 'submit_cv.html', context)


def details(request,job_id):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        applied = False
        job = Job.objects.get(id=job_id)
        if request.user in job.appliers.all():
            applied = True
        context = {
            'user':request.user,
            'job': job,
            'applied': applied,
        }
        return render(request, 'details.html', context)


def add(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        user = request.user
        if request.method == 'POST':
            if request.is_ajax():
                cuser = request.POST.get('cuser',False)
                if user == User.objects.get(username=cuser):
                    applied_job_id = request.POST.get('job',False)
                    applied_job = Job.objects.get(id=applied_job_id)
                    if user not in applied_job.appliers.all():
                        applied_job.appliers.add(user)
                    print(applied_job.appliers.all())
                    return JsonResponse({'data':applied_job_id})
                return JsonResponse({'data':"users not same"})
        return JsonResponse({'data':"not post"})
