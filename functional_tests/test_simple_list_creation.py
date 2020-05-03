from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_create_a_list_and_load_it_by_url(self):
        # I m opening my to do list app
        self.browser.get(self.live_server_url)
        # And expect to see corresponding title in the browser tab and the header
        self.assertIn("Todo", self.browser.title)
        self.assertIn("Todo", self.browser.find_element_by_tag_name("h1").text)
        # I'm typing "zabotat ebalu" into text box with "Enter a task" placeholder"
        input_box = self.get_input_box_id()
        self.assertEqual(input_box.get_attribute("placeholder"), "Enter a task")
        input_box.send_keys("zabotat ebalu")
        # when I hit enter I see updated browser window with typed above task
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_task_table("1: zabotat ebalu")
        # I'm adding another task "zabotat druguyy ebalu"
        # when I hit enter I expect to see updated task list
        input_box = self.get_input_box_id()
        input_box.send_keys("zabotat druguyu ebalu")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_task_table("1: zabotat ebalu")
        self.wait_for_row_task_table("2: zabotat druguyu ebalu")
        # self.fail("Dosviduli")
        # # the list is serialized in the URL
        # # when I navigate by URL i expect to see same list
        # # end of story

    def test_multiple_users_can_stat_list_different_url(self):
        self.browser.get(self.live_server_url)
        # I come and type a task
        input_box = self.get_input_box_id()
        input_box.send_keys("my new task")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_task_table("1: my new task")
        # now list view is opened with corresponding url
        my_url = self.browser.current_url
        self.assertRegex(my_url, "/lists/.+")
        # now second user opens the app
        self.browser.quit()
        self.browser = self.setup_browser()
        self.browser.get(self.live_server_url)
        # no signs of previous user
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("my new task", page_text)
        # she writes her task
        input_box = self.get_input_box_id()
        input_box.send_keys("nogotochki")
        input_box.send_keys(Keys.ENTER)
        # she sees this task only
        self.wait_for_row_task_table("1: nogotochki")
        # url for task list is different
        user_url = self.browser.current_url
        self.assertRegex(user_url, "/lists/.+")
        self.assertNotEqual(my_url, user_url)