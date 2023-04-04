from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    """
    Edit The Show Profile Model in Admin Panel
    """

    list_display = ["__str__", "lastname", "email", "thumbnail_image"]


admin.site.register(Profile, ProfileAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["__str__", "user_agent", "country"]


admin.site.register(Company, CompanyAdmin)


class CompanyTokenAdmin(admin.ModelAdmin):
    list_display = ["__str__", "company", "created_time"]


admin.site.register(CompanyToken, CompanyTokenAdmin)


class EmailCodeAdmin(admin.ModelAdmin):
    list_display = ["__str__", "created_at", "email_code"]


admin.site.register(EmailCodes, EmailCodeAdmin)
