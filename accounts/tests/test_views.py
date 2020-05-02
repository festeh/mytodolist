from unittest.mock import patch, call

from django.test import TestCase
from accounts import views
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):
    EMAIL = "kabanch@ik.ru"

    def test_view_redirects(self):
        response = self.client.post("/accounts/send_login_email",
                                    data={"email": self.EMAIL})
        self.assertRedirects(response, "/")

    @patch("accounts.views.send_mail")
    def test_email_sends_from_post(self, mock_send_mail):
        self.client.post("/accounts/send_login_email",
                         data={"email": self.EMAIL})
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(mock_send_mail.called, True)
        self.assertEqual(subject, "Your login link for TODO task list")
        self.assertEqual(from_email, "testinggoat@mail.ru")
        self.assertEqual(to_list, [self.EMAIL])

    def test_success_message_shown(self):
        response = self.client.post("/accounts/send_login_email",
                                    data={"email": self.EMAIL}, follow=True)
        message = list(response.context["messages"])[0]
        self.assertEqual(message.message, "Check your email for login link")
        self.assertEqual(message.tags, "success")

    def test_token_is_created_for_email(self):
        self.client.post("/accounts/send_login_email",
                         data={"email": self.EMAIL}, follow=True)
        token = Token.objects.first()
        self.assertEqual(token.email, self.EMAIL)

    @patch("accounts.views.send_mail")
    def test_token_uid_is_in_message(self, mock_send_mail):
        self.client.post("/accounts/send_login_email",
                         data={"email": self.EMAIL}, follow=True)
        token = Token.objects.first()
        url = f"http://testserver/accounts/login?token={token.uid}"
        _, body, *__ = mock_send_mail.call_args[0]
        self.assertIn(url, body)


@patch("accounts.views.auth")
class LoginViewTest(TestCase):
    EMAIL = "kabanch@ik.ru"

    def test_view_redirects(self, fake_auth):
        response = self.client.get("/accounts/login?token=xXx420xXx")
        self.assertRedirects(response, "/")

    def test_user_token_authenticated(self, fake_auth):
        response = self.client.get("/accounts/login?token=1234")
        self.assertEqual(fake_auth.authenticate.call_args,
                         call(uid="1234"))

    def test_user_login_called_after_auth(self, fake_auth):
        response = self.client.get("/accounts/login?token=1234")
        self.assertEqual(fake_auth.login.call_args,
                         call(response.wsgi_request, fake_auth.authenticate.return_value))

    def test_not_login_after_bad_auth(self, fake_auth):
        fake_auth.authenticate.return_value = None
        response = self.client.get("/accounts/login?token=1234")
        self.assertEqual(fake_auth.login.called, False)
