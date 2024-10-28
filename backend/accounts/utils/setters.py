from accounts.selectors.users import get_user_by_id
from accounts.selectors.mentors import get_mentor_by_id
from accounts.selectors.departments import get_departments_by_id
from accounts.selectors.intern_schools import get_intern_school_by_id

from accounts.serializers.users import CustomUserSerializer
from accounts.serializers.departments import DepartmentSerializer
from accounts.serializers.intern_schools import InternSchoolSerializer
from accounts.serializers.mentors import MentorSerializer


def set_supervisor(data: dict):
    if data["supervisor"]:
        supervisor = get_user_by_id(data["supervisor"])
        data["supervisor"] = CustomUserSerializer(supervisor).data
        return data
    return None


def set_department(data: dict):
    if data["department"]:
        department = get_departments_by_id(data["department"])
        data["department"] = DepartmentSerializer(department).data
        return data
    return None


def set_intern_school(data: dict):
    if data["intern_school"]:
        intern_school = get_intern_school_by_id(data["intern_school"])
        data["intern_school"] = InternSchoolSerializer(intern_school).data
        return data
    return None


def set_mentor(data: dict):
    if data["mentor"]:
        mentor = get_mentor_by_id(data["mentor"])
        data["mentor"] = MentorSerializer(mentor).data
        return data
    return None

def user_info(user, request):
    data = CustomUserSerializer(user).data
    data = set_department(data)
    data = set_intern_school(data)
    data = set_supervisor(data)
    data = set_mentor(data)
    return data
