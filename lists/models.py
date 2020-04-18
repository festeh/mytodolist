from django.db import models


class List(models.Model):
    pass


class Task(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None)
