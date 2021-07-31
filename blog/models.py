import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.mail import send_mail, get_connection
from django.core.mail.message import (EmailMultiAlternatives)
from django.shortcuts import reverse
from tinymce.models import HTMLField


DEFAULT_FROM_EMAIL = ''


class User(AbstractUser):
    class Meta:
        ordering = ['id']

    id = models.AutoField(primary_key=True)
    date_deleted = models.DateField(null=True, blank=True)
    about_you = models.TextField(null=True, blank=True)

    def send_custom_mail(self, subject, message, from_email, recipient_list,  # noqa
                         fail_silently=False, auth_user=None, auth_password=None):
        connection = get_connection(
            username=auth_user,
            auth_password=auth_password,
            fail_silently=fail_silently,
            port=587,
        )
        mail = EmailMultiAlternatives(subject, message, from_email, recipient_list, connection=connection)
        result = mail.send()
        return result

    def send_email_to_user(self, subject, message):
        subject = subject
        message = message
        email = self.email
        result = self.send_custom_mail(
            subject=subject,
            message=message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )
        return result

    def get_absolute_url(self):
        return reverse("user-detail", kwargs={"slug": self.username})

    @staticmethod
    def get_update_url():
        return reverse("account-update")

    @staticmethod
    def get_delete_url():
        return reverse("account-delete")

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username


class AbstractBaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", blank=True, editable=False)
    timestamp_created = models.DateTimeField(editable=False)
    timestamp_changed = models.DateTimeField(editable=False)

    def clean(self):
        if not self.timestamp_created:
            self.timestamp_created = timezone.now()
        self.timestamp_changed = timezone.now()

    @staticmethod
    def get_id_slug(length):
        return ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=length))

    def get_absolute_url(self):
        raise Exception("Improperly configured, please configure get_absolute_url function.")

    def get_update_url(self):
        return self.get_absolute_url() + "update/"

    def get_overview_url(self):
        raise Exception("Improperly configured, please configure get_overview_url function.")

    @staticmethod
    def get_create_url():
        raise Exception("Improperly configured, please configure get_create_url function.")


class Article(AbstractBaseModel):
    id_slug = models.CharField(max_length=18, unique=True, editable=False)
    publish = models.BooleanField(default=False)
    title = models.CharField(max_length=160)
    date = models.DateField()
    content = HTMLField()

    def get_absolute_url(self):
        return reverse("article-detail", args=[self.id_slug])

    @staticmethod
    def get_create_url():
        return reverse("article-create")

    def get_delete_url(self):
        return reverse("article-delete", args=[self.id_slug])

    def __str__(self):
        return self.title


class BlogComment(AbstractBaseModel):
    id_slug = models.CharField(max_length=18, unique=True, editable=False)
    article = models.ForeignKey(Article, models.CASCADE, editable=False)
    counter = models.IntegerField(default=0, editable=False)
    answer_to_number = models.IntegerField(default=0, blank=True, editable=False)
    comment = models.TextField()
    hide = models.BooleanField(default=False)

    def get_create_url(self):
        return reverse('blog-comment-create')

    def get_update_url(self):
        return reverse('blog-comment-update', args=[self.id_slug])

    def get_absolute_url(self):
        return reverse('article-detail', args=[self.article.id_slug])

    def __str__(self):
        return self.comment
