from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, views, generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from .serializers import *
from .models import *
from .mixins import *
from .tasks import mail_send
from .utils import *
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import RedirectView
import requests
import json
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializer


@csrf_exempt
def login(request):
    if request.method == "POST":
        user = User.objects.filter(
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        ).first()
        if user is None:
            return JsonResponse(
                {
                    "error": "Could not find this user Please check your username or password"
                }
            )
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({"token": str(token)}, status=200)
    return Response(
        {"detail": "Just Send The POST Request! With your username and password"}
    )


@csrf_exempt
def home(request):
    """
    Just A Simple Home Page
    """
    context = {}
    return render(request, "home.html", context)


# =================================================================


class LogoutPage(CheckCompanyTokenExist, views.APIView):
    """Logout a user from the specified organization"""

    def delete(self, request, format=None):
        is_exists, get_company = check_token_exist(request=request)
        # Check The Company exists or Not
        if not is_exists:
            return get_company

        request.auth.delete()
        return Response({"Detail": "Successfully Logout!"})


# =================================================================


class RegisterPage(RegisterMixin, views.APIView):
    """Register a new account for a given account type and account name."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response({"details": "Method GET Not Allowed"})

    def post(self, request, format=None):
        # Serialize data and validate them
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Set the user info and return Them
        user = serializer.save()
        user.save()
        get_profile = Profile.objects.get(user=user)
        get_profile.company = self.company
        get_profile.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.id,
                "user_name": user.username,
            }
        )


# =================================================================


class ProfilePage(CheckCompanyTokenExist, generics.RetrieveAPIView):
    # class ProfilePage(generics.RetrieveAPIView):
    """Profile page for the specified user."""

    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.user.is_authenticated)
        self.profile = Profile.objects.filter(user=request.user).first()
        # ===========================
        serialize_profile = ProfileSerializer(self.profile, many=False)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """Get The Data from the model"""
        get_profile = Profile.objects.filter(user=self.request.user)
        self.kwargs["pk"] = get_profile.first().id
        return get_profile


# =================================================================
class ProfileEdit(CheckCompanyTokenExist, generics.RetrieveUpdateAPIView):
    """Edit The Profile Section"""

    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        return Response({"detail": "Just Send A PUT Request with your info"})

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        """Get The Data from the model"""
        get_profile = Profile.objects.filter(user=self.request.user)
        self.kwargs["pk"] = get_profile.first().id
        return get_profile


# ===============================================================
from django_countries import countries


class CompanyCreate(generics.CreateAPIView):
    """Create The Company to use our API"""

    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def perform_create(self, serializer):
        """Do Somthing before create the Company"""
        self.company = serializer.save(user_agent=self.request.user)
        self.comp_token = CompanyToken.objects.create(company=self.company)

    def post(self, request, *args, **kwargs):
        """Handle The POST Method"""
        countries_list = []
        for country in countries:
            countries_list.append(country)
        # Get The Country
        country = request.POST.get("country")
        if country is None:
            return Response(
                {"detail": "Country Should Set!", "countries": countries_list}
            )

        response = super().post(request, *args, **kwargs)
        serialize_data = CompanySerializer(self.company, many=False)
        data = {
            "company_detail": serialize_data.data,
            "Token": CompanyTokenSerializer(self.comp_token, many=False).data,
        }
        response.data = data
        return response


# ===========================================

# ===========================================


class VerifyEmail(CheckCompanyTokenExist, views.APIView):
    """Verify The Email Address"""

    def get(self, request, format=None):
        """
        Handle The GET Request
        """
        return Response({"detail": "Just Send The POST method with your email"})

    def post(self, request, format=None):
        user = request.user
        """
        Handle The POST Request
        """
        get_email = request.POST.get("email")
        if not get_email:
            return Response({"detail": "Enter Your email address!"})

        # Check The Email
        bool_res, res = check_email_code(request.user, get_email)
        if not bool_res:
            return res

        return Response(
            {
                "detail": "Successfully The Verification Code Sent!\nNote:Verification Code will Expire After 2 Minutes"
            }
        )


class VerifyEmailCode(CheckCompanyTokenExist, views.APIView):
    def get(self, request, *args, **kwargs):

        """Handle The GET Request"""
        return Response(
            {"detail": "Just Send The POST Request With The Code That Emailed For You"}
        )

    def post(self, request, *args, **kwargs):
        """Handle The POST Request"""
        get_user = self.request.user
        get_email = EmailCodes.objects.filter(user=get_user).first()

        if get_email is None:
            return Response({"detail": "You don't have email in your profile"})

        elif get_email.verified:
            return Response({"detail": "Your Email Verified!"})
        # Get The Verification Code
        get_code = request.POST.get("code")
        if get_code is None:
            return Response({"detail": "Please Give The Verification Code"})

        # =============================================
        # Check Section
        res = check_verified_email(get_email.email_code, get_code)
        return res


# =========================================
# Social Authentication


@permission_classes((AllowAny,))
class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """

        POST with "auth_token"

        Send an idtoken as from google to get user information

        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data["auth_token"]
        return Response(data, status=status.HTTP_200_OK)


# Instagram OAtuh2
#
#
# class InstagramCallbackView(RedirectView):
#     pattern_name = 'home'
#
#     # تابع برای دریافت access_token از طریق کد ورود ایجاد شده توسط Instagram
#     def get_redirect_url(self, *args, **kwargs):
#         code = self.request.GET.get('code')
#         data = {
#             'client_id': settings.SOCIAL_AUTH_INSTAGRAM_KEY,
#             'client_secret': settings.SOCIAL_AUTH_INSTAGRAM_SECRET,
#             'grant_type': 'authorization_code',
#             'redirect_uri': 'https://localhost:8000/instagram-callback/',
#             'code': code,
#             "scopes": settings.SOCIAL_AUTH_INSTAGRAM_SCOPE
#         }
#         headers = {
#             'Content-Type': 'application/json'
#         }
#
#         response = requests.post('https://api.instagram.com/oauth/access_token', data=json.dumps(data), headers=headers)
#         json_data = json.loads(response.text)
#
#         # ثبت access_token در session
#         self.request.session['access_token'] = json_data['access_token']
#         return super().get_redirect_url(*args, **kwargs)
