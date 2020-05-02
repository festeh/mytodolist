from django.contrib import messages
from django.contrib import auth
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import Token


def send_login_email(request):
    email = request.POST["email"]
    token = Token.objects.create(email=email)
    login_link = request.build_absolute_uri(f'{reverse("login")}?token={token.uid}')
    send_mail("Your login link for TODO task list",
              f"Use this link to login: {login_link}", "noreply@tasklist", [email])
    messages.success(request,
                     "Check your email for login link")
    return redirect("/")


def login(request):
    user = auth.authenticate(uid=request.GET.get("token"))
    if user:
        auth.login(request, user)
    return redirect("/")
