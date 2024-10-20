from rest_framework import serializers

from accounts.models.faculties import Faculty

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"