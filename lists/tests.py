from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page


class HomePageTest(TestCase):
    def test_home_page_resturns_correct_response(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_post_request(self):
        response = self.client.post("/", data={"task_text": "A new task"})
        self.assertIn("A new task", response.content.decode())
        self.assertTemplateUsed(response, "home.html")
