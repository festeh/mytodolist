from django.db import models
from django.urls import reverse


class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Task(models.Model):

    class Meta:
        ordering = ('id', )
        unique_together = ('list', 'text')

    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None)

    def __str__(self):
        return self.text
