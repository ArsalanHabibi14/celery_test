# Import the Module that Requires
import os.path

from django.db.models.signals import post_save, post_delete
from .models import Profile, CompanyToken, Company, EmailCodes
from django.contrib.auth.models import User


def create_email(sender, created, instance, **kwargs):
    """Just For Create An Email"""
    if created:
        email = instance
        profile = Profile.objects.get(user=email.user)
        profile.email = email.email
        profile.save()


def create_user(sender, created, instance, **kwargs):
    """
    This Function Use To Automatically Create a Profile When a User Create
    """

    if created:
        user = instance
        Profile.objects.create(
            user=user, username=user.username, lastname=user.last_name, email=user.email
        )
        EmailCodes.objects.create(user=user)


def edit_user(sender, created, instance, **kwargs):
    """
    This Function Use to Automatically Edit a User When A Profile Edited
    """
    profile = instance
    user = profile.user

    if created == False:
        user.username = profile.username
        user.last_name = profile.lastname
        user.email = profile.email
        user.save()


def delete_user(sender, instance, **kwargs):
    """
    This Method Is Use to Automatically delete a User when a Profile Delete
    """

    try:
        user = instance.user
        get_path = user.profile_image.path
        if os.path.exists(get_path):
            os.remove(get_path)
        user.delete()
    except:
        pass


# def create_company_token(sender, created, instance, **kwargs):
#     """Just For Create The Company Token"""
#     if created:
#         company = instance
#         CompanyToken.objects.create(company=company)


# def delete_company_token(sender, instance, **kwargs):
#     """Just For Delete The Company Token"""
#     company = instance
#     company_token = CompanyToken.objects.filter(company=company).first()
#     company_token.delete()


post_save.connect(create_email, EmailCodes)
# post_save.connect(create_company_token, Company)
post_save.connect(create_user, User)
post_save.connect(edit_user, Profile)
post_delete.connect(delete_user, Profile)
# post_delete.connect(delete_company_token, Profile)
