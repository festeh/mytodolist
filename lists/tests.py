from django.test import TestCase
from lists.models import Task


class HomePageTest(TestCase):
    def test_home_page_resturns_correct_response(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_post_request(self):
        self.client.post("/", data={"task_text": "A new task"})
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().text, "A new task")

    def test_redirect_after_post_request(self):
        response = self.client.post("/", data={"task_text": "A new task"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

    def test_only_save_nonempty_tasks(self):
        self.client.post("/", data={"task_text": ""})
        self.assertEqual(Task.objects.count(), 0)

    def test_added_tasks_are_displayed(self):
        task1 = Task.objects.create(text="get a bath")
        task2 = Task.objects.create(text="drink a cup of coffee")
        response_text = self.client.get("/").content.decode()
        self.assertIn("get a bath", response_text)
        self.assertIn("drink a cup of coffee", response_text)


class TaskModelTest(TestCase):
    def test_save_load_items(self):
        first_item = Task()
        first_item.text = "First one"
        first_item.save()

        second_item = Task()
        second_item.text = "The second"
        second_item.save()

        saved_items = Task.objects.all()
        self.assertEqual(len(saved_items), 2)

        self.assertEqual(saved_items[0].text, "First one")
        self.assertEqual(saved_items[1].text, "The second")