from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("", views.home, name="home_page"),
    path("login/", views.login, name="login_page"),
    path("logout/", views.LogoutPage.as_view(), name="logout_page"),  # For logging out
    path("signup/", views.RegisterPage.as_view(), name="register_page"),  # For Sign Up
    path(
        "profile/", views.ProfilePage.as_view(), name="profile_page"
    ),  # For User Profile
    path(
        "profile/edit/", views.ProfileEdit.as_view(), name="profile_edit"
    ),  # For Edit User Profile
    path("company/", views.CompanyCreate.as_view(), name="company_name"),

    #     Verification URLS
    path("verify/email/", views.VerifyEmail.as_view(), name="verify_email"),
    path("verify/email/submit/", views.VerifyEmailCode.as_view(), name="submit_verify_email"),
    #     ======
    #     Social Authentication
    path('google/', views.GoogleSocialAuthView.as_view()),
    # path("login/google/", views.GoogleLogin.as_view(), name="google_login"),
    # path("login/facebook/", views.FacebookLogin.as_view(), name="facebook_login"),
    # path("login/instagram/", views.login, name="login_page"),
    # path("instagram-callback/", views.InstagramCallbackView.as_view(), name="instagram_callback"),

]
