from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import List, Task


class TaskModelTest(TestCase):

    def test_cannot_add_empty_task(self):
        list_ = List.objects.create()
        task = Task(list=list_, text='')
        with self.assertRaises(ValidationError):
            task.full_clean()
            task.save()

    def test_default_text(self):
        task = Task()
        self.assertEqual(task.text, '')

    def test_task_related_list(self):
        list_ = List.objects.create()
        task = Task.objects.create(text="hoba", list=list_)
        self.assertIn(task, list_.task_set.all())


class ListModelTest(TestCase):
    def test_get_absolute_url_list(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
