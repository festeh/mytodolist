from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.shortcuts import render, redirect
from lists.models import Task, List


def home_page(request: HttpRequest):
    return render(request, "home.html")


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == "POST":
        try:
            task = Task(text=request.POST["task_text"], list=list_)
            task.full_clean()
            task.save()
            return redirect(f"/lists/{list_.id}/")
        except ValidationError:
            error = "Cannot add an empty task"
    return render(request, "list.html", {"list": list_, "error": error})


def new_list(request):
    list_ = List.objects.create()
    task = Task(text=request.POST["task_text"], list=list_)
    try:
        task.full_clean()
        task.save()
    except ValidationError:
        list_.delete()
        err_msg = "Cannot add an empty task"
        return render(request, "home.html", {"error": err_msg})
    return redirect(f"/lists/{list_.id}/")
