import time

from django.test import LiveServerTestCase
from selenium import webdriver
import unittest

from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_task_table(self, row_text):
        table = self.browser.find_element_by_id("id_task_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_create_a_list_and_load_it_by_url(self):
        # I m opening my to do list app
        self.browser.get(self.live_server_url)
        # And expect to see corresponding title in the browser tab and the header
        self.assertIn("Todo", self.browser.title)
        self.assertIn("Todo", self.browser.find_element_by_tag_name("h1").text)
        # I'm typing "zabotat ebalu" into text box with "Enter a task" placeholder"
        input_box = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(input_box.get_attribute("placeholder"), "Enter a task")
        input_box.send_keys("zabotat ebalu")

        # when I hit enter I see updated browser window with typed above task
        input_box.send_keys(Keys.ENTER)
        time.sleep(1.0)
        self.check_for_row_task_table("1: zabotat ebalu")
        # I'm adding another task "zabotat druguyy ebalu"
        # when I hit enter I expect to see updated task list
        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys("zabotat druguyu ebalu")
        input_box.send_keys(Keys.ENTER)
        time.sleep(1.0)
        self.check_for_row_task_table("1: zabotat ebalu")
        self.check_for_row_task_table("2: zabotat druguyu ebalu")
        self.fail("Dosviduli")

        # the list is serialized in the URL

        # when I navigate by URL i expect to see same list

        # end of story


if __name__ == "__main__":
    unittest.main()
