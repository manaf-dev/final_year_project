from .models import Cohort


def get_cohort_by_id(cohort_id):
    try:
        cohort = Cohort.objects.get(id=cohort_id)
        return cohort
    except Cohort.DoesNotExist:
        return None
