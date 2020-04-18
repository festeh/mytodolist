from django.http import HttpRequest
from django.shortcuts import render, redirect
from lists.models import Task


def home_page(request: HttpRequest):
    if request.method == "POST":
        task_text = request.POST["task_text"]
        if task_text:
            Task.objects.create(text=task_text)
        return redirect("/lists/my_unique_list")
    return render(request, "home.html", {"items": Task.objects.all()})


def view_list(request):
    return render(request, "home.html", {"items": Task.objects.all()})
