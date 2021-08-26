import datetime
from django.test import TestCase
from django.contrib.auth.views import LoginView, LogoutView
from tests.tests_mixins import *
from blog.models import *
from blog.views import *

class BlogViewTests(TestCase):
    def test_get_not_logged_in(self):
        response = self.client.get(reverse("landingpage"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['view']), BlogView)


class LoginViewTest(TestCase):
    def test_get_not_logged_in(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['view']), LoginView)


