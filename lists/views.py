from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.shortcuts import render, redirect

from lists.forms import TaskForm, ExistingListTaskForm, NewListTaskForm
from lists.models import Task, List


def home_page(request: HttpRequest):
    return render(request, "home.html", {"form": TaskForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListTaskForm(for_list=list_)
    if request.method == "POST":
        form = ExistingListTaskForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, "list.html", {"list": list_,
                                         "form": form,
                                         })


def new_list(request):
    form = NewListTaskForm(data=request.POST)
    if form.is_valid():
        task_list = form.save(owner=request.user)
        return redirect(task_list)
    return render(request, "home.html", {"form": form})


User = get_user_model()


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, "my_lists.html", {"owner": owner})


def share_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return redirect(list_)
