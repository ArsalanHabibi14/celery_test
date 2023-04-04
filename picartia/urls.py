from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.views import PasswordResetConfirmView

# from rest_framework_social_oauth2.views import (TokenHasReadWriteScope, TokenHasScope)
urlpatterns = [
    path("admin/", admin.site.urls),
    # Custom App's URLS
    path("", include("users.urls", namespace="user")),
    path("", include("mosaic.urls", namespace="mosaic")),
    # ==================================
    path("", include("dj_rest_auth.urls")),  # The all authentication pages
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),  # password reset confirmation url
    #     =================
    path("social-auth/", include("social_django.urls", namespace="social-auth")),
    path("accounts/", include("rest_framework_social_oauth2.urls")),
    # url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    # url(r'^verify-email/(?P<key>.+)/$', VerifyEmailView.as_view(), name='account_verify_email'),
    # url(r'^account-email-verification-sent/$', VerifyEmailSentView.as_view(), name='account_email_verification_sent')
]

# Set STATIC & MEDIA Files URLS
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
