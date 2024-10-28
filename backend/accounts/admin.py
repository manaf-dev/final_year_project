from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

# from accounts.models.users import CustomUser
from accounts.models import *

admin.site.site_header = "Internship Admin"
admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(InternSchool)
admin.site.register(Mentor)


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
                    "avatar",
                    "phone",
                    "department",
                    "supervisor_account",
                    "intern_account",
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
