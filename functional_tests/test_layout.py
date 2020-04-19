from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class LayoutTest(FunctionalTest):
    def test_layout_styling(self):
        # I'm opening home page and expect to see nice CENTERED task field
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        input_box = self.browser.find_element_by_id("id_new_item")
        # rounding errors ( ͡° ͜ʖ ͡°)
        self.assertAlmostEqual(input_box.location["x"] + input_box.size['width'] / 2,
                               512,
                               delta=10)
        # Then I add a task and and expect to see same field position on new page
        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys("my new task")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_task_table('1: my new task')
        input_box = self.browser.find_element_by_id("id_new_item")
        self.assertAlmostEqual(input_box.location["x"] + input_box.size['width'] / 2,
                               512,
                               delta=10)