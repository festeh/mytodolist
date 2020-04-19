from django.test import TestCase

from lists.models import List, Task


class HomePageTest(TestCase):
    def test_home_page_resturns_correct_response(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ListViewTest(TestCase):

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
                         data={"task_text": "And another one"})
        self.assertEqual(Task.objects.count(), 1)
        added_task = Task.objects.first()
        self.assertEqual(added_task.text, "And another one")
        self.assertEqual(added_task.list, our_list)

    def test_redirect_list_view_after_adding_task(self):
        old_list = List.objects.create()
        our_list = List.objects.create()
        response = self.client.post(f"/lists/{our_list.id}/",
                                    data={"task_text": "And another one"})
        self.assertRedirects(response, f"/lists/{our_list.id}/")


class NewListTest(TestCase):
    def test_can_save_post_request(self):
        self.client.post("/lists/new", data={"task_text": "A new task"})
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().text, "A new task")

    def test_redirect_after_post_request(self):
        response = self.client.post("/lists/new", data={"task_text": "A new task"})
        # we created db from scratch so it's safe
        created_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{created_list.id}/")

    def test_validation_errors_are_passed_to_template(self):
        response = self.client.post("/lists/new", data={"task_text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        err_msg = "Cannot add an empty task"
        self.assertContains(response, err_msg)

    def test_empty_tasks_not_saved(self):
        self.client.post("/lists/new", data={"task_text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Task.objects.count(), 0)

    # def test_only_save_nonempty_tasks(self):
    #     self.client.post("/lists/new", data={"task_text": ""})
    #     self.assertEqual(Task.objects.count(), 0)
