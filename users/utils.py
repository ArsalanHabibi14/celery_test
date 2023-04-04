import random

from django.conf import settings
from django.utils import timezone

from .models import CompanyToken, EmailCodes, Profile
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status


def check_token_exist(token):
    """Check The Token For Company is exists"""
    # get_token = request.headers["Company_Auth"]
    get_company = CompanyToken.objects.filter(token=str(token)).first()

    if get_company is None:
        return False, "Company Not Found!"
    return True, get_company.company


from .tasks import mail_send


# ====================================
def check_email_code(user, email):
    get_email = EmailCodes.objects.filter(user=user, email=email).first()
    if get_email is not None:
        if get_email.verified:
            return False, Response({"detail": "Your Email Verified!"})
        else:
            get_email.delete()
            create_email = EmailCodes.objects.create(user=user, email=email)
            mail_send.delay(
                "Verify Your Email",
                f"Use This Code To Verify your email\nVerification Code : {create_email.email_code}",
                settings.EMAIL_HOST_USER,
                [create_email.email],
            )
            return False, Response({"detail": "The Code Sent To Your Email!"})
    return True, True


# ========================================
def check_verified_email(email_id, get_code):
    get_email = EmailCodes.objects.filter(email_code=email_id).first()
    #     =================================
    #   Check The Code
    # Expire Check
    get_time = get_email.created_at + timezone.timedelta(minutes=2)
    if timezone.now() > get_time:
        get_email.delete()
        return Response({"detail": "The Verification Code Expired!"})

    elif int(get_code) != get_email.email_code:
        return Response({"detail": "The Verification Code is incorrect!"})

    elif int(get_code) == get_email.email_code:
        get_email.verified = True
        get_email.save()
        return Response({"detail": "Your Email Has been Successfully Verified!"})
    else:
        return Response({"detail": "An error occurred!"})
