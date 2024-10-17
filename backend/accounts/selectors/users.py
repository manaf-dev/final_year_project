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
