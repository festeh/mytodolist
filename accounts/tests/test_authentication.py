from django.test import TestCase

from accounts.authentication import PasswordlessAuthBackend
from accounts.models import Token, User


class AuthenticateTest(TestCase):
    EMAIL = "kabanch@ik.ru"

    def test_none_for_bad_token(self):
        self.assertIsNone(PasswordlessAuthBackend().authenticate("ololo"))

    def test_new_user_for_valid_token(self):
        token = Token.objects.create(email=self.EMAIL)
        user = PasswordlessAuthBackend().authenticate(token.uid)
        new_user = User.objects.get(email=self.EMAIL)
        self.assertEqual(user, new_user)

    def test_existing_user_for_valid_token(self):
        existing_user = User.objects.create(email=self.EMAIL)
        token = Token.objects.create(email=self.EMAIL)
        user = PasswordlessAuthBackend().authenticate(token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):
    EMAIL = "kabanch@ik.ru"

    def test_none_for_not_existing_user(self):
        self.assertIsNone(PasswordlessAuthBackend().get_user("notkabanch@ik.ru"))

    def test_user_for_existing_user(self):
        User.objects.create(email="notkabanch@ik.ru")
        user = User.objects.create(email=self.EMAIL)
        self.assertEqual(PasswordlessAuthBackend().get_user(self.EMAIL),
                         user)
