from django.http import HttpRequest
from django.shortcuts import render, redirect
from lists.models import Task, List


def home_page(request: HttpRequest):
    return render(request, "home.html")


def view_list(request, list_id):
    return render(request, "list.html", {"list": List.objects.get(id=list_id)})


def new_list(request):
    task_text = request.POST["task_text"]
    list_ = List.objects.create()
    Task.objects.create(text=task_text, list=list_)
    return redirect(f"/lists/{list_.id}/")


def add_task(request, list_id):
    list_ = List.objects.get(id=list_id)
    Task.objects.create(text=request.POST["task_text"], list=list_)
    return redirect(f"/lists/{list_.id}/")
