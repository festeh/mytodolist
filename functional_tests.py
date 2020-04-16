import time

from selenium import webdriver
import unittest

from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_create_a_list_and_load_it_by_url(self):
        # I m opening my to do list app
        self.browser.get("http://localhost:8000")
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
        table = self.browser.find_element_by_id("id_task_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertTrue(any(row.text == "1: zabotat ebalu" for row in rows))

        # I'm adding another task "zabotat druguyy ebalu"
        self.fail("Dosviduli")

        # when I hit enter I expect to see updated task list

        # the list is serialized in the URL

        # when I navigate by URL i expect to see same list

        # end of story


if __name__ == "__main__":
    unittest.main()
