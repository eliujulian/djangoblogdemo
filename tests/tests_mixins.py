from django.shortcuts import reverse
from django.test import Client
from blog.models import User


class CreateUserMixin:
    def setUp(self):
        super().setUp()  # noqa
        self.client = Client()

        password = "123456"
        data = {"username": "adam", "first_name": "Adam", "last_name": "Test", "password": password}
        data_2 = {"username": "bdam", "first_name": "Bert", "last_name": "Test", "password": password}

        self.client.post(reverse("account-register"), data=data)
        self.client.post(reverse("account-register"), data=data_2)
        self.user = User.objects.get(username="adam")  # noqa
        self.user.is_active = True
        self.user.is_superuser = True
        self.user.save()
        self.user2 = User.objects.get(username="bdam")  # noqa
        self.user2.is_active = True
        self.user2.save()
        self.client.login(username="adam", password=password)
