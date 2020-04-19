from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import List, Task


class ListAndTaskModelTest(TestCase):

    def test_cannot_add_empty_task(self):
        list_ = List.objects.create()
        task = Task(list=list_, text='')
        with self.assertRaises(ValidationError):
            task.full_clean()
            task.save()

    def test_save_load_items(self):
        list_ = List()
        list_.save()

        first_item = Task()
        first_item.text = "First one"
        first_item.list = list_
        first_item.save()

        second_item = Task()
        second_item.text = "The second"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(list_, saved_list)

        saved_items = Task.objects.all()
        self.assertEqual(len(saved_items), 2)

        self.assertEqual(saved_items[0].text, "First one")
        self.assertEqual(saved_items[0].list, list_)
        self.assertEqual(saved_items[1].text, "The second")
        self.assertEqual(saved_items[1].list, list_)