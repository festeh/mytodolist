from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from functional_tests.base import FunctionalTest

User = get_user_model()


class TaskListTest(FunctionalTest):
    def create_pre_authd_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        # need to open smth, just to set cookeis
        self.browser.get(self.live_server_url + "/404_oops/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path="/"
        ))

    def test_pre_authd_working(self):
        email = "kabanch@ik.ru"
        self.browser.get(self.live_server_url)
        self.wait_for_logout(email)
        self.create_pre_authd_session(email)
        self.browser.get(self.live_server_url)
        self.wait_for_login(email)
