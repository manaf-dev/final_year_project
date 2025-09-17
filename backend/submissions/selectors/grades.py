from typing import List, Optional
from django.db.models import QuerySet
from submissions.models.grades import InternGrade
from accounts.models.users import UserAccount


def get_intern_grade_by_intern_id(intern_id: str) -> Optional[InternGrade]:
    """Get grades for a specific intern"""
    try:
        return InternGrade.objects.select_related("intern", "graded_by").get(
            intern_id=intern_id
        )
    except InternGrade.DoesNotExist:
        return None


def get_intern_grade_by_id(intern_id: str) -> Optional[InternGrade]:
    """Get grades for a specific intern (alias for compatibility)"""
    return get_intern_grade_by_intern_id(intern_id)


def get_or_create_intern_grade(intern: UserAccount) -> InternGrade:
    """Get or create grades record for an intern"""
    grade, created = InternGrade.objects.get_or_create(intern=intern)
    return grade


def get_cohort_intern_grades(cohort_id: str) -> QuerySet[InternGrade]:
    """Get all intern grades for a specific cohort"""
    return InternGrade.objects.select_related(
        "intern", "intern__department", "graded_by"
    ).filter(intern__cohort_id=cohort_id)


def get_all_intern_grades() -> QuerySet[InternGrade]:
    """Get all intern grades"""
    return InternGrade.objects.select_related(
        "intern", "intern__department", "graded_by"
    ).all()


def update_portfolio_score(
    intern_id: str, month: int, score: float, graded_by: UserAccount
) -> bool:
    """Update portfolio score for a specific month"""
    try:
        grade = get_or_create_intern_grade(UserAccount.objects.get(id=intern_id))

        if month == 1:
            grade.portfolio_month_1 = score
        elif month == 2:
            grade.portfolio_month_2 = score
        elif month == 3:
            grade.portfolio_month_3 = score
        elif month == 4:
            grade.portfolio_month_4 = score
        else:
            return False

        grade.graded_by = graded_by
        grade.save()
        return True
    except Exception:
        return False


def update_teaching_philosophy_score(
    intern_id: str, score: float, graded_by: UserAccount
) -> bool:
    """Update teaching philosophy score"""
    try:
        grade = get_or_create_intern_grade(UserAccount.objects.get(id=intern_id))
        grade.teaching_philosophy_score = score
        grade.graded_by = graded_by
        grade.save()
        return True
    except Exception:
        return False


def update_reflective_practice_score(
    intern_id: str, score: float, graded_by: UserAccount
) -> bool:
    """Update reflective practice score"""
    try:
        grade = get_or_create_intern_grade(UserAccount.objects.get(id=intern_id))
        grade.reflective_practice_score = score
        grade.graded_by = graded_by
        grade.save()
        return True
    except Exception:
        return False
