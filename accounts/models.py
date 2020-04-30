from uuid import uuid4

from django.db import models

# Create your models here.
from django.db.models import EmailField, CharField


class User(models.Model):
    email = EmailField(unique=True, primary_key=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    email = EmailField()
    uid = CharField(default=uuid4, max_length=40)
