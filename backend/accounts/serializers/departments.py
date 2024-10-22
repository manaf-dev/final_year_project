from ._base_imports import *

from accounts.models.departments import Department
from accounts.models.faculties import Faculty
from accounts.serializers.faculties import FacultySerializer


class DepartmentSerializer(serializers.ModelSerializer):
    faculty = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all())

    class Meta:
        model = Department
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["faculty"] = FacultySerializer(instance.faculty).data
        return representation
