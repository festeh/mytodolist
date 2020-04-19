from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class TaskValidationTest(FunctionalTest):

    def test_cannot_add_empty_task(self):
        self.browser.get(self.live_server_url)
        # I'm misclicking Enter with empty field
        self.get_input_box_id().send_keys(Keys.ENTER)
        # No task is added, warning is shown
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
                                               "Cannot add an empty task"))
        # I'm correcting myself this time and add valid task, which is shown
        self.get_input_box_id().send_keys("Get some stuff done")
        self.get_input_box_id().send_keys(Keys.ENTER)
        self.wait_for_row_task_table("1: Get some stuff done")
        # Then I again misclick and nothing happens, except for warning
        self.get_input_box_id().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
                                               "Cannot add an empty task"))
        # Finally new task is added
        self.get_input_box_id().send_keys("Change your priorities")
        self.get_input_box_id().send_keys(Keys.ENTER)
        self.wait_for_row_task_table("1: Get some stuff done")
        self.wait_for_row_task_table("2: Change your priorities")
