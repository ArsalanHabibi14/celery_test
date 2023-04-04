from datetime import datetime

from django.utils import timezone
from django.utils.crypto import get_random_string
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.html import format_html
from rest_framework.authtoken.models import Token
import random
import string
from django_countries.fields import CountryField


def random_num():
    return random.randint(100000, 999999)


class EmailCodes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    email = models.EmailField(max_length=2000)
    email_code = models.IntegerField(default=random_num, primary_key=True,
                                     unique=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username


# =============================================

def generate_id():
    letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "".join(random.choices(letters, k=7))


def gen_token():
    """Generate Token For Company"""
    token = get_random_string(length=45)
    return token


class Company(models.Model):
    user_agent = models.CharField(max_length=200, null=True)
    company_name = models.CharField(max_length=200, unique=True)
    country = CountryField(null=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    id = models.CharField(
        max_length=7, primary_key=True, default=generate_id, editable=False, unique=True
    )

    def __str__(self):
        return self.company_name


class CompanyToken(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, unique=True)
    token = models.CharField(
        max_length=45, default=gen_token, editable=False, primary_key=True, unique=True
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token

    class Meta:
        ordering = ("-created_time",)


# ===================================================================


class Profile(models.Model):
    """
    This Model Is for the Profile
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True
    )
    username = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField(max_length=2000)
    profile_image = models.ImageField(upload_to="users/", default="avatar.svg")
    phonenumber = PhoneNumberField(null=True, blank=True, unique=True)
    country = CountryField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    join_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    id = models.CharField(
        max_length=7, editable=False, primary_key=True, default=generate_id
    )

    def __str__(self):
        return self.username

    def thumbnail_image(self):
        return format_html(
            f"<a href='{self.profile_image.url}'><img src='{self.profile_image.url}' alt='{self.username}' style='width:70px;height:70px;border-radius:50px;'></a>"
        )
