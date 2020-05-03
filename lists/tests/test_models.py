from django.contrib.auth import get_user_model
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


User = get_user_model()


class ListModelTest(TestCase):
    def test_get_absolute_url_list(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_lists_can_haz_owners(self):
        user = User.objects.create(email="a@b.com")
        task_list = List.objects.create(owner=user)
        self.assertIn(task_list, user.list_set.all())

    def test_owner_is_optional(self):
        task_list = List.objects.create()
        Task.objects.create(list=task_list, text="First task")
        Task.objects.create(list=task_list, text="Second task")
        self.assertEqual(task_list.name, "First task")
