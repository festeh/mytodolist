from django.test import TestCase
from lists.models import Task


class HomePageTest(TestCase):
    def test_home_page_resturns_correct_response(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_post_request(self):
        response = self.client.post("/", data={"task_text": "A new task"})
        self.assertIn("A new task", response.content.decode())
        self.assertTemplateUsed(response, "home.html")


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