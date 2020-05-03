from django.test import TestCase

from lists.forms import TaskForm, EMPTY_TASK_ERROR, DUPLICATING_TASK_ERROR, ExistingListTaskForm
from lists.models import List, Task


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


class NewListTest(TestCase):
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


class MyListsTest(TestCase):
    def test_my_lists_template_rendered(self):
        response = self.client.get("/lists/users/a@b.com/")
        self.assertTemplateUsed(response, "my_lists.html")