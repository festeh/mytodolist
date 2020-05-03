import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

from functional_tests.server_tools import reset_database

MAX_WAIT = 10


def wait(fn):
    def wrapped(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    return wrapped


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = self.setup_browser()
        self.staging_server = os.environ.get("STAGING_SERVER")
        if self.staging_server:
            self.live_server_url = "http://" + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self) -> None:
        self.browser.quit()

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_for_row_task_table(self, row_text):
        table = self.browser.find_element_by_id("id_task_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for_login(self, email):
        self.browser.find_element_by_link_text("Logout")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(email, navbar.text)

    @wait
    def wait_for_logout(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertNotIn(email, navbar.text)

    def get_input_box_id(self):
        return self.browser.find_element_by_id("id_text")

    def add_task_to_list(self, task_text):
        n_rows = len(self.browser.find_elements_by_css_selector("#id_task_table tr"))
        self.get_input_box_id().send_keys(task_text)
        self.get_input_box_id().send_keys(Keys.ENTER)
        task_num = n_rows + 1
        self.wait_for_row_task_table(f"{task_num}: {task_text}")

    def setup_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        return webdriver.Chrome(chrome_options=options)
