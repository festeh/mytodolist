from django.conf import settings
from django.db import models
from django.urls import reverse


class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

    @staticmethod
    def create_new(first_task_text, owner=None):
        task_list = List.objects.create(owner=owner)
        Task.objects.create(text=first_task_text, list=task_list)
        return task_list

    @property
    def name(self):
        return self.task_set.first().text


class Task(models.Model):
    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')

    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None)

    def __str__(self):
        return self.text
