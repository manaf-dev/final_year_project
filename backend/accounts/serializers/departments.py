from ._base_imports import *

from accounts.models.departments import Department
from accounts.serializers.faculties import FacultySerializer


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["faculty"] = FacultySerializer(instance.faculty).data
        return data
