from ._base_imports import *
from accounts.models.users import UserAccount
from accounts.serializers.departments import DepartmentSerializer
from internships.serializers import CohortSerializer


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["department"] = (
            DepartmentSerializer(instance.department).data
            if instance.department
            else None
        )
        data["supervisor"] = (
            {
                "title": instance.supervisor.title,
                "first_name": instance.supervisor.first_name,
                "last_name": instance.supervisor.last_name,
                "phone": instance.supervisor.phone,
                "email": instance.supervisor.email,
                "department": DepartmentSerializer(instance.supervisor.department).data,
            }
            if instance.supervisor
            else None
        )
        data["cohort"] = (
            CohortSerializer(instance.cohort).data if instance.cohort else None
        )
        return data
