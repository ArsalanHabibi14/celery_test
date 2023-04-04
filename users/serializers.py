from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import CompanyToken, Profile, Company
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    """Serializer for User objects in Django models that support serialization"""

    class Meta:
        model = User
        fields = ["username", "last_name", "email", "password"]
        extra_kwargs = {
            "password": {"required": True},
            "email": {"required": True},
            "last_name": {"required": True},
        }


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "username",
            "lastname",
            "email",
            "profile_image",
            "phonenumber",
            "twitter_link",
            "facebook_link",
            "instagram_link",
        ]


class CompanySerializer(serializers.ModelSerializer):
    user_agent = serializers.ReadOnlyField(source="user_agent.username")

    class Meta:
        model = Company
        fields = ["company_name", "user_agent", "country"]


class CompanyTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyToken
        fields = "__all__"


# Password Reset
from rest_framework import serializers
from . import google_auth, facebook, twitterhelper
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""

    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            user_id = user_data["id"]
            email = user_data["email"]
            name = user_data["name"]
            provider = "facebook"
            return register_social_user(
                provider=provider, user_id=user_id, email=email, name=name
            )
        except Exception as identifier:

            raise serializers.ValidationError(
                "The token  is invalid or expired. Please login again."
            )


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google_auth.Google.validate(auth_token)
        try:
            user_data["sub"]
        except:
            raise serializers.ValidationError(
                "The token is invalid or expired. Please login again."
            )

        if user_data["aud"] != os.environ.get("GOOGLE_CLIENT_ID"):
            raise AuthenticationFailed("oops, who are you?")

        user_id = user_data["sub"]
        email = user_data["email"]
        name = user_data["name"]
        provider = "google"

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name
        )


class TwitterAuthSerializer(serializers.Serializer):
    """Handles serialization of twitter related data"""

    access_token_key = serializers.CharField()
    access_token_secret = serializers.CharField()

    def validate(self, attrs):

        access_token_key = attrs.get("access_token_key")
        access_token_secret = attrs.get("access_token_secret")

        user_info = (
            twitterhelper.TwitterAuthTokenVerification.validate_twitter_auth_tokens(
                access_token_key, access_token_secret
            )
        )

        try:
            user_id = user_info["id_str"]
            email = user_info["email"]
            name = user_info["name"]
            provider = "twitter"
        except:
            raise serializers.ValidationError(
                "The tokens are invalid or expired. Please login again."
            )

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name
        )
