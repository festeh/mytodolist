import unittest
from unittest.mock import patch, Mock

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from lists.forms import TaskForm, EMPTY_TASK_ERROR, DUPLICATING_TASK_ERROR, ExistingListTaskForm, NewListTaskForm
from lists.models import List, Task


class TaskFormTest(TestCase):
    def test_form_had_placeholder_and_bs_class(self):
        form = TaskForm()
        self.assertIn('placeholder="Enter a task"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_from_validation_empty_task(self):
        form = TaskForm(data={"text": ""})
        # has a side effect of populating errors
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_TASK_ERROR])

    def test_duplicating_tasks_not_allowed(self):
        list_ = List.objects.create()
        Task.objects.create(text="just do it", list=list_)
        with self.assertRaises(ValidationError):
            task = Task(text="just do it", list=list_)
            task.full_clean()

    def test_duplicating_tasks_different_lists_allowed(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Task.objects.create(text="just do it later", list=list1)
        task = Task.objects.create(text="just do it later", list=list2)
        task.full_clean()

    def test_list_ordering(self):
        list_ = List.objects.create()
        task1 = Task.objects.create(text="hey", list=list_)
        task2 = Task.objects.create(text="ho", list=list_)
        task3 = Task.objects.create(text="lets go", list=list_)
        self.assertEqual(list(Task.objects.all()), [task1, task2, task3])

    def test_task_string_representation(self):
        list_ = List.objects.create()
        task = Task.objects.create(text="this is no ordinary love", list=list_)
        self.assertEqual(str(task), task.text)


class NewListTaskFormTest(unittest.TestCase):

    @patch("lists.forms.List.create_new")
    def test_creates_new_list_unauthd_user(self, mock_list_create_new):
        user = Mock(is_authenticated=False)
        form = NewListTaskForm(data={"text": "a new task"})
        form.is_valid()
        form.save(owner=user)
        mock_list_create_new.assert_called_once_with(
            first_task_text="a new task"
        )

    @patch("lists.forms.List.create_new")
    def test_creates_new_list_authd_user(self, mock_list_create_new):
        user = Mock(is_authenticated=True)
        form = NewListTaskForm(data={"text": "a new task"})
        form.is_valid()
        form.save(owner=user)
        mock_list_create_new.assert_called_once_with(
            first_task_text="a new task", owner=user
        )

    @patch("lists.forms.List.create_new")
    def test_save_returns_new_list_object(self, mock_list_create_new):
        user = Mock(is_authenticated=True)
        form = NewListTaskForm(data={"text": "a new task"})
        form.is_valid()
        response = form.save(user)
        self.assertEqual(response, mock_list_create_new.return_value)


class ExistingListTaskFormTest(TestCase):
    def test_form_had_placeholder_and_bs_class(self):
        form = ExistingListTaskForm(for_list=List.objects.create())
        self.assertIn('placeholder="Enter a task"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_from_validation_empty_task(self):
        form = ExistingListTaskForm(for_list=List.objects.create(), data={"text": ""})
        # has a side effect of populating errors
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_TASK_ERROR])

    def test_from_validation_duplicate(self):
        list_ = List.objects.create()
        Task.objects.create(text="just do it", list=list_)
        form = ExistingListTaskForm(for_list=list_,
                                    data={"text": "just do it"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATING_TASK_ERROR])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListTaskForm(for_list=list_, data={'text': 'hi there'})
        new_task = form.save()
        self.assertEqual(new_task, Task.objects.all()[0])
