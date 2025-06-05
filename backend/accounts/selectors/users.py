from accounts.models.users import UserAccount
from accounts.serializers.users import UserAccountSerializer

from accounts.selectors.departments import get_departments_by_id
from internships.selectors import get_cohort_by_id
from accounts.serializers.departments import DepartmentSerializer
from internships.serializers import CohortSerializer

from accounts.models.tokens import Token as TokenModel


def get_users():
    return UserAccount.objects.all()


def get_user_by_id(user_id: str):
    try:
        user = UserAccount.objects.get(id=user_id)
    except UserAccount.DoesNotExist:
        return None
    else:
        return user


def get_user_by_email(email: str):
    try:
        user = UserAccount.objects.get(email=email)
        return user
    except UserAccount.DoesNotExist:
        return None


def get_user_by_username(username: str):
    try:
        user = UserAccount.objects.get(username=username)
        return user
    except UserAccount.DoesNotExist:
        return None


def get_user_by_token(token: str):
    try:
        token = TokenModel.objects.get(key=token)
        user = token.user
    except TokenModel.DoesNotExist:
        return None
    else:
        return user


def get_interns_by_supervisor(supervisor: str):
    interns = UserAccount.objects.filter(supervisor=supervisor)
    return interns


def get_supervisor_interns_by_cohort(supervisor: str, cohort: str):
    interns = UserAccount.objects.filter(supervisor=supervisor, cohort=cohort)
    return interns


def user_representation(user: UserAccount, many: bool = False):
    serializer = UserAccountSerializer(user, many=many)
    return serializer.data
