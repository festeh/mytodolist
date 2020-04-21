from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class TaskValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_task(self):
        self.browser.get(self.live_server_url)
        # I'm misclicking Enter with empty field
        self.get_input_box_id().send_keys(Keys.ENTER)
        # No task is added, warning is shown
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))
        # I'm correcting myself this time and add valid task, which is shown
        self.get_input_box_id().send_keys("Get some stuff done")
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
        self.get_input_box_id().send_keys(Keys.ENTER)
        self.wait_for_row_task_table("1: Get some stuff done")
        # Then I again misclick and nothing happens, except for warning
        self.get_input_box_id().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))
        # Finally new task is added
        self.get_input_box_id().send_keys("Change your priorities")
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
        self.get_input_box_id().send_keys(Keys.ENTER)
        self.wait_for_row_task_table("1: Get some stuff done")
        self.wait_for_row_task_table("2: Change your priorities")

    def test_cannot_add_duplicating_task(self):
        self.browser.get(self.live_server_url)
        # I'm adding a task
        self.get_input_box_id().send_keys("Get some stuff done")
        self.get_input_box_id().send_keys(Keys.ENTER)
        self.wait_for_row_task_table("1: Get some stuff done")
        # I'm trying to add a same task
        self.get_input_box_id().send_keys("Get some stuff done")
        self.get_input_box_id().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(self.get_error_element().text,
                                               "Cannot add a duplicating task"))

    def test_duplication_message_are_not_shown_after_edit(self):
        self.browser.get(self.live_server_url)
        # I'm adding a task
        self.get_input_box_id().send_keys("Get some stuff done")
        self.get_input_box_id().send_keys(Keys.ENTER)
        self.wait_for_row_task_table("1: Get some stuff done")
        # I'm trying to add a same task
        self.get_input_box_id().send_keys("Get some stuff done")
        self.get_input_box_id().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertTrue(self.get_error_element().is_displayed()))
        # I'm then starting to make an edit
        self.get_input_box_id().send_keys("!")
        self.wait_for(lambda: self.assertFalse(self.get_error_element().is_displayed()))
