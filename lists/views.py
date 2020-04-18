from django.http import HttpRequest
from django.shortcuts import render, redirect
from lists.models import Task


def home_page(request: HttpRequest):
    return render(request, "home.html")


def view_list(request):
    return render(request, "list.html", {"items": Task.objects.all()})


def new_list(request):
    task_text = request.POST["task_text"]
    if task_text:
        Task.objects.create(text=task_text)
    return redirect("/lists/my_unique_list/")
