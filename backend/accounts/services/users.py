from accounts.serializers.users import UserAccountSerializer


def create_user(data: dict):
    serializer = UserAccountSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data, None
    return None, serializer.errors
