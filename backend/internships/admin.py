from django.contrib import admin

from .models import Cohort


# Register your models here.
@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    """Admin View for Cohort"""

    list_display = ("year", "start_date", "end_date")
    list_filter = ("year",)
