from accounts.serializers.users import CustomUserSerializer


def create_user(data):
    serializer = CustomUserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    return None, serializer.errors
