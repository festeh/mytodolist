from django.test import TestCase
from lists.models import List, Task


class HomePageTest(TestCase):
    def test_home_page_resturns_correct_response(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ListViewTest(TestCase):

    def test_corect_template_is_used(self):
        response = self.client.get("/lists/my_unique_list/")
        self.assertTemplateUsed(response, "list.html")

    def test_task_list_is_shown(self):
        parent_list = List.objects.create()
        Task.objects.create(text="get a bath", list=parent_list)
        Task.objects.create(text="drink a cup of coffee", list=parent_list)
        response = self.client.get("/lists/my_unique_list/")
        self.assertContains(response, "get a bath")
        self.assertContains(response, "drink a cup of coffee")


class NewListTest(TestCase):
    def test_can_save_post_request(self):
        self.client.post("/lists/new", data={"task_text": "A new task"})
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().text, "A new task")

    def test_redirect_after_post_request(self):
        response = self.client.post("/lists/new", data={"task_text": "A new task"})
        self.assertRedirects(response, "/lists/my_unique_list/")

    def test_only_save_nonempty_tasks(self):
        self.client.post("/lists/new", data={"task_text": ""})
        self.assertEqual(Task.objects.count(), 0)


class ListAndTaskModelTest(TestCase):
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
