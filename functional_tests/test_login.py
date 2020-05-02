import re
import time
from os import getenv
from poplib import POP3_SSL

from django.core import mail
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest

SUBJECT = "Your login link for TODO task list"
TEXT = "Use this link to login"


class LoginTest(FunctionalTest):

    def wait_for_email(self, email_address, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(email_address, email.to)
            self.assertIn(SUBJECT, email.subject)
            self.assertIn(TEXT, email.body)
            return email.body
        start_time = time.time()
        inbox = POP3_SSL('pop.mail.ru')
        try:
            inbox.user(email_address)
            inbox.pass_(getenv("EMAILPASSWORD"))
            while time.time() - start_time < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    print(lines)
                    if f'Subject: {subject}' in lines:
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            inbox.quit()

    def test_can_get_email_to_login(self):
        # I want to register on the site so I press login button
        if self.staging_server:
            test_email = "testinggoat@mail.ru"
        else:
            test_email = "kabanch@ik.ru"
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("email").send_keys(test_email)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # new page in opened
        self.wait_for(lambda: self.assertIn("Check your email",
                                            self.browser.find_element_by_tag_name("body").text))

        # there's new email in inbox
        email_body = self.wait_for_email(test_email, SUBJECT)
        print("BODY", email_body)
        url_search = re.search(r"http://.+/.+$", email_body)
        if not url_search:
            self.fail(f'Could not find login url in {email_body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # I'm clicking it
        self.browser.get(url)

        # My email is displayed on the page
        self.wait_for_login(test_email)

        # Now I'm logging out
        self.browser.find_element_by_link_text("Logout").click()

        # Enter email field should return, my email should not be shown
        self.wait_for_logout(test_email)
