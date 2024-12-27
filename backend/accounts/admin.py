from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

# from accounts.models.users import CustomUser
from accounts.models import *

admin.site.site_header = "TIPS Admin"
admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(Mentor)


@admin.register(InternSchool)
class InternSchoolAdmin(admin.ModelAdmin):
    list_display = ["school", "location", "district", "region"]
    list_filter = ["district", "region"]
    search_fields = ["school", "location", "district", "region"]


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ["username", "email", "is_staff"]

    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "title",
                    "avatar",
                    "phone",
                    "department",
                    "account_type",
                    "supervisor",
                    "intern_school",
                    "mentor",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
