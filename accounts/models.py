from uuid import uuid4
from django.db import models
from django.contrib import auth
# Create your models here.
from django.db.models import EmailField, CharField
auth.signals.user_logged_in.disconnect(auth.models.update_last_login)


class User(models.Model):
    email = EmailField(unique=True, primary_key=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    email = EmailField()
    uid = CharField(default=uuid4, max_length=40)
