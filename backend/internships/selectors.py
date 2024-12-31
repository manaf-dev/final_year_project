from .models import Cohort


def get_cohort_by_id(cohort_id):
    try:
        cohort = Cohort.objects.get(id=cohort_id)
        return cohort
    except Cohort.DoesNotExist:
        return None


def get_cohort_by_year(year):
    try:
        cohort = Cohort.objects.get(year=year)
        return cohort
    except Cohort.DoesNotExist:
        return None
