from ._base_imports import *

from accounts.utils.setters import *
from accounts.models.users import CustomUser
from accounts.serializers.users import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        users = serializer.data

        for user in users:
            self.set_fk_fields(user)

        return Response(users)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        user = serializer.data

        self.set_fk_fields(user)

        return Response(user)

    def set_fk_fields(self, user_data: dict):
        set_department(user_data)

        if user_data["supervisor_account"]:
            return user_data

        set_supervisor(user_data)
        set_intern_school(user_data)
        set_mentor(user_data)

        return user_data
