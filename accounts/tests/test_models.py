from django.contrib import auth
from django.test import TestCase

# Create your tests here.
from accounts.models import User, Token


class UserModelTest(TestCase):
    EMAIL = "abc@def.com"

    def test_user_with_only_email_is_valid(self):
        user = User(email=self.EMAIL)
        user.full_clean()

    def test_email_is_primary_key(self):
        user = User(email=self.EMAIL)
        self.assertEqual(user.pk, self.EMAIL)

    def test_no_problem_auth_login(self):
        user = User.objects.create(email=self.EMAIL)
        user.backend = ''
        auth.login(self.client.request().wsgi_request, user)


class TokenModelTest(TestCase):
    EMAIL = "abc@def.com"

    def test_tokens_not_equal(self):
        token_1 = Token.objects.create(email=self.EMAIL)
        token_2 = Token.objects.create(email=self.EMAIL)
        self.assertNotEqual(token_1.uid, token_2.uid)
