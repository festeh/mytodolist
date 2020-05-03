from django.conf import settings
from django.contrib.auth import get_user_model
from functional_tests.base import FunctionalTest
from functional_tests.management.commands.create_session import create_local_pre_auth_session
from functional_tests.server_tools import create_server_pre_auth_server

User = get_user_model()


class TaskListTest(FunctionalTest):
    def create_pre_authd_session(self, email):
        if self.staging_server:
            session_key = create_server_pre_auth_server(self.staging_server, email)
        else:
            session_key = create_local_pre_auth_session(email)
        # need to open smth, just to set cookeis
        self.browser.get(self.live_server_url + "/404_oops/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path="/"
        ))

    def test_pre_authd_working(self):
        email = "kabanch@ik.ru"
        self.browser.get(self.live_server_url)
        self.wait_for_logout(email)
        self.create_pre_authd_session(email)
        self.browser.get(self.live_server_url)
        self.wait_for_login(email)
