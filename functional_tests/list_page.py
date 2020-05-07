from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from functional_tests.base import wait, FunctionalTest


class ListPage:
    def __init__(self, test):
        self.test: FunctionalTest = test
        self.browser: webdriver.Chrome = self.test.browser

    def get_table_rows(self):
        return self.browser.find_elements_by_css_selector("#id_task_table tr")

    @wait
    def wait_row_table(self, num, text):
        expected = f"{num}: {text}"
        rows = self.get_table_rows()
        self.test.assertIn(expected, [row.text for row in rows])

    def get_task_input_box(self):
        return self.browser.find_element_by_id("id_text")

    def add_task_to_list(self, text):
        n_rows = len(self.get_table_rows())
        self.get_task_input_box().send_keys(text)
        self.get_task_input_box().send_keys(Keys.ENTER)
        task_num = n_rows + 1
        self.wait_row_table(task_num, text)
        return self

    def get_share_box(self):
        return self.browser.find_element_by_css_selector("input[name='share']")

    def get_shared_with_list(self):
        return self.browser.find_element_by_css_selector(".list-share")

    def share_task_list_with(self, email):
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(Keys.ENTER)
        self.test.wait_for(
            lambda: self.test.assertIn(
                email,
                [task.text for task in self.get_shared_with_list()]
            )
        )

    def go_to_my_lists_page(self):
        self.browser.get(self.test.live_server_url)
        self.browser.find_element_by_link_text("My Task Lists").click()
        self.test.wait_for(
            lambda: self.test.assertEqual(
                self.test.browser.find_element_by_tag_name("h1").text,
                "My Task Lists"
            )
        )
        return self

    def get_list_owner(self):
        return self.browser.find_element_by_id("id_list_owner").text
