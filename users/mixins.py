from django.http import JsonResponse
from django.shortcuts import redirect
from .models import *
from .utils import check_token_exist
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CheckLoginMixin:
    """Check if a user is logged in."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/profile/")

        return super().dispatch(request, *args, **kwargs)


from rest_framework.response import Response


# =====================================


class RegisterMixin:
    def dispatch(self, request, *args, **kwargs):
        token = request.headers.get("company-auth")
        if token is None:
            return JsonResponse({"detail": "company-auth should set!"})
        # ======================================
        get_company = CompanyToken.objects.filter(token=token).first()
        if get_company is None or get_company.company is None:
            return JsonResponse({"detail": "Company Not Found!"})
        else:
            self.company = get_company.company
        return super().dispatch(request, *args, **kwargs)


# =====================================


class CheckCompanyTokenExist:
    def dispatch(self, request, *args, **kwargs):
        # ====================================
        # Check Company Token Exist
        token = request.headers.get("company-auth")
        if token is None:
            return JsonResponse({"detail": "company-auth should set!"})
        # Get The User
        try:
            user_id = TokenAuthentication().authenticate(request)[0].id
            user = User.objects.get(pk=user_id)
        except AuthenticationFailed:
            return JsonResponse({"detail": "Invalid token"})
        except:
            return JsonResponse(
                {"detail": "Authentication Credintal could not provided!"}
            )

        # ======================================
        # is_exists, get_company = check_token_exist(token)
        get_company = CompanyToken.objects.filter(token=str(token)).first()
        if get_company is None or get_company.company is None:
            return JsonResponse({"detail": "Company Not Found!"})
        else:
            get_profile = Profile.objects.filter(user=user, company=get_company.company).first()
            if get_profile is None:
                return JsonResponse({"detail": "Profile Not Found!"})
            self.company = get_company.company
            self.profile = get_profile
            if get_profile.company is None:
                get_profile.company = get_company.company
                get_profile.save()
        return super().dispatch(request, *args, **kwargs)


class ProfileCheck:
    def get_user(self, request):
        user = None
        try:
            user_id = TokenAuthentication().authenticate(request)[0].id
            user = User.objects.get(pk=user_id)
        except:
            pass
        return user


class TestUserMixin:
    def dispatch(self, request, *args, **kwargs):
        print(request.user)
        return super(TestUserMixin, self).dispatch(request, *args, **kwargs)


# ================
class TestMethod:
    def get(self, request, format=None):
        print("Hello World!")

    def post(self, request, format=None):
        print("This is Post Request")
