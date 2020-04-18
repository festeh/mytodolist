from django.http import HttpRequest
from django.shortcuts import render, redirect
from lists.models import Task, List


def home_page(request: HttpRequest):
    return render(request, "home.html")


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    tasks = Task.objects.filter(list=list_)
    return render(request, "list.html", {"items": tasks})


def new_list(request):
    task_text = request.POST["task_text"]
    list_ = List.objects.create()
    Task.objects.create(text=task_text, list=list_)
    return redirect(f"/lists/{list_.id}/")
