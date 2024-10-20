from rest_framework import serializers
from rest_framework.response import Response

from accounts.models.departments import Department
from accounts.serializers.faculties import FacultySerializer


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        department = Department.objects.create(
            name=validated_data.get("name"),
            department_code=validated_data.get("department_code"),
            faculty=validated_data.get("faculty"),
        )
        department.save()

        return Response(department)
