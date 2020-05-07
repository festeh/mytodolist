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

    def test_create_new_creates_list_with_task(self):
        List.create_new(first_task_text="let's go")
        new_task = Task.objects.first()
        self.assertEqual(new_task.text, "let's go")
        new_list = List.objects.first()
        self.assertEqual(new_task.list, new_list)

    def test_list_owner_is_saved(self):
        user = User.objects.create()
        List.create_new(first_task_text="let's go", owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_list_can_have_owner(self):
        List(owner=User())

    def test_owner_is_optional(self):
        List().full_clean()

    def test_create_new_returns_list(self):
        first_list = List.create_new("a new task")
        self.assertEqual(first_list, List.objects.first())

    def test_task_list_can_haz_name(self):
        task_list = List.objects.create()
        Task.objects.create(list=task_list, text="First task")
        Task.objects.create(list=task_list, text="Second task")
        self.assertEqual(task_list.name, "First task")

    def test_shared_with(self):
        email = "kek@cheburek.com"
        user = User.objects.create(email=email)
        task_list = List.create_new("boo")
        task_list.shared_with.add(email)
        self.assertIn(user, task_list.shared_with.all())
