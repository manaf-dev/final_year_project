from dj_rest_auth.registration.serializers import RegisterSerializer
from ._base_imports import *

from accounts.models.users import CustomUser
from accounts.selectors.departments import get_departments_by_id
from accounts.serializers.departments import DepartmentSerializer


class SupervisorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "title",
            "first_name",
            "last_name",
            "phone",
            "email",
            "department",
        )


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "title",
            "first_name",
            "last_name",
            "phone",
            "email",
            "avatar",
            "account_type",
            "department",
            "supervisor",
            "intern_school",
            "mentor",
        )


class CustomRegisterSerializer(RegisterSerializer):
    title = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    account_type = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    department = serializers.CharField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        print(self.validated_data)
        data["title"] = self.validated_data.get("title", "")
        data["first_name"] = self.validated_data.get("first_name", "")
        data["last_name"] = self.validated_data.get("last_name", "")
        data["account_type"] = self.validated_data.get("account_type", "")
        data["phone"] = self.validated_data.get("phone", "")
        data["department"] = self.validated_data.get("department", "")
        print(data)
        return data

    def save(self, request):
        user = super().save(request)
        user.title = self.cleaned_data["title"]
        user.account_type = self.cleaned_data["account_type"]
        user.phone = self.cleaned_data["phone"]

        department = get_departments_by_id(self.cleaned_data["department"])
        if not department:
            raise serializers.ValidationError("Department not found")

        user.department = department
        user.save()
        return user
