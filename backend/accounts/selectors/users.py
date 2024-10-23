from accounts.models.users import CustomUser


def get_users():
    return CustomUser.objects.all()


def get_user_by_id(user_id: int):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return None
    else:
        return user


def get_user_by_username(username: str):
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
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
