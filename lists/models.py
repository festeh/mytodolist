from django.db import models


class Task(models.Model):
    text = models.TextField(default="")
