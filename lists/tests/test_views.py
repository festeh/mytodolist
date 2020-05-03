import unittest
from unittest.mock import patch, Mock

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase

from lists.forms import TaskForm, EMPTY_TASK_ERROR, DUPLICATING_TASK_ERROR, ExistingListTaskForm
from lists.models import List, Task
from lists.views import new_list


class HomePageTest(TestCase):
    def test_home_page_uses_correct_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_uses_task_form(self):
        response = self.client.get("/")
        self.assertIsInstance(response.context["form"], TaskForm)


class ListViewTest(TestCase):

    def post_empty_task(self):
        our_list = List.objects.create()
        return self.client.post(f"/lists/{our_list.id}/", data={"text": ""})

    def test_corect_template_is_used(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_task_list_is_shown_and_only_these(self):
        parent_list = List.objects.create()
        Task.objects.create(text="get a bath", list=parent_list)
        Task.objects.create(text="drink a cup of coffee", list=parent_list)
        response = self.client.get(f"/lists/{parent_list.id}/")
        self.assertContains(response, "get a bath")
        self.assertContains(response, "drink a cup of coffee")
        new_list = List.objects.create()
        Task.objects.create(text="do some stuff", list=new_list)
        response = self.client.get(f"/lists/{new_list.id}/")
        self.assertNotContains(response, "get a bath")
        self.assertNotContains(response, "drink a cup of coffee")
        self.assertContains(response, "do some stuff")

    def test_list_id_passed_to_template(self):
        old_list = List.objects.create()
        our_list = List.objects.create()
        response = self.client.get(f"/lists/{our_list.id}/")
        self.assertEqual(response.context["list"], our_list)

    def test_can_add_new_task_existing_list(self):
        old_list = List.objects.create()
        our_list = List.objects.create()

        self.client.post(f"/lists/{our_list.id}/",
                         data={"text": "And another one"})
        self.assertEqual(Task.objects.count(), 1)
        added_task = Task.objects.first()
        self.assertEqual(added_task.text, "And another one")
        self.assertEqual(added_task.list, our_list)

    def test_redirect_list_view_after_adding_task(self):
        old_list = List.objects.create()
        our_list = List.objects.create()
        response = self.client.post(f"/lists/{our_list.id}/",
                                    data={"text": "And another one"})
        self.assertRedirects(response, f"/lists/{our_list.id}/")

    def test_empty_task_not_saved(self):
        self.post_empty_task()
        self.assertEqual(Task.objects.count(), 0)

    def test_empty_task_leads_to_same_page(self):
        response = self.post_empty_task()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list.html")

    def test_empty_task_passes_form_template(self):
        response = self.post_empty_task()
        self.assertIsInstance(response.context['form'], ExistingListTaskForm)

    def test_adding_duplicate_task_leads_to_error_message(self):
        list_ = List.objects.create()
        Task.objects.create(text="my task", list=list_)
        response = self.client.post(f"/lists/{list_.id}/",
                                    data={"text": "my task"})
        self.assertContains(response, DUPLICATING_TASK_ERROR)
        self.assertTemplateUsed(response, "list.html")
        self.assertEqual(Task.objects.count(), 1)

    def test_empty_task_error_message_shown(self):
        response = self.post_empty_task()
        self.assertContains(response, EMPTY_TASK_ERROR)

    def test_task_form_is_displayed(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertIsInstance(response.context['form'], ExistingListTaskForm)
        self.assertContains(response, 'name="text"')


User = get_user_model()


class NewListViewIntegratedTest(TestCase):
    def test_can_save_post_request(self):
        self.client.post("/lists/new", data={"text": "A new task"})
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().text, "A new task")

    def test_redirect_after_post_request(self):
        response = self.client.post("/lists/new", data={"text": "A new task"})
        # we created db from scratch so it's safe
        created_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{created_list.id}/")

    def test_empty_task_input_leads_home_page(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_empty_task_input_leads_to_home_page_with_correct_form(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertIsInstance(response.context['form'], TaskForm)

    def test_empty_task_input_leads_to_correct_error_msg(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertContains(response, EMPTY_TASK_ERROR)

    def test_empty_tasks_not_saved(self):
        self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Task.objects.count(), 0)

    def test_new_list_has_owner(self):
        user = User.objects.create(email="a@b.com")
        self.client.force_login(user)
        self.client.post("/lists/new", data={"text": "some task"})
        task_list = List.objects.first()
        self.assertEqual(task_list.owner, user)


@patch("lists.views.NewListTaskForm")
class NewListViewUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.request = HttpRequest()
        self.request.POST["text"] = "my new task"
        self.request.user = Mock()

    def test_POST_data_passed_new_form(self, mock_new_task_list_form: Mock):
        new_list(self.request)
        mock_new_task_list_form.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_is_valid(self, mock_new_task_list_form):
        mock_form = mock_new_task_list_form.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch("lists.views.redirect")
    def test_redirects_to_form_return_object_if_form_is_valid(self, mock_redirect, mock_new_task_list_form):
        mock_form = mock_new_task_list_form.return_value
        mock_form.is_valid.return_value = True
        response = new_list(self.request)
        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch("lists.views.render")
    def test_renders_home_page_if_form_is_invalid(self, mock_render, mock_new_task_list_form):
        mock_form = mock_new_task_list_form.return_value
        mock_form.is_valid.return_value = False
        response = new_list(self.request)
        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(self.request, 'home.html', {'form': mock_form})

    def test_no_save_invalid_form(self, mock_new_task_list_form):
        mock_form = mock_new_task_list_form.return_value
        mock_form.is_valid.return_value = False
        new_list(self.request)
        self.assertFalse(mock_form.save.called)


class MyListsTest(TestCase):
    def test_my_lists_template_rendered(self):
        User.objects.create(email="a@b.com")
        response = self.client.get("/lists/users/a@b.com/")
        self.assertTemplateUsed(response, "my_lists.html")

    def test_correct_owner_is_passed_to_template(self):
        wrong_user = User.objects.create(email="kek@cheburek.com")
        right_user = User.objects.create(email="a@b.com")
        response = self.client.get("/lists/users/a@b.com/")
        self.assertEqual(response.context["owner"], right_user)
