from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Job, Application
from .forms import ApplicationForm, JobForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})
@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})
@login_required
def apply_for_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applied_date = timezone.now()
            application.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_for_job.html', {'job': job, 'form': form})

@login_required
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.owner = request.user
            job.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'jobs/add_job.html', {'form': form})

@login_required
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.owner != request.user:
        return redirect('job_detail', pk=job.pk)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/edit_job.html', {'form': form, 'job': job})

@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.owner == request.user:
        job.delete() 
    return redirect('job_list')

@login_required
def view_applications(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.owner != request.user:
        return redirect('job_detail', pk=job.pk)
    applications = job.applications.all()
    return render(request, 'jobs/view_applications.html', {'job': job, 'applications': applications})

@login_required
def profile(request):
    # Get the currently logged-in user
    user = request.user
    # Get all applications where the current user is the applicant
    applications = Application.objects.filter(applicant_name=user)
    
    return render(request, 'profile.html', {'applications': applications})


def home(request):
    return render(request, 'home.html')