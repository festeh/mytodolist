import re

from django.core import mail
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest

TEST_EMAIL = "dimich3d@ya.ru"
SUBJECT = "Your login link for"
TEXT = "Use this link to login"


class LoginTest(FunctionalTest):
    def test_can_get_email_to_login(self):
        # I want to register on the site so I press login button
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("email").send_keys(TEST_EMAIL)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # new page in opened
        self.wait_for(lambda: self.assertIn("Check your email",
                                            self.browser.find_element_by_tag_name("body").text))

        # there's new email in inbox
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertIn(SUBJECT, email.subject)
        self.assertIn(TEXT, email.body)
        url_search = re.search(r"http://.+/.+$", email.body)
        if not url_search:
            self.fail(f'Could not find login url in {email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # I'm clicking it
        self.browser.get(url)

        # My email is displayed on the page
        self.wait_for_login(TEST_EMAIL)

        # Now I'm logging out
        self.browser.find_element_by_link_text("Logout").click()

        # Enter email field should return, my email should not be shown
        self.wait_for_logout(TEST_EMAIL)
