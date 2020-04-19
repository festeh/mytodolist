from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.shortcuts import render, redirect

from lists.forms import TaskForm
from lists.models import Task, List


def home_page(request: HttpRequest):
    return render(request, "home.html", {"form": TaskForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(data=request.POST)
        if form.is_valid():
            Task.objects.create(text=request.POST["text"], list=list_)
            return redirect(list_)
    return render(request, "list.html", {"list": list_,
                                         "form": form,
                                         })


def new_list(request):
    form = TaskForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Task.objects.create(text=request.POST["text"], list=list_)
        return redirect(list_)
    else:
        return render(request, "home.html", {"form": form})

