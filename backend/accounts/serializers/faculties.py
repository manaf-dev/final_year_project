from ._base_imports import *

from accounts.models.faculties import Faculty


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"
