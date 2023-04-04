from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import os
import random

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


def generate_username(name):
    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():
        # if provider == filtered_user_by_email[0].auth_provider:
        new_user = User.objects.get(email=email)

        registered_user = User.objects.get(email=email)
        registered_user.check_password(os.environ.get("GOOGLE_SECRET_KEY"))

        get_token = Token.objects.filter(user=registered_user)
        if not get_token.exists():
            Token.objects.create(user=registered_user)
        new_token = list(Token.objects.filter(
            user_id=registered_user).values("key"))

        return {
            'username': registered_user.username,
            'email': registered_user.email,
            'tokens': str(new_token[0]['key'])}
        # else:
        #     raise AuthenticationFailed(
        #         detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'username': email, 'email': email,
            'password': os.environ.get("GOOGLE_SECRET_KEY")
        }
        user = User.objects.create_user(**user)
        user.is_active = True
        user.auth_provider = provider
        user.save()
        new_user = User.objects.get(email=email)
        new_user.check_password(os.environ.get("GOOGLE_SECRET_KEY"))
        Token.objects.create(user=new_user)
        new_token = list(Token.objects.filter(user_id=new_user).values("key"))
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': str(new_token[0]['key']),
        }
