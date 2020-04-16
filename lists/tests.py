from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page(self):
        self.assertEqual(resolve("/").func, home_page)

    def test_home_page_resturns_correct_response(self):
        request = HttpRequest()
        response = home_page(request)
        html_content = response.content.decode("utf-8")
        self.assertTrue(html_content.startswith("<html>"))
        self.assertIn("<title>Todo list</title>", html_content)
        self.assertTrue(html_content.endswith("</html>"))
