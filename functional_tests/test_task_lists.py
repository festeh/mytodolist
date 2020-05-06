from django.contrib.auth import get_user_model
from functional_tests.base import FunctionalTest

TEST_MAIL = "kabanch@ik.ru"

User = get_user_model()


class TaskListTest(FunctionalTest):

    def test_pre_authd_working(self):
        email = TEST_MAIL
        self.browser.get(self.live_server_url)
        self.wait_for_logout(email)
        self.create_pre_authd_session(email)
        self.browser.get(self.live_server_url)
        self.wait_for_login(email)

    def test_my_lists_shown(self):
        # I'm opening the site and create a task list
        self.create_pre_authd_session(TEST_MAIL)
        self.browser.get(self.live_server_url)
        self.add_task_to_list("Delay raz")
        self.add_task_to_list("Delay dva")

        # I notice a new button and click it
        this_list_url = self.browser.current_url
        self.browser.find_element_by_link_text("My Task Lists").click()

        # Here lies my new list, named after first task
        self.wait_for(lambda: self.browser.find_element_by_link_text("Delay raz"))
        self.browser.find_element_by_link_text("Delay raz").click()
        # I'm clicking it and return to my list
        self.wait_for(lambda: self.assertEqual(this_list_url, self.browser.current_url))

        # Then I want to add another list - I click home page and
        # enter new task
        self.browser.get(self.live_server_url)
        self.add_task_to_list("Do less lists")
        new_list_url = self.browser.current_url

        self.browser.find_element_by_link_text("My Task Lists").click()

        # Here lies my new list, named after first task
        self.wait_for(lambda: self.browser.find_element_by_link_text("Do less lists"))
        self.browser.find_element_by_link_text("Do less lists").click()
        self.wait_for(lambda: self.assertEqual(new_list_url, self.browser.current_url))

        # I'm logging out, no My Lists is shown
        self.browser.find_element_by_link_text("Logout").click()
        self.wait_for(lambda: self.assertEqual(self.browser.find_elements_by_link_text("My Task Lists"),
                                               []))
