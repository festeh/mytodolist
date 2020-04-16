from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = browser = webdriver.Chrome()
    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_create_a_list_and_load_it_by_url(self):
        # I m opening my to do list app
        self.browser.get("http://localhost:8000")
        # And expect to see corresponding title
        self.assertIn("Todo", self.browser.title)

        # I'm typing "zabotat ebalu" into text box

        # when I hit enter I see updated browser window with typed above task

        # I'm adding another task "zabotat druguyy ebalu"

        # when I hit enter I expect to see updated task list

        # the list is serialized in the URL

        # when I navigate by URL i expect to see same list

        # end of story

if __name__ == '__main__':
    unittest.main()