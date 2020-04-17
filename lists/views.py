from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_page(request: HttpRequest):
    print(request.method, request.POST.__dict__)
    if request.method == "POST":
        return render(request, "home.html",
                      {"new_task_text": request.POST.get("task_text", "")})
    return render(request, "home.html")
