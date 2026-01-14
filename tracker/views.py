from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Job

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"],
            password=request.POST["password"]
        )
        if user:
            login(request, user)
            return redirect("dashboard")
    return render(request, "login.html")


@login_required
def dashboard(request):
    if request.method == "POST":
        Job.objects.create(
            company=request.POST["company"],
            role=request.POST["role"],
            status=request.POST["status"]
        )
        return redirect("dashboard")

    jobs = Job.objects.all()
    return render(request, "dashboard.html", {"jobs": jobs})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    return redirect("dashboard")


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        job.company = request.POST["company"]
        job.role = request.POST["role"]
        job.status = request.POST["status"]
        job.save()
        return redirect("dashboard")

    return render(request, "edit.html", {"job": job})
