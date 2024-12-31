from dj_rest_auth.registration.serializers import RegisterSerializer
from ._base_imports import *

from accounts.models.users import CustomUser
from accounts.selectors.departments import get_departments_by_id
from accounts.serializers.departments import DepartmentSerializer
from internships.selectors import get_cohort_by_id


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
            "level",
            "department",
            "supervisor",
            "intern_school",
            "mentor",
            "cohort",
            "last_login",
        )


class CustomRegisterSerializer(RegisterSerializer):
    title = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    account_type = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    department = serializers.CharField(required=True)
    level = serializers.CharField(required=True)
    cohort = serializers.CharField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update(
            {
                field: self.validated_data.get(field, "")
                for field in [
                    "title",
                    "first_name",
                    "last_name",
                    "account_type",
                    "phone",
                    "department",
                    "level",
                    "cohort",
                ]
            }
        )
        return data

    def save(self, request):
        user = super().save(request)
        user.title = self.cleaned_data["title"]
        user.account_type = self.cleaned_data["account_type"]
        user.phone = self.cleaned_data["phone"]
        user.level = self.cleaned_data["level"]

        try:
            department = get_departments_by_id(self.cleaned_data["department"])
            if not department:
                raise serializers.ValidationError("Department not found")
            user.department = department

            cohort = get_cohort_by_id(self.cleaned_data["cohort"])
            if not cohort:
                raise serializers.ValidationError("Cohort not found")
            user.cohort = cohort

            user.save()
        except Exception as e:
            raise serializers.ValidationError(str(e))

        return user
