from unittest.case import TestCase

from lists.forms import TaskForm, EMPTY_TASK_ERROR


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
