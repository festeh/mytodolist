from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from lists.models import Task


def home_page(request: HttpRequest):
    if request.method == "POST":
        task_text = request.POST["task_text"]
        if task_text:
            Task.objects.create(text=task_text)
        return redirect("/")
    return render(request, "home.html", {"items": Task.objects.all()})
