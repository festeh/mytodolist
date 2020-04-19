from unittest.case import TestCase

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
