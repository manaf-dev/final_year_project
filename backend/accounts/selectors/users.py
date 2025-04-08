from accounts.models.users import CustomUser
from accounts.serializers.users import CustomUserSerializer, SupervisorSerializer

from accounts.selectors.departments import get_departments_by_id
from accounts.selectors.intern_schools import get_intern_school_by_id
from accounts.selectors.mentors import get_mentor_by_id
from internships.selectors import get_cohort_by_id

from accounts.serializers.departments import DepartmentSerializer
from accounts.serializers.intern_schools import InternSchoolSerializer
from accounts.serializers.mentors import MentorSerializer
from internships.serializers import CohortSerializer

from dj_rest_auth.models import TokenModel


def get_users():
    return CustomUser.objects.all()


def get_user_by_id(user_id: int):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return None
    else:
        return user


def get_user_by_email(email: str):
    try:
        user = CustomUser.objects.get(email=email)
        return user
    except CustomUser.DoesNotExist:
        return None


def get_user_by_username(username: str):
    try:
        user = CustomUser.objects.get(username=username)
        return user
    except CustomUser.DoesNotExist:
        return None


def get_user_by_token(token: str):
    try:
        token = TokenModel.objects.get(key=token)
        user = token.user
    except TokenModel.DoesNotExist:
        return None
    else:
        return user


def get_interns_by_supervisor(supervisor_id: int):
    try:
        interns = CustomUser.objects.filter(supervisor=supervisor_id)
    except CustomUser.DoesNotExist:
        return None
    else:
        return interns


def set_supervisor(data: dict):
    if data["supervisor"]:
        supervisor = get_user_by_id(data["supervisor"])
        data["supervisor"] = SupervisorSerializer(supervisor).data
        return data
    return data


def set_department(data: dict):
    if data["department"]:
        department = get_departments_by_id(data["department"])
        data["department"] = DepartmentSerializer(department).data
        return data
    return data


# def set_intern_school(data: dict):
#     if data["intern_school"]:
#         intern_school = get_intern_school_by_id(data["intern_school"])
#         data["intern_school"] = InternSchoolSerializer(intern_school).data
#         return data
#     return data


# def set_mentor(data: dict):
#     if data["mentor"]:
#         mentor = get_mentor_by_id(data["mentor"])
#         data["mentor"] = MentorSerializer(mentor).data
#         return data
#     return data


def set_cohort(data: dict):
    if data["cohort"]:
        cohort = get_cohort_by_id(data["cohort"])
        data["cohort"] = CohortSerializer(cohort).data
        return data
    return data


def user_info(user):
    data = CustomUserSerializer(user).data
    data = set_department(data)
    data = set_supervisor(data)
    # data = set_intern_school(data)
    # data = set_mentor(data)
    data = set_cohort(data)
    return data
