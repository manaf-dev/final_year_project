from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.template.response import TemplateResponse

from .forms import CustomUserCreationForm, CustomUserChangeForm, BulkAssignmentForm

# from accounts.models.users import CustomUser
from accounts.models import *

admin.site.site_header = "TIPS Admin"
admin.site.register(Department)
admin.site.register(Faculty)
# admin.site.register(Mentor)


# @admin.register(InternSchool)
# class InternSchoolAdmin(admin.ModelAdmin):
#     list_display = ["school", "location", "district", "region"]
#     list_filter = ["district", "region"]
#     search_fields = ["school", "location", "district", "region"]


@admin.action(description="Assign selected interns to a supervisor")
def assign_interns_to_supervisor(modeladmin, request, queryset):
    print("post", request.POST)
    if request.method == "POST":
        form = BulkAssignmentForm(request.POST)
        print("form", form)
        if form.is_valid():
            supervisor = form.cleaned_data["supervisor"]
            print("clean", form.cleaned_data["supervisor"])
            count = queryset.update(supervisor=supervisor)
            modeladmin.message_user(
                request,
                f"Successfully assigned {count} interns to {supervisor}.",
            )
            return
    else:
        form = BulkAssignmentForm()

    context = {
        "form": form,
        "title": "Bulk Assign Interns",
        "queryset": queryset,
        "description": "Assign the selected interns to a supervisor.",
    }
    return TemplateResponse(request, "admin/bulk_assignment_form.html", context)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ("username", "email", "account_type", "supervisor", "cohort")
    list_filter = ("account_type", "cohort", "department")
    search_fields = ("username", "email", "department_name")
    actions = [assign_interns_to_supervisor]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(account_type="intern") | Q(account_type="supervisor"))

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields["supervisor"].queryset = CustomUser.objects.filter(
                account_type="supervisor"
            )
        return form

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
                    "level",
                    "supervisor",
                    "cohort",
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
