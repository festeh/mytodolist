from django.db import IntegrityError
from django.test import TestCase
from lists.forms import TaskForm, EMPTY_TASK_ERROR
from lists.models import List, Task


class ItemFormTest(TestCase):
    def test_form_had_placeholder_and_bs_class(self):
        form = TaskForm()
        self.assertIn('placeholder="Enter a task"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_from_validation_empty_task(self):
        form = TaskForm(data={"text": ""})
        # has a side effect of populating errors
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_TASK_ERROR])

    def test_form_saves_input_to_list(self):
        list_ = List.objects.create()
        form = TaskForm(data={'text': 'a new task'})
        new_task = form.save(for_list=list_)
        self.assertEqual(new_task, Task.objects.first())
        self.assertEqual(new_task.text, "a new task")
        self.assertEqual(new_task.list, list_)

    def test_duplicating_tasks_not_allowed(self):
        list_ = List.objects.create()
        Task.objects.create(text="just do it", list=list_)
        with self.assertRaises(IntegrityError):
            Task.objects.create(text="just do it", list=list_)

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
